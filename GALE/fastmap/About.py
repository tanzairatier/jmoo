
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

class About(object):
  def put(i,x)     : pass # update 
  def get(i)       : pass # sample
  def of(i,x)      : pass # make x of distribution
  def read(i,x)    : pass # read from string, 
  def status(i)    : pass # this column's summary
  def delta(i,x,y) : pass # difference of  2 things
  def furthest(i,x): pass # a thing very far from x
  def __init__(i,name,pos,w=1): 
     i.name, i.origin, i.at, i.n, i.w = \
      name,  pos,       pos, 0,   w

  def __repr__(i) :
    return ":class %s :name %s :pos %s :w %s" \
         % (type(i).__name__,i.name,i.at,i.w)