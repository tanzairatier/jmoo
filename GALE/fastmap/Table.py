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

from spec import *
from Row import *
#from cluster1d import *
from pprint import pprint

def more(x,y): return x > y
def less(x,y): return x < y

class Table(object):
  def __init__(i,specs,data=[]):
    i.rows = []
    i.specs = []
    i.objectives, i.nums, i.syms = [], [], []
    for pos,aSpec in enumerate(specs):
      spec(pos,aSpec,i.specs,i.nums, i.syms, i.objectives)
    i.headers= i.nums + i.syms + i.objectives
    for pos,h in enumerate(i.headers): h.at = pos
    i.n = len(i.headers)
    i.puts(data)

  def puts(i,data):
    for cells in data:
       i.put(cells)

  def put(i,cells):
    for h in i.headers:
       h.put(cells[h.at])
    i.rows += [Row(i, cells)]

  def read(i,rawData): 
    return [h.read(rawData[h.origin]) 
           for h in i.headers]

  def status(i):
    return ', '.join([obj.status() for obj 
                      in i.objectives])
  def clone(i,data=[]):
    return Table(i.specs,data)

class Table2:
  def __init__(self,skipClass=True) :
    self.data=[]
    self.skipClass= skipClass
  def slurp(self,file):
    for n,row in rows(file,-1):
      self.header(row) if n==0 else self.cells(row)
    self.complete()
    return self
  def complete(self):
    self.discretizeColumns()
  def header(self,names) :
    self.names = names
    self.nums=[]; self.syms=[];
    for i,head in enumerate(names):
      self.klass=i
      (self.nums if "$" in head else self.syms).append(i)
  def cells(self,cells) :
    for col in self.nums: 
      if cells[col] != '?':
        cells[col] = float(cells[col])
    self.data.append(cells)   
  def discretizeColumns(self):
    cols= zip(*self.data)
    for col in self.nums:
      if col != self.klass:
        cols[col] = self.discreteColumn(cols[col])
      else:
        if not self.skipClass:
          cols[col] = self.discreteColumn(cols[col])
    self.data = zip(*cols)
  def discreteColumn(self,nums):
    ranks = divlist(nums,cohen=0.2,minObs=4,accept=lambda x: x != "?")
    return [self.discreteNumber(x,ranks) for x in nums] 
  def discreteNumber(self,x,ranks) :
    #return x if x == "?" else ranks[x].rank
    return x if x == "?" else ranks[x].mu()