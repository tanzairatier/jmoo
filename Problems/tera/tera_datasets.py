import csv
from sklearn import tree
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import sys
from jmoo_objective import *
from jmoo_decision import *
from jmoo_problem import jmoo_problem

def avg(lst):
    return sum(lst)/float(len(lst))

class Abcd: 
  def __init__(i,db="all",rx="all"):
    i.db = db; i.rx=rx;
    i.yes = 0
    i.no = 0
    i.known = {}; i.a= {}; i.b= {}; i.c= {}; i.d= {}
  def __call__(i,actual=None,predicted=None):
    return i.keep(actual,predicted)
  def tell(i,actual,predict):
    i.knowns(actual)
    i.knowns(predict)
    if actual == predict: i.yes += 1 
    else                :  i.no += 1
    for x in  i.known:
      if actual == x:
        if  predict == actual: i.d[x] += 1 
        else                 : i.b[x] += 1
      else:
        if  predict == x     : i.c[x] += 1 
        else                 : i.a[x] += 1
  def knowns(i,x):
    if not x in i.known:
      i.known[x]= i.a[x]= i.b[x]= i.c[x]= i.d[x]= 0.0
    i.known[x] += 1
    if (i.known[x] == 1):
      i.a[x] = i.yes + i.no
  def header(i, dontprint=True):
    if not dontprint:
        print "#",('{0:20s} {1:11s}  {2:4s}  {3:4s} {4:4s} '+ \
                     '{5:4s}{6:4s} {7:3s} {8:3s} {9:3s} '+ \
           '{10:3s} {11:3s}{12:3s}{13:10s}').format(
      "db", "rx", 
     "n", "a","b","c","d","acc","pd","pf","prec",
      "f","g","class")
        print '-'*100
  def ask(i, dontprint=True):
    def p(y) : return int(100*y + 0.5)
    def n(y) : return int(y)
    pd = pf = pn = prec = g = f = acc = 0
    for x in i.known:
      a= i.a[x]; b= i.b[x]; c= i.c[x]; d= i.d[x]
      if (b+d)    : pd   = d     / float(b+d)
      if (a+c)    : pf   = c     / float(a+c)
      if (a+c)    : pn   = (b+d) / float(a+c)
      if (c+d)    : prec = d     / float(c+d)
      if (1-pf+pd): g    = 2*(1-pf)*pd / float(1-pf+pd)
      if (prec+pd): f    = 2*prec*pd/float(prec+pd)
      if (i.yes + i.no): acc= i.yes/float(i.yes+i.no)
      if not dontprint:
          print "#",('{0:20s} {1:10s} {2:4d} {3:4d} {4:4d} '+ \
                '{5:4d} {6:4d} {7:4d} {8:3d} {9:3d} '+ \
         '{10:3d} {11:3d} {12:3d} {13:10s}').format(i.db,
          i.rx,  n(b + d), n(a), n(b),n(c), n(d), 
          p(acc), p(pd), p(pf), p(prec), p(f), p(g)," " + str(x))
    return acc, pd, pf, prec #return just the last row (bugs found class)
      


tera_decisions = [jmoo_decision("min_samples_split", 1, 100),
                  jmoo_decision("max_depth", 1, 100),
                  jmoo_decision("min_samples_leaf", 1, 100),
                  jmoo_decision("max_leaf_nodes", 2, 100),
                  jmoo_decision("criterion", 1, 2),]  #gini or entropy
tera_objectives = [jmoo_objective("acc", False),
                   jmoo_objective("pd", False),
                   jmoo_objective("pf", True),
                   jmoo_objective("prec", False),]


def readDataset(file, properties):
    prefix = "tera/"
    suffix = ".csv"
    finput = open(prefix + file + suffix, 'rb')
    reader = csv.reader(finput, delimiter=',')
    dataread = []
    try:
        k = properties.unusual_range_end
    except:
        k = 3
    for i,row in enumerate(reader):
        if i > 0: #ignore header row
            line = []
            for item in row[k:]:
                try:
                    line.append(float(item))
                except:
                    pass
            if line[-1] > 0: line[-1] = True
            else: line[-1] = False  
            dataread.append(np.array(line))
    properties = row[:k]
    #print properties
    return np.array(dataread), properties

