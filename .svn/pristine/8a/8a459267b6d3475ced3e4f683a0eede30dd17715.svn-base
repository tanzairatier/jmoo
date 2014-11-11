
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
"Representation of an Objective"
   
class jmoo_objective:
    "representation of an objective"
    
    def __init__(obj,name,lismore,low=None,up=None):
        obj.name = name                 # name of objective
        obj.lismore = lismore           # optimization direction.  lismore = less is more = true if minimize
        obj.low = low                   # lower bound if any; set to none if unknown
        obj.up = up                     # upper bound if any; set to none if unknown