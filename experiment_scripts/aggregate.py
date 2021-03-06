#!/usr/bin/python3
"""Calculate grouped basic statistics for one or two csv-files obtained e.g. by
summary.py.

The input data are either given via stdin or in one or two files provided 
as parameters. If two tsv files are given, they are assumed to be results
from two different algorithms on the same instances, and they are compared
including a Wilcoxon rank sum test.

Important: For the aggregation to work correctly, adapt in particular
below definitions of categ, categ2 and categbase according to your
conventions for the filenames encoding instance and run information.
"""

import pandas as pd
import numpy as np
import scipy.stats
import sys
import re
import warnings
import argparse
import math


#--------------------------------------------------------------------------------
def categ(x):
    """Determine the category name to aggregate over from the given file name.
    
    For aggregating a single table of raw data,  
    return category name for a given file name.
    """
    #home/matthias/va-scheduling/results/nt5000_as05__007.out
    # re.sub(r"^(.*)/(T.*)-(.*)_(.*).res",r"\1/\2-\3",x)
    #return re.sub(r".*[lcs|lcps]_(\d+)_(\d+)_(\d+)\.(\d+)(\.out)", 
    #    r"\1/\2-\3",x)
    return re.sub(r"^.*/(n\d*)_(m\d*)__(.*)\.out",r"\2-\1",x)
#
    #return re.sub(r"([^/#_]*)(_.*_)?([^/#_]*)(__\d+)?([^/#_]*)\.out",
    #    r"\1\3\5",x)

def categ2(x):
    """For aggregating two tables corresponding to two different summary files,
    extract category name from the given file names that shall be compared.
    """
    # re.sub(r"^(.*)/(T.*)-(.*)_(.*).res",r"\2-\3")
    #return re.sub(r"^.*[lcs|lcps]_(\d+)_(\d+)_(\d+)\.(\d+)(\.out)",
    #       r"\1/\2-\3",x)
    return re.sub(r"^.*/(n\d*)_(m\d*)__(.*)\.out",r"\2-\1",x)
    #return re.sub(r"^.*/([^/#_]*)(_.*_)?([^/#_]*)(#\d+)?([^/#_]*)\.out",
    #       r"\1\2\3\4\5",x)

def categbase(x):
    """For aggregating two tables corresponding to two different 
    configurations that shall be compared, return detailed name of run 
    (basename) that should match a corresponding one of the other configuration.
    """
    #re.sub(r"^.*/(T.*)-(.*)_(.*).res",r"\1-\2-\3",x)
    #return re.sub(r"^.*[lcs|lcps]_(\d+)_(\d+)_(\d+)\.(\d+)(\.out)",
    #       r"\1_\2_\3.\4\5",x)
    return re.sub("^.*/.*_(n\d*)_(m\d*)__(.*)\.out",
                  r"\2\1__\3",x)
    #return re.sub(r"^.*/([^/#_]*)(_.*_)?([^/#_]*)(#\\d+)?([^/#_]*)\\.out",
    #       r"\1_\2_\3.\4\5",x)
       
def print_table_context():
    """Set display options forprinting tables unabbreviated.
    """
    return pd.option_context("display.width",100000,
                             "display.max_rows",1000,
                             "display.max_colwidth",10000,
                             "display.precision",8)

#--------------------------------------------------------------------------------
# General helper functions

def geometric_mean(x,shift=0):
    """Calculates geometric mean with shift parameter.
    """
    return math.exp(math.mean(math.log(x+shift)))-shift   

#-------------------------------------------------------------------------
# Aggregation of one summary data frame

def aggregate(rawdata,categfactor=categ):
  
    """Determine aggregated results for one summary data frame.
    """
    rawdata["cat"]=rawdata.apply(lambda row: categfactor(row["file"]),axis=1)
    print(rawdata["cat"])
    rawdata["obj"]=rawdata.apply(lambda row: row["obj"] if row["obj"] != np.nan else 0,axis=1)
    #rawdata["ttot"]=rawdata.apply(lambda row: row["ttot"] if row["ttot"] != np.nan else 0,axis=1)
    #rawdata["babn"]=rawdata.apply(lambda row: row["babn"] if row["babn"] != np.nan else 0,axis=1)
    if "db" in rawdata:
        rawdata["gap"]=rawdata.apply(lambda row: abs(row["db"]-row["obj"])/
               max(row["obj"],row["db"]) if row["db"] != np.nan and max(row["obj"],row["db"]) > 0 else np.nan,axis=1)
        rawdata["isopt"]=rawdata.apply(lambda row: row["db"]==row["obj"] if row["db"] != np.nan and max(row["obj"],row["db"]) > 0 else False,axis=1)
    rawdata["status"] = [1 if item =='Optimal' else 0 for item in rawdata["status"]]
    grp = rawdata.groupby("cat")
    aggregated=pd.DataFrame({"runs":grp["obj"].size()})
    aggregated["obj_mean"]=grp["obj"].mean()
    aggregated["obj_sd"]=grp["obj"].std()
    aggregated["ttot_med"]=grp["ttot"].median()
    aggregated["babn_mean"]=grp["babn"].mean()

    stats = grp["status"]
    aggregated["status"] = stats.mean()
    aggregated.index.name = None  

    
    return aggregated
    
