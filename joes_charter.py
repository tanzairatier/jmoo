from pylab import *
import csv
from jmoo_problems import *
from jmoo_algorithms import *
from jmoo_properties import *
from utility import *

fignum = 0
data = []
heads = []
best = []
foam = []
RRS_scores = []
RRS = []
for p,prob in enumerate(problems):
    
    data.append([])
    heads.append([])
    best.append([])
    foam.append([])
    RRS.append([])
    RRS_scores.append([])
    for a,alg in enumerate(algorithms):
        finput = open("data/results_" + prob.name + "_" + alg.name + ".datatable", 'rb')
        f2input = open(DATA_PREFIX + RRS_TABLE + "_" + prob.name + "_" + alg.name + DATA_SUFFIX, 'rb')
        reader = csv.reader(finput, delimiter=',')
        reader2 = csv.reader(f2input, delimiter=',')
        data[p].append( [] )
        heads[p].append( [] )
        best[p].append( [] )
        foam[p].append( [] )
        RRS[p].append( [] )
        RRS_scores[p].append( [] )
        for o,obj in enumerate(prob.objectives): 
            foam[p][a].append([])
            foam[p][a][o] = {}
            RRS[p][a].append([])
            RRS[p][a][o] = {}
        
        for i,row in enumerate(reader2):
            for j,col in enumerate(row):
                if i == 0:
                    print col
                    RRS_scores[p][a].append([float(col.strip("%)( "))])
                else:
                    RRS_scores[p][a][j].append(float(col.strip("%)( ")))
            for o,obj in enumerate(prob.objectives):
                n = RRS_scores[p][a][-1][-1]
                n = (int(round(n/5.0)*5.0))
                if n in RRS[p][a][o]: RRS[p][a][o][n].append(float(RRS_scores[p][a][o][-1]))
                else: RRS[p][a][o][n] = [float(RRS_scores[p][a][o][-1])]
        for i,row in enumerate(reader):
            if not str(row[0]) == "0":
                for j,col in enumerate(row):
                    if i == 0:
                        heads[p][a].append(col)
                        data[p][a].append([])
                        best[p][a].append(999999)
                    else:
                        if not col == "":
                            data[p][a][j].append(float(col.strip("%)(")))
                            if data[p][a][j][-1] < best[p][a][j]: best[p][a][j] = data[p][a][j][-1]
                # row is now read
                if i > 0:
                    for o,obj in enumerate(prob.objectives):
                        n = data[p][a][0][-1]
                        n = (int(round(n/20.0)*20.0))
                        if n in foam[p][a][o]: foam[p][a][o][n].append(float(data[p][a][o*3+2][-1]))
                        else: foam[p][a][o][n] = [float(data[p][a][o*3+2][-1])]
            # all rows read
        # Interpolate foam keys
        for doit in range(5):
            for o,obj in enumerate(prob.objectives):
                keys = sorted(foam[p][a][o].keys())
                for key,nextkey in zip(keys[0:-1], keys[1:]):
                    foam[p][a][o][(nextkey-key)/2 + key] = foam[p][a][o][key]
                keys = sorted(foam[p][a][o].keys())
        """
        if alg.name == "GALE": 
            skips = 5
            dur = 20000
        else: 
            skips = 100
            dur = 20000
        
        for o,obj in enumerate(prob.objectives):
            for n in range(0, dur):
                nk = (int(round(n/float(skips))*float(skips)))
                if nk >= dur: nk = dur - skips
                nk1 = nk
                nk2 = nk
                while len(foam[p][a][o][n]) == 0: # and (nk1 < dur or nk2 >= 0):  
                    if nk1 < dur and len(foam[p][a][o][n]) == 0 and len(foam[p][a][o][nk1]) > 0:
                        for na in range(n, nk1):
                            foam[p][a][o][na].append(min(foam[p][a][o][nk1]) if obj.lismore else max(foam[p][a][o][nk1]))
                    if nk2 >= 0 and len(foam[p][a][o][n]) == 0 and len(foam[p][a][o][nk2]) > 0:
                        for na in range(nk2+1, n+1):
                            foam[p][a][o][na].append(min(foam[p][a][o][nk2]) if obj.lismore else max(foam[p][a][o][nk2]))
                    nk1 = nk1 + skips
                    #nk1 = (int(round(nk1/float(5.0))*float(5.0)))
                    nk2 = nk2 - skips
                    #nk2 = (int(round(nk2/float(5.0))*float(5.0))) 
            for n in range(0, 20000):
            #    print n, len(foam[p][a][o][n])  
                if len(foam[p][a][o][n]) == 0: foam[p][a][o][n].append(prob.referencePoint[o])
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


codes = ["rx", "b+", "g1"]
codes2= ["r-", "b-", "g-"]
colors= ["r", "b", "g"]
symbols=["x", "+", "1"]
line =  "-"
dotted= "--"
algnames = [alg.name for alg in algorithms]
axy = [0,1,2,3]
axx = [0,0,0,0]
f, axarr = plt.subplots(max(2,max([len(prob.objectives) for prob in problems])), max(2,len(problems)))
for p,prob in enumerate(problems):
    
    for o,obj in enumerate(prob.objectives):
        maximum = -9999999.9
        minimum = +9999999.9
        if not o == 112:
            o_o = o
            if o > 4:
                o_o = o - 1
            for a,alg in enumerate(algorithms):
                maximum = max(max(data[p][a][o*3+2]), maximum)
                minimum = min(min(data[p][a][o*3+2]), minimum)
            for a,alg in enumerate(algorithms):
                if o == 0:
                    axarr[o_o][p].set_title(prob.name)
                if p == 0:
                    axarr[o_o][p].set_ylabel(prob.objectives[o].name, rotation=90)
                #axarr[o_o][p].plot([x for x in range(0,10000,10)], [100 for x in range(0,10000,10)], 'k-', [int(round(x/5.0)*5.0) for x in data[p][a][0]], data[p][a][o*3+2], codes[a],label=alg.name, markersize=1)
                #axarr[o_o][p].plot([x for x in range(0,10000,10)], [best[p][a][o*3+2] for x in range(0,10000,10)], colors[a]+dotted, markersize=1)
                #axarr[o_o][p].plot([x for x in data[p][a][0]], [best[p][a][o*3+2] for x in data[p][a][0]], codes2[a])
                #axarr[o_o][p].plot([x for x in range(0,10000,10)], [100 for x in range(0,10000,10)], 'k-', [key for key in RRS[p][a][o].keys()], [getPercentile(RRS[p][a][o], 25), getPercentile(RRS[p][a][o], 50), getPercentile(RRS[p][a][o], 75)], codes[a],label=alg.name, markersize=4)
                X = []
                Y = []
                for key in RRS[p][a][o]: 
                    #print key, getPercentile(RRS[p][a][o][key], 25), getPercentile(RRS[p][a][o][key], 50), getPercentile(RRS[p][a][o][key], 75)
                    X += [key, key, key]
                    Y += [getPercentile(RRS[p][a][o][key], 25), getPercentile(RRS[p][a][o][key], 50), getPercentile(RRS[p][a][o][key], 75)]
                    
                for r in range(len(X)/3):
                    axarr[o_o][p].plot(X[r*3:(r+1)*3], Y[r*3:(r+1)*3], codes2[a],label=alg.name, markersize=1)
                for r in range(3):
                    axarr[o_o][p].plot([X[(k)*3+r] for k in range(len(X)/3)], [Y[(k)*3+r] for k in range(len(X)/3)], colors[a]+["_", "o", "_"][r % 3],label=alg.name, markersize=[8, 3, 8][r])
                axarr[o_o][p].plot([x for x in range(0,10000,10)], [100 for x in range(0,10000,10)], 'k-')
                
                #axarr[o_o][p].plot([key for key in sorted(foam[p][a][o].keys())], [min(foam[p][a][o][key]) for key in sorted(foam[p][a][o].keys())], colors[a]+"-", markersize=1)
                axarr[o_o][p].set_autoscale_on(False)
                axarr[o_o][p].set_xlim([0, 10000])
                axarr[o_o][p].set_xscale('log')
                
                if maximum > 1000: axarr[o_o][p].set_yscale('log')
                f.set_size_inches(2.75*4, 2.75*3)
                """
                if obj.name == "Cost":
                    axarr[o_o][p].set_ylim([-10, 210])
                elif obj.name == "Completion":
                    axarr[o_o][p].set_ylim([50, 150])
                elif obj.name == "Idle":
                    axarr[o_o][p].set_ylim([-10, 210])
                elif obj.name == "Score":
                    axarr[o_o][p].set_ylim([-10, 140])
                else:
                """    
                axarr[o_o][p].set_ylim([minimum-(maximum-minimum)*0.10, maximum+(maximum-minimum)*0.10])
                    
                #if prob.name == "Viennet2":
                #    axarr[o_o][p].set_ylim([50, 110])
                #xlabel("num evaluations")
                #ylabel("% of initial")
#suptitle(prob.name, fontsize=11)
plt.subplots_adjust(top=0.85)
plt.subplots_adjust(bottom=0.15)
legend(loc='upper center', bbox_to_anchor=(-0.10, -0.10), ncol=3, prop=fontP)
#show()

fignum = len([name for name in os.listdir('charts/' + date_folder_prefix)])
print fignum
plt.savefig('charts/' + date_folder_prefix + '/figure' + str("%02d" % fignum) + "_" + "objectives_" + prob.name + "_" + tag + '.png', dpi=100)
cla()
