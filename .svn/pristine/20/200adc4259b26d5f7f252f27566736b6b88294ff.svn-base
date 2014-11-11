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

from The import *
from lib import *
from math import *

def all(headers,row1,row2):
  for h in headers:
    yield h, row1.cells[h.at], row2.cells[h.at]
    
class Row(object):
  id = 0
  def __init__(i,t,cells):
    i.id = Row.id = Row.id + 1
    i.table, i.cells = t,cells
  def __cmp__(i1,i2) : return i1.id - i2.id

  def mutate(i,p=0.33):
    out = i.cells.copy
    for x in i.table.headers.nums:
      if any(0,1) < p:
         out[x.pos] = i.cells[x.pos] 
    return out
 
  def distance(i1,i2,nums=True,syms=True,
                    objs=False, gone=The.missing):
    d =  n = 0.0
    def aha91(headers,d,n):
       for  h,x,y in all(headers,i1,i2):
         # handle missing values
         if x == y == gone : continue
         if x == gone      : x = h.furthest(y)
         if y == gone      : y = h.furthest(x)
         # normalize everything 0..1
         x1 = h.of(x,True)
         y1 = h.of(y,True)
         # weight distance calculation
         d += h.w * h.delta(x1,y1)
         n += h.w
       return d,n
    if nums: d,n = aha91(i1.table.nums,d,n)
    if syms: d,n = aha91(i1.table.syms,d,n)
    if objs: d,n = aha91(i1.table.objectives,d,n)
    return d**0.5/n**0.5
    #return (sum([h.delta(x,y) for h,x,y in all(i1.table.nums,i1, i2)])**0.5) #euclidean hard and dumb

  def closest(i1, init= The.inf, better = less):
    delta,out = init, None
    for i2 in i1.table.rows:
      if i2 != i1:
        tmp = i1.distance(i2)
        if better(tmp, delta):
           delta,out = tmp,i2
    return out 

  def furthest(i): return i.closest(The.ninf,more)