def totalagg(agg):
    """Calculate total values over aggregated data.
    """
    total = pd.DataFrame({"total":[""]})
    total["runs"]=[agg["runs"].sum()]
    total["obj_mean"]=[agg["obj_mean"].mean()]
    total["obj_sd"]=[agg["obj_sd"].mean()]
    total["ttot_med"]=[agg["ttot_med"].median()]
    total["babn_mean"]=[agg["babn_mean"].mean()]
    total["status"] = [agg["status"].mean()]
    total = total.set_index("total")
    total.index.name = None
    return total

def make_index(a):
    """Assumes that the index is a filename and turns it into a multilevel index."""
    idx = {}
    for fn in a.index:
        l = re.findall("[a-zA-Z]+\d+",fn)
        for s in l:
            m = re.match("([a-zA-Z]+)(\d+)$",s)
            if m.group(1) in idx:
                idx[m.group(1)].append(int(m.group(2)))
            else:
                idx[m.group(1)] = [int(m.group(2))]
    for k in idx: 
        a[k] = idx[k]
    a.set_index(list(idx.keys()),inplace=True)
    return a
            
def roundagg(a):
    """Reasonably round aggregated results for printing.
    """
    return a.round({'obj_mean':6, 'obj_sd':6, 'db_mean':6, 'db_std':6, 
                    'gap_mean':6, 'gap_std':6,'ittot_med':1, 'itbest_med':1,
                    'ttot_med':1, 'tbest_med':1, 'topt_med':1,
                    'obj0_mean':6, 'obj0_gmean':6, 'obj1_mean':6,'obj1_gmean':6,
                    'V_mean':1, 'exps_mean':1, 'pruned_mean':1, 'reexps_mean':1,
                    'A_mean':1, 'afilt_mean':1, 'nfilt_mean':1, 'dbfilt_mean':1, 'tfilt_mean':1,
                    })

def agg_print(rawdata):
    """Perform aggregation and print results for one summary data frame.
    """
    nfcateg = {"nfmlbp": (lambda x: re.sub(r"^.*/(n\d*)_(m\d*)_(q\d*)__(.*)\.out", r"\3-\2-\1", x)),
               }
    aggregated = aggregate(rawdata, nfcateg["nfmlbp"])
    aggtotal = totalagg(aggregated)
    with print_table_context():
        print(roundagg(aggregated).to_string())
        print("\nTotals:")
        print(roundagg(aggtotal))


#-------------------------------------------------------------------------
# Aggregation and comparison of two summary data frames


def stattest(col1,col2):
    """Perform statistical test (Wilcoxon signed ranktest) on col1[x] and col2[x]
    """
    dif = col1-col2
    noties = len(dif[dif!=0])
    lessass = dif.sum()<0
    if noties<1:
        return float(1)
    # if (col1==col2).all():
    #     return 3
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        msr,p = scipy.stats.wilcoxon(col1,col2,correction=True,zero_method="wilcox")
    #s,p = scipy.stats.mannwhitneyu(col1,col2,alternative="less")
    p = p/2
    if not lessass:
        p = 1-p
    return p

def doaggregate2(raw,fact,criterion):
    """Aggregate results of differences for the given criterion on
       two merged summary data frames.
    """
    c_diff=criterion+"_diff"
    c_x=criterion+"_x"
    c_y=criterion+"_y"
    raw[c_diff]=raw.apply(lambda row: row[c_x]-row[c_y],axis=1)
    raw["AlessB"]=raw.apply(lambda row: int(row[c_x]<row[c_y]),axis=1)
    raw["BlessA"]=raw.apply(lambda row: int(row[c_x]>row[c_y]),axis=1)
    raw["AeqB"]=raw.apply(lambda row: int(row[c_x]==row[c_y]),axis=1)
    # rawdata["gap"]=raw.apply(lambda row: (row["ub"]-row["obj"])/row["ub"],axis=1)
    grp = raw.groupby(fact)
    p_AlessB=[]
    p_BlessA=[]
    for g,d in grp:
        p_AlessB.append(stattest(d[c_x],d[c_y]))
        p_BlessA.append(stattest(d[c_y],d[c_x]))
    aggregated = pd.DataFrame({"runs":grp[c_x].size()})
    aggregated["A_"+criterion+"_mean"]=grp[c_x].mean()
    aggregated["B_"+criterion+"_mean"]=grp[c_y].mean()
    aggregated["diff_mean"]=grp[c_diff].mean()
    aggregated["AlessB"]=grp["AlessB"].sum()
    aggregated["BlessA"]=grp["BlessA"].sum()
    aggregated["AeqB"]=grp["AeqB"].sum()
    aggregated["p_AlessB"]=p_AlessB
    aggregated["p_BlessA"]=p_BlessA
    return aggregated
    
