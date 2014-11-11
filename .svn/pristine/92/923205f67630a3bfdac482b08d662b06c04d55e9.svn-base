
"""
##########################################################
### @Author Joe Krall      ###############################
### @copyright see below   ###############################

    This file is part of JMOO,
    Copyright Joe Krall, 2014.

    JMOO is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    JMOO is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with JMOO.  If not, see <http://www.gnu.org/licenses/>.
    
###                        ###############################
##########################################################
"""

"Brief notes"
"Representation of a Decision"
  
class jmoo_decision:
    "representation of a decision"
    
    def __init__(dec,name,low,up):
        dec.name = name             # name of decision
        dec.low = low               # lower bound
        dec.up = up                 # upper bound
        
    def normalize(dec, x):
        "return a normalized value between 0 and 1"
        tmp = float(x  - dec.low) / (dec.up - dec.low + 0.000001)
        if tmp > 1: return 1
        elif tmp < 0: return 0
        else: return tmp
    
