#ifndef __NF_MLBP_FORMULATION_H__
#define __NF_MLBP_FORMULATION_H__


#include "problems.h"
#include "mipsolver.h"

template<typename> struct Instance;
template<typename> struct Solution;

class NF_MLBPFormulation : public MIPFormulation<MLBP>
{
public:
	virtual void createDecisionVariables(IloEnv env, const Instance<MLBP>& inst);
	virtual void addConstraints(IloEnv env, IloModel model, const Instance<MLBP>& inst);
	virtual void addObjectiveFunction(IloEnv env, IloModel model, const Instance<MLBP>& inst);
	virtual void extractSolution(IloCplex cplex, const Instance<MLBP>& inst, Solution<MLBP>& sol);
private:
	//TODO: add decision variables
	// binary decision variables x_{kij}: item i is inserted into bin j (=1) or not (=0)
	IloArray<IloArray<IloNumVarArray>> x;

	// decision variables y_{kj}
	IloArray<IloNumVarArray> y;

	//decision variable f_{kij}
	IloArray<IloArray<IloNumVarArray>> f;
};


#endif // __NF_MLBP_FORMULATION_H__
