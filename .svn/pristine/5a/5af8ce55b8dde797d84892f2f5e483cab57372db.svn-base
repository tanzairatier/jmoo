from pylab import *
from Slurp import *
import csv
from jmoo_problems import *



#GRAPH RRSLGA.DATATABLE

algorithms = ["NSGAII", "SPEA2", "GALE"]
#problems = ["Fonseca", "Golinski", "Kursawe", "Poloni", "Schaffer", "Viennet2", "Viennet3", "Viennet4", "Pom2Joe", "Srinivas", "Tanaka", "Osyczka2", "ConstrEx", "ZDT1", "ZDT2", "ZDT3", "ZDT4", "ZDT6"]
problems = [osyczka2(), zdt1(), schaffer(), tanaka()]
data = []
heads = []
for p,prob in enumerate(problems):
    data.append([])
    heads.append([])
    for a,alg in enumerate(algorithms):
        finput = open("data/results_" + prob.name + "_" + alg + ".datatable", 'rb')
        reader = csv.reader(finput, delimiter=',')
        
        data[p].append( [] )
        heads[p].append( [] )
        for i,row in enumerate(reader):
            for j,col in enumerate(row[:len(prob.objectives)*2+3]):
                if i == 0:
                    heads[p][a].append(col)
                    data[p][a].append([])
                else:
                    if not col == "":
                        data[p][a][j].append(float(col))

fignum = 0
colors = ['r', 'b', 'g']
from matplotlib.font_manager import FontProperties

fontP = FontProperties()
fontP.set_size('small')
ax = plt.subplot(111)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

for p,prob in enumerate(problems):
    for i in range((len(heads[p][0])-3)/2):  #heads for any alg are same
        for a,alg in enumerate(algorithms):
            plot([x if x > 0 else 0 for x in data[p][a][0]], data[p][a][1 + i*2], colors[a], label=alg + ":" + heads[p][a][1 + i*2])      #median
            plot([x if x > 0 else 0 for x in data[p][a][0]], data[p][a][2 + i*2], colors[a]+'--', label=alg + ":" + heads[p][a][2 + i*2]) #spread
            
            
            
            if prob.objectives[i].lismore: dirn = "(Minimize)"
            else: dirn = "(Maximize)"
            title(prob.name + "_" + alg + ": " + heads[p][a][i*2 + 1] + "/" + heads[p][a][i*2 + 2] + " " + dirn)
            xlabel("num evaluations")
            
            legend(loc='center left', bbox_to_anchor=(1, 0.5), prop = fontP)
            #show()
            
            fignum += 1
            plt.savefig('charts/4-2-2013/figure' + str("%02d" % fignum) + "_" + prob.name + "_" + alg + '_f' + str(i+1) + '.png', dpi=100)
            cla()
    
            plot([x for x in data[p][a][0]], data[p][a][len(prob.objectives)*2 + 1], 'k', label="IBD")
            plot([x for x in data[p][a][0]], data[p][a][len(prob.objectives)*2 + 2], 'k--', label="IBS")
            title(prob.name + ": " + heads[p][a][i*2 + 1] + "/" + heads[p][a][i*2 + 2] + " " + dirn)
            xlabel("num evaluations")
            
            legend(loc='center left', bbox_to_anchor=(1, 0.5), prop = fontP)
            #show()
            
            fignum += 1
            plt.savefig('charts/4-2-2013/figure' + str("%02d" % fignum) + "_" + prob.name + "_" + alg + '_ibd_ibs.png', dpi=100)
            cla()
    
"""
for i in range(numObjectives):
    plot([x/100 for x in rrslgadata[0]], rrslgadata[1+i*2], 'r', label = headers[1+i*2]) #median
    plot([x/100 for x in rrslgadata[0]], rrslgadata[2+i*2], '--r', label = headers[2+i*2]) #spread
    plot([x/100 for x in nsgadata[0]], nsgadata[1+i*2], 'b', label = headers[1+i*2]) #median
    plot([x/100 for x in nsgadata[0]], nsgadata[2+i*2], '--b', label = headers[2+i*2]) #spread
    plot([x/100 for x in speadata[0]], speadata[1+i*2], 'g', label = headers[1+i*2]) #median
    plot([x/100 for x in speadata[0]], speadata[2+i*2], '--g', label = headers[2+i*2]) #spread
    title(headers[1+i*2] + "/" + headers[2+i*2])
    legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1,
       ncol=2, mode="expand", borderaxespad=0.)
    
    show()

# GRAPH A PARETO FRONTIER

input = open('data/SchafferPF.pf', 'rb')
reader = csv.reader(input, delimiter='\t')

PF = [[], []]
for row in reader:
    PF[0].append(float(row[0]))
    PF[1].append(float(row[1]))

X = PF[0]
Y = PF[1]

input = open('data/Schaffer_rrsl_front', 'rb')
reader = csv.reader(input, delimiter=',')
PF = [[], []]
for row in reader:
    PF[0].append(float(row[0]))
    PF[1].append(float(row[1]))

X2 = PF[0]
Y2 = PF[1]


plot(X, Y, '-')
plot(X2,Y2, 'ro')
show()
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5,10.5)
plt.savefig('charts/schaffer10krrsl.png',dpi=100)


"""


#GRAPH OF THE DISTRIBUTIONS OF EACH POM2JOE OBJECTIVE
"""
readData = slurpFile("data/foo10000.txt")
X = [[] for x in range(len(readData.headers))]

for row in readData.rows:
    for i in range(len(X)):
        X[i].append(row.cells[i])

print X[9]
subplot(2, 2, 0)
hist(X[1])
title("score")
subplot(2,2,1)
hist([X[10]])
title("cost")
subplot(2,2,2)
hist([X[11]])
title("completion")
subplot(2,2,3)
hist([X[12]])
title("idle")
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5,10.5)
plt.savefig('charts/objective_distributions.png',dpi=100)
"""