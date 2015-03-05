#!/usr/bin/python
from velocityField import * 
from mesh import * 

def testProblem1():

    mesh2=mesh(-1,1,41)#Three arguments are xmin of grid, xmax of grid, number of grid points.
    velocity2 = velocityField(mesh2,IC_stepFunction,1,0.4,'neumann')#Arguments are mesh object, initial condition function ( for now, two options can
#be chosen, one is IC_stepFunction, another is IC_gaussian), peak value for step function( or centered point for gaussian function),
#width for step function(or width for gaussian function), BC(for now, three options are available, one is 'periodic', one is 'neumann',
#another is 'dirichlet', in which case two more arguments to specify u_min and u_max is required) .
    
    #These method will create corresponding *.png files in current folder. 
    velocity2.plot_uVsIndex()
    velocity2.plot_gapSpaceVsIndex()
    velocity2.plot_pointVsIndex()
    velocity2.plot_uVsX()
    print velocity2.u



def testProblem2():
    mesh1=mesh(0,1,51,5,0.2)
    velocity1 = velocityField(mesh1,IC_gaussian,0.2,0.1,'periodic')
    velocity1.plot_uVsIndex()
    velocity1.plot_gapSpaceVsIndex()
    velocity1.plot_pointVsIndex()
    velocity1.plot_uVsX()

#testProblem2()

testProblem1()

            
    

