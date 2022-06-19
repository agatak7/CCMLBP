///////////////////////////////////////////////////////////////////////////////////////////////////
//  MLBP Instances
///////////////////////////////////////////////////////////////////////////////////////////////////

example of filename: n0005_m01__001.inst 
 n0005 -> number of items  (here 5 items)
 m01   -> number of levels (here 1 level)
 __001 -> instance index 
 
++ format ++
m
n^0 n^1 ... n^m
s^0_1 s^0_2 ... s^0_{n^0}
s^1_1 s^1_2 ... s^1_{n^1}
...
s^m_1 s^m_2 ... s^m_{n^m}
w^1_1 w^1_2 ... w^1_{n^1}
...
w^m_1 w^m_2 ... w^m_{n^m}
c^1_1 c^1_2 ... c^1_{n^1}
...
c^m_1 c^m_2 ... c^m_{n^m}

++ explanation ++
first  line:  number of levels
second line:  number of items (n^0) + number of bins at each level (n^1 ... n^m)
third  line:  size of each item 
next m lines: size of each bin at each level
next m lines: weight of each bin at each level
next m lines: cost of each bin at each level



///////////////////////////////////////////////////////////////////////////////////////////////////
//  CCMLBP Instances
///////////////////////////////////////////////////////////////////////////////////////////////////

example of filename: n0005_m01_q025__001.inst 
 n0005 -> number of items  (here 5 items)
 m01   -> number of levels (here 1 level)
 q025  -> maximum number of different classes, based on the number of items in percent (here 25% of 5 items = 2.5 -> at most 3 different classes)
 __001 -> instance index 
 
++ format ++
m
n^0 n^1 ... n^m
s^0_1 s^0_2 ... s^0_{n^0}
s^1_1 s^1_2 ... s^1_{n^1}
...
s^m_1 s^m_2 ... s^m_{n^m}
w^1_1 w^1_2 ... w^1_{n^1}
...
w^m_1 w^m_2 ... w^m_{n^m}
c^1_1 c^1_2 ... c^1_{n^1}
...
c^m_1 c^m_2 ... c^m_{n^m}
q
Q^1 Q^2 ... Q^m
kappa^1 kappa^2 ... kappa^_{n^0}

++ explanation ++
first  line:  number of levels
second line:  number of items (n^0) + number of bins at each level (n^1 ... n^m)
third  line:  size of each item 
next m lines: size of each bin at each level
next m lines: weight of each bin at each level
next m lines: cost of each bin at each level
next line:    number of classes 
next line:    for each level: bound for the number of different allowed classes in bins
next line:    class of each item



///////////////////////////////////////////////////////////////////////////////////////////////////
//  MLBPCC Instances
///////////////////////////////////////////////////////////////////////////////////////////////////

example of filename: n0005_m01_p025__001.inst 
 n0005 -> number of items  (here 5 items)
 m01   -> number of levels (here 1 level)
 p025  -> the probability that two items are in conflict with each other (here 25%)
 __001 -> instance index 
 
++ format ++
m
n^0 n^1 ... n^m
s^0_1 s^0_2 ... s^0_{n^0}
s^1_1 s^1_2 ... s^1_{n^1}
...
s^m_1 s^m_2 ... s^m_{n^m}
w^1_1 w^1_2 ... w^1_{n^1}
...
w^m_1 w^m_2 ... w^m_{n^m}
c^1_1 c^1_2 ... c^1_{n^1}
...
c^m_1 c^m_2 ... c^m_{n^m}
I_{i} I_{j_1} I_{j_2} ...
...

++ explanation ++
first  line:  number of levels
second line:  number of items (n^0) + number of bins at each level (n^1 ... n^m)
third  line:  size of each item 
next m lines: size of each bin at each level
next m lines: weight of each bin at each level
next m lines: cost of each bin at each level
next lines:   for each item I_{i} the adjacency list of conflict items (I_{j_1} I_{j_1} ...); Note that if an item does not conflict with any other item, the corresponding line of that item is omitted



///////////////////////////////////////////////////////////////////////////////////////////////////
//  MLBPPO Instances
///////////////////////////////////////////////////////////////////////////////////////////////////

