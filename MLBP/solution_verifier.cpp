#include "solution_verifier.h"
#include "instance.h"
#include "solution.h"

#include <sstream>
#include <algorithm>
#include <set>



/*************************************************************************************************/
/* BP ********************************************************************************************/
/*************************************************************************************************/
bool SolutionVerifier<BP>::verify(const Instance<BP>& inst, const Solution<BP>& sol, std::vector<std::string>* error_msg)
{
	bool ret = true;
	std::vector<int> levels(sol.total_bins, 0);  // size of each bin
	for (int i : inst.I) {
		int bin = sol.item_to_bins[i];
		if (bin >= sol.total_bins) {
			if (error_msg) {
				std::stringstream ss;
				ss << "Detected bin with id " << bin << " but solutions claims that there are only " << sol.total_bins << ".";
				error_msg->push_back(ss.str());
			}
			ret = false;
		}
		else if (bin < 0) {
			if (error_msg) {
				std::stringstream ss;
				ss << "Item " << i << " is not assigned to any bin.";
				error_msg->push_back(ss.str());
			}
			ret = false;
		}
		else {
			levels[bin] += inst.s[i];
		}
	}
	for (int bin = 0; bin < sol.total_bins; bin++) {
		if (levels[bin] > inst.smax) {
			if (error_msg) {
				std::stringstream ss;
				ss << "Bin " << bin << " of size " << levels[bin] << " exceeds maximum capaicty (" << inst.smax << ").";
				error_msg->push_back(ss.str());
			}
			ret = false;
		}
	}
	return ret;
}


/*************************************************************************************************/
/* MLBP ******************************************************************************************/
/*************************************************************************************************/
bool SolutionVerifier<MLBP>::verify(const Instance<MLBP>& inst, const Solution<MLBP>& sol, std::vector<std::string>* error_msg)
{
	bool ret = true;
	/*

	//1. All items are in the bins of every level
	//2. No bin contents exceed its capacity
	//3. Once items/bins have been put into the same bin, they have to stay together in all the upcoming bins


	std::vector<std::vector<int>> bins;  // size of each bin
	std::vector<std::vector<bool>> used_binsItems;
	for (int k : inst.M) {
		bins.push_back(std::vector<int>(inst.n[k], 0));
		used_binsItems.push_back(std::vector<bool>(inst.n[k - 1], false)); //correct
		for (int i = 0; i < inst.n[0]; i++) {
			int curr = i;
			if (k > 1) {
				curr = sol.items_to_bins[k - 2][i];
			}
			int bin_idx = sol.items_to_bins[k - 1][i];
			//1.
			if (bin_idx < 0) {
				if (error_msg) {
					std::stringstream ss;
					ss << "Item " << i << " has not been assigned to any bin at level " << k;
					error_msg->push_back(ss.str());
				}
				ret = false;
				return ret;
			}
			if (!used_binsItems[k - 1][curr]) {
				used_binsItems[k - 1][curr] = true;
				bins[k - 1][bin_idx] += inst.s[k - 1][curr];
			}

		}
	}

	for (int k : inst.M) {
		for (int j = 0; j < inst.n[k]; j++) {
			//2.
			if (bins[k - 1][j] > inst.w[k][j]) {
				if (error_msg) {
					std::stringstream ss;
					ss << "Bin " << j << " at level " << k << " with contents of size " << bins[k - 1][j] << " exceeds maximum capaicty (" << inst.w[k][j] << ").";
					error_msg->push_back(ss.str());
				}
				ret = false;
			}
		}
	}

	for (int k : inst.M) {
		std::vector<std::vector<int>> same_bins_set;

		for (int i = 0; i < inst.n[0]; i++) {
			same_bins_set.push_back(std::vector<int>());
			for (int j = 1; j < same_bins_set[i].size(); j++) {
				//3.
				if (sol.items_to_bins[k - 1][same_bins_set[i][0]] != sol.items_to_bins[k - 1][same_bins_set[i][j]]) {
					if (error_msg) {
						std::stringstream ss;
						ss << "Items [" << same_bins_set[i][0] << ", " << same_bins_set[i][j] << "]" <<
							" were put together in level " << k - 1 << ", but are in seperate bins in level " << k;
						error_msg->push_back(ss.str());
					}
					ret = false;
				}
			}
		}

		for (int i = 0; i < inst.n[k - 1]; i++) {
			int item_or_bin_idx = sol.items_to_bins[k - 1][i];
			same_bins_set[item_or_bin_idx].push_back(i);
		}
	}
	*/

	/*{
	std::vector<std::vector<int>> bins;
	std::vector<std::vector<bool>> used_bins;
	for (int k : inst.M) {
		bins.push_back(std::vector<int>(inst.n[k], 0));
		used_bins.push_back(std::vector<bool>(inst.n[k], false));
	}
	for (int i = 0; i < inst.n[0]; i++) {
		int next_level_idx = i;

		for (int k = 1; k <= inst.m; k++) {
			int prev = next_level_idx;
			next_level_idx = sol.item_to_bins[k-1][next_level_idx];
			//1. //needs to be fixed TODO
			if (next_level_idx == -1) {
				if (error_msg) {
					std::stringstream ss;
					ss << "Item " << i << " is not assigned to any bin in the top level.";
					error_msg->push_back(ss.str());
				}
				ret = false;
				break;
			}
			if (!used_bins[k - 1][next_level_idx]) {
				used_bins[k - 1][next_level_idx] = true;
				bins[k - 1][next_level_idx] += inst.s[k - 1][prev];
			}
			//2.
			if (bins[k - 1][next_level_idx] > inst.w[k][next_level_idx]) {
				if (error_msg) {
					std::stringstream ss;
					ss << "Bin " << next_level_idx << " at level " << k << " with contents of size " << bins[k - 1][next_level_idx] << " exceeds maximum capaicty (" << inst.w[k][next_level_idx] << ").";
					error_msg->push_back(ss.str());
				}
				ret = false;
			}

		}
	}
	*/
	return ret;
}





