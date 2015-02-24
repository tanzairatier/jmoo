import csv
from jmoo_properties import *

import random, utility

from time import *
import os
import pylab as mpl
from histobin import *

def validation(z):
    #read baseline
    f2input = open("data/" + problem.name + str(MU) + "dataset.txt", 'rb')
    reader2 = csv.reader(f2input, delimiter=',')
    referencePoint = []
    for i,row in enumerate(reader2):
        if i > MU:
            referencePoint.append(float(row[1]))
            
    validation_vector = utility.matrix_avg(trials)
    
    
    z += str("%10.2f" % 0)
    for vv in validation_vector: z += str("%10.2f" % vv) + ","
    
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
    z += str("%10.2f" % IBD) + "," + str("%10.2f" % IBS)
    z += str("%10.2f" % 0)
    print z
    
    
    return IBD
tag = ""



#container for summary data
data = []
decision_data = []
objective_data = []

plot_points = []
plot_points_bindraw = []
plot_points_rexdraw = []
plot_points_norexbest = []
plot_points_rexbest = []

for p,problem in enumerate(problems):
    data.append([])
    decision_data.append([])
    objective_data.append([])
    plot_points.append([])
    plot_points_bindraw.append([])
    plot_points_rexdraw.append([])
    plot_points_norexbest.append([])
    plot_points_rexbest.append([])
    for a,algorithm in enumerate(algorithms):
        finput = open(DATA_PREFIX + SUMMARY_RESULTS + problem.name + "_" + algorithm.name + DATA_SUFFIX, 'rb')
        reader = csv.reader(finput, delimiter=',')
        plot_points[p].append([])
        plot_points_bindraw[p].append([])
        plot_points_rexdraw[p].append([])
        plot_points_norexbest[p].append([])
        plot_points_rexbest[p].append([])
        data[p].append([])
        
        for i,row in enumerate(reader):
            if i == 0: 
                data[p][a] = [[] for obj in problem.objectives] + [[],[],[],[]]
                
            elements = row
            data[p][a][0].append( int(elements[2]) )
            for o,obj in enumerate(problem.objectives):
                data[p][a][1+o].append( float(elements[3+o]) )
            data[p][a][1+len(problem.objectives)].append( float(elements[3+len(problem.objectives)]) )
            data[p][a][2+len(problem.objectives)].append( float(elements[4+len(problem.objectives)]) )
            data[p][a][3+len(problem.objectives)].append( float(elements[5+len(problem.objectives)]) )
        
        
        
        # read decision data
        finput = open(DATA_PREFIX + DECISION_BIN_TABLE + "_" + problem.name + "_" + algorithm.name + DATA_SUFFIX, 'rb')
        reader = csv.reader(finput, delimiter=',')
        
        decision_data[p].append([])
        objective_data[p].append([])
        
        for i,row in enumerate(reader):
            if i == 0: 
                objective_data[p][a] = [[] for obj in problem.objectives]
                plot_points[p][a] = [[] for obj in problem.objectives]
                plot_points_bindraw[p][a] = [[] for obj in problem.objectives]
                plot_points_rexdraw[p][a] = [[] for obj in problem.objectives]
                plot_points_rexbest[p][a] = [[] for obj in problem.objectives]
                plot_points_norexbest[p][a] = [[] for obj in problem.objectives]
                decision_data[p][a] = [[] for dec in problem.decisions]
                
            elements = row
            for d,dec in enumerate(problem.decisions):
                decision_data[p][a][d].append(float(elements[d]))
            d = len(problem.decisions)
            
            for o,obj in enumerate(problem.objectives):
                if not elements[d+o].strip() == "?":
                    objective_data[p][a][o].append(float(elements[d+o]))
                    plot_points[p][a][o].append(float(elements[d+o]))
                
                    
    
        #################### Originals ######################
        s = '{0: <12}'.format(problem.name) + "," + '{0: <12}'.format(algorithm.name) + "," + '{0: <12}'.format("Original") + "," 
        for dug in data[p][a]:
            s += str("%10.2f" % avg(dug)) + ","
        print s
    
        #################### BIN DRAW ORIGINALS ###################
        numBins = 10
        numAttributes = len(problem.decisions)
        histobins = [histobin(numBins, problem.decisions[i], i) for i in range(numAttributes)]
        novel_candidates = []
        for c,hbin in enumerate(histobins):
            novel_candidates.append( [[] for d in problem.decisions] ) 
            hbin.populate(decision_data[p][a][c])
            
            #for iii in range(10):
            #    hbin.rex()
        
        trials = []
        for repeat in range(20):
            
            accepted = False
            while not accepted:
                novel_candidate = [random.uniform(dec.low,dec.up) for dec in problem.decisions]
                
                for h,hbin in enumerate(histobins):
                    summer = 0.0
                    roll = random.randint(0,100)
                    hbin.sort("count")
                    for bin in hbin.bins:
                        summer += hbin.freq(bin)
                        if roll <= summer and bin.count > 0: 
                            entry = random.uniform(bin.low, bin.up)
                            novel_candidate[hbin.decIndex] = entry
                    
                if not problem.evalConstraints(novel_candidate):            
                    trials.append(problem.evaluate(novel_candidate))
                    accepted = True
            for o,obj in enumerate(trials[-1]):
                plot_points_bindraw[p][a][o].append(obj)
        validation('{0: <12}'.format(problem.name) + "," + '{0: <12}'.format(algorithm.name) + "," + '{0: <12}'.format("OriginalDraw") + ",")
        
        
        
        #################### BIN DRAW REX ###################
        numBins = 10
        numAttributes = len(problem.decisions)
        histobins = [histobin(numBins, problem.decisions[i], i) for i in range(numAttributes)]
        novel_candidates = []
        for c,hbin in enumerate(histobins):
            novel_candidates.append( [[] for d in problem.decisions] ) 
            hbin.populate(decision_data[p][a][c])
            
            for iii in range(10):
                hbin.rex()
        
        trials = []
        for repeat in range(20):
            
            accepted = False
            while not accepted:
                novel_candidate = [random.uniform(dec.low,dec.up) for dec in problem.decisions]
                
                for h,hbin in enumerate(histobins):
                    summer = 0.0
                    roll = random.randint(0,100)
                    hbin.sort("count")
                    for bin in hbin.bins:
                        summer += hbin.freq(bin)
                        if roll <= summer and bin.count > 0: 
                            entry = random.uniform(bin.low, bin.up)
                            novel_candidate[hbin.decIndex] = entry
                    
                if not problem.evalConstraints(novel_candidate):            
                    trials.append(problem.evaluate(novel_candidate))
                    accepted = True
            for o,obj in enumerate(trials[-1]):
                plot_points_rexdraw[p][a][o].append(obj)
        validation('{0: <12}'.format(problem.name) + "," + '{0: <12}'.format(algorithm.name) + "," + '{0: <12}'.format("RexDraw") + ",")
        
        #################### BIN DRAW NO_REX+PRUNE ###################
        numBins = 10
        numAttributes = len(problem.decisions)
        histobins = [histobin(numBins, problem.decisions[i], i) for i in range(numAttributes)]
        novel_candidates = []
        for c,hbin in enumerate(histobins):
            novel_candidates.append( [[] for d in problem.decisions] ) 
            hbin.populate(decision_data[p][a][c])
            
            #for iii in range(10):
            #    hbin.rex()
        
        #calculate global importance
        imps = []
        for hb in histobins:
            imps.append(hb.newImportance(histobins))
        histobins.sort(key=lambda hbs: hbs.NI)
        #for hb in histobins:
        #    print hb, str("%5.2f" % hb.newImportance(histobins) )
        #print sum(imps)
        
        numUniforms = len(histobins)
        splits = 0
        IBDs = []
        trialOuters = []
        while(numUniforms > 0):
            numUniforms = int(len(histobins)/((splits+1)*2))
            splits += 1
            trials = []
            for repeat in range(20):
                
                accepted = False
                while not accepted:
                    novel_candidate = [random.uniform(dec.low,dec.up) for dec in problem.decisions]
                    
                    for h,hbin in enumerate(histobins):
                        if h > numUniforms:
                            summer = 0.0
                            roll = random.randint(0,100)
                            hbin.sort("count")
                            for bin in hbin.bins:
                                summer += hbin.freq(bin)
                                if roll <= summer and bin.count > 0: 
                                    entry = random.uniform(bin.low, bin.up)
                                    novel_candidate[hbin.decIndex] = entry
                        
                    if not problem.evalConstraints(novel_candidate):            
                        trials.append(problem.evaluate(novel_candidate))
                        accepted = True
            
            IBDs.append(validation('{0: <12}'.format(problem.name) + "," + '{0: <12}'.format(algorithm.name) + "," + '{0: <12}'.format("NoRex" + str(100.0/(2**(splits-1))) + "%") + ","))
            trialOuters.append(trials)
        bestIBD = 999
        bestTrialOuter = None
        for i,ibd in enumerate(IBDs):
            if ibd < bestIBD:
                bestIBD = ibd
                bestTrialOuter = trialOuters[i]
        for t,trial in enumerate(bestTrialOuter):
            for o,obj in enumerate(trial):
                plot_points_norexbest[p][a][o].append(obj)
            
            
            
        
        #################### BIN DRAW REX+PRUNE ###################
        numBins = 10
        numAttributes = len(problem.decisions)
        histobins = [histobin(numBins, problem.decisions[i], i) for i in range(numAttributes)]
        novel_candidates = []
        for c,hbin in enumerate(histobins):
            novel_candidates.append( [[] for d in problem.decisions] ) 
            hbin.populate(decision_data[p][a][c])
            
            for iii in range(10):
                hbin.rex()
        
        #calculate global importance
        imps = []
        for hb in histobins:
            imps.append(hb.newImportance(histobins))
        histobins.sort(key=lambda hbs: hbs.NI)
        #for hb in histobins:
        #    print hb, str("%5.2f" % hb.newImportance(histobins) )
        #print sum(imps)
        
        numUniforms = len(histobins)
        splits = 0
        IBDs = []
        trialOuters = []
        while(numUniforms > 0):
            numUniforms = int(len(histobins)/((splits+1)*2))
            splits += 1
            trials = []
            for repeat in range(20):
                
                accepted = False
                while not accepted:
                    novel_candidate = [random.uniform(dec.low,dec.up) for dec in problem.decisions]
                    
                    for h,hbin in enumerate(histobins):
                        if h > numUniforms:
                            summer = 0.0
                            roll = random.randint(0,100)
                            hbin.sort("count")
                            for bin in hbin.bins:
                                summer += hbin.freq(bin)
                                if roll <= summer and bin.count > 0: 
                                    entry = random.uniform(bin.low, bin.up)
                                    novel_candidate[hbin.decIndex] = entry
                        
                    if not problem.evalConstraints(novel_candidate):            
                        trials.append(problem.evaluate(novel_candidate))
                        accepted = True
            IBDs.append(validation('{0: <12}'.format(problem.name) + "," + '{0: <12}'.format(algorithm.name) + "," + '{0: <12}'.format("Rex" + str(100.0/(2**(splits-1))) + "%") + ","))
            trialOuters.append(trials)
        bestIBD = 999
        bestTrialOuter = None
        for i,ibd in enumerate(IBDs):
            if ibd < bestIBD:
                bestIBD = ibd
                bestTrialOuter = trialOuters[i]
        for t,trial in enumerate(bestTrialOuter):
            for o,obj in enumerate(trial):
                plot_points_rexbest[p][a][o].append(obj)
                
                
                
