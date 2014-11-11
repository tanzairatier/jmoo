
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
"Report tool for keeping track of stats during MOEAs"

import math
import jmoo_algorithms
from jmoo_individual import *
from jmoo_properties import *
from utility import *
from deap.tools.support import ParetoFront

class jmoo_stats:
    "A single stat box - a simple record"
    def __init__(stats, population, fitnesses, fitnessMedians, fitnessSpreads, numEval, gen, IBD, IBS, changes):
        stats.population = population
        stats.fitnesses = fitnesses
        stats.fitnessMedians = fitnessMedians
        stats.fitnessSpreads = fitnessSpreads
        stats.numEval = numEval
        stats.gen = gen
        stats.IBD = IBD
        stats.IBS = IBS
        stats.changes = changes
        
     
          
class jmoo_stats_box:
    "Management of one stat box per generation"
    def __init__(statBox, problem, alg, foam=None):
        statBox.problem = problem
        statBox.numEval = 0
        statBox.box = []
        statBox.alg = alg
        statBox.foam = [{} for o in problem.objectives]
        statBox.bests = [100.0 for o in problem.objectives]
        statBox.bests_actuals = [0 for o in problem.objectives]
        statBox.lives = 3
    
    def update(statBox, population, gen, numNewEvals, initial = False, printOption=True):
        "add a stat box - compute the statistics first"
        fa = open("data/results_"+statBox.problem.name+"_"+statBox.alg.name+".datatable", 'a')
        
        # Calculate percentage of violations
        violationsPercent = sum([ 1 for pop in population if statBox.problem.evalConstraints(pop.decisionValues)])/float(len(population))
        
        # Update Number of Evaluations
        statBox.numEval += numNewEvals
        #front = population
        #for pop in population:
        #    if not pop.valid: pop.evaluate()
        population = [pop for pop in population if pop.fitness.valid]
        
        #population = jmoo_algorithms.deap_format(statBox.problem, population)
        
        #front = ParetoFront()
        #front.update(population)
        
        """
        fitnesses = []
        population = []
        for i,dIndividual in enumerate(front):
            cells = []
            for j in range(len(dIndividual)):
                cells.append(dIndividual[j])
            fit = []
            for k in range(len(statBox.problem.objectives)):
                fit.append(dIndividual.fitness.values[k])
            population.append( jmoo_individual(statBox.problem, cells, fit) )
        """         
        # Evaluate Fitnesses
        #for individual in population:
        #    if not individual.valid: individual.evaluate()
        fitnesses = [individual.fitness.fitness for individual in population if individual.valid]
    
                
        
                
        # Split Columns into Lists
        fitnessColumns = [[fit[i] for fit in fitnesses] for i,obj in enumerate(statBox.problem.objectives)]
    
        # Calculate Medians and Spreads
        fitnessMedians = [median(fitCol) for fitCol in fitnessColumns]
        fitnessSpreads = [spread(fitCol) for fitCol in fitnessColumns]
        
        # Initialize Reference Point on Initial Run
        if initial == True:
            #statBox.referencePoint = fitnessMedians 
            #statBox.referencePoint = statBox.problem.referencePoint
            #statBox.referencePoint = statBox.problem.evaluate(population[0].decisionValues)
            statBox.referencePoint = [o.med for o in statBox.problem.objectives]
            print [(o.low, o.up) for o in statBox.problem.objectives]
            

        # Calculate IBD & IBS
        norms = [[min(fitnessColumns[i]+[statBox.referencePoint[i]]), max(fitnessColumns[i]+[statBox.referencePoint[i]])] for i,obj in enumerate(statBox.problem.objectives)]
        lossInQualities = [loss_in_quality(statBox.problem, [statBox.referencePoint], fit, norms) for fit in fitnesses]
        IBD = median(lossInQualities)
        IBS = spread(lossInQualities)
        
        if initial == True:
            IBD = 1.0
            statBox.referenceIBD = 1.0
        
        
        changes = []
        # Print Option
        if printOption == True:
            outString = ""
            
            if initial:
                outString += str(statBox.numEval) + ","
                for med,spr,initmed,obj,o in zip(statBox.referencePoint, [0 for x in statBox.problem.objectives], statBox.referencePoint,statBox.problem.objectives,range(len(statBox.problem.objectives))):
                    change = percentChange(med, initmed, obj.lismore, obj.low, obj.up)
                    changes.append(float(change.strip("%")))
                    statBox.bests[o] = changes[-1]
                    statBox.bests_actuals[o] = med
                    outString += str("%8.4f" % med) + "," + change + "," + str("%8.4f" % spr) + ","
                    if statBox.numEval in statBox.foam[o]: statBox.foam[o][statBox.numEval].append(change)
                    else: statBox.foam[o][statBox.numEval] = [change]
                outString += str("%8.4f" % IBD) + "," + percentChange(statBox.referenceIBD, statBox.referenceIBD, True, 0, 1) + "," + str("%8.4f" % IBS)
            else:
                outString += str(statBox.numEval) + ","
                for med,spr,initmed,obj,o in zip(fitnessMedians, fitnessSpreads, statBox.referencePoint,statBox.problem.objectives,range(len(statBox.problem.objectives))):
                    change = percentChange(med, initmed, obj.lismore, obj.low, obj.up)
                    changes.append(float(change.strip("%")))
                    if changes[-1] < statBox.bests[o]: 
                        statBox.bests[o] = changes[-1]
                        statBox.bests_actuals[o] = med
                    outString += str("%8.4f" % med) + "," + change + "," + str("%8.4f" % spr) + ","
                    if statBox.numEval in statBox.foam[o]: statBox.foam[o][statBox.numEval].append(change)
                    else: statBox.foam[o][statBox.numEval] = [change]
                outString += str("%8.4f" % IBD) + "," + percentChange(IBD, statBox.referenceIBD, True, 0, 1) + "," + str("%8.4f" % IBS)
                
            print outString  + ", violations: " + str("%4.1f" % violationsPercent)
            fa.write(outString + "\n")
        
            
        # Add Stat to the Stat Box
        trunk = []
        for i,pop in enumerate(population):
            trunk.append(jmoo_individual(statBox.problem, pop.decisionValues, pop.fitness.fitness))
            #if i < 5: print trunk[-1].decisionValues, statBox.problem.evalConstraints(trunk[-1].decisionValues)
        statBox.box.append(jmoo_stats(trunk, fitnesses, fitnessMedians, fitnessSpreads, statBox.numEval, gen, IBD, IBS, changes))
        fa.close()
