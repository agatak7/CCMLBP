#ifndef __SOLUTION_H__
#define __SOLUTION_H__


#include "problems.h"
#include "instance.h"

#include <vector>
#include <tuple>
#include <algorithm>


/*
 * Generic solution.
 * To write a solution class for a specific problem,
 * speialize this class for the corresponding problem type.
 */
template<typename ProbT>
struct Solution { };




/*****************************************************************************************/
/** Bin Packing Problem ******************************************************************/
/*****************************************************************************************/
template<>
struct Solution<BP>
{
	Solution(const Instance<BP>& inst);
	std::vector<int> item_to_bins;
	int total_bins;
	double db;  // dual bound
};

std::ostream& operator<<(std::ostream& os, const Solution<BP>& sol);




/*****************************************************************************************/
/** Multi-Level Bin Packing Problem ******************************************************/
/*****************************************************************************************/
template<>
struct Solution<MLBP>
{
	Solution(const Instance<MLBP>& inst);
	std::vector<std::vector<int>> items_to_bins;
	int total_bin_cost;
	double db;  // dual bound
};

std::ostream& operator<<(std::ostream& os, const Solution<MLBP>& sol);




/*****************************************************************************************/
/** Class Constrained Multi-Level Bin Packing Problem ************************************/
/*****************************************************************************************/
template<>
struct Solution<CCMLBP> : public Solution<MLBP>
{
	Solution(const Instance<CCMLBP>& inst);
	std::vector<std::vector<int>> items_to_bins;
	int total_bin_cost;
	std::vector<std::vector<std::vector<int>>> classes_in_bins;
	double db;  // dual bound
};

std::ostream& operator<<(std::ostream& os, const Solution<CCMLBP>& sol);




/*****************************************************************************************/
/** Multi-Level Bin Packing Problem with Conflict Constraints ****************************/
/*****************************************************************************************/
template<>
struct Solution<MLBPCC> : public Solution<MLBP>
{
	Solution(const Instance<MLBPCC>& inst);
};

std::ostream& operator<<(std::ostream& os, const Solution<MLBPCC>& sol);




/*****************************************************************************************/
/** Multi-Level Bin Packing Problem with Partial Orders **********************************/
/*****************************************************************************************/
template<>
struct Solution<MLBPPO> : public Solution<MLBP>
{
	Solution(const Instance<MLBPPO>& inst);
};




/*****************************************************************************************/
/** Multi-Level Bin Packing Problem with Time Windows ************************************/
/*****************************************************************************************/
template<>
struct Solution<MLBPTW> : public Solution<MLBP>
{
	Solution(const Instance<MLBPTW>& inst);
};

std::ostream& operator<<(std::ostream& os, const Solution<MLBPPO>& sol);




/*****************************************************************************************/
/** Multi-Level Bin Packing Problem with Fragmentation Constraints ***********************/
/*****************************************************************************************/
template<>
struct Solution<MLBPFC> : public Solution<MLBP>
{
	Solution(const Instance<MLBPFC>& inst);
};

std::ostream& operator<<(std::ostream& os, const Solution<MLBPFC>& sol);



#endif // __SOLUTION_H__
