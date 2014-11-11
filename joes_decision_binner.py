
"""
##########################################################
### @Author Joe Krall      ###############################
### @copyright see below   ###############################

    This file is part of JMOO,
    Copyright Joe Krall, 2014.

    JMOO is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    JMOO is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with JMOO.  If not, see <http://www.gnu.org/licenses/>.
    
###                        ###############################
##########################################################
"""

"Brief notes"
"Report on decision bins used."

from pylab import *
import csv
from jmoo_problems import *
from jmoo_algorithms import *
from jmoo_stats_box import *
from jmoo_properties import *
import random, utility

from time import *
import os

class histobin:
     def __init__(self, numBins, decision):
         self.numBins = numBins
         self.bins = []
         spread  =  decision.up - decision.low
         step = spread/float(numBins)
         self.bins = [bin(i, decision.low + step*i, decision.low + step*(i+1)) for i in range(numBins)]
     def getTotal(self):
         total = 0
         for bin in self.bins:
             total += bin.count
         return total
     def __repr__(self):
         s = "["
         total = self.getTotal()
         if total == 0: return  str([0 for bin in self.bins])
         for bin in self.bins:
             s += str("%3.0f" % (100.0*bin.count/float(total))) + " "
         s += "]"
         return s
     def populate(self, data):
         for item in data:
             for b,bin in enumerate(self.bins):
                 if b == 0:
                     if item >= bin.low and item < bin.up:
                         self.bins[b].add(item)
                         break
                 elif b == (len(self.bins)-1):
                     if item > bin.low and item <= bin.up:
                         self.bins[b].add(item)
                         break
                 else:
                     if item > bin.low and item < bin.up:
                         self.bins[b].add(item)
                         break
     def sort(self, bywhat=None):
         if bywhat == "count": bywhat = lambda bin: bin.count
         else: bywhat = lambda bin: bin.index
         
         self.bins = sorted(self.bins, key=bywhat)
class bin:
     def __init__(self, ind, low, up):
         self.index = ind
         self.low = low
         self.up = up
         self.count = 0
         self.items = []
     def add(self, item):
         self.count += 1
         self.items.append(item)
         
