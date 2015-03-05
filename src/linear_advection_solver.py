#!/usr/bin/python
import numpy as np
from velocityField import *
from mesh import *

def LaxWendroff(a,velocityField,tfinal,nsteps,output_path='./plots'): #u should be an object of velocityField class and must has initial value at t=0
    dt = float(tfinal)/nsteps
    dx = velocityField.mesh.minimumDeltaX#This is in fact the minimum grid space
    udtdx = float(a) * dt / dx
    cfl = abs(udtdx)
    print "dx = %g,  dt = %g" % (dx,dt)
    print "Courant number is ",cfl
    
    un=np.zeros(velocityField.mx)
    for n in range(0,nsteps):
        for i in range(1,velocityField.mx-1):
            un[i]=velocityField.u[n,i]-udtdx*(velocityField.u[n,i+1]-velocityField.u[n,i-1])/2+pow(udtdx,2)*(velocityField.u[n,i+1]-2*velocityField.u[n,i]+velocityField.u[n,i-1])/2

        velocityField.u=np.vstack([velocityField.u,un])

        velocityField.applyBC(n+1)

        velocityField.plot_uVsX(n+1, output_path+'/'+'timestep='+str(n+1))

    return True 






