#include "ccmlbpformulation.h"
#include "instance.h"
#include "solution.h"
#include "users.h"
#include <set>


void CCMLBPFormulation::createDecisionVariables(IloEnv env, const Instance<CCMLBP>& inst)
{
	SOUT() << "HELLO " << std::endl;
	// decision variables x_{ikj}
	x = IloArray<IloArray<IloNumVarArray>>(env, inst.m + 1);

	for (int k : inst.M) if (k > 0) {
		x[k] = IloArray<IloNumVarArray>(env, inst.n[k - 1]);
		for (int i : inst.B[k - 1]) // for every i create array of size j
			x[k][i] = IloNumVarArray(env, inst.n[k], 0, 1, ILOBOOL);
	}
	int num = 0;
	for (int k : inst.M) {
		num += inst.n[k - 1] * inst.n[k];
	}

	SOUT() << "created" << num << " x_{ijk} variables" << std::endl;

	//decision variables y_{kj}

	y = IloArray<IloNumVarArray>(env, inst.m + 1);

	for (int k : inst.M)  if (k > 0) {
		y[k] = IloNumVarArray(env, inst.n[k], 0, 1, ILOBOOL);
	}

	num = 0;
	for (int k : inst.M) {
		num += inst.n[k];
	}

	SOUT() << "created " << num << " y_{kj} variables" << std::endl;

	//decision variable c_kqj : is class q in bin j on level k
	c = IloArray<IloArray<IloNumVarArray>>(env, inst.m + 1);
	
	for (int k : inst.M) if (k > 0) { //for all levels
		c[k] = IloArray<IloNumVarArray>(env, inst.q); //length = number of classes
		for (int q = 0; q < inst.q; q++) // for every class, create a binary array of size j (nr of bins)
			c[k][q] = IloNumVarArray(env, inst.n[k], 0, 1, ILOBOOL);
	}
	
	num = 0;
	for (int k : inst.M) if (k > 0) {
		num += inst.q * inst.q;
	}

	SOUT() << "created" << num << " c_{qjk} variables" << std::endl;

}

void CCMLBPFormulation::addConstraints(IloEnv env, IloModel model, const Instance<CCMLBP>& inst)
{
	//At level 1 -> Each item into ona bin
	for (int i : inst.B[0]) {
		IloExpr sum(env);
		for (int j : inst.B[1])
			sum += x[1][i][j];
		model.add(sum == 1);
		sum.end();
	}

	//at level k
	for (int k : inst.M) if (k > 1) {
		for (int i : inst.B[k - 1]) {
			IloExpr sum(env);
			for (int j : inst.B[k])
				sum += x[k][i][j];
			model.add(sum == y[k - 1][i]);
			sum.end();
		}
	}
	int num = 0;
	for (int k : inst.M)
		num += inst.n[k - 1] * inst.n[k];
	SOUT() << "added " << num << " constraints to enforce the packing of each item to every level" << std::endl;


	//content of bin must be within capacity
	for (int k : inst.M) if (k > 0) {
		for (int j : inst.B[k]) {
			IloExpr sum(env); 
			for (int i : inst.B[k - 1]) {
				sum += x[k][i][j] * inst.s[k - 1][i]; //add size of item i if added to j at lvl k
			}
			model.add(sum <= y[k][j] * inst.w[k][j]); //total size leq capacity
			sum.end();


		}
	}

	num = 0;
	for (int k : inst.M)
		num += inst.n[k - 1] * inst.n[k];
	SOUT() << "added " << num << " capacity constraints" << std::endl;
	
	//Class Constraints 
	//On level one, if an item is in a bin, that class must be in the bin
	for (int i : inst.B[0]) { //for each item
		for (int j : inst.B[1]) { //for each bin on level 1
			// class of i = inst
			int class_i = inst.kappa[i];
			//SOUT() << "class of " << i << " is " << inst.kappa[i] << std::endl;
			//model.add(x[1][i][j] <= x[1][i][j] * c[1][class_i][j]); //if item i is in bin j then the class of i is in j
			model.add(x[1][i][j] <=  c[1][class_i][j]);
		}
	}

	//On level k > 1, 
	//For each bin if a bin/item on the previous level is inserted into it
	//They must contain the same classes
	for (int k : inst.M) if (k > 1) {
		for (int j : inst.B[k]) { //for each bin
			for (int i : inst.B[k - 1]) {
				//if i insterted into j x[k][i][j] 
				//then c[k - 1][for all classes!][i] <= c[k][for all classes][j]
				for (int q = 0; q < inst.q; q++) {
					//if an item gets put in some bin and that item has that class then the bin also has that class
					model.add(IloIfThen(env, x[k][i][j] == 1 && c[k - 1][q][i] == 1, c[k][q][j] == 1));
					//model.add(x[k][i][j] * c[k - 1][q][i] <= x[k][i][j] * c[k][q][j]);
				}
			}
		}
	}
	//TODO: some constraint s.t if none of the items in a bin have that class then that bin must not have that class!!!
	/*
		for (int k : inst.M) if (k > 1) {
		for (int j : inst.B[k]) { //for each bin
			for (int q = 0; q < inst.q; q++) {
				IloExpr sum(env);
				for (int i : inst.B[k - 1]) {
					sum += x[k][i][j] * c[k - 1][q][i];
				}
			}
		}
	}

	*/
	//OR, that the nr of classes in a bin must be less than the number of items
	/*
	for (int k : inst.M) if (k > 1) {
		for (int j : inst.B[k]) { //for each bin
			IloExpr sum_class(env);
			for (int q = 0; q < inst.q; q++) {
				sum_class += c[k][q][j];
			}
			IloExpr sum_item(env);
			for (int i : inst.B[k - 1]) {
				sum_item += x[k][i][j];
			}
			model.add(sum_class <= sum_item);
			sum_class.end();
			sum_item.end();
		}
	}
	*/
	/*
	//Class bound constraint
	for (int k : inst.M) if (k > 0) {
		int class_bound = inst.Q[k]; //bound for that level
		for (int j : inst.B[k]) {
			IloExpr sum(env);
			for (int q = 0; q < inst.q; q++) // for every class
				sum += c[k][q][j]; // add 1 if class q is in bin j 
			model.add(sum <= class_bound); //total sum leq bound
			sum.end();
		}
	}
	*/
	
	
	for (int k : inst.M) if (k > 0) {
		int class_bound = inst.Q[k]; //bound for that level
		for (int j : inst.B[k]) {
			IloExpr sum(env);
			for (int q = 0; q < inst.q; q++) // for every class
				sum += c[k][q][j]; // add 1 if class q is in bin j 
			model.add(sum <= class_bound * y[k][j]); //total sum leq bound if a bin is used.
			sum.end();
		}
	}

	for (int k : inst.M) if (k > 0) {
		for (int j : inst.B[k]) {
			IloExpr sum(env);
			for (int q = 0; q < inst.q; q++) // for every class
				sum += c[k][q][j]; // add 1 if class q is in bin j 
			model.add(sum >= y[k][j]); //if a bin is used then at least one class is assigned
			sum.end();
		}
	}
	


	

}

