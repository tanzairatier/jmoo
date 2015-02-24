from jmoo_properties import *
import csv

s = ""

for p,prob in enumerate(problems):
        
        
        for a,alg in enumerate(algorithms):
            f4input = open(DATA_PREFIX + "decision_bin_table" + "_" + prob.name + "_" + alg.name + DATA_SUFFIX, 'rb')
            reader4 = csv.reader(f4input, delimiter=',')
            
            for line in reader4:
                s += prob.name + "," + alg.name + ","
                for item in line:
                    s += str(item) + "," 
                s += "\n"
                
print s

fa = open('data/decision_bin_table_.databtable', 'w')
fa.write(s)