
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
"Representation of Fitness"

class jmoo_fitness:
    def __init__(fit, problem, fitness = None):
        fit.problem = problem
        fit.fitness = fitness
        if fitness:
            weights=[-1.0 if obj.lismore else 1.0 for obj in problem.objectives]
            fit.weightedFitness = (f*w for f,w in zip(fitness,weights))
    def setFitness(fit, fitness):
        fit.fitness = fitness
        weights=[-1.0 if obj.lismore else 1.0 for obj in fit.problem.objectives]
        fit.weightedFitness = (f*w for f,w in zip(fitness,weights))
        
    @property
    def valid(self):
        return not(self.fitness == None)
    
    def __gt__(self, other):
        return not self.__le__(other)
        
    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return self.weightedFitness <= other.weightedFitness

    def __lt__(self, other):
        return self.weightedFitness < other.weightedFitness
    
    def __deepcopy__(self, memo):
        """Replace the basic deepcopy function with a faster one.
        
        It assumes that the elements in the :attr:`values` tuple are 
        immutable and the fitness does not contain any other object 
        than :attr:`values` and :attr:`weights`.
        """
        copy = self.__class__()
        copy.weightedFitness = self.weightedFitness
        return copy