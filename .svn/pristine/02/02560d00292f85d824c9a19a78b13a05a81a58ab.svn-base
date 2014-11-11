"""
    This file is part of GALE,
    Copyright Joe Krall, 2014.

    GALE is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GALE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with GALE.  If not, see <http://www.gnu.org/licenses/>.
"""

# Python library routines
# Search-based software: cs791i@wvu.fall12
# tim@menzies.us

""""

Demos and Tests
===============

Demos
-----

The library codes has code that lets us implement a set of *demos* that can show off particular features. The functions inclded in the demos
will be marked with `@demo`; for example:

    @demo
    def demoed() : print "I am a demo"

"""

def demo(f=None,demos=[]): 
  if f: demos.append(f); return f
  for d in demos: 
    print '\n--|',d.func_name,'|','-'*40,'\n',d.__doc__,'\n'
    d()

"""

Tests
-----

Also, the library also supports  test functions that return a list of pairs `[(got,want)]` and the test is passed in `got==want`.

    @test
    def tested(): 
      thing = 22
      return [(22,thing),  # multiple test results can be returned
              (False, type thing = float)]

"""

def test(f=None,tests=[]): 
  if f: tests.append(f); return f
  ok=no=0
  for t in tests: 
    print "#",t.func_name + ': ',t.__doc__
    for n,(want,got) in  enumerate(t()):
      if want == got:
        ok += 1; print "CORRECT:",t.func_name,'question', n+1
      else:
        no += 1; print "WRONG  :",t.func_name,'question',n+1
  if tests:
    print '\n# Final score = %s/%s = %s%% CORRECT' \
            % (ok,(ok+no),round(100*ok/(ok+no)))

""""

In Use
------

All those  demos and all the tests can be exercised as follows:

    python moo.py -i 'demos()'
    python moo.py -i 'tests()'


"""


def tested1():
  "Test functions return lists of (want,got) pairs"
  return [(1,1),
          (True,type(1) == int),
          (False,type(1) == float)]


def tested2():
  "Test that the test code can catch a failure."
  return [(0,1)]


"""

Note that one test suite item will fail 
(just to test that the test suite can catch failing code) so the number of
correct tests is never  100%.

Math Stuff
==========

""" 

import math

def more(x,y): return x > y
def less(x,y): return x < y

def normd(d):
  sum,out = 0,{}
  for k in d : sum += d[k]
  for k in d : out[k] = round(100*d[k]/sum)
  return out

"""

Random Stuff
------------

"""

import random
any = random.uniform
normal= random.gauss
seed  = random.seed

def sometimes(p) : 
  "Returns True at probability 'p;"
  return p > any(0,1)

def one(lst): 
  "Returns one item in a list, selected at random"
  return lst[  int(any(0,len(lst) - 1)) ]

def some(lst,p)  : 
  "Returns 'p'% of a list,selected at random."
  return [x for x in lst if sometimes(p)]

"""

String Stuff
===========

"""

import re,string,sys

sub=re.sub
ljust=string.ljust

def say(x) : sys.stdout.write(x); sys.stdout.flush()
"""

File Stuff
==========

"""

def lines(file, n=0, bad=r'["\' \t\r\n]',sep=',',shuffle=False) :
  if shuffle:
    all = [line for line in open(file,'r')]
    head = all[0]
    data = all[1:]
    random.shuffle(data)
    for line in [head] + data:
      n += 1
      yield sub(bad,"",line).split(sep),n 
  else: 
    for line in open(file,'r') :
      n += 1
      yield sub(bad,"",line).split(sep),n 

"""

Histogram Stuff
================

"""
        
def histogram(lst, decimals=2):
  d = {}
  r = 10**decimals
  for x in lst:
    x= int(x) if decimals==0 else math.ceil(x * r) / r
    d[x] = d.get(x,0) + 1
  return d

def printh(h,shrink=1,header=None,pre="") :
  if header: print header 
  for key in h: 
    print pre+ (str(key).rjust(5)), \
        str(h[key]).rjust(5),\
        '*' * (h[key]/shrink)

@demo
def histogramed():
   "What histogram is seen in 1000 samples of a normal(10,2) curve?"
   printh(histogram([round(normal(10,2)) for x in range(1000)]),
          shrink=10)
   
   
def rows(file, n=0, bad=r'["\' \t\r\n]',sep=',') :
  for line in open(file,'r') :
    n += 1
    line = re.sub(bad,"",line).split(sep)
    if line: yield n,line

class Deep(dict) :
  def __getitem__(self,x) :
    if x in self: return self.get(x)
    new = self[x] = Deep()
    return new
  def push(self,k,v) :
    all = self[k] if k in self else []
    all.append(v)
    self[k]=all
    return all
  def at(self,lst,default=None) :
    here=self
    for key in lst:
      if not key in here:
        return default
      here = here[key]
    return here
  def inc(self,k,n=1):
    new = (self[k] if k in self else 0) + n
    self[k] = new
    return new     