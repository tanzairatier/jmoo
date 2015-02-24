import csv
#from jmoo_problems import *
from jmoo_properties import *
#from jmoo_algorithms import *
#from jmoo_stats_box import *

import random, utility

from time import *
import os
import pylab as mpl

def validation():
    #read baseline
    f2input = open("data/" + problem.name + str(MU) + "dataset.txt", 'rb')
    reader2 = csv.reader(f2input, delimiter=',')
    referencePoint = []
    for i,row in enumerate(reader2):
        if i > MU:
            referencePoint.append(float(row[1]))
            
    z = ""
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
    
    print z
    
    
    
class histobin:
        def __init__(self, numBins, decision, decIndex):
            self.decIndex = decIndex
            self.numAttributes = numAttributes
            self.numBins = numBins
            self.bins = []
            spread  =  decision.up - decision.low
            step = spread/float(numBins)
            self.bins = [singleBin(i, decision.low + step*i, decision.low + step*(i+1)) for i in range(numBins)]
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
                if bin.count == 0: 
                    s += '{0: >3}'.format("-") + " "
                else:
                    s += str("%3.0f" % (100.0*bin.count/float(total))) + " "
            s += "]"
            return s
        def var(self):
            total = float(self.getTotal())
            counts = [100*bin.count/total for bin in self.bins]
            return var(counts)
        def stdev(self):
            return self.var()**0.5
        def externalVar(self, histobins):
            allCounts = []
            for hb in histobins:
                total = float(hb.getTotal())
                for bin in hb.bins:
                    allCounts.append(100*bin.count/total)
            return var(allCounts)
        def importance(self):
            max_case = [0 for bin in self.bins]
            max_case[0] = 100
            max_var = var(max_case)
            return self.var()/max_var
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
                        if item > bin.low and item <= bin.up:
                            self.bins[b].add(item)
                            break
        def sort(self, bywhat=None):
            if bywhat == "count": bywhat = lambda bin: bin.count
            else: bywhat = lambda bin: bin.index
            
            self.bins = sorted(self.bins, key=bywhat)
        def freq(self, bin):
            total = float(self.getTotal())
            return 100 * bin.count / total 
        def newImportance(self, histobins):
            self.NI =(self.var()) / sum([hb.var() for hb in histobins]) 
            return self.NI
        def rex(self):
            self.sort("count")
            importance = self.importance()*100
            removed_sum = 0
            self.rex_bins = []
            for bin in self.bins:
                binfreq = self.freq(bin)
                if removed_sum+binfreq < importance:
                    removed_sum += binfreq
                    #self.rex_bins.append(bin)
                    #self.rex_bins[-1].count = 0
                    bin.count = 0
                #else:
                    #self.rex_bins.append(bin)
            
            #self.bins = self.rex_bins
            """
            self.rex_bins = sorted(self.rex_bins, key=lambda bin: bin.index)
            s = "["
            total = self.getTotal()
            if total == 0: return  str([0 for bin in self.rex_bins])
            for bin in self.rex_bins:
                if bin.count == 0:
                    s += '{0: >3}'.format("X") + " "
                else:
                    s += str("%3.0f" % (100.0*bin.count/float(total))) + " "
            s += "]"
            print s
            """ 
                
class singleBin:
        def __init__(self, ind, low, up):
            self.index = ind
            self.low = low
            self.up = up
            self.count = 0
            self.items = []
        def add(self, item):
            self.count += 1
            self.items.append(item)

date_folder_prefix = strftime("%m-%d-%Y")
if not os.path.isdir('reports/' + date_folder_prefix):
    os.makedirs('reports/' + date_folder_prefix)
fignum = len([name for name in os.listdir('reports/' + date_folder_prefix)]) + 1
#optional tag name for the file
#fa = open('reports/' + date_folder_prefix + "/decision_bin_rules_report" + "_" + tag + str("%02d" % fignum) + ".txt", 'w')

decision_data = []
objective_data = []
hbinloves = []
for p,problem in enumerate(problems):
    decision_data.append([])
    objective_data.append([])
    hbinloves.append([])
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
        
        for rexReps in range(1,2):
            numBins = 10
            numAttributes = len(problem.decisions)
            histobins = [histobin(numBins, problem.decisions[i], i) for i in range(numAttributes)]
            lows = []
            ups = []
            novel_candidates = []
            for c,hbin in enumerate(histobins):
                novel_candidates.append( [[] for d in problem.decisions] )
                #print decision_data[p][a][c] 
                hbin.populate(decision_data[p][a][c])
                hbin.sort("count")
                #print hbin
                hbin.sort()
                
                #for iii in range(10):
                #    hbin.rex()
                
                
                hbin.sort()
                #print hbin, hbin.importance()
    
                
                
                highest = 0
                biggestbin = 0
                
                
            #calculate global importance
            imps = []
            for hb in histobins:
                imps.append(hb.newImportance(histobins))
            histobins.sort(key=lambda hbs: hbs.NI)
            for hb in histobins:
                print hb, str("%5.2f" % hb.newImportance(histobins) )
            print sum(imps)
            
            
            
            
            hbinloves.append(hbin)
            trials = []
            for hbin in histobins:
                hbin.sort("count")
            
            numUniforms = len(histobins)
            splits = 0
            f, axarr = mpl.plt.subplots(3, 3)
            while(numUniforms > 0):
                
                numUniforms = int(len(histobins)/((splits+1)*2))
                trials = []
                print hbin.getTotal()
                for repeat in range((hbin.getTotal())):
                    novel_candidate = [random.uniform(dec.low,dec.up) for dec in problem.decisions]
                    
                    for h,hbin in enumerate(histobins):
                        if h > numUniforms:
                            summer = 0.0
                            roll = random.randint(0,100)
                            hbin.sort()
                            for bin in hbin.bins:
                                summer += hbin.freq(bin)
                                if roll <= summer and bin.count > 0: 
                                    if hbin.freq(bin) < 50: bin = hbin.bins[0]
                                    entry = random.choice(bin.items)
                                    novel_candidate[hbin.decIndex] = entry
                    trials.append(problem.evaluate(novel_candidate))
                X = [t[0] for t in trials]
                Y = [t[1] for t in trials]
                axarr[int(splits/3)][(splits % 3)].plot(X, Y, linestyle='None', marker=algorithm.type, color=algorithm.color, markersize=5, markeredgecolor='none')
                validation()
                splits += 1
            if not os.path.isdir('charts/' + date_folder_prefix):
                os.makedirs('charts/' + date_folder_prefix)
        
            fignum = len([name for name in os.listdir('charts/' + date_folder_prefix)]) + 1
            print fignum
            mpl.plt.savefig('charts/' + date_folder_prefix + '/REX(splits=)'+str(splits) + 'figure' + str("%02d" % fignum) + "_" + problem.name + "_" + algorithm.name + "_"+ '.png', dpi=100)
            mpl.cla()
                
                
                
                    
                
            