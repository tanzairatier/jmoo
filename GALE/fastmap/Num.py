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

class Num(About) :
  def __init__(i,name,at=0,w=1):
    About.__init__(i,name,at,w)
    i.n   = 0.0 
    i.mu  = i.sigma = i.m2 = 0.0 # m2 used by Knuth
    i.max = The.ninf
    i.min = i.max * -1

  def read(i,x)    : 
     return x if x == The.missing else float(x)

  def delta(i,x,y) : return (x -  y)**2

  def furthest(i,x): 
    return i.max if x <(i.max-i.min)/2 else i.min

  def status(i):
     return ":%s %5.3f +- %5.3f" \
             % (i.name,i.mu,i.sigma)

  def normalize(i,x):
    tmp = float((x - i.min)) / \
                (i.max - i.min + 0.000001)
    if   tmp > 1 : return 1
    elif tmp < 0 : return 0
    else         : return tmp

  def puts(i,l): 
    for x in lst: i.put(x)
    
  

  def put(i,x):
    if x != The.missing:
      i.n    += 1
      delta   = x - i.mu
      i.mu   += delta/i.n
      i.m2   += delta*(x - i.mu)
      i.sigma = (i.m2/i.n)**0.5
      i.max   = max(i.max,x)
      i.min   = min(i.min,x)

  def get(i):
    return normal(i.mu, i.sigma)

  def of(i,x, normalize=True,standardize=False):
    
    if x == The.missing : return i.mu 
    elif normalize   : return i.normalize(x)
    elif standardize : return (x - i.mu)/i.sigma
    else             : return x