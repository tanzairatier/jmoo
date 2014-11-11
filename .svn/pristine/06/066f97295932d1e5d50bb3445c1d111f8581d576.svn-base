
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
"Objective Space Plotter"

from pylab import *
import csv
from jmoo_problems import *
from jmoo_algorithms import *
from jmoo_properties import *
from utility import *
import numpy
from time import *
import os
from deap.tools.support import ParetoFront

def joes_charter_reporter(problems, algorithms, tag=""):
    date_folder_prefix = strftime("%m-%d-%Y")
    
    fignum = 0
    
            
    base = []
    final = []
    RRS = []
    data = []
    foam = []
    
    for p,prob in enumerate(problems):
        base.append([])
        final.append([])
        RRS.append([])
        data.append([])
        foam.append([])
        
        for a,alg in enumerate(algorithms):
            finput = open("data/" + prob.name + str(MU) + "dataset.txt", 'rb')
            f2input = open(DATA_PREFIX + RRS_TABLE + "_" + prob.name + "_" + alg.name + DATA_SUFFIX, 'rb')
            f3input = open("data/results_" + prob.name + "_" + alg.name + ".datatable", 'rb')
            f4input = open(DATA_PREFIX + "decision_bin_table" + "_" + prob.name + "_" + alg.name + DATA_SUFFIX, 'rb')
            reader = csv.reader(finput, delimiter=',')
            reader2 = csv.reader(f2input, delimiter=',')
            reader3 = csv.reader(f3input, delimiter=',')
            reader4 = csv.reader(f4input, delimiter=',')
            base[p].append( [] )
            final[p].append( [] )
            RRS[p].append( [] )
            data[p].append( [] )
            foam[p].append( [] )
            
            for i,row in enumerate(reader):
                if i <= 100 and i > 0:
                    candidate = [float(col) for col in row]
                    fitness = prob.evaluate(candidate)
                    base[p][a].append(candidate+fitness)

            for i,row in enumerate(reader4):
                n = len(prob.decisions)
                candidate = [float(col) for col in row[:n]]
                fitness = prob.evaluate(candidate)
                final[p][a].append(candidate+fitness)
            
            for o,obj in enumerate(prob.objectives): 
                RRS[p][a].append([])
                RRS[p][a][o] = {}
                foam[p][a].append([])
                foam[p][a][o] = {}
            
                        
            for i,row in enumerate(reader2):
                k = len(prob.objectives)
                fitness = [float(col) for col in row[-k-1:-1]]
                for o,fit in enumerate(fitness):
                    n = int(row[k])
                    n = (int(round(n/5.0)*5.0))
                    if n in RRS[p][a][o]: RRS[p][a][o][n].append(fit)
                    else: RRS[p][a][o][n] = [fit]    
            
            for i,row in enumerate(reader3):
                if not str(row[0]) == "0":
                    for j,col in enumerate(row):
                        if i == 0:
                            data[p][a].append([])
                        else:
                            if not col == "":
                                data[p][a][j].append(float(col.strip("%)(")))
                    # row is now read
                    if i > 0:
                        for o,obj in enumerate(prob.objectives):
                            n = data[p][a][0][-1]
                            n = (int(round(n/20.0)*20.0))
                            if n in foam[p][a][o]: foam[p][a][o][n].append(float(data[p][a][o*3+2][-1]))
                            else: foam[p][a][o][n] = [float(data[p][a][o*3+2][-1])]         
                        
                        
                        
                        
    fignum = 0
    colors = ['r', 'b', 'g']
    from matplotlib.font_manager import FontProperties
    font = {'family' : 'sans-serif',
            'weight' : 'normal',
            'size'   : 8}
    
    matplotlib.rc('font', **font)
    fontP = FontProperties()
    fontP.set_size('x-small')
    
    
    codes = ["b*", "r.", "g*"]
    
    line =  "-"
    dotted= "--"
    algnames = [alg.name for alg in algorithms]
    axy = [0,1,2,3]
    axx = [0,0,0,0]
    codes2= ["b-", "r-", "g-"]
    colors= ["b", "r", "g"]
    ms = 8
    from mpl_toolkits.mplot3d import Axes3D
    #fig  = plt.figure()
    #ax = fig.gca(projection='3d')
    
    

    print 'hello'
    
    for p,prob in enumerate(problems):
        for a,alg in enumerate(algorithms):
            n = len(prob.decisions)
            population = [jmoo_individual(prob, f[:n], f[n:]) for f in final[p][a]]
            population = deap_format(prob, population)
            front = ParetoFront()
            front.update(population)
            d_ = []
            for i,fit_i in enumerate(front):
                fma = []
                for j,fit_j in enumerate(front):
                    if not i == j:
                        fma.append(sum([abs(fit_i.fitness.values[k] - fit_j.fitness.values[k]) for k in range(len(prob.objectives))]))                                            
                d_.append(min(fma))
            d_bar = average(d_)
            ssm =   ((1 / float(len(front) - 1)) * sum([(d_bar - d_i)**2 for d_i in d_]))**0.5   
            print prob.name + "," + alg.name + ", size of pareto front: ", len(front), ", spacing: ", ssm
    
    
    for p,prob in enumerate(problems):
                f, axarr = plt.subplots(len(prob.objectives)+1, len(prob.objectives))
    
                
                for o1,obj1 in enumerate(prob.objectives):
                    for o2,obj2 in enumerate(prob.objectives):
                        
                        if o1 == 0: 
                            axarr[o1][o2].set_title(obj2.name)
                        if o2 == 0:
                            axarr[o1][o2].set_ylabel(obj1.name)
                        for a,alg in enumerate(algorithms):
                            
                            
                            #fitnesses = []
                            numAlts = len(final[p][a][0])
                            k = len(prob.objectives)
                            n = len(prob.decisions)
                            
                            population = [jmoo_individual(prob, f[:n], f[n:]) for f in final[p][a]]
                            population = deap_format(prob, population)
                            
                            #for j in range(numAlts):
                            #    fitnesses.append([final[p][a][i][j] for i in range(k)])

                            #front = fitnesses
                            #population = [jmoo_individual(prob, f, f) for f in front]
                            
                            #if not alg.name == "GALE":
                            front = ParetoFront()
                            front.update(population)
                            #else:
                            #    front = population
                                
                            front = [[fit.fitness.values[i] for fit in front] for i,obj in enumerate(prob.objectives)]                                    
                            axarr[o1][o2].plot(front[o1], front[o2], linestyle='None', marker=alg.type, color=alg.color, markersize=5, markeredgecolor='none')
                        front = [[fit[n+i] for fit in base[p][a]] for i,obj in enumerate(prob.objectives)]
                        axarr[o1][o2].plot(front[o1], front[o2], 'y.', markersize=3)
                
                for o,obj in enumerate(prob.objectives):
                    maxEvals = 0
                    for a,alg in enumerate(algorithms):
                        maxEvals = max(maxEvals, max(data[p][a][0]))
                    for a,alg in enumerate(algorithms):    
                        
                        scores = {}
                        
                        for score,eval in zip(data[p][a][o*3+2], data[p][a][0]):
                            eval = int(round(eval/5.0)*5.0)
                            if eval in scores: scores[eval].append(score)
                            else: scores[eval] = [score]
                        
                        keylist = [1]
                        scorelist = [100]
                        smallslist = [100]
                        for eval in sorted(scores.keys()):
                            lq = getPercentile(scores[eval], 25)
                            uq = getPercentile(scores[eval], 75) 
                            scores[eval] = [score for score in scores[eval] if score >= lq and score <= uq ]
                            for item in scores[eval]: 
                                keylist.append(eval)
                                scorelist.append(item)
                                if len(smallslist) == 0: 
                                    smallslist.append(min(scores[eval]))
                                else:
                                    smallslist.append(    min(min(scores[eval]), min(smallslist))  )
                            
                        axarr[len(prob.objectives)][o].plot(keylist, scorelist, linestyle='None', marker=alg.type, color=alg.color, markersize=4, markeredgecolor='none')
                        axarr[len(prob.objectives)][o].plot(keylist, smallslist, color=alg.color)
                        axarr[len(prob.objectives)][o].set_autoscale_on(True)
                        axarr[len(prob.objectives)][o].set_xlim([-10, 10000])
                        axarr[len(prob.objectives)][o].set_xscale('log', nonposx='clip')
                    
                        
                if not os.path.isdir('charts/' + date_folder_prefix):
                    os.makedirs('charts/' + date_folder_prefix)
                
                fignum = len([name for name in os.listdir('charts/' + date_folder_prefix)]) + 1
                print fignum
                plt.savefig('charts/' + date_folder_prefix + '/figure' + str("%02d" % fignum) + "_" + prob.name + "_" + tag + '.png', dpi=100)
                cla()
    #show()



