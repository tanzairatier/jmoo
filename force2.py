import csv
from jmoo_properties import *
from jmoo_algorithms import *

import random, utility

from time import *
import os
import pylab as mpl
from histobin import *

def sinebow(h):
  h += 1/2
  h *= -1
  r = sin(pi * h)
  g = sin(pi * (h + 1/3))
  b = sin(pi * (h + 2/3))
  return (int(255*chan**2) for chan in (r, g, b))
  

def frange5(limit1, limit2 = None, increment = 1.):
  """
  Range function that accepts floats (and integers).

  Usage:
  frange(-2, 2, 0.1)
  frange(10)
  frange(10, increment = 0.5)

  The returned value is an iterator.  Use list(frange) for a list.
  """

  if limit2 is None:
    limit2, limit1 = limit1, 0.
  else:
    limit1 = float(limit1)

  count = int(math.ceil(limit2 - limit1)/increment)
  return (limit1 + n*increment for n in range(count))
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
leaf_plots = []
for p,problem in enumerate(problems):
    data.append([])
    decision_data.append([])
    objective_data.append([])
    plot_points.append([])
    plot_points_bindraw.append([])
    plot_points_rexdraw.append([])
    plot_points_norexbest.append([])
    plot_points_rexbest.append([])
    leaf_plots.append([])
    for a,algorithm in enumerate(algorithms):
        finput = open(DATA_PREFIX + SUMMARY_RESULTS + problem.name + "_" + algorithm.name + DATA_SUFFIX, 'rb')
        reader = csv.reader(finput, delimiter=',')
        plot_points[p].append([])
        plot_points_bindraw[p].append([])
        plot_points_rexdraw[p].append([])
        plot_points_norexbest[p].append([])
        plot_points_rexbest[p].append([])
        data[p].append([])
        leaf_plots[p].append([])
        
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
    
        population = []
        for i in range(len(decision_data[p][a][0])):
            decisions = [decision_data[p][a][d][i] for d in range(len(problem.decisions ))]
            scores    = [plot_points[p][a][o][i]   for o in range(len(problem.objectives))]
            #print decisions, scores
            population.append(jmoo_individual(problem, decisions, scores))
        
        
        problem.loadInitialPopulation(MU) #this loads up the objective hi and lows
        GALE = jmoo_GALE()
        leafs, numEval = GALE.selector(problem, population)#, wantEverything = True)
        
        
            
            
        print len(population), numEval
        n = len(problem.decisions)
        leaf_plots[p][a] =  [ [] for leaf in range(len(leafs))]
        for l,leaf in enumerate(leafs):
            leaf_plots[p][a][l] =  [ [] for obj in problem.objectives]  
            for row in leaf.table.rows:
                for o,obj in enumerate(problem.objectives):
                    leaf_plots[p][a][l][o].append(float(row.cells[n+o]))
        print str(len(leafs)) + " leafs detected"
        
        
        
            
for p,problem in enumerate(problems):
    f, axarr = mpl.plt.subplots(3, 1)
    for a,algorithm in enumerate(algorithms):
        X = plot_points[p][a][0]
        Y = plot_points[p][a][1]
        #axarr[a][0].plot(X, Y, linestyle='None', marker=algorithm.type, color='Silver', markersize=5, markeredgecolor='none')
        OX,OY = X, Y
        #front = ParetoFront()
        #population = [jmoo_individual(problem, [], [x,y]) for x,y in zip(X,Y)]
        #population = deap_format(problem, population)
        #front.update(population)
        #front = [[fit.fitness.values[i] for fit in front] for i,obj in enumerate(problem.objectives)]
        #Ofront = front
        #axarr[a][0].plot(front[0], front[1], linestyle='None', marker=algorithm.type, color=algorithm.color, markersize=5, markeredgecolor='none')
        
        axarr[a].set_xlim([min(OX), max(OX)])
        axarr[a].set_ylim([min(OY), max(OY)])        

        colors = ["Red", "Pink", "Orange", "Gold", "Yellow", "Green", "Blue", "Indigo", "Violet", "Black"]#Green", "Blue", "Green", "Pink", "Yellow", "Orange", "Purple", "Black", "Brown"]#, "IndianRed", "GreenYellow", "Aqua", "Gold", "Khaki", "SteelBlue", "PowderBlue"]
        import colorsys
        N = len(leaf_plots[p][a])
        print N
        HSV_tuples = [(x/360.0, 0.5, 0.9) for x in frange5(0, 360, (360/float(N)))]
        colors = map(lambda x: colorsys.hls_to_rgb(*x), HSV_tuples)
        numBins = len(colors)
        numAttributes = 3
        rgb_names = ["red", "green", "blue"]
        
        histobins = [histobin(numBins, jmoo_decision(rgb_names[i], 0, 1), i) for i in range(numAttributes)]
        for c,hbin in enumerate(histobins): 
            hbin.populate([color[c] for color in colors])
            for iii in range(10):
                hbin.rex()
        N = len(colors)
        print histobins
        colors = [ [] for attr in range(3)  ]
        for h,hbin in enumerate(histobins):
                for bin in hbin.bins:
                    colors[h] +=   [ bin.low + (bin.up-bin.low)/2 for i in range(int(N*hbin.freq(bin)/100.0)) ]
        
        #print colors
        
        
        #markers = ["p", "^", "*", ".", "x", 'd']
        string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890!@#$%^&*()=+~"
        #markers = ["$a$", "$k$", "$w$", "$y$", "$z$", "$o$", "$s$", "$H$", "$I$"]
        for l,leaf in enumerate(leaf_plots[p][a]):
            X = leaf[0]
            Y = leaf[1]
            color_choice = [ colors[i][l] for i in range(3)]
            #color_choice = colors[l]
            axarr[a].plot(X, Y, linestyle='None', marker='.', color=color_choice, markersize=10, markeredgecolor='none')

    
    date_folder_prefix = strftime("%m-%d-%Y")
    
    #if folder does not exist, create it
    if not os.path.isdir('charts/' + date_folder_prefix):
        os.makedirs('charts/' + date_folder_prefix)
    
    #fignum generator counts the number of files in the folder
    fignum = len([name for name in os.listdir('charts/' + date_folder_prefix)]) + 1
    print fignum
    F = mpl.gcf()
    DefaultSize = F.get_size_inches()
    F.set_size_inches( (DefaultSize[0]*1, DefaultSize[1]*3) )
    mpl.plt.savefig('charts/' + date_folder_prefix + '/force_' + 'figure' + str("%02d" % fignum) + "_" + problem.name + "_" + algorithm.name + "_"+ '.png', dpi=100)
    mpl.cla()        
                
    