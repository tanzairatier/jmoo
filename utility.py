
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
"Bunch of often used functions"

import numpy 
import math

def avg(list):
    return (float)(sum(list))/(float)(len(list))

def sum(list):
    sum = 0;
    for i in list:
        sum+= i;
    return sum

def median(list):
    return getPercentile(list, 50)

def spread(list):
    return getPercentile(list, 75) - getPercentile(list, 25)
    
def mul(list):
    sum = list[0]
    for i in list[1:]:
        sum *= i
    return sum

def var(list):
   mean = avg(list)
   squared_diffs = []
   for i in list:
       squared_diffs.append((i-mean)**2)
   return ((float)(sum(squared_diffs))/(float)(len(list)-1))

def avg2(list, index):
    "return the average of a particular column from an array of arrays"
    newlist = []
    for i in list:
        newlist.append(i[index])
    return avg(newlist)

def matrix_avg(matrix):
    vals = []
    averages = []
    
    #populate vals with empty frames
    for i in range(len(matrix[0])):
        vals.append([])
    
    #populate vals with matrix data
    for i,row in enumerate(matrix):
        for j,col in enumerate(row):
            vals[j].append(col)
            
    #compute averages of each column
    for i,col in enumerate(vals):
        averages.append(avg(col))
    
    return averages

def matrix_var(matrix):
    vals = []
    variances = []
    
    #populate vals with empty frames
    for i in range(len(matrix[0])):
        vals.append([])
    
    #populate vals with matrix data
    for i,row in enumerate(matrix):
        for j,col in enumerate(row):
            vals[j].append(col)
            
    #compute averages of each column
    for i,col in enumerate(vals):
        variances.append(var(col))
    
    return variances

def getPercentile(list, percentile):
        import math
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
def avg(list):
      return (float)(sum(list))/(float)(len(list))

def sum(list):
      sum = 0;
      for i in list:
          sum+= i;
      return sum
  
def var(list):
     mean = avg(list)
     squared_diffs = []
     for i in list:
         squared_diffs.append((i-mean)**2)
     return ((float)(sum(squared_diffs))/(float)(len(list)-1))
 
def dist(A,B):
    return sum([(a-b)**2 for a,b in zip(A,B)])**0.5
def pretty_print(matrix):
    for row in matrix:
        s = ""
        for val in row:
            s += str('%15.3f'%(val)) + ", "
        print s
        
        
def getFront(problem, population):
    #fitnesses = [list(x) for x in set(tuple(x) for x in fitnesses)]

    myList = []
    for i,ind in enumerate(population):
        for d,decision in enumerate(problem.decisions):
            decision.value = ind.decisionValues[d]
        if True: #not problem.evalConstraints():
            myList.append(population[i])
        
    #for i,pop in enumerate(population):
    #    print pop.decisionValues, sum(problem.evalConstraintOverages(pop.decisionValues)), problem.evalConstraints(pop.decisionValues)
            
    # Sort the list in either ascending or descending order of X
    myList = sorted(myList, key= lambda pop: pop.fitness.fitness)
    
    # Start the Pareto frontier with the first value in the sorted list
    p_front = []
    for pair in myList:
        if pair.valid and not problem.evalConstraints(pair.decisionValues):
            p_front = [pair]
            break
        
    # Loop through the sorted list
    for pair in myList[1:]: 
            if pair.valid and pair.fitness.fitness[1] <= p_front[-1].fitness.fitness[1] and not problem.evalConstraints(pair.decisionValues):
                p_front.append(pair)
    
    
    area = 1
        
    return p_front, area

def pareto_frontier_multi(myArray):
    #fitnesses = [list(x) for x in set(tuple(x) for x in fitnesses)]
    
    # Sort on first dimension
    
    myArray = myArray[myArray[:,0].argsort()]
    # Add first row to pareto_frontier
    pareto_frontier = myArray[0:1,:]
    # Test next row against the last row in pareto_frontier
    for row in myArray[1:,:]:
        if sum([row[x] >= pareto_frontier[-1][x]
                for x in range(len(row))]) == len(row):
            # If it is better on all features add the row to pareto_frontier
            pareto_frontier = numpy.concatenate((pareto_frontier, [row]))
    return pareto_frontier

def normalize(x, min, max):
    tmp = float((x - min)) / \
                (max - min + 0.000001) 
    if   tmp > 1 : return 1
    elif tmp < 0 : return 0
    else         : return tmp 
    
def loss(x1, x2, mins=None, maxs=None):
    #normalize if mins and maxs are given
    if mins and maxs:
        x1 = [normalize(x, mins[i], maxs[i]) for i,x in enumerate(x1)]
        x2 = [normalize(x, mins[i], maxs[i]) for i,x in enumerate(x2)]
    
    o = min(len(x1), len(x2)) #len of x1 and x2 should be equal 
    return sum([math.exp((x2i - x1i)/o) for x1i, x2i in zip(x1,x2)])/o

def cdom(x1, x2, mins=None, maxs=None):
    return loss(x1,x2, mins, maxs) / loss(x2,x1, mins, maxs)

def spacing(dataset):
    dim = len(dataset[0])
    d_ = []
    for i,fit_i in enumerate(dataset):
        fma = []
        for j,fit_j in enumerate(dataset):
            if not i == j:
                fma.append(sum([abs(fit_i[k] - fit_j[k]) for k in range(dim)]))                                            
        d_.append(min(fma))
    d_bar = avg(d_)
    ssm =   ((1 / float(len(dataset) - 1)) * sum([(d_bar - d_i)**2 for d_i in d_]))**0.5
    return ssm
  
"""
def losstest():
x1 = [0.1, 0.1, 0.1, 0.1]
x2 = [9, 6, 5, 4]
x3 = [0.8, 0.6, 0.5, 0.4]
x4 = [8, 6, 5, 4]
x5 = [0.4, 0.5, 0.4, 0.3]
x6 = [4, 5, 4, 3]
"""