def evaluator(input, properties):
    
    mss = int(round(input[0]))
    md  = int(round(input[1]))
    msl = int(round(input[2]))
    mln = int(round(input[3]))
    if input[4] >= 1.5: cri = "entropy"
    else: cri = "gini" 
    
    #data_train = [readDataset(data) for data in properties.training_dataset]
    data_train = ([], [])
    for data in properties.training_dataset:
        read = readDataset(data, properties)
        data_train = (np.array(list(data_train[0]) + list(read[0])), read[1])
    data_test  = readDataset(properties.test_dataset, properties)
    
    #train the learner
    indep = np.array(map(lambda x: np.array(x[:-1]), data_train[0]))
    dep   = np.array(map(lambda x: np.array(x[-1:]), data_train[0]))
    clf   = DecisionTreeClassifier(random_state=0, min_samples_split=mss, max_depth=md, max_leaf_nodes=mln, criterion=cri, min_samples_leaf=msl)
    clf.fit(indep, dep)
    
    #test the learner
    test_indep = np.array(map(lambda x: np.array(x[:-1]), data_test[0]))
    test_dep   = np.array(map(lambda x: np.array(x[-1:]), data_test[0]))
    t = clf.predict(test_indep)
    
    #tim's abcd
    abcd = Abcd(db=data_test[1][0], rx=data_test[1][1])
    for predicted, actual in zip(t, test_dep):
      abcd.tell(actual[0], predicted)
    abcd.header()
    outputs = abcd.ask()
    
    return outputs
        

class Properties:
    def __init__(self, name, test_file, train_file):
        self.dataset_name = name
        self.training_dataset = train_file
        self.test_dataset = test_file

