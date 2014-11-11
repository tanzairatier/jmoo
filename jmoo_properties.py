
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
"Property File.  Defines default settings."

import jmoo_algorithms as MOEAS
from jmoo_problems import *


# JMOO Experimental Definitions
algorithms = [
              
              #MOEAS.jmoo_NSGAII(),
              MOEAS.jmoo_GALE(), 
              #MOEAS.jmoo_SPEA2()
              
              ]

problems = [
            
            fonseca(3)
            #POM3B()
            #POM3A(), POM3B(), POM3C()#, POM3D()
            #srinivas(), zdt1(), osyczka2(), viennet2(), tanaka(), schaffer(), golinski(), POM3A(), POM3B(), POM3C(), POM3D()
            
            ]
build_new_pop = False                                       # Whether or not to rebuild the initial population



# JMOO Universal Properties
repeats = 20    #Repeats of each MOEA
MU      = 100   #Population Size
PSI     = 20    #Maximum number of generations

# Properties of GALE
GAMMA   = 0.15  #Constrained Mutation Parameter
EPSILON = 1.00  #Continuous Domination Parameter
LAMBDA =  3     #Number of lives for bstop

# File Names
DATA_PREFIX        = "data/"

"decision bin tables are a list of decisions and objective scores for a certain model"
DECISION_BIN_TABLE = "decision_bin_table"

"result scores are the per-generation list of IBD, IBS, numeval,scores and change percents for each objective - for a certain model"
RESULT_SCORES      = "result_"

SUMMARY_RESULTS    = "summary_"

RRS_TABLE = "RRS_TABLE_"
DATA_SUFFIX        = ".datatable"