###########
### Utility Functions
###########

def percentChange(new, old, lismore, low, up):
    return str("%1.1f" % changeFromOld(new, old, lismore, low, up)) + "%"
def changeFromOld(new, old, lismore, low, up):
    if new < 0 or old < 0: 
        ourlismore = not lismore
        new = abs(new)
        old = abs(old)
    else: ourlismore = lismore
    

    
    
    #if new == 0 or old == 0: return 0 if ourlismore else 110
    new = normalize(new, low, up)
    old = normalize(old, low, up)
    if old == 0: x = 0
    else: x = (new/float(old))
    if x == 0: 
        if ourlismore: return 0
        else: return 1
    else: return 100.0*x**(1 if ourlismore else -1)
def median(list):
    return getPercentile(list, 50)

def spread(list):
    return getPercentile(list, 75) - getPercentile(list, 25)

def getPercentile(list, percentile):
        if len(list) == 0: return 0
        #sort the list
        list.sort()
        
        k = (len(list) - 1) * (percentile/100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            val = list[int(k)]
        else:
            d0 = list[int(f)] * (c-k)
            d1 = list[int(c)] * (k-f)
            val = d0+d1
        return val

def normalize(x, min, max):
    tmp = float((x - min)) / \
                (max - min + 0.000001) 
    if   tmp > 1 : return 1
    elif tmp < 0 : return 0
    else         : return tmp 
    
def loss_in_quality(problem, pop, fit1, norms):
    "Loss in Quality Indicator"
    weights = [-1 if o.lismore else +1 for o in problem.objectives]    
    k = len(weights)
    
    # Calculate the loss in quality of removing fit1 from the population
    F = []
    for X2 in pop:
        F.append(-k/(sum([-math.exp(-w*(normalize(p2,n[0],n[1]) - normalize(p1,n[0],n[1]))/k) for w,p1,p2,n in zip(weights,fit1,  X2,        norms)])))
    F1 = sum(F)
    
    return F1