class xalan25(jmoo_problem):
    def __init__(prob):
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.name = "Xalan2.5"
        prob.properties = Properties(prob.name, "xalan-2.5", ["xalan-2.4"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class xalan26(jmoo_problem):
    def __init__(prob):
        prob.name = "Xalan2.6"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "xalan-2.6", ["xalan-2.4", "xalan-2.5"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class xalan27(jmoo_problem):
    def __init__(prob):
        prob.name = "Xalan2.7"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "xalan-2.7", ["xalan-2.4", "xalan-2.5", "xalan-2.6"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class xerces12(jmoo_problem):
    def __init__(prob):
        prob.name = "Xerces1.2"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "xerces-1.2", ["xerces-init"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class xerces13(jmoo_problem):
    def __init__(prob):
        prob.name = "Xerces1.3"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "xerces-1.3", ["xerces-init", "xerces-1.2"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class xerces14(jmoo_problem):
    def __init__(prob):
        prob.name = "Xerces1.4"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "xerces-1.4", ["xerces-init", "xerces-1.2", "xerces-1.3"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class velocity15(jmoo_problem):
    def __init__(prob):
        prob.name = "Velocity1.5"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "velocity-1.5", ["velocity-1.4"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class velocity16(jmoo_problem):
    def __init__(prob):
        prob.name = "Velocity1.6"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "velocity-1.6", ["velocity-1.4", "velocity-1.5"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class prop2(jmoo_problem):
    def __init__(prob):
        prob.name = "prop-2"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "prop-2", ["prop-1"])
        prob.properties.unusual_range_end = 2
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class prop3(jmoo_problem):
    def __init__(prob):
        prob.name = "prop-3"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "prop-3", ["prop-1", "prop-2"])
        prob.properties.unusual_range_end = 2
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class prop4(jmoo_problem):
    def __init__(prob):
        prob.name = "prop-"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "prop-4", ["prop-1", "prop-2", "prop-3"])
        prob.properties.unusual_range_end = 2
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class prop5(jmoo_problem):
    def __init__(prob):
        prob.name = "prop-5"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "prop-5", ["prop-1", "prop-2", "prop-3", "prop"])
        prob.properties.unusual_range_end = 2
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class prop6(jmoo_problem):
    def __init__(prob):
        prob.name = "prop-6"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "prop-6", ["prop-1", "prop-2", "prop-3", "prop-4", "prop-5"])
        prob.properties.unusual_range_end = 2
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class synapse11(jmoo_problem):
    def __init__(prob):
        prob.name = "synapse-1.1"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "synapse-1.1", ["synapse-1.0"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class synapse12(jmoo_problem):
    def __init__(prob):
        prob.name = "synapse-1.2"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "synapse-1.2", ["synapse-1.0", "synapse-1.1"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class poi20(jmoo_problem):
    def __init__(prob):
        prob.name = "poi-2.0"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "poi-2.0", ["poi-1.5"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class poi25(jmoo_problem):
    def __init__(prob):
        prob.name = "poi-2.5"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "poi-2.5", ["poi-1.5", "poi-2.0"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class poi30(jmoo_problem):
    def __init__(prob):
        prob.name = "poi-3.0"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "poi-3.0", ["poi-1.5", "poi-2.0", "poi-2.5"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

class lucene22(jmoo_problem):
    def __init__(prob):
        prob.name = "lucene-2.2"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "lucene-2.2", ["lucene-2.0"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class lucene24(jmoo_problem):
    def __init__(prob):
        prob.name = "lucene-2.4"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "lucene-2.4", ["lucene-2.0", "lucene-2.2"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class jedit40(jmoo_problem):
    def __init__(prob):
        prob.name = "jedit-4.0"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "jedit-4.0", ["jedit-3.2"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class jedit41(jmoo_problem):
    def __init__(prob):
        prob.name = "jedit-4.1"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "jedit-4.1", ["jedit-3.2", "jedit-4.0"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class jedit42(jmoo_problem):
    def __init__(prob):
        prob.name = "jedit-4.2"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "jedit-4.2", ["jedit-3.2", "jedit-4.0","jedit-4.1"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class jedit43(jmoo_problem):
    def __init__(prob):
        prob.name = "jedit-4.3"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "jedit-4.3", ["jedit-3.2", "jedit-4.0", "jedit-4.1", "jedit-4.2"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class ivy14(jmoo_problem):
    def __init__(prob):
        prob.name = "ivy-1.4"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "ivy-1.4", ["ivy-1.1"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class ivy20(jmoo_problem):
    def __init__(prob):
        prob.name = "ivy-2.0"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "ivy-2.0", ["ivy-1.1", "ivy-1.4"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class forrest07(jmoo_problem):
    def __init__(prob):
        prob.name = "forrest-0.7"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "forrest-0.7", ["forrest-0.6"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class forrest08(jmoo_problem):
    def __init__(prob):
        prob.name = "forrest-0.8"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "forrest-0.8", ["forrest-0.6", "forrest-0.7"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class camel12(jmoo_problem):
    def __init__(prob):
        prob.name = "camel-1.2"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "camel-1.2", ["camel-1.0"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class camel14(jmoo_problem):
    def __init__(prob):
        prob.name = "camel-1.4"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "camel-1.4", ["camel-1.0", "camel-1.2"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class camel16(jmoo_problem):
    def __init__(prob):
        prob.name = "camel-1.6"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "camel-1.6", ["camel-1.0", "camel-1.2", "camel-1.4"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class ant14(jmoo_problem):
    def __init__(prob):
        prob.name = "ant-1.4"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "ant-1.4", ["ant-1.3"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class ant15(jmoo_problem):
    def __init__(prob):
        prob.name = "ant-1.5"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "ant-1.5", ["ant-1.3", "ant-1.4"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class ant16(jmoo_problem):
    def __init__(prob):
        prob.name = "ant-1.6"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "ant-1.6", ["ant-1.3", "ant-1.4", "ant-1.5"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints
    
class ant17(jmoo_problem):
    def __init__(prob):
        prob.name = "ant-1.7"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "ant-1.7", ["ant-1.3", "ant-1.4", "ant-1.5", "ant-1.6"])
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        prob.objectives[0].value = output[0]
        prob.objectives[1].value = output[1]
        prob.objectives[2].value = output[2]
        prob.objectives[3].value = output[3]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints