from _model import *
import sys

class Model:
    def __init__(self,name):
        self.name = name
        if name == 'pom3':
            self.model = Pom()
        elif name == 'xomo':
            self.model = Xomo(model = 'flight')
        elif name == 'xomoflight':
            self.model = Xomo(model='flight')
        elif name == 'xomoground':
            self.model = Xomo(model='ground')
        elif name == 'xomoosp':
            self.model = Xomo(model='osp')
        elif name == 'xomoosp2':
            self.model = Xomo(model='osp2')
        elif name == 'xomoall':
            self.model = Xomo(model='all')
        else:
            sys.stderr.write("Enter valid model name pom3 or xomoflight --> xomo[flight/ground/osp/osp2/all]\n")
            sys.exit()
    
    def trials(self,N,verbose=False):
        #returns headers and rows
        return self.model.trials(N,verbose)

    def update(self,fea,cond,thresh):
        #cond is true when <=
        self.model.update(fea,cond,thresh)

    def __repr__(self):
        return self.name

def p(m,headers,rows):
    print "#"*50,m
    print ">>>>>>","headers"
    print headers
    print ">>>>>","rows"
    print rows

def modeld():
    m = Model('xomoall')
    headers,rows = m.trials(5)
    p(m,headers,rows)
    m = Model('pom3')
    headers,rows = m.trials(5)
    p(m,headers,rows)

if __name__ == '__main__':
    modeld()
