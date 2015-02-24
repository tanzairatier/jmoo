
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
"Just a simple way to find out MOP runtimes"

#from jmoo_problems import *
from jmoo_properties import *
import time


runtimes = []

print "Model Name".ljust(14) + ", " + "   Min.".ljust(10) + "," + "   Avg.".ljust(10) + "," + "   Med.".ljust(10) + "," + "   Max.".ljust(10) + "," + "   Var.".ljust(10)   
for problem in problems:
    runtimes.append([])
    for n in range(1000):
        start = time.time()
        problem.evaluate(problem.generateInput())
        end = time.time()
        runtimes[-1].append((end-start)*1000)
    # "(Min, Avg, Med, Max, Var)"
    # Reporting Milliseconds
    pname = problem.name + "-d" + str(len(problem.decisions)) + "-o" + str(len(problem.objectives))
    print pname.ljust(14) + ", " + str("%10.5f" % min(runtimes[-1])) + "," + str("%10.5f" % avg(runtimes[-1])) + "," + str("%10.5f" % getPercentile(runtimes[-1], 50)) + "," + str("%10.5f" % max(runtimes[-1])) + "," + str("%10.5f" % var(runtimes[-1]))
    
    