
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
"Stats reports for MOEAs"

from pylab import *
import csv
#from jmoo_problems import *
#from jmoo_algorithms import *
from jmoo_properties import *
from utility import *
from scipy import stats 

from time import *
import os

from stats import *
from a12 import *


def joes_stats_reporter(problems, algorithms, tag=""):
    
    #folder prefix for storing reports
    date_folder_prefix = strftime("%m-%d-%Y")
    
    #if folder does not exist, create it
    if not os.path.isdir('reports/' + date_folder_prefix):
        os.makedirs('reports/' + date_folder_prefix)
        
    #fignum generator counts the number of files in the folder
    fignum = len([name for name in os.listdir('reports/' + date_folder_prefix)]) + 1
    
    #optional tag name for the file
    fa = open('reports/' + date_folder_prefix + "/stats_suite_summary_report" + "_" + tag + str("%02d" % fignum) + ".txt", 'w')
    
    #container for summary data
    data = []
    algranks = [[] for alg in algorithms]
    nemalgranks = [[] for alg in algorithms]
    for p,problem in enumerate(problems):
        data.append([])
        reports = []
        for a,algorithm in enumerate(algorithms):
            filename = DATA_PREFIX + SUMMARY_RESULTS+problem.name + "-p" + str(MU) + "-d" + str(len(problem.decisions)) + "-o" + str(len(problem.objectives))+"_"+algorithm.name+DATA_SUFFIX
            finput = open(filename, 'rb')
            reader = csv.reader(finput, delimiter=',')
            
            
            data[p].append([])
            
            for i,row in enumerate(reader):
                if i == 0: 
                    data[p][a] = [[] for obj in problem.objectives] + [[],[],[],[]]
                    
                elements = row
                data[p][a][0].append( int(elements[3]) )
                for o,obj in enumerate(problem.objectives):
                    data[p][a][1+o].append( float(elements[4+o]) )
                data[p][a][1+len(problem.objectives)].append( float(elements[4+len(problem.objectives)]) )
                data[p][a][2+len(problem.objectives)].append( float(elements[5+len(problem.objectives)]) )
                data[p][a][3+len(problem.objectives)].append( float(elements[6+len(problem.objectives)]) )
            s = '{0: <12}'.format(problem.name + "-p" + str(MU) + "-d" + str(len(problem.decisions)) + "-o" + str(len(problem.objectives))) + "," + '{0: <12}'.format(algorithm.name) + ","
            s += str(avg(data[p][a][0])) + ","
            for dug in data[p][a]:#[len(problem.objectives)+1:]:
                s += str("%10.2f" % avg(dug)) + ","
            reports.append( s  )
        
        #read baseline
        filename = "data/" + problem.name + "-p" + str(MU) + "-d" + str(len(problem.decisions)) + "-o" + str(len(problem.objectives)) + "-dataset.txt"
        f2input = open(filename, 'rb')
        reader2 = csv.reader(f2input, delimiter=',')
        
        s = '{0: <12}'.format(problem.name) + "," + '{0: <12}'.format("Baseline") + "," + str("%10.2f" % 0) + ",0,"
        for i,row in enumerate(reader2):
            if i > MU:
                s += str("%10.2f" % float(row[1])) + ","
        s += str("%10.2f" % 1) + "," + str("%10.2f" % 0)
        print s
        fa.write(s + "\n")
                
        
            
        IBDs = [data[p][a][1+len(problem.objectives)] for a in range(len(algorithms))]
        AVGs = [avg(IBDs[a]) for a in range(len(algorithms))]
        #print avg(IBDs[0]), avg(IBDs[1]), avg(IBDs[2])
        
        groups = IBDs
        num_groups =  len(algorithms)
        num_blocks =  repeats
        cd = critical_difference(0.01, num_groups, num_blocks)
        #normed_data = [ [(g - avg(group))/(var(group)**2) for g in group] for group in groups] 
        #rv = [stats.kstest(nd, 'norm') for nd in normed_data]
        
        #print "We can reject that the data is normal: ", [r[1]<0.01 for r in rv]
        ranks = []
        for i in range(len(groups[0])):
            array = numpy.array([group[i] for group in groups])
            ranks.append( stats.rankdata(array) )
        rankcols = [[rank[i] for rank in ranks] for i in range(len(groups))]
        rankavgs = [avg(rankcols[i]) for i in range(len(groups))] 
        
        
        
        
        z1,p1 = stats.ranksums(IBDs[0], IBDs[1])
        z2,p2 = stats.ranksums(IBDs[0], IBDs[2])
        z3,p3 = stats.ranksums(IBDs[1], IBDs[2])
        
        a1= a12(IBDs[0], IBDs[1])
        a2= a12(IBDs[0], IBDs[2])
        a3= a12(IBDs[1], IBDs[2])
        
        a12mat = []
        #print "A12 Effect Size Matrix"
        #print '{0: <12}'.format(""      ),   '{0: >12}'.format("NSGAII"), '{0: >12}'.format("GALE"), '{0: >12}'.format("SPEA2")
        #print '{0: <12}'.format("NSGAII"),   
        a12mat.append('{0: >12}'.format("-"     ) + "," + str("%12.2f" % a1) + "," +        str("%12.2f" % a2))
        #print '{0: <12}'.format("GALE"  ),   
        a12mat.append(str("%12.2f" % (1-a1)) + ","    +  '{0: >12}'.format("-"  ) +"," +  str("%12.2f" % a3))
        #print '{0: <12}'.format("SPEA2" )
        a12mat.append(str("%12.2f" % (1-a2)) + ","     +  str("%12.2f" % (1-a3)) +"," +    '{0: >12}'.format("-"))
        alpha = 0.05
        wins = [0 for a in range(len(algorithms))]
        nemwins = [0 for a in range(len(algorithms))]
        if p1 < alpha: 
            "gale vs nsgaii are different"
            if AVGs[0] < AVGs[1]: 
                "gale wins over nsgaii"
                wins[0] += 1
            else: 
                wins[1] += 1
        
        if p2 < alpha: 
            "gale vs spea2 are different"
            if AVGs[0] < AVGs[2]:
                "gale wins over spea2"
                wins[0] += 1
            else:
                wins[2] += 1
        
        if p3 < alpha:
            "nsgaii vs spea2 are different"
            if AVGs[1] < AVGs[2]:
                wins[1] += 1
            else:
                wins[2] += 1
           
           
        #nemenyi ranking     
        if (abs(rankavgs[0]-rankavgs[1])) > cd: 
            "gale vs nsgaii are different"
            if rankavgs[0] < rankavgs[1]: 
                "gale wins over nsgaii"
                nemwins[0] += 1
            else: 
                nemwins[1] += 1
        
        if (abs(rankavgs[0]-rankavgs[2])) > cd: 
            "gale vs spea2 are different"
            if rankavgs[0] < rankavgs[2]:
                "gale wins over spea2"
                nemwins[0] += 1
            else:
                nemwins[2] += 1
        
        if (abs(rankavgs[1]-rankavgs[2])) > cd:
            "nsgaii vs spea2 are different"
            if rankavgs[1] < rankavgs[2]:
                nemwins[1] += 1
            else:
                nemwins[2] += 1        
        # rank algorithms by wins
        names = [alg.name for alg in algorithms]
        ranks = {}
        for index,w in enumerate(wins):
            if w in ranks: ranks[w].append(names[index])
            else: ranks[w] = [names[index]]
        reversed_keys = sorted(ranks.keys(), reverse=True)
        #print [str(ranks[r]) + "#" + str(rk+1) for rk,r in enumerate(reversed_keys)]
    
        # rank algorithms by nemwins
        names = [alg.name for alg in algorithms]
        nemranks = {}
        for index,w in enumerate(wins):
            if w in nemranks: nemranks[w].append(names[index])
            else: nemranks[w] = [names[index]]
        reversed_keys = sorted(nemranks.keys(), reverse=True)
        
        rank_reports = ["" for alg in algorithms]
        for rk,r in enumerate(reversed_keys):
            for item in ranks[r]:
                for what,name in enumerate(names):
                    if item == name: it = what
                algranks[it].append(rk+1)   
                rank_reports[it] = "Rank" + ": #" + str(rk+1)
        
        nemrank_reports = ["" for alg in algorithms]
        for rk,r in enumerate(reversed_keys):
            for item in nemranks[r]:
                for what,name in enumerate(names):
                    if item == name: it = what
                nemalgranks[it].append(rk+1)   
                nemrank_reports[it] = "nemRank" + ": #" + str(rk+1)
            
        nemenyi = []    
        for ra in rankavgs:
            nemenyi.append( str(ra) + "," + str(cd) )
    
        for dig,dug,dag,dog,deg in zip(reports, rank_reports, a12mat, nemenyi,nemrank_reports):
            print dig,  dug,  "," , dag, ", ", deg
            fa.write(dig + dug + dag + dog + deg + "\n")
        
        
    
    print "===Average Rank==="
    fa.write("===Average Rank===\n")
    for rk,alg in zip(algranks, algorithms):
        print alg.name + ":" + str("%12.2f" % avg(rk))
        fa.write(alg.name + ":" + str("%12.2f" % avg(rk)) + "\n")
        
    print "===Average nemRank==="
    fa.write("===Average nemRank===\n")
    for rk,alg in zip(nemalgranks, algorithms):
        print alg.name + ":" + str("%12.2f" % avg(rk))
        fa.write(alg.name + ":" + str("%12.2f" % avg(rk)) + "\n")
        
    fa.close()
        
    




    