void CCMLBPFormulation::addObjectiveFunction(IloEnv env, IloModel model, const Instance<CCMLBP>& inst)
{
	IloExpr sum(env);
	for (int k : inst.M) if (k > 0) {
		for (int j = 0; j < inst.n[k]; j++) {
			sum += y[k][j] * inst.c[k][j];
		}
	}
	model.add(IloMinimize(env, sum));
	sum.end();

	SOUT() << "added objective function" << std::endl;
}

void CCMLBPFormulation::extractSolution(IloCplex cplex, const Instance<CCMLBP>& inst, Solution<CCMLBP>& sol)
{


	sol.total_bin_cost = 0;
	
	for (int k : inst.M) if (k > 0) {
		sol.items_to_bins[k - 1].assign(inst.n[k - 1], -1);  // initialise array with value -1 for every outgoing edge
		for (int j : inst.B[k]) {  // for every bin add cost to total if bin j is used
			if (cplex.getValue(y[k][j]) > 0.5)
				sol.total_bin_cost += inst.c[k][j];
			for (int i : inst.B[k - 1])  // for every outgoing edge store the target node
				if (cplex.getValue(x[k][i][j]) > 0.5)
					sol.items_to_bins[k - 1][i] = j;

			for (int q = 0; q < inst.q; q++) {
				//SOUT() << "c for lvl " << k << ", class " << q << ", bin " << j << " is : " << cplex.getValue(c[k][q][j]);
				if (cplex.getValue(c[k][q][j]) > 0.5) {
					sol.classes_in_bins[k][q][j] = 1;
				}
				else {
					sol.classes_in_bins[k][q][j] = 0;
				}

			}
		}
	}

	//TODO

/*
	sol.total_bin_cost = 0;
	for (int k : inst.M) if (k > 0) {
		sol.items_to_bins[k - 1].assign(inst.n[k - 1], -1);
		for (int j : inst.B[k]) {
			if (cplex.getValue(y[k][j]) > 0.5) {
				sol.total_bin_cost += inst.c[k][j];
			}
			for (int i : inst.B[k - 1]) {
				if (cplex.getValue(x[k][i][j]) > 0.5) {
					sol.items_to_bins[k - 1][i] = j;
				}
			}
		}
	}

	for (int i = 0; i < sol.items_to_bins.size(); i++) {
		for (int j = 0; j < sol.items_to_bins[i].size(); j++)
			SOUT() << sol.items_to_bins[i][j] << " ";
		SOUT() << std::endl;


	}
	*/

}
