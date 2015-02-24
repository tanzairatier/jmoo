from jmoo_properties import *

MUS = [20,40,60,80,100,120,140,160,180,200,220,240,260,300,320,340,360,380,400]


for somemu in MUS:
    
    MU = somemu

    for problem in problems:
        initialPopulation(problem, MU)
        
    # Wrap the tests in the jmoo core framework
    tests = jmoo_test(problems, algorithms)
    
    # Define the reports
    reports = []
    
    # Associate core with tests and reports
    core = JMOO(tests, reports)
    
    # Perform the tests
    core.doTests()