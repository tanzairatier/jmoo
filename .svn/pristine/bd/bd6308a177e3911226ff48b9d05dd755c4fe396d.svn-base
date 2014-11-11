from pylab import *
import csv
from jmoo_problems import *
from jmoo_algorithms import *
from jmoo_properties import *
import random, utility

from time import *
import os



class histobin:
    def __init__(self, numBins, decision):
        self.numBins = numBins
        self.bins = []
        self.decision = decision
        spread  =  decision.up - decision.low
        step = spread/float(numBins)
        self.bins = [bin(i, decision.low + step*i, decision.low + step*(i+1)) for i in range(numBins)]
    def getTotal(self):
        total = 0
        for bin in self.bins:
            total += bin.count
        return total
    def __repr__(self):
        s = self.decision.name
        total = self.getTotal()
        if total == 0: return  str([0 for bin in self.bins])
        for bin in self.bins:
            s += str("%3.0f" % (100.0*bin.count/float(total))) + ","
        s += str("%5.2f" % self.decision.low) + "," + str("%5.2f" % ((self.decision.up-self.decision.low)/float(self.numBins)))
        #s += "]"
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
            
decision_data = []
objective_data = []
for p,problem in enumerate(problems):
    decision_data.append([])
    objective_data.append([])
    for a,algorithm in enumerate(algorithms):
        print "" + algorithm.name + "" + problem.name 
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
        numBins = 10
        columns = decision_data[p][a]
        histobins = [histobin(numBins, problem.decisions[i]) for i in range(len(problem.decisions))]
        for c,hbin in enumerate(histobins):
            hbin.populate(columns[c])
            #hbin.sort("count")
            #print hbin
            hbin.sort()
            print hbin
        """
        for c,col in enumerate(decision_data[p][a]):
            histo,bin = numpy.histogram(col, bins=10, range=[problem.decisions[c].low, problem.decisions[c].up])
            bins = []
            total = float(sum(histo))
            s = ""
            for h in histo:
                bins.append(   ((h/total)*100)   )
                s += str( ("%4.0f" % bins[-1]   ) ) + ","

            print s
        """