# Integer Programming Models for the Class Constrained Multi-Level Bin Packing Problem

### Source code and reproducibility package.
-	-----
This repository is an addition to the [Research Project CSE3000](https://github.com/TU-Delft-CSE/Research-Project) (2022) about *Integer Programming Models for the Class Constrained Multi-Level Bin Packing Problem*, see the report for more details.
### 1. Source Code
The **MLBP** folder contains all of the source code for the C++ framework and the implementations of the four formulations:
MLBP, NFMLBP, CCMLBP, NFCCMLBP.

In addition, all of the instances used to perform the experiments and the scripts used to generate new instances are in the *MLBP/inst* directory.


### 2. Reproducibility
To reproduce the results of this work, the experiments have to be repeated on the DelftBlue cluster. All scripts necessary for this can be found in the */experiment_scripts* directory.
To run the experiments follow the instructions:

1. Install CPLEX and upload all of the source code onto the used DelftBlue directory.
2. Set the enviornment variable by running: 
`echo 'export CPLEXDIR=/home/<netid>/ILOG/' >> ~/.bash_profile`
3. Compile the source code using `make`
4. Create a list of absolute paths for the used instances by running the following command in the `inst` folder
`ls -d -1 $PWD/mlbp/* > inst.txt`
5. Run a specific formulation using the command: 
`./run_experiments.py <path to executable> <path to file with list of instances> <path to file with parameter configurations> <destination folder> --summary summary.py`


### 3. Results
All of the summarised results obtained during the experiments performed on the DelftBlue cluster can be found in the */summaries* directory.

These summaries aggregated by instance class can be found in the */aggregated* directory.