/*************************************************************************************************/
/* CCMLBP ****************************************************************************************/
/*************************************************************************************************/
bool SolutionVerifier<CCMLBP>::verify(const Instance<CCMLBP>& inst, const Solution<CCMLBP>& sol, std::vector<std::string>* error_msg)
{	//1. MLBP stuff
	//4. All classes of previous bins are in the next bins
	//5. Class constraints not violated.
	bool ret = true;

	//1. All items are in the bins of every level
	//2. No bin contents exceed its capacity
	//3. Once items/bins have been put into the same bin, they have to stay together in all the upcoming bins


	std::vector<std::vector<int>> bins;  // size of each bin
	std::vector<std::vector<bool>> used_binsItems;
	/*
	for (int k : inst.M) if (k > 0) {
		bins.push_back(std::vector<int>(inst.n[k], 0));
		used_binsItems.push_back(std::vector<bool>(inst.n[k - 1], false)); //correct
		for (int i = 0; i < inst.n[0]; i++) {
			int curr = i;
			if (k > 1) {
				curr = sol.items_to_bins[k - 2][i];
			}
			int bin_idx = sol.items_to_bins[k - 1][i];
			//1.
			if (bin_idx < 0) {
				if (error_msg) {
					std::stringstream ss;
					ss << "Item " << i << " has not been assigned to any bin at level " << k;
					error_msg->push_back(ss.str());
				}
				ret = false;
				return ret;
			}
			if (!used_binsItems[k - 1][curr]) {
				used_binsItems[k - 1][curr] = true;
				bins[k - 1][bin_idx] += inst.s[k - 1][curr];
			}

		}
	}

	for (int k : inst.M) {
		for (int j = 0; j < inst.n[k]; j++) {
			//2.
			if (bins[k - 1][j] > inst.w[k][j]) {
				if (error_msg) {
					std::stringstream ss;
					ss << "Bin " << j << " at level " << k << " with contents of size " << bins[k - 1][j] << " exceeds maximum capaicty (" << inst.w[k][j] << ").";
					error_msg->push_back(ss.str());
				}
				ret = false;
			}
		}
	}
	*/
	/*

	for (int k : inst.M) if (k > 0) {
		std::vector<std::vector<int>> same_bins_set;

		for (int i = 0; i < inst.n[0]; i++) {
			same_bins_set.push_back(std::vector<int>());
			for (int j = 1; j < same_bins_set[i].size(); j++) {
				//3.
				if (sol.items_to_bins[k - 1][same_bins_set[i][0]] != sol.items_to_bins[k - 1][same_bins_set[i][j]]) {
					if (error_msg) {
						std::stringstream ss;
						ss << "Items [" << same_bins_set[i][0] << ", " << same_bins_set[i][j] << "]" <<
							" were put together in level " << k - 1 << ", but are in seperate bins in level " << k;
						error_msg->push_back(ss.str());
					}
					ret = false;
				}
			}
		}

		for (int i = 0; i < inst.n[k - 1]; i++) {
			int item_or_bin_idx = sol.items_to_bins[k - 1][i];
			same_bins_set[item_or_bin_idx].push_back(i);
		}
	}

	*/

	//4. Class consistency 
	for (int i : inst.B[0]) {//for all items
		int item = i;
		int class_i = inst.kappa[i];

		for (int k : inst.M) if (k > 0){
			if (sol.items_to_bins[k - 1][item] < 0) {
				break;
			}
			int bin = sol.items_to_bins[k - 1][item];
			
			if (sol.classes_in_bins[k][class_i][bin] == 0) {
				if (error_msg) {
					std::stringstream ss;
					ss << "item " << i << " was inserted into bin " << bin << " on level " << k << " but the class of this item: " << class_i <<
						" is not in this bin.";
					error_msg->push_back(ss.str());
				}
				ret = false;
			}
			item = bin;
		}
	
	}


	//5. Class bounds
	for (int k : inst.M) {
		int class_bound = inst.Q[k];
		
		for (int j = 0; j < inst.n[k]; j++) {
			int bin_sum = 0;
			for (int q = 0; q < inst.q; q++) {
				bin_sum += sol.classes_in_bins[k][q][j];
			}

			if (bin_sum > class_bound) {
				if (error_msg) {
					std::stringstream ss;
					ss << "The class bound for level " << k << " was " << class_bound << " but the number of classes in bin " <<
						j << " was " << bin_sum;
					error_msg->push_back(ss.str());
				}
				ret = false;
			}
		}
	}
	return ret;
}