def joes_decision_reporter(problems, algorithms, tag=""):
    date_folder_prefix = strftime("%m-%d-%Y")
    if not os.path.isdir('reports/' + date_folder_prefix):
        os.makedirs('reports/' + date_folder_prefix)
    fignum = len([name for name in os.listdir('reports/' + date_folder_prefix)]) + 1
    #optional tag name for the file
    fa = open('reports/' + date_folder_prefix + "/decision_bin_rules_report" + "_" + tag + str("%02d" % fignum) + ".txt", 'w')
    
    decision_data = []
    objective_data = []
    
    f, axarr = plt.subplots(max(2,len(problems)), max(2,len(algorithms)))
    f.set_size_inches(6.75, 10.25)
    for p,problem in enumerate(problems):
        decision_data.append([])
        objective_data.append([])
        for a,algorithm in enumerate(algorithms):
            finput = open(DATA_PREFIX + DECISION_BIN_TABLE + "_" + problem.name + "_" + algorithm.name + DATA_SUFFIX, 'rb')
            reader = csv.reader(finput, delimiter=',')
            
            decision_data[p].append([])
            objective_data[p].append([])
            
            for i,row in enumerate(reader):
                if i == 0: 
                    objective_data[p][a] = [[] for obj in problem.objectives]
                    decision_data[p][a] = [[] for dec in problem.decisions]
                    
                elements = row
                for d,dec in enumerate(problem.decisions):
                    decision_data[p][a][d].append(float(elements[d]))
                d = len(problem.decisions)
                
                for o,obj in enumerate(problem.objectives):
                    if not elements[d+o].strip() == "?": objective_data[p][a][o].append(float(elements[d+o]))
            
            # histogram
            recommendations = []
            lows = []
            ups = []
            ranges = []
            numAttributes = len(problem.decisions)
            numBins = 10
            for c,col in enumerate(decision_data[p][a]):
                histobins = [histobin(numBins, problem.decisions[i]) for i in range(numAttributes)]
                histobins[c].populate(col)
                
                histo,bin = numpy.histogram(col, bins=10)
                bins = []
                total = float(sum(histo))
                s = ""
                for h in histo:
                    bins.append(   ((h/total)*100)   )
                    s += str( ("%4.0f" % bins[-1]   ) ) + ","
                print histobins[c], algorithm.name, ",", problem.name, ", ", problem.decisions[c].name
                maxbin = 0
                biggest = 0
                for ix,b in enumerate(bins):
                    if b > biggest:
                        biggest = b
                        maxbin = ix
                
                lows.append(bin[maxbin])
                ups.append(bin[maxbin+1])
                recommendations.append(    "[" + str( bin[maxbin]) + "~" +  str(bin[maxbin+1]) +  "]"     )
                ranges.append(   [ bin[maxbin],  bin[maxbin+1]  ]   )
                #print s, algorithm.name, ",", problem.name, ", ", problem.decisions[c].name, ",", str(maxbin), ", ", bin[maxbin], ", ", bin[maxbin+1], ", [", bin[maxbin], "~", bin[maxbin+1], "]"
            """ 
            for d,dec in enumerate(problem.decisions):
                z = algorithm.name + " on " + problem.name + " recommends the following range for " + dec.name + ":" + recommendations[d]
                print z
                fa.write(z + "\n")
            """
            z = '{0: <16}'.format(problem.name) + "," + '{0: <16}'.format(algorithm.name) + "," + '{0: <16}'.format("DecisionNames, ")
            for d in problem.decisions: z += '{0: >8}'.format(d.name) + ","
            z += "\n" + '{0: <16}'.format(problem.name) + "," + '{0: <16}'.format(algorithm.name) + "," + '{0: <16}'.format("LowerBounds, ")
            for l in lows: z += str("%8.2f" % l) + ","
            z += "\n" + '{0: <16}'.format(problem.name) + "," + '{0: <16}'.format(algorithm.name) + "," + '{0: <16}'.format("UpperBounds, ")
            for u in ups: z += str("%8.2f" % u) + ","
            z += "\n" + '{0: <16}'.format(problem.name) + "," + '{0: <16}'.format(algorithm.name) + "," + '{0: <16}'.format("ObjectiveNames, ")
            for o in problem.objectives: z += '{0: >8}'.format(o.name) + ","
            
            #read baseline
            f2input = open("data/" + problem.name + str(MU) + "dataset.txt", 'rb')
            reader2 = csv.reader(f2input, delimiter=',')
            referencePoint = []
            for i,row in enumerate(reader2):
                if i > MU:
                    referencePoint.append(float(row[1]))
            
            trials = []
            for repeat in range(20):
                novel_candidate = [  random.uniform(rng[0], rng[1]) for rng in ranges  ]
                trials.append(problem.evaluate(novel_candidate))
            validation_vector = utility.matrix_avg(trials)
            
            z += "\n" + '{0: <16}'.format(problem.name) + "," + '{0: <16}'.format(algorithm.name) + "," + '{0: <16}'.format("Validation, ")
            for vv in validation_vector: z += str("%8.2f" % vv) + ","
            
            # Split Columns into Lists
            fitnessColumns = [[fit[i] for fit in trials] for i,obj in enumerate(problem.objectives)]
        
            # Calculate Medians and Spreads
            fitnessMedians = [median(fitCol) for fitCol in fitnessColumns]
            fitnessSpreads = [spread(fitCol) for fitCol in fitnessColumns]
            
            # Calculate IBD & IBS
            norms = [[min(fitnessColumns[i]+[referencePoint[i]]), max(fitnessColumns[i]+[referencePoint[i]])] for i,obj in enumerate(problem.objectives)]
            lossInQualities = [loss_in_quality(problem, [referencePoint], fit, norms) for fit in trials]
            IBD = median(lossInQualities)
            IBS = spread(lossInQualities)
            z += str("%8.2f" % IBD) + "," + str("%8.2f" % IBS)
            
            
            
            z += "\n" + '{0: <16}'.format(problem.name) + "," + '{0: <16}'.format(",") + "," + '{0: <16}'.format("Baseline, ")
            for i,row in enumerate(referencePoint):
                    z += str("%8.2f" % float(row)) + ","
            
            
            
            
            
            #print z
            fa.write(z + "\n")
                
            for c,col in enumerate(objective_data[p][a]):
                histo,bin = numpy.histogram(col, bins=10)
                total = float(sum(histo))
                s = ""
                for h in histo:
                    s += str( ("%4.0f" % ((h/total)*100)) ) + ","
                #print s, algorithm.name, ",", problem.name, ", ", problem.objectives[c].name
            