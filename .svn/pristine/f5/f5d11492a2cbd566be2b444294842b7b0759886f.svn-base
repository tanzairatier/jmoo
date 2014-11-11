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

from About import *
from lib import *

class Sym(About):
  def __init__(i,name,at=0): 
     About.__init__(i,name,at)
     i.counts = {}; i.mostOften=0;  i.mode=None
     i.n=0; i.sorted=[]

  def read(i,x)    : return x
  def delta(i,x,y) : return 0 if x == y else 1
  def furthest(i,x): return "SoMEcrazyTHing"
  def status(i)    : return ":%s %s"%(i.name,i.mode)

  def put(i,x):
     if x != The.missing:
       i.sorted=[]
       i.n += 1
       old = i.counts.get(x,0) #default old value=0
       new = i.counts[x] = old + 1
       if new > i.mostOften:   
          i.mostOften, i.mode = new, x

  def get(i) :
     if not i.sorted:
        i.sorted = sorted(i.counts.items(), 
                          key = lambda x: -1 * x[1])
     r = any(0,i.n)
     sofar  = 0
     for x,count in i.sorted:
       sofar += count
       if sofar > r: return x

  def of(i,x,normalize=True): 
     return i.mode if x == The.missing else x