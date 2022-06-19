#! /usr/bin/python3
# Creates instance files 

import sys
import os
import argparse
import math

# instance classes
ns  = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 100]
ms  = [1, 2, 3, 4, 5]
tws = [1, 5, 10]

x = 2 # number of times first fit is repeated

ninst = 10 # number of instances per class


parser = argparse.ArgumentParser(description="Create benchmark instances")
parser.add_argument("destination", nargs=1, type=str, help="Destination folder of created instances")
parser.add_argument("-n", type=int, default=10, help="Number of instances per instance class")
parser.add_argument("-v", "--verbose", help="Let the world know about progress", action="store_true")
args = parser.parse_args()

outfolder = args.destination[0]
ninst = args.n;

for n in ns:
    for m in ms:
        for tw in tws:
            for i in range(ninst):
                cmd = './randgen.py {} {} {} --s 1 20 --type MLBPTW --pl 10 --tw {} --p 40 > {}n{:04d}_m{:02d}_pl10_tw{:02d}_p40__{:03d}.inst'.format(n, m, x, tw, outfolder, n, m, tw, i)
                os.system(cmd)
                if args.verbose:
                    print(cmd)
