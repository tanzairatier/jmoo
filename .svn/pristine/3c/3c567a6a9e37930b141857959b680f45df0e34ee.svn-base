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

class BinaryTree(object):
   def __init__(i):
     i.n, i.rhs, i.lhs = 0, None, None

   def isLeaf(i) : 
     return not i.rhs and not i.lhs

   def leaves(i) : 
     return [x for x in i.nodes() if x.isLeaf()]
 
   def nonPrunedLeaves(i):
       return [x for x in i.nodes() if (x.isLeaf() and x.abort == False)]
   
   def prunedLeaves(i):
       return [x for x in i.nodes() if (x.isLeaf() and x.abort == True)]

   def nodes(i,all=None):
     if not all: all=[]
     all += [i]
     for x in [i.lhs,i.rhs]: 
       if x: x.nodes(all)
     return all
           
   def show(i, s, tab = 0, pad = "|  ", pre = ""):
     #print (pad * tab) + pre, i
     s = str((pad*tab)) + str(pre) + str(i) + "\n"
     if i.lhs: 
        s += i.lhs.show(s, tab = tab + 1, pad=pad, pre=">")
     if i.rhs: 
        s += i.rhs.show(s, tab = tab + 1, pad=pad, pre="<")
     return s
   