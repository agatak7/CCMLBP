#! /usr/bin/python3
# Writes a problem instance to stdout 

import sys
import random
import argparse
import math
import itertools

# returns a flat list of a list of lists t
def flatten(t):
    return [item for sublist in t for item in sublist]

# returns true if there exists a path from node v1 to v2 in graph given by adj. matrix adj
def does_path_exists(v1, v2, adj):
    if v1 == v2:
        return True 
    visited = [False] * len(adj)
    queue = [v1]
    while len(queue) != 0:
        u = queue[0]
        queue.pop(0)
        if u == v2:
            return True
        if visited[u] == True:
            continue
        visited[u] = True
        queue.extend([v for v in range(len(adj)) if adj[u][v] == True and visited[v] == False])
    return False

# returns random topological order, based on Kahn's algorithm
def random_topological_sort(adj):
    L = [] # topologiacl order
    S = []
    adj_matrix = [[adj[v1][v2] for v2 in range(len(adj))] for v1 in range(len(adj))]
    for v2 in range(len(adj)):
        if not any([adj[v1][v2] for v1 in range(len(adj))]):
            S.append(v2)
    while len(S) != 0:
        random.shuffle(S)
        v1 = S.pop()
        L.append(v1)
        for v2 in range(len(adj)):
            if adj_matrix[v1][v2] == 1:
                adj_matrix[v1][v2] = False
                if not any([adj_matrix[v3][v2] for v3 in range(len(adj))]):
                    S.append(v2)
    return L


def first_fit(items, s, capacities):
    random.shuffle(items)  # insert items in random order
    bins = [(0, c, 0) for c in capacities]
    for item in items:
        inserted = False
        for pos, b in enumerate(bins):
            if b[0] + s[item] <= b[1]:
                bins[pos] = (b[0] + s[item], b[1], b[2] + 1)
                inserted = True
                break
        if inserted == False:
            # item could not be inserted -> create new bin with a bin size between s[item] ... s[item] * 1.9
            bins.append((s[item], s[item] + random.randint(0, int(math.ceil(s[item] * 0.9))), 1))
    return bins


# bins -> list of tuples (current size, capacity, items)
def first_fit_ccmlbp(items, s, kappa, Q, capacities):
    random.shuffle(items)
    bins = [(0, c, []) for c in capacities]
    for item in items:
        inserted = False
        for pos, b in enumerate(bins):
            if b[0] + s[item] <= b[1] and len(set(flatten([kappa[i] for i in b[2]] + [kappa[item]]))) <= Q:
                bins[pos] = (b[0] + s[item], b[1], b[2] + [item])
                inserted = True
                break
        if inserted == False:
            bins.append((s[item], s[item] + random.randint(0, int(math.ceil(s[item] * 0.9))), [item]))
    return bins


def first_fit_mlbpcc(items, s, conflicts, capacities):
    random.shuffle(items)
    bins = [(0, c, []) for c in capacities]
    for item in items:
        inserted = False
        for pos, b in enumerate(bins):
            if b[0] + s[item] <= b[1] and not any([conflicts[item][i] for i in b[2]]):
                bins[pos] = (b[0] + s[item], b[1], b[2] + [item])
                inserted = True
                break
        if inserted == False:
            bins.append((s[item], s[item] + random.randint(0, int(math.ceil(s[item] * 0.9))), [item]))
    return bins


def first_fit_mlbppo(items, s, adj, capacities):
    items = random_topological_sort(adj)
    #print(items)
    bins = [(0, c, []) for c in capacities]
    for item in items:
        inserted = False
        visited = [False for _ in range(len(items))]
        pred = [v for v in range(len(items)) if adj[v][item] == True]
        for pos, b in enumerate(bins):
            if b[0] + s[item] <= b[1] and all([visited[v] for v in pred]):
                bins[pos] = (b[0] + s[item], b[1], b[2] + [item])
                inserted = True
                break
            for i in b[2]:
                visited[i] = True
        if inserted == False:
            bins.append((s[item], s[item] + random.randint(0, int(math.ceil(s[item] * 0.9))), [item]))
    return bins