/*************************************************************************************************/
/* MLBPCC ****************************************************************************************/
/*************************************************************************************************/
bool SolutionVerifier<MLBPCC>::verify(const Instance<MLBPCC>& inst, const Solution<MLBPCC>& sol, std::vector<std::string>* error_msg)
{
	bool ret = true;
	// TODO
	return ret;
}




/*************************************************************************************************/
/* MLBPPO ****************************************************************************************/
/*************************************************************************************************/
bool SolutionVerifier<MLBPPO>::verify(const Instance<MLBPPO>& inst, const Solution<MLBPPO>& sol, std::vector<std::string>* error_msg)
{
	bool ret = true;
	// TODO
	return ret;
}




/*************************************************************************************************/
/* MLBPTW ****************************************************************************************/
/*************************************************************************************************/
bool SolutionVerifier<MLBPTW>::verify(const Instance<MLBPTW>& inst, const Solution<MLBPTW>& sol, std::vector<std::string>* error_msg)
{
	bool ret = true;
	// TODO
	return ret;
}




/*************************************************************************************************/
/* MLBPFC ****************************************************************************************/
/*************************************************************************************************/
bool SolutionVerifier<MLBPFC>::verify(const Instance<MLBPFC>& inst, const Solution<MLBPFC>& sol, std::vector<std::string>* error_msg)
{
	bool ret = true;
	// TODO
	return ret;
}