#### PLOT THEM ####


for p,problem in enumerate(problems):
    f, axarr = mpl.plt.subplots(len(algorithms), 5)
    for a,algorithm in enumerate(algorithms):
        X = plot_points[p][a][0]
        Y = plot_points[p][a][1]
        axarr[a][0].plot(X, Y, linestyle='None', marker=algorithm.type, color='Silver', markersize=5, markeredgecolor='none')
        OX,OY = X, Y
        front = ParetoFront()
        population = [jmoo_individual(problem, [], [x,y]) for x,y in zip(X,Y)]
        population = deap_format(problem, population)
        front.update(population)
        front = [[fit.fitness.values[i] for fit in front] for i,obj in enumerate(problem.objectives)]
        Ofront = front
        axarr[a][0].plot(front[0], front[1], linestyle='None', marker=algorithm.type, color=algorithm.color, markersize=5, markeredgecolor='none')
        
        axarr[a][0].set_xlim([min(OX), max(OX)])
        axarr[a][0].set_ylim([min(OY), max(OY)])
        
        X = plot_points_bindraw[p][a][0]
        Y = plot_points_bindraw[p][a][1]
        axarr[a][1].plot(Ofront[0], Ofront[1], marker=algorithm.type, color='Yellow', markersize=5, markeredgecolor='none')
        axarr[a][1].plot(X, Y, linestyle='None', marker=algorithm.type, color='Silver', markersize=5, markeredgecolor='none')
        front = ParetoFront()
        population = [jmoo_individual(problem, [], [x,y]) for x,y in zip(X,Y)]
        population = deap_format(problem, population)
        front.update(population)
        front = [[fit.fitness.values[i] for fit in front] for i,obj in enumerate(problem.objectives)]
        axarr[a][1].plot(front[0], front[1], linestyle='None', marker=algorithm.type, color=algorithm.color, markersize=5, markeredgecolor='none')
        axarr[a][1].set_xlim([min(OX), max(OX)])
        axarr[a][1].set_ylim([min(OY), max(OY)])
        
        X = plot_points_rexdraw[p][a][0]
        Y = plot_points_rexdraw[p][a][1]
        axarr[a][2].plot(Ofront[0], Ofront[1], marker=algorithm.type, color='Yellow', markersize=5, markeredgecolor='none')
        axarr[a][2].plot(X, Y, linestyle='None', marker=algorithm.type, color='Silver', markersize=5, markeredgecolor='none')
        front = ParetoFront()
        population = [jmoo_individual(problem, [], [x,y]) for x,y in zip(X,Y)]
        population = deap_format(problem, population)
        front.update(population)
        front = [[fit.fitness.values[i] for fit in front] for i,obj in enumerate(problem.objectives)]
        axarr[a][2].plot(front[0], front[1], linestyle='None', marker=algorithm.type, color=algorithm.color, markersize=5, markeredgecolor='none')
        axarr[a][2].set_xlim([min(OX), max(OX)])
        axarr[a][2].set_ylim([min(OY), max(OY)])
        
        X = plot_points_norexbest[p][a][0]
        Y = plot_points_norexbest[p][a][1]
        axarr[a][3].plot(Ofront[0], Ofront[1], marker=algorithm.type, color='Yellow', markersize=5, markeredgecolor='none')
        axarr[a][3].plot(X, Y, linestyle='None', marker=algorithm.type, color='Silver', markersize=5, markeredgecolor='none')
        front = ParetoFront()
        population = [jmoo_individual(problem, [], [x,y]) for x,y in zip(X,Y)]
        population = deap_format(problem, population)
        front.update(population)
        front = [[fit.fitness.values[i] for fit in front] for i,obj in enumerate(problem.objectives)]
        axarr[a][3].plot(front[0], front[1], linestyle='None', marker=algorithm.type, color=algorithm.color, markersize=5, markeredgecolor='none')
        axarr[a][3].set_xlim([min(OX), max(OX)])
        axarr[a][3].set_ylim([min(OY), max(OY)])
        
        X = plot_points_rexbest[p][a][0]
        Y = plot_points_rexbest[p][a][1]
        axarr[a][4].plot(Ofront[0], Ofront[1], marker=algorithm.type, color='Yellow', markersize=5, markeredgecolor='none')
        axarr[a][4].plot(X, Y, linestyle='None', marker=algorithm.type, color='Silver', markersize=5, markeredgecolor='none')
        front = ParetoFront()
        population = [jmoo_individual(problem, [], [x,y]) for x,y in zip(X,Y)]
        population = deap_format(problem, population)
        front.update(population)
        front = [[fit.fitness.values[i] for fit in front] for i,obj in enumerate(problem.objectives)]
        axarr[a][4].plot(front[0], front[1], linestyle='None', marker=algorithm.type, color=algorithm.color, markersize=5, markeredgecolor='none')
        axarr[a][4].set_xlim([min(OX), max(OX)])
        axarr[a][4].set_ylim([min(OY), max(OY)])
        
        if a == 0:
            axarr[a][0].set_title("Original")
            axarr[a][1].set_title("Bin Draw")
            axarr[a][2].set_title("Rex Draw")
            axarr[a][3].set_title("No Rex Best")
            axarr[a][4].set_title("Rex Best")
            
        axarr[a][0].set_ylabel(algorithm.name)
        
    #folder prefix for storing reports
    date_folder_prefix = strftime("%m-%d-%Y")
    
    #if folder does not exist, create it
    if not os.path.isdir('charts/' + date_folder_prefix):
        os.makedirs('charts/' + date_folder_prefix)
    
    #fignum generator counts the number of files in the folder
    fignum = len([name for name in os.listdir('charts/' + date_folder_prefix)]) + 1
    print fignum
    F = mpl.gcf()
    DefaultSize = F.get_size_inches()
    F.set_size_inches( (DefaultSize[0]*3, DefaultSize[1]*2) )
    mpl.plt.savefig('charts/' + date_folder_prefix + '/force_' + 'figure' + str("%02d" % fignum) + "_" + problem.name + "_" + algorithm.name + "_"+ '.png', dpi=100)
    mpl.cla()        
                