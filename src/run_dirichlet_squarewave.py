#!/usr/bin/python
import numpy as np
from velocityField import *
from mesh import *
from linear_advection_solver import *

mesh1=mesh(-1,1,101)#Three arguments are xmin of grid, xmax of grid, number of grid points.
velocityField1 = velocityField(mesh1,IC_stepFunction,1,0.4,'dirichlet',0,0)#Arguments are mesh object, initial condition function ( for now, two options can
a=0.5
tfinal=3
nsteps=94
LaxWendroff(a,velocityField1,tfinal,nsteps,'./dirichlet_squarewave')
#velocityField1.plot_uVsX(nsteps,'./plots/')
#velocityField1.plot_uVsX(nsteps/2.0,'u_half')