example of filename: n0005_m01_p025__001.inst 
 n0005 -> number of items  (here 5 items)
 m01   -> number of levels (here 1 level)
 p025  -> number of precedence relationships, based on the number of items in percent (here 25% of 5 items = 2.5 -> at 3 precedence relationships between items)
 __001 -> instance index 
 
++ format ++
m
n^0 n^1 ... n^m
s^0_1 s^0_2 ... s^0_{n^0}
s^1_1 s^1_2 ... s^1_{n^1}
...
s^m_1 s^m_2 ... s^m_{n^m}
w^1_1 w^1_2 ... w^1_{n^1}
...
w^m_1 w^m_2 ... w^m_{n^m}
c^1_1 c^1_2 ... c^1_{n^1}
...
c^m_1 c^m_2 ... c^m_{n^m}
p
I_{j_1} I_{j2}
...

++ explanation ++
first  line:  number of levels
second line:  number of items (n^0) + number of bins at each level (n^1 ... n^m)
third  line:  size of each item 
next m lines: size of each bin at each level
next m lines: weight of each bin at each level
next m lines: cost of each bin at each level
next line:    number of precedence relationships
next p lines: pairs of items I_{j_1} I_{j2} such that item I_{j_1} must be packed in a bin with lower index number than item I_{j_2}



///////////////////////////////////////////////////////////////////////////////////////////////////
//  MLBPTW Instances
///////////////////////////////////////////////////////////////////////////////////////////////////

example of filename: n0005_m01_pl10_tw05_p40__001.inst 
 n0005 -> number of items  (here 5 items)
 m01   -> number of levels (here 1 level)
 pl10  -> planning horizon (here 10 time units, e.g. 10 days)
 tw05  -> maximum length of time windows (here 5 days)
 p     -> penalty factor (here 40)
 __001 -> instance index 
 
++ format ++
m
n^0 n^1 ... n^m
s^0_1 s^0_2 ... s^0_{n^0}
s^1_1 s^1_2 ... s^1_{n^1}
...
s^m_1 s^m_2 ... s^m_{n^m}
w^1_1 w^1_2 ... w^1_{n^1}
...
w^m_1 w^m_2 ... w^m_{n^m}
c^1_1 c^1_2 ... c^1_{n^1}
...
c^m_1 c^m_2 ... c^m_{n^m}
p
e_1 e_2 ... e_{n^0}
e_2 l_2 ... l_{n^0}


++ explanation ++
first  line:  number of levels
second line:  number of items (n^0) + number of bins at each level (n^1 ... n^m)
third  line:  size of each item 
next m lines: size of each bin at each level
next m lines: weight of each bin at each level
next m lines: cost of each bin at each level
next line:    penalty factor
next line:    earliest packing time of each item
next line:    latest packing time of each item



///////////////////////////////////////////////////////////////////////////////////////////////////
//  MLBPFC Instances
///////////////////////////////////////////////////////////////////////////////////////////////////

example of filename: n0005_m01_q025_p40__001.inst 
 n0005 -> number of items  (here 5 items)
 m01   -> number of levels (here 1 level)
 q025  -> maximum number of different groups, based on the number of items in percent (here 25% of 5 items = 2.5 -> at most 3 different groups)
 p40   -> penalty factor (here 40)
 __001 -> instance index 
 
++ format ++
m
n^0 n^1 ... n^m
s^0_1 s^0_2 ... s^0_{n^0}
s^1_1 s^1_2 ... s^1_{n^1}
...
s^m_1 s^m_2 ... s^m_{n^m}
w^1_1 w^1_2 ... w^1_{n^1}
...
w^m_1 w^m_2 ... w^m_{n^m}
c^1_1 c^1_2 ... c^1_{n^1}
...
c^m_1 c^m_2 ... c^m_{n^m}
q p
g_1 g_2 ... g_{n^0}


++ explanation ++
first  line:  number of levels
second line:  number of items (n^0) + number of bins at each level (n^1 ... n^m)
third  line:  size of each item 
next m lines: size of each bin at each level
next m lines: weight of each bin at each level
next m lines: cost of each bin at each level
next line:    number of different groups and penalty factor
next line:    group of each item
