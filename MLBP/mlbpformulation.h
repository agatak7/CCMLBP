#ifndef __MLBP_FORMULATION_H__
#define __MLBP_FORMULATION_H__


#include "problems.h"
#include "mipsolver.h"

template<typename> struct Instance;
template<typename> struct Solution;

class MLBPFormulation : public MIPFormulation<MLBP>
{
public:
	virtual void createDecisionVariables(IloEnv env, const Instance<MLBP>& inst);
	virtual void addConstraints(IloEnv env, IloModel model, const Instance<MLBP>& inst);
	virtual void addObjectiveFunction(IloEnv env, IloModel model, const Instance<MLBP>& inst);
	virtual void extractSolution(IloCplex cplex, const Instance<MLBP>& inst, Solution<MLBP>& sol);
private:
	//TODO: add decision variables
	// binary decision variables x_{ijk}: item i is inserted into bin j (=1) or not (=0)
	IloArray<IloArray<IloNumVarArray>> x;

	// decision variables y_{kj}
	IloArray<IloNumVarArray> y;
};


#endif // __MLBP_FORMULATION_H__
