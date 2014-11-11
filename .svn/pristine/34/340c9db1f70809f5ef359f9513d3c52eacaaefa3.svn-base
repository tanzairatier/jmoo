
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
"Core Part of JMOO accessed by jmoo_interface."

from jmoo_problems import *
from jmoo_algorithms import *
from jmoo_jmoea import *
from jmoo_properties import *
from jmoo_core import *
from joes_stats_suite import *
from joes_moo_charter import *
from joes_decision_binner import *
import time,sys

class jmoo_stats_report:
    def __init__(self,tests):
        self.tests = tests
    def doit(self,tagnote=""):
        joes_stats_reporter(self.tests.problems, self.tests.algorithms, tag=tagnote)
        
class jmoo_decision_report:
    def __init__(self,tests):
        self.tests = tests
    def doit(self,tagnote=""):
        joes_decision_reporter(self.tests.problems, self.tests.algorithms, tag=tagnote)

class jmoo_chart_report:
    def __init__(self,tests):
        self.tests = tests
    def doit(self,tagnote=""):
        joes_charter_reporter(self.tests.problems, self.tests.algorithms, tag=tagnote)
        
class jmoo_test:
    def __init__(self,problems,algorithms):
        self.problems = problems
        self.algorithms = algorithms
        
class JMOO:
    def __init__(self,tests,reports):
        self.tests = tests
        self.reports = reports
        
    def doTests(self):
        
        sc2 = open(DATA_PREFIX + SUMMARY_RESULTS + DATA_SUFFIX, 'w')
        # Main control loop
        representatives = []                        # List of resulting final generations (stat boxe datatype)
        zOut = "<Experiment>\n"
        for problem in self.tests.problems:
              
            zOut += "<Problem name = '" + problem.name + "'>\n"
            
            for algorithm in self.tests.algorithms:
                
                
                zOut += "<Algorithm name = '" + algorithm.name + "'>\n"
                
                print "#<------- " + problem.name + " + " + algorithm.name + " ------->#"
                
                # Initialize data file for recording summary information [for just this problem + algorithm]
                backend = problem.name + "_" + algorithm.name + ".txt"
                
                # Decision Data
                dbt = open(DATA_PREFIX + DECISION_BIN_TABLE + "_" + problem.name + "_" + algorithm.name + DATA_SUFFIX, 'w')
                sr = open(DATA_PREFIX + SUMMARY_RESULTS + problem.name + "_" + algorithm.name + DATA_SUFFIX, 'w')
                rrs = open(DATA_PREFIX + RRS_TABLE + "_" + problem.name + "_" + algorithm.name + DATA_SUFFIX, 'w')
                
                
                # Results Record:
                # # # Every generation
                # # # Decisions + Objectives
                
                # Summary Record
                # - Best Generation Only
                # - Number of Evaluations + Aggregated Objective Score
                # - 
                
                fa = open("data/results_"+problem.name+"_"+algorithm.name+".datatable", 'w')
                strings = ["NumEval"] + [obj.name + "_median,(%chg)," + obj.name + "_spread" for obj in problem.objectives] + ["IBD,(%chg), IBS"]
                for s in strings: fa.write(s + ",")
                fa.write("\n")
                fa.close()
                
                # Repeat Core
                for repeat in range(repeats):
                    
                    # Run 
                    
                    zOut += "<Run id = '" + str(repeat+1) + "'>\n"
                    
                    
                    start = time.time()
                    statBox = jmoo_evo(problem, algorithm)
                    end = time.time()
                    
                    # Record
                    
                    # Find best generation
                    representative = statBox.box[0]
                    for r,rep in enumerate(statBox.box):
                        if rep.IBD < representative.IBD: 
                            representative = statBox.box[r]
                    representatives.append(representative)
                    
                    
                    
                    
                        
                    # Decision Bin Data
                    s = ""
                    for row in representative.population: 
                        for dec in row.decisionValues:
                            s += str("%10.2f" % dec) + ","
                        if row.valid:
                            for obj in row.fitness.fitness:
                                s += str("%10.2f" % obj) + "," 
                        else:
                            for obj in problem.objectives:
                                s += "?" + ","
                            
                        s += str(representative.numEval) + ","
                        s += "\n"
                        
                    dbt.write(s)
                        
                    baseline = problem.referencePoint
                    s = ""
                    for row in representative.population:
                        #if not row.valid:
                        #    row.evaluate()
                        if row.valid:
                            for o,base,obj in zip(row.fitness.fitness, baseline, problem.objectives ):
                                c = percentChange(o, base, obj.lismore, obj.low, obj.up)
                                s += c + ","
                            s += str(representative.numEval) + "," 
                            for o,base,obj in zip(row.fitness.fitness, baseline, problem.objectives ):
                                c = str("%12.2f" % o)
                                s += c + ","
                            s += "\n"
                    rrs.write(s)
                        
                    #output every generation
                    for box in [representative]:
                        s_out = ""
                        s_out += problem.name + ","
                        s_out += algorithm.name + ","
                        s_out += str(box.numEval) + ","
                        for low in statBox.bests_actuals:
                            s_out += str("%10.2f" % low) + ","
                        s_out += str("%10.2f" % box.IBD) + "," + str("%10.2f" % box.IBS) + "," + str((end-start))
                        sr.write(s_out + "\n")
                        sc2.write(s_out + "\n")


                    zOut += "<Summary>\n"
                    zOut += "<NumEvals>" + str(representative.numEval) + "</NumEvals>\n"
                    zOut += "<RunTime>" + str((end-start)) + "</RunTime>\n"
                    zOut += "<IBD>" + str(box.IBD) + "</IBD>\n"
                    zOut += "<IBS>" + str(box.IBS) + "</IBS>\n"
                    for i in range(len(problem.objectives)):
                        zOut += "<" + problem.objectives[i].name + ">" + str(representative.fitnessMedians[i]) + "</" + problem.objectives[i].name + ">\n" 
                    zOut += "</Summary>"
                        
                        
                    
                    
                    # Finish
                    zOut += "</Run>\n"
                    print " # Finished: Celebrate! # " + " Time taken: " + str("%10.5f" % (end-start)) + " seconds."
                    
                zOut += "</Algorithm>\n"
            zOut += "</Problem>\n"
        zOut += "</Experiment>\n"
        zOutFile = open("ExperimentRecords.xml", 'w')
        zOutFile.write(zOut)
                    
                    
                    
    def doReports(self,thing=""):
        for report in self.reports:
            report.doit(tagnote = thing)
        
        
        