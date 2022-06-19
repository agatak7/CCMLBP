import os
import subprocess
from itertools import takewhile
from tqdm import tqdm

n_trials = 1

MLBP_instances = []
n = ['005', '010', '020', '030', '040', '050', '100']
#n = ['10', '20', '30', '40']
m = [2, 3, 4, 5]
q = ['025', '050', '075', '100']
#inst = [0, 1, 2, 3, 4]
inst = [0,1,2,3,4,5,6,7,8,9]
data = []
stat_data = []
for i in n:
    for j in m:
        for c in q:
            for k in inst:
                MLBP_instances.append("n00{}_m0{}_q{}__00{}.inst".format(i,j,c,k))

t = 600
opt_count = 0
fea_count = 0
idk_count = 0
result = ""

avg_time = 0
avg_ticks = 0
avg_bb = 0
ins = 0
num_ins = 10

for inst in tqdm(MLBP_instances):
    input_str = ".\\x64\\Debug\\MLBP.exe ifile inst\\ccmlbp\\{} prob MLBP ttime {}".format(inst, t)

    n_avg = 0
    ticks = 'undefined'
    for i in range(n_trials):
        try:
            res = subprocess.run(input_str, shell=True, capture_output=True, text=True) #, timeout=1
            output = res.stdout
            err = res.stderr
            if err:
                print("Error in " + inst + " -> " + err)
            #     # break

            try:
                a1 = output[output.index('CPLEX status:') + len('CPLEX status:'):]
                b = a1[:a1.index('\n')].strip()
                status = ''.join(takewhile(lambda x: str.isalpha(x), b))

                optim = output[output.index('optimality gap:') + len('optimality gap:'):]
                opt = optim[:optim.index('\n')].strip()
                print('optimality gap ' + opt)

                if status == 'Optimal':
                    bb = output[output.index('Branch-and-Bound nodes:') + len('Branch-and-Bound nodes:'):]
                    # bb =  bb[: bb.index('\n')].strip()
                    a5 = bb[: bb.index('\n')].strip()
                    x = a5
                    y = ''
                    while x[0].isdigit():
                        y += x[0]
                        x = x[1:]

                    avg_bb += float(y)

                    a4 = output[output.index('Total (root+branch&cut)') + len('Total (root+branch&cut) = '):]
                    # print(a4)
                    ticks = a4[:a4.index('\n')].strip()
                    ticks = ticks[ticks.index('(') + len('('): ticks.index('ticks)')]
                    # print(ticks)
                    avg_ticks += float(ticks)
                    a3 = output[output.index('CPU time:') + len('CPU time:'):]
                    time = a3[:a3.index('\n')].strip()
                    avg_time += float(time)  ## ???
                    stat_data.append([inst, status])
                else:
                    num_ins -= 1
                    stat_data.append([inst, status])
                    # add the optimality gap

            except ValueError:
                print(output)
                result += output + '\n'

        except subprocess.TimeoutExpired:
            break

    #print(inst + " -> Time: {}".format(n_avg / n_trials))
    result += inst + " -> " + ticks + ' ticks '+'\n'
    #result += inst + " -> Time: {}".format(n_avg / n_trials) + '\n'
    if (ins >= 9):
        ins = 0
        print('average time for inst ' + inst + ': ' + str(avg_time / 10))
        print('avg ticks ' + inst + ': ' + str(avg_ticks / 10))
        print('avg bb nodes ' + str(avg_bb / 10))
        print(inst[:9])
        if (num_ins > 0):
            data.append([inst[:9], avg_time / num_ins, avg_ticks / num_ins, avg_bb / num_ins])
        else:
            data.append([inst[:9], -1, -1, -1])
        avg_time = 0
        avg_ticks = 0
        avg_bb = 0
        num_ins = 10

    else:
        ins += 1
print(result)
# print("Optimal: " + str(opt_count) + " | " + "Feasible: " + str(fea_count) + " | " + "Unknown: " + str(idk_count))
# print(str(opt_count + fea_count) + '/' + str(len(MLBP_instances)))
# result += "Optimal: " + str(opt_count) + " | " + "Feasible: " + str(fea_count) + " | " + "Unknown: " + str(idk_count) + '\n'
# result += str(opt_count + fea_count) + '/' + str(len(MLBP_instances)) + '\n'

file = open("ccmlbp_test_{}.txt".format(t), "w")
file.write(result)
file.close()