def print_mlbp(m, N, S, W, C):
    print(m)
    print(*N, sep=' ')
    for i in range(m+1):
        print(*S[i], sep=' ')
    for i in range(1, m+1):
        print(*W[i], sep=' ')
    for i in range(1, m+1):
        print(*C[i], sep=' ')


# Read input parameters
parser = argparse.ArgumentParser()
parser.add_argument("n", help="number of items", type=int)
parser.add_argument("m", help="number of levels", type=int)
parser.add_argument("x", help="number of times first fit algorithm is repeated to create bins", type=int)
parser.add_argument("--s", help="sample range of item sizes", type=int, nargs=2)
parser.add_argument("--type", help="problem type", choices=['MLBP','CCMLBP', 'MLBPCC', 'MLBPPO', 'MLBPTW', 'MLBPFC'], type=str, default='MLBP')
parser.add_argument("--q", help="CCMLBP: maximum number of different classes, MLBPFC: maximum number of different groups", type=int, default=1)
parser.add_argument("--Q", help="CCMLBP: for each level i, bound on the number of different classes within a bin of level i", type=int, nargs='+')
parser.add_argument("--p", help="MLBPCC: possibilty from 1 to 100 of adding a conflict between two items, MLBPPO: percentage of partial orders, MLBPFC: penalty factor", type=int, default=20)
parser.add_argument("--pl", help="planning horizon", type=int, default=10)
parser.add_argument("--tw", help="maximum time window lenght", type=int, default=3)
args = parser.parse_args()

#H = args.hbr * 0.9;

s_min = 1
s_max = 100
if args.s != None:
        s_min = args.s[0]
        s_max = args.s[1]

N = [0]*(args.m+1)                 # number of items/bins
S = [[] for _ in range(args.m+1)]  # item/bins sizes
W = [[] for _ in range(args.m+1)]  # bin capacities
C = [[] for _ in range(args.m+1)]  # bin cost

# sample item sizes
N[0] = args.n
S[0] = [random.randint(s_min, s_max+1) for _ in range(args.n)]

if args.type == 'MLBP':
    # sample bins
    for j in range(args.x):
        for i in range(args.m):
            bins = first_fit(list(range(N[i])), S[i], W[i+1])
            S[i+1] = [b[1] + random.randint(0, int(b[1] * 0.5)) for b in bins]
            W[i+1] = [b[1] for b in bins]
            N[i+1] = len(S[i+1])
            C[i+1] = [int(100*math.sqrt(s)) for s in S[i+1]]

    print_mlbp(args.m, N, S, W, C)

if args.type == 'CCMLBP':
    if args.Q == None or len(args.Q) != args.m:
        print("ERROR: please provide for each level a bound Q!")
        exit(1)
    
    # sample classes
    kappa = [random.randint(0, args.q-1) for _ in range(args.n)]

    # sample bins
    for j in range(args.x):
        kappas = [[k] for k in kappa]
        for i in range(args.m):
            bins = first_fit_ccmlbp(list(range(N[i])), S[i], kappas, args.Q[i], W[i+1])
            S[i+1] = [b[1] + random.randint(0, int(b[1] * 0.5)) for b in bins]
            W[i+1] = [b[1] for b in bins]
            N[i+1] = len(S[i+1])
            C[i+1] = [int(100*math.sqrt(s)) for s in S[i+1]]
            kappas = [flatten([kappas[item] for item in b[2]]) for b in bins]
            assert(len(S[i+1]) == len(C[i+1]) == N[i+1])

    print_mlbp(args.m, N, S, W, C)
    print(args.q)
    print(*args.Q, sep=' ')
    print(*kappa, sep=' ')

