
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
"Representation of a 'Candidate' or 'Individual'"

from jmoo_fitness import *

class jmoo_individual:
    def __init__(ind, problem, decisionValues, fitness = None):
        ind.problem = problem
        ind.decisionValues = decisionValues
        ind.fitness = jmoo_fitness(problem, fitness=fitness)
    def evaluate(ind):
        if ind.fitness: 
            ind.fitness.setFitness( ind.problem.evaluate(ind.decisionValues) )
        else: 
            ind.fitness = jmoo_fitness(ind.problem)
            ind.fitness.setFitness( ind.problem.evaluate(ind.decisionValues) )       
    @property
    def valid(self):
        if self.fitness == None: return False
        else: return self.fitness.valid