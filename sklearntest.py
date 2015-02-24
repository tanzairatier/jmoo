import csv
from sklearn import tree
import numpy as np
from sklearn.tree import DecisionTreeClassifier


import sys
sys.dont_write_bytecode = True

class Abcd: 
  def __init__(i,db="all",rx="all"):
    i.db = db; i.rx=rx;
    i.yes = i.no = 0
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
  def header(i):
    print "#",('{0:20s} {1:11s}  {2:4s}  {3:4s} {4:4s} '+ \
                     '{5:4s}{6:4s} {7:3s} {8:3s} {9:3s} '+ \
           '{10:3s} {11:3s}{12:3s}{13:10s}').format(
      "db", "rx", 
     "n", "a","b","c","d","acc","pd","pf","prec",
      "f","g","class")
    print '-'*100
  def ask(i):
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
      print "#",('{0:20s} {1:10s} {2:4d} {3:4d} {4:4d} '+ \
                '{5:4d} {6:4d} {7:4d} {8:3d} {9:3d} '+ \
         '{10:3d} {11:3d} {12:3d} {13:10s}').format(i.db,
          i.rx,  n(b + d), n(a), n(b),n(c), n(d), 
          p(acc), p(pd), p(pf), p(prec), p(f), p(g)," " + str(x))
      return acc, pd, pf, prec
      

def readDataset(file):
    finput = open(file, 'rb')
    reader = csv.reader(finput, delimiter=',')
    dataread = []
    for i,row in enumerate(reader):
        if i > 0: #ignore header row
            line = []
            for item in row:
                try:
                    line.append(float(item))
                except:
                    pass
            dataread.append(np.array(line))
    properties = row[:2]
    print properties
    return np.array(dataread), properties


#### xalan
data_train = readDataset("tera/xalan-2.4.csv")
data_test = [readDataset("tera/xalan-2.5.csv"),
             readDataset("tera/xalan-2.6.csv"),
             readDataset("tera/xalan-2.7.csv"),]

#train the learner
indep = np.array(map(lambda x: np.array(x[:-1]), data_train[0]))
dep   = np.array(map(lambda x: np.array(x[-1:]), data_train[0]))
clf   = DecisionTreeClassifier(random_state=0, min_samples_split=100)
clf.fit(indep, dep)

#test the learner
for test in data_test:
    test_indep = np.array(map(lambda x: np.array(x[:-1]), test[0]))
    t = clf.predict(test_indep)

    #joe's correctness
    correct = 0
    for guess,truth in zip(t, dep):
        if guess==truth[0]:
            correct += 1
    print "Correctness: " + str("%.1f" % (100*correct/float(len(t)))) + "%"

    #tim's abcd        
    abcd = Abcd(db=test[1][0], rx=test[1][1])
    for predicted, actual in zip(t, dep):
      abcd.tell(actual[0], predicted)
    abcd.header()
    abcd.ask()
        
        
        
        
        
        
        
        
        
        




    
    

