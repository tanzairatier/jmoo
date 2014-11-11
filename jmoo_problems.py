
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
"Implementation of a variety of Multi-Objective Problems"

from jmoo_objective import *
from jmoo_decision import *
from jmoo_problem import *
from jmoo_stats_box import *

import math
from math import *
import os,sys,inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"Problems/pom3")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import pom3

def distance(in1, in2):
    return sum([abs(x-y) for x,y in zip(in1,in2)])**0.5

def initialPopulation(problem, n):
    #generate dataset
    dataset = []
    for run in range(n):
        dataset.append(problem.generateInput())
        
    #write the dataset to file
    filename = "data/" + problem.name + str(n) + "dataset.txt"  #i.e. "Golinski100dataset.txt"  
    fo = open(filename, 'w')
    h = problem.buildHeader() #the header row
    fo.write(h + "\n")
    for data in dataset: #each row of actual data
        fo.write(str(data).strip("[]") + "\n")
    
    print "Dataset generated for " + problem.name + " in " + filename + "."
    
    #preprocessing
    #take first X guys of dataset to get reference point and objective highs and lows
    fitnesses = []
    for i in range(500):
        fitnesses.append( problem.evaluate(problem.generateInput()) )
    # Split Columns into Lists
    fitnessColumns = [[fit[i] for fit in fitnesses] for i,obj in enumerate(problem.objectives)]

    # Calculate Medians and Spreads
    fitnessMedians = [median(fitCol) for fitCol in fitnessColumns]
    
    # Calculate highs and lows of each objective
    fitnessLows = [min(fitCol) for fitCol in fitnessColumns]
    fitnessUps = [max(fitCol) for fitCol in fitnessColumns]
    
    s = ""
    for x,y,z in zip(fitnessLows, fitnessMedians, fitnessUps): s += str(x) + "," + str(y) + "," + str(z) + "\n"
    fo.write(s)
    fo.close()
    
def dataGen(problem, n):
    "Generate data to be used in Initial Population of jmoo_jmeoa" 
    "- This method generates data for a particular problem."
    "- The data consists of a header row, followed by rows of actual data."
    "- Each row of data after the header contains values for each decision/objective."
    "- '$' indicates a decision, while '>>' indicates an objective to minimize.  '<<' is" 
    "  an objective to maximize."
    
    ins = []
    
    #generate random center
    center = problem.generateInput()
    c_dists = []
    
    #generate pre-set
    for run in range(1000):
        ins.append(problem.generateInput())
        c_dists.append(distance(ins[-1], center))
    
    
    spacer = max(c_dists) / 2.0
    print spacer
    ins = []
    for run in range(n):
        print run
        newdist = 100000
        while newdist > spacer:
            newguy = problem.generateInput()
            newdist = distance(newguy, center)
        ins.append(newguy)
    
    print len(ins)
    
    dataset = []
    for guy in ins:
        dataset.append(guy + problem.evaluate(guy))
    
    #generate dataset
    #dataset = []
    #for run in range(n):
    #    dataset.append(problem.generateInput() + problem.evaluate())
        
    #write the dataset to file
    filename = "data/" + problem.name + str(n) + "dataset.txt"  #i.e. "Golinski100dataset.txt"  
    fo = open(filename, 'w')
    h = problem.buildHeader() #the header row
    fo.write(h + "\n")
    for data in dataset: #each row of actual data
        fo.write(str(data).strip("[]") + "\n")
    fo.close()
    print "Dataset generated for " + problem.name + " in " + filename + "."

class kursawe(jmoo_problem):
    "Kursawe"
    def __init__(prob, n):
        prob.name = "Kursawe"
        names = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8"]
        n = max(min(8, n), 1) #constrain n to its range
        prob.decisions = [jmoo_decision(names[i], -5, 5) for i in range(n)]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        X = [decision.value for decision in prob.decisions]
        prob.objectives[0].value = sum(-10 * exp(-0.2 * sqrt(x * x + y * y)) for x, y in zip(X[:-1], X[1:]))
        prob.objectives[1].value = sum(abs(x)**0.8 + 5 * sin(x * x * x) for x in X)
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class schaffer(jmoo_problem):
    "Schaffer"
    def __init__(prob):
        prob.name = "Schaffer"
        prob.decisions = [jmoo_decision("x1", -10, 10)]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x = [decision.value for decision in prob.decisions][0]
        prob.objectives[0].value = x**2
        prob.objectives[1].value = (x-2)**2
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

