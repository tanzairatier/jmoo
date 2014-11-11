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

class The():
  # discretization contol
  bins    = 5       # number of bins      
  binsMin = 20      # when to start discretization
  
  # recursion control: 
  alpha           = 1.0  # prunes data in recursion
  allowDomination = True # enables sub-tree pruning

  # misc
  inf     =  10**32 # largest known number
  ninf    = -10**32 #  smallest number known 
  
  # cell marker: for missing values
  missing = "?"    
  
  # column header markers
  more    = ">"     # objective to MINIMZE
  less    = "<"     # objective to MAXIMIZE
  num     = "$"     # numerics
  ignore  = "~"     # column to ignore
  
def rstop(t): return  (len(t.rows)**0.5)
def stop(default): return default #return False