def aggregate2(rawdata1,rawdata2,criterion):
    """Determine aggregated results for two summarry data frames including 
       statistical tests for significant differences of results for the
       given criterion.
    """
    rawdata1["base"]=rawdata1.apply(lambda row: categbase(row["file"]),axis=1)
    rawdata2["base"]=rawdata2.apply(lambda row: categbase(row["file"]),axis=1)
    raw = pd.merge(rawdata1,rawdata2,on="base",how="outer")
    raw["class"]=raw.apply(lambda row: categ2(row["file_x"]),axis=1)
    aggregated = doaggregate2(raw,"class",criterion)
    raw["total"]=raw.apply(lambda row: "total",axis=1)
    aggtotal = doaggregate2(raw,"total",criterion)
    return {"grouped":aggregated,"total":aggtotal}

def roundagg2(a,criterion):
    """Rounds aggregated data for two summary data frames for printing.
    """
    a["AlessB"] = a["AlessB"].map(lambda x: int(x))
    a["BlessA"] = a["BlessA"].map(lambda x: int(x))
    a["AeqB"] = a["AeqB"].map(lambda x: int(x))
    a = a.round({"A_"+criterion+"_mean":6, "B_"+criterion+"_mean":6, "diff_mean":6, 
                    "AlessB":0, "BlessA":0, "AeqB":0, "p_AlessB":4, "p_BlessA":4})
    return a
    
def printsigdiffs(agg2):
    """Print signifficant differences in aggregated data for two summary 
    data frames.
    """
    Awinner = sum(agg2["AlessB"]>agg2["BlessA"])
    Bwinner = sum(agg2["AlessB"]<agg2["BlessA"])
    gr = agg2["AlessB"].size
    print("A is yielding more frequently better results on ", Awinner,
          " groups (",round(Awinner/gr*100,2),"%)") 
    print("B is yielding more frequently better results on ", Bwinner, 
          " groups (",round(Bwinner/gr*100,2),"%)") 
    print("\nSignificant differences:")
    sigAlessB = agg2[agg2.p_AlessB<=0.05] 
    sigBlessA = agg2[agg2.p_BlessA<=0.05] 
    if not sigAlessB.empty:
        print("\np_AlessB<=0.05\n",sigAlessB)
    if not sigBlessA.empty:
        print("\np_BlessA<=0.05\n",sigBlessA)         

def agg2_print(rawdata1,rawdata2,criterion):
    """Perform aggregation and print comparative results for two summary 
    data frames.
    """
    with print_table_context():
        aggregated = aggregate2(rawdata1,rawdata2,criterion)
        print(roundagg2(pd.concat([aggregated["grouped"],aggregated["total"]]),
                        criterion))
        #print(roundagg2(aggregated["total"]))
        print("")
        printsigdiffs(roundagg2(pd.concat([aggregated["grouped"],
                                           aggregated["total"]]), criterion))
    
#-------------------------------------------------------------------------
# main part

# If called as script read one or two summary files or summary data from
# stdin, aggregate, and print.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate aggregated statistics for one or two summary files obtained from summary.py")
    parser.add_argument("file", nargs="?", help="File from summary.py to be aggregated")
    parser.add_argument("file2", nargs="?", help="Second file from summary.py to be aggregated and compared to")
    parser.add_argument("-c", "--criterion", default="obj", help="Criterion for statistical tests, default: obj")
    args = parser.parse_args()
    
    if not args.file2:
        # process one summary file
        f = args.file if args.file else sys.stdin 
        rawdata = pd.read_csv(f, sep='\t')
        #rawdata["obj"] = calculateObj(rawdata,args)
        agg_print(rawdata)
    else:
        # process and compare two summary files
        rawdata1 = pd.read_csv(args.file, sep='\t')
        rawdata2 = pd.read_csv(args.file2, sep='\t')
        agg2_print(rawdata1,rawdata2,args.criterion) 
