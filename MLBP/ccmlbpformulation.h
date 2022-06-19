#ifndef __CCMLBP_FORMULATION_H__
#define __CCMLBP_FORMULATION_H__


#include "problems.h"
#include "mipsolver.h"

template<typename> struct Instance;
template<typename> struct Solution;

class CCMLBPFormulation : public MIPFormulation<CCMLBP>
{
public:
	virtual void createDecisionVariables(IloEnv env, const Instance<CCMLBP>& inst);
	virtual void addConstraints(IloEnv env, IloModel model, const Instance<CCMLBP>& inst);
	virtual void addObjectiveFunction(IloEnv env, IloModel model, const Instance<CCMLBP>& inst);
	virtual void extractSolution(IloCplex cplex, const Instance<CCMLBP>& inst, Solution<CCMLBP>& sol);
private:
	//TODO: add decision variables
	// binary decision variables x_{ijk}: item i is inserted into bin j (=1) or not (=0)
	IloArray<IloArray<IloNumVarArray>> x;


	// decision variables y_{kj}
	IloArray<IloNumVarArray> y;

	// decision variable c_{qjk}: is class q in bin j on lvl k (=1) or not (=0) 
	IloArray<IloArray<IloNumVarArray>> c;

};


#endif // __CCMLBP_FORMULATION_H__