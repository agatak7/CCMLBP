#include "solution.h"

#include "lib/util.h"
#include "users.h"

#include <algorithm>
#include <numeric>
#include <cassert>



/*****************************************************************************************/
/** Bin Packing Problem ******************************************************************/
/*****************************************************************************************/
Solution<BP>::Solution(const Instance<BP>& inst) : item_to_bins(inst.s.size())
{
	std::iota(item_to_bins.begin(), item_to_bins.end(), 0);
	total_bins = (int)inst.s.size();
}

std::ostream& operator<<(std::ostream& os, const Solution<BP>& sol)
{
	os << sol.item_to_bins;
	return os;
}




/*****************************************************************************************/
/** Multi-Level Bin Packing Problem ******************************************************/
/*****************************************************************************************/
Solution<MLBP>::Solution(const Instance<MLBP>& inst) : db(-1)
{
	items_to_bins = std::vector<std::vector<int>>(inst.m + 1);
	for (int k : inst.M) if (k > 0) {
		items_to_bins[k] = std::vector<int>(inst.n[k - 1]);
		//SOUT() << items_to_bins[k];
		//std::iota(items_to_bins[k].begin(), items_to_bins[k].end(), 0);

	}
}

std::ostream& operator<<(std::ostream& os, const Solution<MLBP>& sol) {
	// TODO
	return os;
}




/*****************************************************************************************/
/** Class Constrained Multi-Level Bin Packing Problem ************************************/
/*****************************************************************************************/
Solution<CCMLBP>::Solution(const Instance<CCMLBP>& inst) : Solution<MLBP>(inst)
{

	items_to_bins = std::vector<std::vector<int>>(inst.m + 1);
	for (int k : inst.M) if (k > 0) {
		items_to_bins[k] = std::vector<int>(inst.n[k - 1]);
		//SOUT() << items_to_bins[k];
		//std::iota(items_to_bins[k].begin(), items_to_bins[k].end(), 0);

	}

	//std::vector<std::vector<std::vector<int>>> classes_in_bins;
	classes_in_bins = std::vector<std::vector<std::vector<int>>>(inst.m + 1);
	for (int k : inst.M) if (k > 0) {
		classes_in_bins[k] = std::vector<std::vector<int>>(inst.q);
		for (int q = 0; q < inst.q; q++) {
			classes_in_bins[k][q] = std::vector<int>(inst.n[k]);
		}
	}
}

std::ostream& operator<<(std::ostream& os, const Solution<CCMLBP>& sol) {
	// TODO
	return os;
}




/*****************************************************************************************/
/** Multi-Level Bin Packing Problem with Conflict Constraints ****************************/
/*****************************************************************************************/
Solution<MLBPCC>::Solution(const Instance<MLBPCC>& inst) : Solution<MLBP>(inst)
{
}

std::ostream& operator<<(std::ostream& os, const Solution<MLBPCC>& sol) {
	// TODO
	return os;
}




/*****************************************************************************************/
/** Multi-Level Bin Packing Problem with Partial Orders **********************************/
/*****************************************************************************************/
Solution<MLBPPO>::Solution(const Instance<MLBPPO>& inst) : Solution<MLBP>(inst)
{
}

std::ostream& operator<<(std::ostream& os, const Solution<MLBPPO>& sol) {
	// TODO
	return os;
}




/*****************************************************************************************/
/** Multi-Level Bin Packing Problem with Time Windows ************************************/
/*****************************************************************************************/
Solution<MLBPTW>::Solution(const Instance<MLBPTW>& inst) : Solution<MLBP>(inst)
{
}

std::ostream& operator<<(std::ostream& os, const Solution<MLBPTW>& sol) {
	// TODO
	return os;
}




/*****************************************************************************************/
/** Multi-Level Bin Packing Problem with Fragmentation Constraints ***********************/
/*****************************************************************************************/
Solution<MLBPFC>::Solution(const Instance<MLBPFC>& inst) : Solution<MLBP>(inst)
{
}

std::ostream& operator<<(std::ostream& os, const Solution<MLBPFC>& sol) {
	// TODO
	return os;
}


