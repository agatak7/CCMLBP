#include "mlbpformulation.h"

#include "instance.h"
#include "solution.h"
#include "users.h"


void MLBPFormulation::createDecisionVariables(IloEnv env, const Instance<MLBP>& inst)
{
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

}

void MLBPFormulation::addConstraints(IloEnv env, IloModel model, const Instance<MLBP>& inst)
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



}

void MLBPFormulation::addObjectiveFunction(IloEnv env, IloModel model, const Instance<MLBP>& inst)
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

void MLBPFormulation::extractSolution(IloCplex cplex, const Instance<MLBP>& inst, Solution<MLBP>& sol)
{
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

}

