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

def nonlinear_solver(velocityField,tfinal,cfl,flux_function,mu=0.001,output_path='./plots'):
    #discretized eq: (u^n+1_j-u^n_j)/dt = (f^n+_j-f^n+_j-1)/dx + (f^n-_j+1-f^n-_j)/dx = mu*uxx
    #R.H.S is discretized using eq 3.9 in the notes
    dx = velocityField.mesh.minimumDeltaX#This is in fact the minimum grid space
    a = 1#assume a = 1 since u = sin(x), which has a maximum value of 1
    dt = float(cfl)*dx/a
    nsteps = int(float(tfinal)/dt)
    output_interval = 5#every outptu_interval time steps, it will write result
    print "minimum dx = %g,  dt = %g" % (dx,dt)

    
    flag = 0
    velocityField.plot_uVsX(0, output_path+'/'+'timestep='+str(0+1))
    for n in range(0,nsteps):
        un=np.zeros(velocityField.mesh.numberOfPoints+4)
        fplus = np.zeros(velocityField.mesh.numberOfPoints+4)
        fminus = np.zeros(velocityField.mesh.numberOfPoints+4)
        x = np.array(velocityField.mesh.coordinates)
        for i in range(0,velocityField.mesh.numberOfPoints+4): #compute fplus_j and fminux_j
            fplus[i] = max(0,flux_function(velocityField.u[n,i]))
            fminus[i] = min(0,flux_function(velocityField.u[n,i]))
        for i in range(2,velocityField.mesh.numberOfPoints+2):#compute u
            un[i] = velocityField.u[n,i]+dt*(mu/(x[i+1]-x[i])*((velocityField.u[n,i+1]-velocityField.u[n,i])/(x[i+1]-x[i])-(velocityField.u[n,i]-velocityField.u[n,i-1])/(x[i]-x[i-1]))-(fplus[i]-fplus[i-1])/(x[i]-x[i-1]) - (fminus[i+1]-fminus[i])/(x[i+1]-x[i]))

        velocityField.u=np.vstack([velocityField.u,un])

        velocityField.applyBC(n+1)

        flag = flag + 1
        if flag >= output_interval:
            velocityField.plot_uVsX(n+1, output_path+'/'+'timestep='+str(n+1))
            flag = 0


    return True 

def flux_function_burger(u):
    return 0.5*u*u
def flux_linear(u):
    return 1*u
