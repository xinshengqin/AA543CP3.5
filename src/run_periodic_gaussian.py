#!/usr/bin/python
import numpy as np
from velocityField import *
from mesh import *
from linear_advection_solver import *

mesh1=mesh(0,1,101)#Three arguments are xmin of grid, xmax of grid, number of grid points.
velocityField1 = velocityField(mesh1,IC_gaussian,0.2,0.1,'periodic',0,0)#Arguments are mesh object, initial condition function ( for now, two options can
a=0.5
tfinal=3
nsteps=194
LaxWendroff(a,velocityField1,tfinal,nsteps,'./periodic_gaussian')
#velocityField1.plot_uVsX(nsteps,'./plots/')
#velocityField1.plot_uVsX(nsteps/2.0,'u_half')
