
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
        finput = open("data/" + prob.name + "-p" + str(MU) + "-d"  + str(len(prob.decisions)) + "-o" + str(len(prob.objectives)) + "-dataset.txt", 'rb')
        reader = csv.reader(finput, delimiter=',')
        for i,row in enumerate(reader):
            if i > MU:
                    base[p].append(float(row[1]))
                    
            
        for a,alg in enumerate(algorithms):
            
            f2input = open(DATA_PREFIX + RRS_TABLE + "_" + prob.name + "-p" + str(MU) + "-d"  + str(len(prob.decisions)) + "-o" + str(len(prob.objectives)) + "_" + alg.name + DATA_SUFFIX, 'rb')
            f3input = open("data/results_" + prob.name + "-p" + str(MU) + "-d"  + str(len(prob.decisions)) + "-o" + str(len(prob.objectives)) + "_" + alg.name + ".datatable", 'rb')
            f4input = open(DATA_PREFIX + "decision_bin_table" + "_" + prob.name + "-p" + str(MU) + "-d"  + str(len(prob.decisions)) + "-o" + str(len(prob.objectives)) + "_" + alg.name + DATA_SUFFIX, 'rb')
            
            reader2 = csv.reader(f2input, delimiter=',')
            reader3 = csv.reader(f3input, delimiter=',')
            reader4 = csv.reader(f4input, delimiter=',')
            base[p].append( [] )
            final[p].append( [] )
            RRS[p].append( [] )
            data[p].append( [] )
            foam[p].append( [] )
            
            
            
            
            
            
            for i,row in enumerate(reader4):
                n = len(prob.decisions)
                o = len(prob.objectives)
                candidate = [float(col) for col in row[:n]]
                fitness = [float(col) for col in row[n:n+o]]#prob.evaluate(candidate)
                final[p][a].append(candidate+fitness)
            
            """
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
            """
            for i,row in enumerate(reader3):
                if not str(row[0]) == "0":
                    for j,col in enumerate(row):
                        if i == 0:
                            data[p][a].append([])
                        else:
                            if not col == "":
                                data[p][a][j].append(float(col.strip("%)(")))
                    """
                    # row is now read
                    if i > 0:
                        for o,obj in enumerate(prob.objectives):
                            n = data[p][a][0][-1]
                            n = (int(round(n/20.0)*20.0))
                            if n in foam[p][a][o]: foam[p][a][o][n].append(float(data[p][a][o*3+2][-1]))
                            else: foam[p][a][o][n] = [float(data[p][a][o*3+2][-1])]         
                    """ 
                        
                        
                        
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
    
    #"""
    #hypervolume and diversity deb metric stuff
    print 'hello'
    
    for p,prob in enumerate(problems):
        for a,alg in enumerate(algorithms):
            
            n = len(prob.decisions)
            population = [jmoo_individual(prob, f[:n], f[n:]) for f in final[p][a]]
            population = deap_format(prob, population)
            front = population
            front.sort(key=lambda x: x.fitness.values)
            
            from stats import diversity
            import hv
            refPoint = ['s' for o in prob.objectives]
            for row in population:
                for i,fit in enumerate(row.fitness.values):
                    if refPoint[i] == 's': refPoint[i] = row.fitness.values[i]
                    else:
                        if prob.objectives[i].lismore: 
                            if refPoint[i] < row.fitness.values[i]: refPoint[i] = row.fitness.values[i]
                        else:
                            if refPoint[i] > row.fitness.values[i]: refPoint[i] = row.fitness.values[i]
            
            finput = open("data/" + prob.name + "-p" + str(MU) + "-d"  + str(len(prob.decisions)) + "-o" + str(len(prob.objectives)) + "-dataset.txt", 'rb')
            reader = csv.reader(finput, delimiter=',')
            
            hellPoint = []
            midPoint = []
            initialFront = []
            lowPoint = []
            
            for i,line in enumerate(reader):
                if i > 100:
                    midPoint.append(float(line[1]))
                    if (prob.objectives[i-100-1].lismore): 
                        hellPoint.append(float(line[2]))
                        lowPoint.append(float(line[0]))
                    else:
                        hellPoint.append(float(line[0]))
                        lowPoint.append(float(line[2]))
                        hellPoint[i-100-1] *= -1
                        midPoint[i-100-1] *= -1
                        refPoint[i-100-1] *= -1
                        lowPoint[i-100-1] *= -1
                else:
                    if i > 0:
                        n = len(prob.decisions)
                        o = len(prob.objectives)
                        candidate = [float(col) for col in line[:n]]
                        fitness = prob.evaluate(candidate)
                        initialFront.append(jmoo_individual(prob, candidate, fitness))
            
            initialFront = deap_format(prob, initialFront)
            refPoint = ['s' for o in prob.objectives]
            for row in initialFront:
                for i,fit in enumerate(row.fitness.values):
                    if refPoint[i] == 's': refPoint[i] = row.fitness.values[i]
                    else:
                        if prob.objectives[i].lismore: 
                            if refPoint[i] < row.fitness.values[i]: refPoint[i] = row.fitness.values[i]
                        else:
                            if refPoint[i] > row.fitness.values[i]: refPoint[i] = row.fitness.values[i]  
            for item in front:
                item.fitness.weightedvalues = [item.fitness.values[o] for o in range(len(prob.objectives))]
            for item in initialFront:
                item.fitness.weightedvalues = [item.fitness.values[o] for o in range(len(prob.objectives))]
            for o,obj in enumerate(prob.objectives):
                if obj.lismore == False:
                    for item in front:
                        item.fitness.weightedvalues[o] = item.fitness.weightedvalues[o]*-1
                    for item in initialFront:
                        item.fitness.weightedvalues[o] = item.fitness.weightedvalues[o]*-1    
            
            #COMPUTE THE DEB SPREAD
            if len(front) > 0:
                div = diversity(front, front[0].fitness.values, front[-1].fitness.values)
            else:
                div = 0
                
            #COMPUTE THE HV
            start = time()
            HV = hv.HyperVolume(refPoint)
            result =    HV.compute([item.fitness.weightedvalues for item in front])
            
            #resultInit =    HV.compute([item.fitness.weightedvalues for item in initialFront])
            #HV = hv.HyperVolume(hellPoint)
            #hellResult = HV.compute([item.fitness.weightedvalues for item in front])
            #hellResultInit = HV.compute([item.fitness.weightedvalues for item in initialFront])
            #HV = hv.HyperVolume(midPoint)
            #midResult = HV.compute([item.fitness.weightedvalues for item in front])
            #midResultInit = HV.compute([item.fitness.weightedvalues for item in initialFront])
            
            
            end = time()
            hvtime = (end-start)
            zzz = prob.name + "-p" + str(MU) + "-d"  + str(len(prob.decisions)) + "-o" + str(len(prob.objectives)) + "," + alg.name + "," + str(len(front))
            zzz += "," + str( div ) + ", " + str(result) + ", " + str(hvtime)# + "," + str(midResult) + "," + str(resultInit) + "," + str(hellResultInit) + ',' + str(midResultInit)   
            print zzz
            
            
            
            #import matplotlib.pyplot as plt
            # import numpy
            # 
            #front = numpy.array([ind.fitness.values for ind in population])
            #optimal_front = numpy.array(optimal_front)
            #plt.scatter(optimal_front[:,0], optimal_front[:,1], c="r")
            #plt.scatter(front[:,0], front[:,1], c="b")
            #plt.axis("tight")
            #plt.show()
            #d_ = []
            #for i,fit_i in enumerate(front):
            #    fma = []
            #    for j,fit_j in enumerate(front):
            #        if not i == j:
            #            fma.append(sum([abs(fit_i.fitness.values[k] - fit_j.fitness.values[k]) for k in range(len(prob.objectives))]))                                            
            #    d_.append(min(fma))
            #d_bar = average(d_)
            #ssm =   ((1 / float(len(front) - 1)) * sum([(d_bar - d_i)**2 for d_i in d_]))**0.5   
            #print prob.name + "," + alg.name + ", size of pareto front: ", len(front), ", spacing: ", ssm
    
    #"""
       
    f, axarr = plt.subplots(4, len(prob.objectives))   #for dtlz123456
    #f, axarr = plt.subplots(3, len(prob.objectives)-1)   #for pom3abc
    #f, axarr = plt.subplots(3, len(prob.objectives))   #for xomo gr fl o2
    F = gcf()
    DefaultSize = F.get_size_inches()
    F.set_size_inches( (DefaultSize[0]*1.5, DefaultSize[1]) )
    for p,prob in enumerate(problems):
                #f, axarr = plt.subplots(len(prob.objectives)+1, len(prob.objectives))
                
    
                """
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
                """
                oo = -1
                for o,obj in enumerate(prob.objectives):
                    
                    b = base[p][o]
                    if o == 11:
                       pass
                    else:
                        oo += 1
                        maxEvals = 0
                        for a,alg in enumerate(algorithms):
                            maxEvals = max(maxEvals, max(data[p][a][0]))
                        for a,alg in enumerate(algorithms):    
                            
                            scores = {}
                            
                            for score,eval in zip(data[p][a][o*3+1], data[p][a][0]):
                                eval = int(round(eval/5.0)*5.0)
                                #print score, eval, b
                                """ << REMOVE THESE TRIPLE LITERALS TO REENABLE percentage of baseline conversion
                                if prob.objectives[o].lismore: 
                                    score = 100*(score/b)
                                else:
                                    try:
                                        score = 100*(b/score)
                                    except: score = 1
                                """
                                # print score
                                if eval in scores: scores[eval].append(score)
                                else: scores[eval] = [score]
                            
                            keylist = []
                            scorelist = []
                            smallslist = []
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
                            
                            if oo==0: axarr[p][oo].set_ylabel(prob.name + "\n_o"+str(len(prob.objectives)), fontweight='bold', fontsize=14)
                            if p ==0: axarr[p][oo].set_title(prob.objectives[oo].name, fontweight='bold', fontsize=14)
                            if p ==(len(problems)-1): axarr[p][oo].set_xlabel("(Log) NumEvals")
                            ax2 = axarr[p][oo].twinx()
                            ax2.get_yaxis().set_ticks([])
                            if oo==(len(prob.objectives)-1): ax2.set_ylabel("Quality")
                            #print scorelist
                            axarr[p][oo].plot(keylist, scorelist, linestyle='None', marker=alg.type, color=alg.color, markersize=7, markeredgecolor='none') #MARKER PLOTS
                            #axarr[p][oo].plot([min(keylist)]+keylist, [100]+smallslist, color=alg.color) #BOTTOMLINE
                            axarr[p][oo].plot([x for x in range(0,10000,10)], [100 for x in range(0,10000,10)], color="Black") #BASELINE
                            axarr[p][oo].set_autoscale_on(True)
                            axarr[p][oo].set_xlim([-10, 10000])
                            #axarr[p][oo].set_ylim([20, 160])# -- xomo
                            #axarr[p][oo].set_ylim([-5, 115])
                            axarr[p][oo].set_ylim([min(scorelist) - 0.1, max(scorelist) + 0.1])# -- tera
                            axarr[p][oo].set_xscale('log', nonposx='clip')
                        
                            
    if not os.path.isdir('charts/' + date_folder_prefix):
        os.makedirs('charts/' + date_folder_prefix)
    
    fignum = len([name for name in os.listdir('charts/' + date_folder_prefix)]) + 1
    print fignum
    plt.savefig('charts/' + date_folder_prefix + '/figure' + str("%02d" % fignum) + "_" + prob.name + "_" + tag + '.png', dpi=100)
    cla()
    #show()



