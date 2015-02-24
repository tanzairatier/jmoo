
import csv
import hv

def getFront(fname):
    file = open(fname, 'rb')
    rdr = csv.reader(file, delimiter=",")
    front = []
    for line in rdr:
        solution = [float(line[2]), float(line[3])]
        front.append(solution)
    return front

file = open("srinivasPF.pf", 'rb')
rdr = csv.reader(file, delimiter="\t")

pf = []
for line in rdr:
    solution = []
    for num in line:
        if num != "": solution.append(float(num))
    pf.append(solution)

#f1 = "data/decision_bin_table_Tanaka-p100-d2-o2_NSGAII.datatable"
#f2 = "data/decision_bin_table_Tanaka-p100-d2-o2_GALE.datatable"
#f3 = "data/decision_bin_table_Tanaka-p100-d2-o2_SPEA2.datatable"

f1 = "data/decision_bin_table_Srinivas-p100-d2-o2_NSGAII.datatable"
f2 = "data/decision_bin_table_Srinivas-p100-d2-o2_GALE.datatable"
f3 = "data/decision_bin_table_Srinivas-p100-d2-o2_SPEA2.datatable"

fronts = [getFront(fname) for fname in [f1, f2, f3]]
HV = hv.HyperVolume([300, 300])
results = [HV.compute(front) for front in fronts]

print results

