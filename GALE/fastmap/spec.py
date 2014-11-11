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
from Num import *
from Objective import *
from lib import *
from Sym import *

def spec(pos, aSpec,specs,nums,syms,objs, 
         maximze  = The.more, 
         minimize = The.less,
         numeric  = The.num,
         skip     = The.ignore,
         num      = Num):
  if not skip in aSpec:
      specs += [aSpec]
      w1 = aSpec.count(maximze)
      w2 = aSpec.count(minimize)
      name = sub(r"[^_0-9a-zA-Z]", "",aSpec) 
      if  numeric in aSpec : 
        nums  += [num(name,pos)]
      elif w1: 
        objs += [Objective(name,pos,   2**(w1-1))]
      elif w2: 
        objs += [Objective(name,pos,-1*2**(w2-1))] 
      else:      
        syms  += [Sym(name,pos)]