class fonseca(jmoo_problem):
    "Fonseca"
    def __init__(prob, n):
        prob.evals = 0
        prob.name = "Fonseca"
        names = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8"]
        n = max(min(8, n), 1) #constrain n to its range
        prob.decisions = [jmoo_decision("x" + str(i+1), -2, 2) for i in range(n)]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        X = [decision.value for decision in prob.decisions]
        prob.objectives[0].value = 1 - exp( -sum([(x - 1/sqrt(len(prob.decisions)))**2 for x in X]) )
        prob.objectives[1].value = 1 - exp( -sum([(x + 1/sqrt(len(prob.decisions)))**2 for x in X]) )
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class poloni(jmoo_problem):
    "Poloni"
    def __init__(prob):
        prob.name = "Poloni"
        prob.decisions = [jmoo_decision("x1", -math.pi, math.pi), jmoo_decision("x2", -math.pi, math.pi)]
        prob.objectives = [jmoo_objective("f1", False), jmoo_objective("f2", False)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input = [decision.value for decision in prob.decisions]
        A = [0.5 * sin(1) - 2 * cos(1) + sin(2) - 1.5 * cos(2),  1.5 * sin(1) - cos(1) + 2 * sin(2) - 0.5 * cos(2)]
        B = [0.5 * sin(input[0]) - 2 * cos(input[0]) + sin(input[1]) - 1.5 * cos(input[1]), 1.5 * sin(input[0]) - cos(input[0]) + 2 * sin(input[1]) - 0.5 * cos(input[1])]
        prob.objectives[0].value = 1 + (A[0] - B[0])**2 + (A[1] - B[1])**2
        prob.objectives[1].value = (input[0] + 3)**2 + (input[1] + 1)**2
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

class viennet2(jmoo_problem):
    "Viennet 2"
    def __init__(prob):
        prob.name = "Viennet2"
        prob.decisions = [jmoo_decision("x1", -4, 4), jmoo_decision("x2", -4, 4)]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True), jmoo_objective("f3", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input = [decision.value for decision in prob.decisions]
        prob.objectives[0].value = (input[0]-2)*(input[0]-2)/2.0 + (input[1]+1)*(input[1]+1)/13.0 + (3.0)
        prob.objectives[1].value = (input[0]+input[1]-3.0)*(input[0]+input[1]-3.0)/36.0 + (-input[0]+input[1]+2.0)*(-input[0]+input[1]+2.0)/8.0 - (17.0)
        prob.objectives[2].value = (input[0]+2*input[1]-1)*(input[0]+2*input[1]-1)/175.0 + (2*input[1]-input[0])*(2*input[1]-input[0])/17.0 - (13.0)
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class viennet3(jmoo_problem):
    "Viennet 3"
    def __init__(prob):
        prob.name = "Viennet3"
        prob.decisions = [jmoo_decision("x1", -3, 3), jmoo_decision("x2", -3, 3)]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True), jmoo_objective("f3", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input = [decision.value for decision in prob.decisions]  
        A = 3.0 * input[0] - 2.0 * input[1] + 4.0
        B = input[0] - input[1] + 1.0
        prob.objectives[0].value = 0.5 * (input[0]*input[0] + input[1]*input[1]) + sin(input[0]*input[0] + input[1]*input[1])
        prob.objectives[1].value = (A * A)/8.0 + (B * B)/27.0 + 15.0
        prob.objectives[2].value = 1.0 / (input[0]*input[0] + input[1]*input[1]+1) - 1.1 * exp(-(input[0]*input[0])-(input[1]*input[1]))
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class viennet4(jmoo_problem):
    "Viennet 4"
    def __init__(prob):
        prob.name = "Viennet4"
        prob.decisions = [jmoo_decision("x1", -4, 4), jmoo_decision("x2", -4, 4)]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True), jmoo_objective("f3", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input = [decision.value for decision in prob.decisions]
        prob.objectives[0].value = (input[0]-2.0)*(input[0]-2.0)/2.0 + (input[1]+1.0)*(input[1]+1.0)/13.0 + 3.0
        prob.objectives[1].value = (input[0]+ input[1]-3.0)*(input[0]+input[1]-3.0)/175.0 +(2.0*input[1]-input[0])*(2.0*input[1]-input[0])/17.0 -13.0
        prob.objectives[2].value = (3.0*input[0]-2.0*input[1]+4.0)*(3.0*input[0]-2.0*input[1]+4.0)/8.0 + (input[0]-input[1]+1.0)*(input[0]-input[1]+1.0)/27.0 + 15.0
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
          
class golinski(jmoo_problem):
    "Golinski"
    def __init__(prob):
        prob.name = "Golinski"
        names = ["x1", "x2", "x3", "x4", "x5", "x6", "x7"]
        LOWS = [2.6, 0.7, 17.0, 7.3, 7.3, 2.9, 5.0]
        UPS = [3.6, 0.8, 28.0, 8.3, 8.3, 3.9, 5.5]
        prob.decisions = [jmoo_decision(names[i], LOWS[i], UPS[i]) for i in range(7)]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input = [decision.value for decision in prob.decisions]
        aux = 745.0 * input[3] / (input[1] * input[2]);
        prob.objectives[0].value = 0.7854 * input[0] *input[1] *input[1] * ((10*input[2]*input[2])/3.0 + 14.933*input[2] - 43.0934) - 1.508*input[0]*(input[5]*input[5] + input[6]*input[6])+7.477*(input[5]*input[5]*input[5] + input[6]*input[6]*input[6]) + 0.7854*(input[3]*input[5]*input[5] + input[4]*input[6]*input[6]);        
        prob.objectives[1].value = sqrt((aux*aux)+1.69e7) / (0.1*input[5]*input[5]*input[5]);
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class zdt1(jmoo_problem):
    "ZDT1"
    def __init__(prob):
        prob.name = "ZDT1"
        names = ["x" + str(i+1) for i in range(30)]
        prob.decisions = [jmoo_decision(names[i], 0, 1) for i in range(len(names))]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input = [decision.value for decision in prob.decisions]
        g  = 1.0 + 9.0*sum(input[1:])/(len(input)-1)
        prob.objectives[0].value = input[0]        
        prob.objectives[1].value = g * (1 - sqrt(input[0] / g))
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

class zdt2(jmoo_problem):
    "ZDT2"
    def __init__(prob):
        prob.name = "ZDT2"
        names = ["x" + str(i+1) for i in range(30)]
        prob.decisions = [jmoo_decision(names[i], 0, 1) for i in range(len(names))]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input = [decision.value for decision in prob.decisions]
        g  = 1.0 + 9.0*sum(input[1:])/(len(input)-1)
        prob.objectives[0].value = input[0]        
        prob.objectives[1].value = g * (1 - (input[0] / g)**2)
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

class zdt3(jmoo_problem):
    "ZDT3"
    def __init__(prob):
        prob.name = "ZDT3"
        names = ["x" + str(i+1) for i in range(30)]
        prob.decisions = [jmoo_decision(names[i], 0, 1) for i in range(len(names))]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input = [decision.value for decision in prob.decisions]
        g  = 1.0 + 9.0*sum(input[1:])/(len(input)-1)
        prob.objectives[0].value = input[0]        
        prob.objectives[1].value = g * (1 - sqrt(input[0]/g) - input[0]/g * math.sin(10*math.pi*input[0]))
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

class zdt4(jmoo_problem):
    "ZDT4"
    def __init__(prob):
        prob.name = "ZDT4"
        names = ["x" + str(i+1) for i in range(10)]
        prob.decisions = [jmoo_decision(names[i], -5, 5) for i in range(len(names))]
        prob.decisions[0].low = 0
        prob.decisions[0].up = 1
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input = [decision.value for decision in prob.decisions]
        g  = 1 + 10*(len(input)-1) + sum(xi**2 - 10*math.cos(4*math.pi*xi) for xi in input[1:])
        prob.objectives[0].value = input[0]        
        prob.objectives[1].value = g * (1 - (input[0] / g)**2)
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

class zdt6(jmoo_problem):
    "ZDT6"
    def __init__(prob):
        prob.name = "ZDT6"
        names = ["x" + str(i+1) for i in range(10)]
        prob.decisions = [jmoo_decision(names[i], 0, 1) for i in range(len(names))]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input = [decision.value for decision in prob.decisions]
        g  = 1 + 9 * (sum(input[1:]) / (len(input)-1))**0.25
        f1 = prob.objectives[0].value = 1 - math.exp(-4*input[0]) * math.sin(6*math.pi*input[0])**6
        prob.objectives[1].value = g * (1 - (f1/g)**2)
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class water(jmoo_problem):
    "Water Problem"
    def __init__(prob):
        prob.name = "Water"
        lows = [0.01, 0.01, 0.01]
        ups = [0.45, 0.10, 0.10]
        prob.decisions = [jmoo_decision("x" + str(i+1), lows[i], ups[i]) for i in range(3)]
        prob.objectives = [jmoo_objective("f" + str(i+1), True) for i in range(5)]
    def evaluate(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1,x2,x3 = prob.decisions[0].value, prob.decisions[1].value, prob.decisions[2].value
        prob.objectives[0].value = 106780.37*(x2+x3) + 61704.67
        prob.objectives[1].value = 3000*x1
        prob.objectives[2].value = (305700*2289*x2)/((0.06*2289)**0.65)
        prob.objectives[3].value = 250*2289*x2*exp(-39.75*x2+9.9*x3+2.74)
        prob.objectives[4].value = 25*(1.39/(x1*x2+4940*x3-80))
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1,x2,x3 = prob.decisions[0].value, prob.decisions[1].value, prob.decisions[2].value
        if (1 -     0.00139 /(x1*x2) + 4.94 *  x3 - 0.08) < 0: return True
        if (1 -     0.000306/(x1*x2) + 1.082 * x3 - 0.0986) < 0: return True
        if (5000 -  12.307  /(x1*x2) + 4.9408* x3 + 4051.02) < 0: return True
        if (16000 - 2.09    /(x1*x2) + 804633* x3 - 696.71) < 0: return True
        if (10000 - 2.138   /(x1*x2) + 7883.39*x3 - 705.04) < 0: return True
        if (2000 -  0.417   /(x1*x2) + 1721.26*x3 - 136.54) < 0: return True
        if (550 -   0.164   /(x1*x2) + 631.13* x3 - 54.48) < 0: return True
        return False
    def evalConstraintOverages(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1,x2,x3 = prob.decisions[0].value, prob.decisions[1].value, prob.decisions[2].value
        g1 = abs(min((1 -     0.00139 /(x1*x2) + 4.94 *  x3 - 0.08), 0))
        g2 = abs(min((1 -     0.000306/(x1*x2) + 1.082 * x3 - 0.0986), 0))
        g3 = abs(min((5000 -  12.307  /(x1*x2) + 4.9408* x3 + 4051.02), 0))
        g4 = abs(min((16000 - 2.09    /(x1*x2) + 804633* x3 - 696.71), 0))
        g5 = abs(min((10000 - 2.138   /(x1*x2) + 7883.39*x3 - 705.04), 0))
        g6 = abs(min((2000 -  0.417   /(x1*x2) + 1721.26*x3 - 136.54), 0))
        g7 = abs(min((550 -   0.164   /(x1*x2) + 631.13* x3 - 54.48), 0))  
        return False
    
class srinivas(jmoo_problem):
    "Srinivas"
    def __init__(prob):
        prob.name = "Srinivas"
        prob.decisions = [jmoo_decision("x" + str(i+1), -20, 20) for i in range(2)]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1,x2 = prob.decisions[0].value, prob.decisions[1].value
        prob.objectives[0].value = (x1-2)**2 + (x2 - 1)**2 + 2  
        prob.objectives[1].value = 9*x1 - (x2 - 1)**2
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1,x2 = prob.decisions[0].value, prob.decisions[1].value
        if (x1**2 +   x2**2 > 225): return True
        if (x1    - 3*x2    > -10): return True
        return False
    def evalConstraintOverages(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1,x2 = prob.decisions[0].value, prob.decisions[1].value
        g1 = max((x1**2 +   x2**2) - 225, 0)
        g2 = max((x1    - 3*x2   ) - -10, 0)
        return [g1, g2]

class constrex(jmoo_problem):
    "ConstrEx"
    def __init__(prob):
        prob.name = "ConstrEx"
        prob.decisions = [jmoo_decision("x1",0.1, 1.0),jmoo_decision("x2", 0, 5)]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1 = prob.decisions[0].value
        x2 = prob.decisions[1].value
        prob.objectives[0].value = x1
        prob.objectives[1].value = (1.0 + x2)/x1
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1 = prob.decisions[0].value
        x2 = prob.decisions[1].value
        if (9*x1 + x2 < 6): return True
        if (9*x1 - x2 < 1): return True
        return False
    def evalConstraintOverages(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1,x2 = prob.decisions[0].value, prob.decisions[1].value
        g1 = max(6 - (9*x1 + x2), 0)
        g2 = max(1 - (9*x1 - x2), 0)    
        return [g1, g2]
    
class tanaka(jmoo_problem):
    "Tanaka"
    def __init__(prob):
        prob.name = "Tanaka"
        prob.decisions = [jmoo_decision("x1",-math.pi, math.pi),jmoo_decision("x2", -math.pi, math.pi)]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1 = prob.decisions[0].value
        x2 = prob.decisions[1].value
        prob.objectives[0].value = x1
        prob.objectives[1].value = x2
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1 = prob.decisions[0].value
        x2 = prob.decisions[1].value
        if x2 == 0: x2 = 0.00001
        if (1 - x1**2 - x2**2 + 0.1*math.cos(16*math.atan(x1/x2)) > 0): return True
        if ((x1 - 0.5)**2 + (x2 - 0.5)**2 > 0.5): return True
        return False
    def evalConstraintOverages(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1 = prob.decisions[0].value
        x2 = prob.decisions[1].value
        if x2 == 0: x2 = 0.00001
        g1 = max(1 - x1**2 - x2**2 + 0.1*math.cos(16*math.atan(x1/x2)), 0)
        g2 = max( ((x1 - 0.5)**2 + (x2 - 0.5)**2) - 0.5, 0)
        return [g1, g2]
class osyczka2(jmoo_problem):
    "Osyczka2"
    def __init__(prob):
        prob.name = "Osyczka2"
        lows = [0, 0, 1, 1, 0, 0]
        ups = [10, 10, 5, 5, 6, 10]
        names = ["x1", "x2", "x3", "x4", "x5", "x6"]
        prob.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(6)]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1 = prob.decisions[0].value
        x2 = prob.decisions[1].value
        x3 = prob.decisions[2].value
        x4 = prob.decisions[3].value
        x5 = prob.decisions[4].value
        x6 = prob.decisions[5].value
        prob.objectives[0].value = 0 - (25*(x1 - 2)**2 + (x2 - 2)**2 + (x3 - 1)**2*(x4 - 4)**2 + (x5 - 2)**2)  
        prob.objectives[1].value = x1**2 + x2**2 + x3**2 + x4**2 + x5**2 + x6**2
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1 = prob.decisions[0].value
        x2 = prob.decisions[1].value
        x3 = prob.decisions[2].value
        x4 = prob.decisions[3].value
        x5 = prob.decisions[4].value
        x6 = prob.decisions[5].value
        if (x1 + x2 - 2 < 0): return True
        if (6 - x1 - x2 < 0): return True
        if (2 - x2 + x1 < 0): return True
        if (2 - x1 + 3*x2 < 0): return True
        if (4 - (x3 - 3)**2 - x4 < 0): return True
        if ((x5 - 3)**3 + x6 - 4 < 0): return True
        return False
    def evalConstraintOverages(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1 = prob.decisions[0].value
        x2 = prob.decisions[1].value
        x3 = prob.decisions[2].value
        x4 = prob.decisions[3].value
        x5 = prob.decisions[4].value
        x6 = prob.decisions[5].value
        g1 = abs(min(x1 + x2 - 2, 0))
        g2 = abs(min(6 - x1 - x2, 0))
        g3 = abs(min(2 - x2 + x1, 0))
        g4 = abs(min(2 - x1 + 3*x2, 0))
        g5 = abs(min(4 - (x3 - 3)**2 - x4, 0))
        g6 = abs(min((x5 - 3)**3 + x6 - 4, 0))
        return [g1, g2, g3, g4, g5, g6]

class joetest1(jmoo_problem):
    "Some Stupid Test Problem"
    def __init__(prob, n):
        prob.name = "JoeTest1"
        names = ["x1", "x2", "x3"]
        prob.decisions = [jmoo_decision(names[i], -2, 2) for i in range(n)]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        X = [decision.value for decision in prob.decisions]
        prob.objectives[0].value = X[0]
        prob.objectives[1].value = X[1]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob):
        return False #no constraints

class POM3A(jmoo_problem):
    "POM3A"
    def __init__(prob):
        prob.name = "POM3A"
        names = ["Culture", "Criticality", "Criticality Modifier", "Initial Known", "Inter-Dependency", "Dynamism", "Size", "Plan", "Team Size"]
        LOWS = [0.1, 0.82, 2,  0.40, 1,   1,  0, 0, 1]
        UPS  = [0.9, 1.20, 10, 0.70, 100, 50, 4, 5, 44]
        prob.decisions = [jmoo_decision(names[i], LOWS[i], UPS[i]) for i in range(len(names))]
        prob.objectives = [jmoo_objective("Cost", True, 0), jmoo_objective("Score", False, 0, 1), jmoo_objective("Completion", False, 0, 1), jmoo_objective("Idle", True, 0, 1)]
        #prob.objectives = [jmoo_objective("Cost", True), jmoo_objective("Score", False), jmoo_objective("Idle", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        else: input = [decision.value for decision in prob.decisions]
        p3 = pom3.pom3()
        output = p3.simulate(input)
        for i,objective in enumerate(prob.objectives):
            objective.value = output[i]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class POM3Asanscomp(jmoo_problem):
    "POM3A"
    def __init__(prob):
        prob.name = "POM3Asanscomp"
        names = ["Culture", "Criticality", "Criticality Modifier", "Initial Known", "Inter-Dependency", "Dynamism", "Size", "Plan", "Team Size"]
        LOWS = [0.1, 0.82, 2,  0.40, 1,   1,  0, 0, 1]
        UPS  = [0.9, 1.20, 10, 0.70, 100, 50, 4, 5, 44]
        prob.decisions = [jmoo_decision(names[i], LOWS[i], UPS[i]) for i in range(len(names))]
        prob.objectives = [jmoo_objective("Cost", True, 0), jmoo_objective("Score", False, 0, 1), jmoo_objective("Idle", True, 0, 1)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        else: input = [decision.value for decision in prob.decisions]
        p3 = pom3.pom3()
        output = p3.simulate(input)
        output = [output[0], output[1], output[3]]
        for i,objective in enumerate(prob.objectives):
            objective.value = output[i]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class POM3B(jmoo_problem):
    "POM3B"
    def __init__(prob):
        prob.name = "POM3B"
        names = ["Culture", "Criticality", "Criticality Modifier", "Initial Known", "Inter-Dependency", "Dynamism", "Size", "Plan", "Team Size"]
        LOWS = [0.10, 0.82, 80, 0.40, 0,   1, 0, 0, 1]
        UPS  = [0.90, 1.26, 95, 0.70, 100, 50, 2, 5, 20]
        prob.decisions = [jmoo_decision(names[i], LOWS[i], UPS[i]) for i in range(len(names))]
        prob.objectives = [jmoo_objective("Cost", True, 0), jmoo_objective("Score", False, 0, 1), jmoo_objective("Completion", False, 0, 1), jmoo_objective("Idle", True, 0, 1)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        else: input = [decision.value for decision in prob.decisions]
        p3 = pom3.pom3()
        output = p3.simulate(input)
        for i,objective in enumerate(prob.objectives):
            objective.value = output[i]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints   
    
class POM3Bsanscomp(jmoo_problem):
    "POM3B"
    def __init__(prob):
        prob.name = "POM3Bsanscomp"
        names = ["Culture", "Criticality", "Criticality Modifier", "Initial Known", "Inter-Dependency", "Dynamism", "Size", "Plan", "Team Size"]
        LOWS = [0.10, 0.82, 80, 0.40, 0,   1, 0, 0, 1]
        UPS  = [0.90, 1.26, 95, 0.70, 100, 50, 2, 5, 20]
        prob.decisions = [jmoo_decision(names[i], LOWS[i], UPS[i]) for i in range(len(names))]
        prob.objectives = [jmoo_objective("Cost", True, 0), jmoo_objective("Score", False, 0, 1), jmoo_objective("Idle", True, 0, 1)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        else: input = [decision.value for decision in prob.decisions]
        p3 = pom3.pom3()
        output = p3.simulate(input)
        output = [output[0], output[1], output[3]]
        for i,objective in enumerate(prob.objectives):
            objective.value = output[i]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints  

class POM3C(jmoo_problem):
    "POM3C"
    def __init__(prob):
        prob.name = "POM3C"
        names = ["Culture", "Criticality", "Criticality Modifier", "Initial Known", "Inter-Dependency", "Dynamism", "Size", "Plan", "Team Size"]
        LOWS = [0.50, 0.82, 2, 0.20, 0,  40, 2, 0, 20]
        UPS  = [0.90, 1.26, 8, 0.50, 50, 50, 4, 5, 44]
        prob.decisions = [jmoo_decision(names[i], LOWS[i], UPS[i]) for i in range(len(names))]
        prob.objectives = [jmoo_objective("Cost", True, 0), jmoo_objective("Score", False, 0, 1), jmoo_objective("Completion", False, 0, 1), jmoo_objective("Idle", True, 0, 1)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        else: input = [decision.value for decision in prob.decisions]
        p3 = pom3.pom3()
        output = p3.simulate(input)
        for i,objective in enumerate(prob.objectives):
            objective.value = output[i]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints    
    
class POM3Csanscomp(jmoo_problem):
    "POM3C"
    def __init__(prob):
        prob.name = "POM3Csanscomp"
        names = ["Culture", "Criticality", "Criticality Modifier", "Initial Known", "Inter-Dependency", "Dynamism", "Size", "Plan", "Team Size"]
        LOWS = [0.50, 0.82, 2, 0.20, 0,  40, 2, 0, 20]
        UPS  = [0.90, 1.26, 8, 0.50, 50, 50, 4, 5, 44]
        prob.decisions = [jmoo_decision(names[i], LOWS[i], UPS[i]) for i in range(len(names))]
        prob.objectives = [jmoo_objective("Cost", True, 0), jmoo_objective("Score", False, 0, 1), jmoo_objective("Idle", True, 0, 1)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        else: input = [decision.value for decision in prob.decisions]
        p3 = pom3.pom3()
        output = p3.simulate(input)
        output = [output[0], output[1], output[3]]
        for i,objective in enumerate(prob.objectives):
            objective.value = output[i]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints 

class POM3D(jmoo_problem):
    "POM3D"
    def __init__(prob):
        prob.name = "POM3D"
        names = ["Culture", "Criticality", "Criticality Modifier", "Initial Known", "Inter-Dependency", "Dynamism", "Size", "Plan", "Team Size"]
        LOWS = [0.10, 0.82, 2, 0.60, 80,  1, 0, 0, 10]
        UPS  = [0.20, 1.26, 8, 0.95, 100, 10, 2, 5, 20]
        prob.decisions = [jmoo_decision(names[i], LOWS[i], UPS[i]) for i in range(len(names))]
        prob.objectives = [jmoo_objective("Cost", True, 0), jmoo_objective("Score", False, 0, 1), jmoo_objective("Completion", False, 0, 1), jmoo_objective("Idle", True, 0, 1)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        else: input = [decision.value for decision in prob.decisions]
        p3 = pom3.pom3()
        output = p3.simulate(input)
        for i,objective in enumerate(prob.objectives):
            objective.value = output[i]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class POM3MIN(jmoo_problem):
    "POM3D"
    def __init__(prob):
        prob.name = "POM3MIN"
        names = ["Culture", "Criticality", "Criticality Modifier", "Initial Known", "Inter-Dependency", "Dynamism", "Size", "Plan", "Team Size"]
        LOWS = [0.80, 1.22, 2, 0.60, 0,  1, 0, 0, 1]
        UPS  = [0.90, 1.62, 6, 0.62, 2, 3, 1, 1, 3]
        prob.decisions = [jmoo_decision(names[i], LOWS[i], UPS[i]) for i in range(len(names))]
        prob.objectives = [jmoo_objective("Cost", True), jmoo_objective("Score", False), jmoo_objective("Completion", False), jmoo_objective("Idle", True)]
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        else: input = [decision.value for decision in prob.decisions]
        p3 = pom3.pom3()
        output = p3.simulate(input)
        for i,objective in enumerate(prob.objectives):
            objective.value = output[i]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob):
        return False #no constraints
    
    
class UF10(jmoo_problem):
    def __init__(prob, n=30):
        prob.name = "UF10"
        prob.decisions = [jmoo_decision("x" + str(i), 0, 1) for i in range(2)] + [jmoo_decision("x" + str(j), -2, 2) for j in range(2, n)]
        prob.objectives = [jmoo_objective("f1", True), jmoo_objective("f2", True), jmoo_objective("f3", True)]
    def evaluate(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        x1 = prob.decisions[0].value
        x2 = prob.decisions[1].value
        X = [prob.decisions[i].value for i in range(len(prob.decisions))]
        
        Y = [None, None] + [  X[j] - 2*X[1]*sin(2*math.pi*X[0] + j*math.pi/len(prob.decisions)) for j in range(2,len(prob.decisions))  ]
        
        J1 = [j  for j in range(2, len(prob.decisions)) if ((j-1) % 3 == 0) ]
        J2 = [j  for j in range(2, len(prob.decisions)) if ((j-2) % 3 == 0)]
        J3 = [j  for j in range(2, len(prob.decisions)) if ((j)   % 3 == 0)]
        
        f1 = cos(0.5*X[0]*math.pi) * cos(0.5*X[1]*math.pi) + (2/len(J1)) * sum([   4*Y[j]**2 - cos(8*math.pi*Y[j])     for j in J1 ])
        f2 = cos(0.5*X[0]*math.pi) * sin(0.5*X[1]*math.pi) + (2/len(J2)) * sum([   4*Y[j]**2 - cos(8*math.pi*Y[j])     for j in J2 ])
        f3 = sin(0.5*X[0]*math.pi)  + (2/len(J3)) * sum([   4*Y[j]**2 - cos(8*math.pi*Y[j])     for j in J3 ])
        
        prob.objectives[0].value = f1
        prob.objectives[1].value = f2
        prob.objectives[2].value = f3
        
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob):
        return False #no constraints