#!/usr/bin/python3
"""Summarizes the essential information from several algorithm runs
   into a CSV-table written to stdout.

The result files to be processed are given as arguments (out-files or 
directories containing out-files)
The CSV-table contains:
- file: name of processed out-filename
- obj: objective value of final solution
- db: best dual bound
- ttot: total CPU-time
  babn: number of branch-and-bound nodes
"""

import argparse, os, glob, re
import numpy as np

# process list of files/directories
def processlist(args, files):
    for file in files:
        if os.path.isdir(file):
            processlist(args,glob.glob(file+"/*.out"))
        else:
            # process out-file
            obj = ttot = cbplb = db = babn = opt = status = np.nan
            with open(file) as f:
                for line in f:
                    m = re.match(r'best objective value:\s(\d+\.?\d*)', line)
                    if m: obj = m.group(1)
                    m = re.match(r'CPU time:\s(\d+\.?\d*)', line)
                    if m: ttot = m.group(1)
                    m = re.match(r'best dual bound value:\s(\d+\.?\d*)', line)
                    if m: db = m.group(1)
                    m = re.match(r'Branch-and-Bound nodes:\s(\d+)', line)
                    if m: babn = m.group(1)
                    m = re.match(r'optimality gap:\s(\d+\.?\d*)', line)
                    if m: opt = m.group(1)
                    m = re.match(r'CPLEX status:\s(\w+\.?\w*)', line)
                    if m: status = m.group(1)

            print(file,obj,db,ttot,babn, opt,status, sep="\t",end='')
            print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exctract summary info from many runs.")
    parser.add_argument("files", nargs="*", help=".out files to be processed")
    args = parser.parse_args()
    print("file\tobj\tdb\tttot\tbabn\toptgap",end='')
    print()
    processlist(args,args.files)