if args.type == 'MLBPCC':
    if args.p <= 0 or args.p > 100:
        print("ERROR: parameter p must be between 1 and 100!")
        exit(1)

    # sample conflicts
    conflicts = [[0 for _ in range(args.n)] for _ in range(args.n)]
    for i in range(args.n):
        for j in range(i+1, args.n):
            if random.randint(0,100) < args.p:
                conflicts[i][j] = 1
                conflicts[j][i] = 1

    # sample bins
    for j in range(args.x):
        conf = conflicts
        for i in range(args.m):
            bins = first_fit_mlbpcc(list(range(N[i])), S[i], conf, W[i+1])
            S[i+1] = [b[1] + random.randint(0, int(b[1] * 0.5)) for b in bins]
            W[i+1] = [b[1] for b in bins]
            N[i+1] = len(S[i+1])
            C[i+1] = [int(100*math.sqrt(s)) for s in S[i+1]]
            conf = [[1 if any([conf[p[0]][p[1]] for p in itertools.product(bins[b1][2],bins[b2][2]) ]) else 0 for b2 in range(N[i+1])] for b1 in range(N[i+1])]

    print_mlbp(args.m, N, S, W, C)
    for i in range(args.n):
        if sum(conflicts[i]) > 0:
            print(i, *[j for j in range(args.n) if conflicts[i][j] == 1], sep=' ')

if args.type == 'MLBPPO':
    if args.p < 0:
        print("ERROR: parameter p must be >= 0!")
        exit(1)

    # sample partial orders
    adj = [[False for _ in range(args.n)] for _ in range(args.n)]
    npos = int(args.n / 100 * args.p) # total number of partial orders
    for i in range(npos):
        while True:
            v1 = random.randint(0, args.n-1)
            v2 = random.randint(0, args.n-1)
            if does_path_exists(v2, v1, adj) == False:
                adj[v1][v2] = True
                break

    #sample bins
    for j in range(args.x):
        adj_matrix = adj
        for i in range(args.m):
            bins = first_fit_mlbppo(list(range(N[i])), S[i], adj_matrix, W[i+1])
            #print(bins)
            S[i+1] = [b[1] + random.randint(0, int(b[1] * 0.5)) for b in bins]
            W[i+1] = [b[1] for b in bins]
            N[i+1] = len(S[i+1])
            C[i+1] = [int(100*math.sqrt(s)) for s in S[i+1]]
            adj_matrix = [[True if any([adj_matrix[p[0]][p[1]] for p in itertools.product(bins[b1][2],bins[b2][2])]) else False for b2 in range(N[i+1])] for b1 in range(N[i+1])]

    print_mlbp(args.m, N, S, W, C)
    print(npos)
    for v1 in range(args.n):
        for v2 in range(args.n):
            if adj[v1][v2] == True:
                print(v1, v2)

if args.type == 'MLBPTW':
    #sample time windows
    e = [random.randint(0, args.pl-1) for _ in range(args.n)]
    l = [min(args.pl-1, e[i] + random.randint(0, args.tw-1)) for i in range(args.n)]

    conflicts = [[0 for _ in range(args.n)] for _ in range(args.n)]
    for i in range(args.n):
        for j in range(i+1, args.n):
            if l[i] < e[j] or l[j] < e[i]:
                conflicts[i][j] = 1
                conflicts[j][i] = 1

    # sample bins
    for j in range(args.x):
        conf = conflicts
        for i in range(args.m):
            bins = first_fit_mlbpcc(list(range(N[i])), S[i], conf, W[i+1])
            S[i+1] = [b[1] + random.randint(0, int(b[1] * 0.5)) for b in bins]
            W[i+1] = [b[1] for b in bins]
            N[i+1] = len(S[i+1])
            C[i+1] = [int(100*math.sqrt(s)) for s in S[i+1]]
            conf = [[1 if any([conf[p[0]][p[1]] for p in itertools.product(bins[b1][2],bins[b2][2]) ]) else 0 for b2 in range(N[i+1])] for b1 in range(N[i+1])]

    print_mlbp(args.m, N, S, W, C)
    print(args.p)
    print(*e, sep=' ')
    print(*l, sep=' ')

if args.type == 'MLBPFC':
    # sample groups
    G = [random.randint(1,args.q) for _ in range(N[0])]

    # sample bins
    for j in range(args.x):
        for i in range(args.m):
            bins = first_fit(list(range(N[i])), S[i], W[i+1])
            S[i+1] = [b[1] + random.randint(0, int(b[1] * 0.5)) for b in bins]
            W[i+1] = [b[1] for b in bins]
            N[i+1] = len(S[i+1])
            C[i+1] = [int(100*math.sqrt(s)) for s in S[i+1]]

    print_mlbp(args.m, N, S, W, C)
    print(args.q, args.p)
    print(*G, sep=' ')

