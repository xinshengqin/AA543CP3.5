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
    
    un=np.zeros(velocityField.mesh.numberOfPoints+4)
    for n in range(0,nsteps):
        for i in range(2,velocityField.mesh.numberOfPoints+2):
            un[i]=velocityField.u[n,i]-udtdx*(velocityField.u[n,i+1]-velocityField.u[n,i-1])/2+pow(udtdx,2)*(velocityField.u[n,i+1]-2*velocityField.u[n,i]+velocityField.u[n,i-1])/2

        velocityField.u=np.vstack([velocityField.u,un])

        velocityField.applyBC(n+1)

        velocityField.plot_uVsX(n+1, output_path+'/'+'timestep='+str(n+1))

    return True 

def nonlinear_solver(velocityField,tfinal,cfl,flux_function,output_path='./plots'):
    dx = velocityField.mesh.minimumDeltaX#This is in fact the minimum grid space
    a = 1#assume a = 1 since u = sin(x), which has a maximum value of 1
    dt = float(cfl)*dx/a
    nsteps = int(float(tfinal)/dt)
    mu = 0.1#viscosity
    print "minimum dx = %g,  dt = %g" % (dx,dt)

    un=np.zeros(velocityField.mx)
    
    for n in range(0,nsteps):
        fplus = np.zeros(velocityField.mx)
        fminus = np.zeros(velocityField.mx)
        for i in range(0,mx): #compute fplus_j and fminux_j
            fplus[j] = max(flux_function(u(n,i)))
            fminus[j] = min(flux_function(u(n,i)))
        for i in range(1,velocityField.mx-1):#compute u
            #un[i]=velocityField.u[n,i]-udtdx*(velocityField.u[n,i+1]-velocityField.u[n,i-1])/2+pow(udtdx,2)*(velocityField.u[n,i+1]-2*velocityField.u[n,i]+velocityField.u[n,i-1])/2
            #un[i] = 
            pass

        velocityField.u=np.vstack([velocityField.u,un])

        velocityField.applyBC(n+1)

        velocityField.plot_uVsX(n+1, output_path+'/'+'timestep='+str(n+1))

    return True 

def flux_function_burger(u):
    return 0.5*u*u
