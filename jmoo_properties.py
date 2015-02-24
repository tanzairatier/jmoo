
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

from jmoo_algorithms import *
from jmoo_problems import *
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"Problems/tera")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
from tera_datasets import *


# JMOO Experimental Definitions
algorithms = [
              
              jmoo_NSGAII(),
              jmoo_GALE(),
              jmoo_SPEA2()
              
              ]
"""
problems =[ivy14(), ivy20(), jedit40(), jedit41(), jedit42(), jedit43(), 
           lucene22(), lucene24(), poi20(), poi25(), poi30(),
           synapse11(), synapse12(), velocity15(), velocity16(),
           xalan25(), xalan26(), xalan27()]  
"""
#problems = [jedit42(), jedit43(), lucene22(), lucene24()]
#problems = [poi20(), poi25(), poi30(), synapse11()]
#problems = [synapse12(), velocity15(), velocity16(), xalan25()]
#problems = [xalan26(), xalan27(), xalan27(), xalan27()]
problems = [ant14()]


[ant14(), ant15(), ant16(), ant17(),
camel12(), camel14(), camel16(),
forrest07(), forrest08(),
ivy14(), ivy20(),
jedit40(), jedit41(), jedit42(), jedit43(),
lucene22(), lucene24(),
poi20(), poi25(), poi30(),
synapse11(), synapse12(),
velocity15(), velocity16(),
xalan25(), xalan26(), xalan27(),
xerces12(), xerces13(), xerces14()]
    
#[POM3A(), POM3B(), POM3C(), XOMO_flight(), XOMO_osp2(), XOMO_ground(), srinivas(), schaffer(), osyczka2(), water(), bnh(), twobartruss(), viennet2(), dtlz2(5,20)]
"""
A0_test(), A001_test(),
scale_test_similar(), scale_test_dissimilar(),
deceptive1_test(), deceptive2_test(),
bias_test(),
dtlz1(5,2), dtlz1(5, 4),
dtlz2(10,2), dtlz2(10, 4),
dtlz3(10,2), dtlz3(10, 4),
dtlz4(10,2), dtlz4(10, 4),
dtlz5(10,2), dtlz5(10, 4),
dtlz6(20,2), dtlz6(20, 4),
XOMO_flight(), XOMO_ground(), XOMO_osp(), XOMO_osp2(), XOMO_all(),
bnh(), schaffer(), constrex(), golinski(), osyczka2(), srinivas(), tanaka(), twobartruss(),
viennet2(), viennet3(), viennet4(), zdt1(), zdt2(), zdt3(), zdt4(), zdt6(), poloni(), kursawe(3), fonseca(3), water(),
#sbnh(), twobartruss(), osyczka2(), srinivas(), tanaka(), water(),constrex(),
#golinski(), osyczka2(), srinivas(), zdt1(), tanaka(), schaffer(), poloni(), kursawe(3), fonseca(3)
POM3A(), POM3B(), POM3C()
#schaffer()

]
"""


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
