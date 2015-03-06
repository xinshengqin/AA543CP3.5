#!/usr/bin/python
import numpy as np
from velocityField import *
from mesh import *
from solver_1d import *
import math

#mesh1=mesh(0,1,101)#Three arguments are xmin of grid, xmax of grid, number of grid points.
#velocityField1 = velocityField(mesh1,IC_gaussian,0.2,0.1,'periodic',0,0)#Arguments are mesh object, initial condition function ( for now, two options can
#cfl_desire = 0.9
#tfinal=3
#nsteps=100
#nonlinear_solver(velocityField1,tfinal,cfl_desire,flux_function_burger,'output_burger')
#nonlinear_solver(velocityField1,tfinal,cfl_desire,flux_linear,'output_burger')


def problemB():
    mesh1 = mesh(-1*math.pi,math.pi,101)
    velocityField1 = velocityField(mesh1,IC_sin,1,1,'periodic',0,0)
    cfl_desire = 0.9
    tfinal=3
    
    if not('output_problemB' in os.listdir('./')):
        os.mkdir('output_problemA')
    mu=0.001
    nonlinear_solver(velocityField1,tfinal,cfl_desire,flux_function_burger,mu,'output_problemB')

def problemC1():
    mesh1 = mesh(-1*math.pi,math.pi,101)
    velocityField1 = velocityField(mesh1,IC_sin,-1,1,'dirichlet',0,0)
    cfl_desire = 0.9
    tfinal=1.5
    
    if not('output_problemC1' in os.listdir('./')):
        os.mkdir('output_problemC1')
    mu=0.001
    nonlinear_solver(velocityField1,tfinal,cfl_desire,flux_function_burger,mu,'output_problemC1')

def problemC2():
    mesh1 = mesh(-1*math.pi,math.pi,101,5,0)
    velocityField1 = velocityField(mesh1,IC_sin,-1,1,'dirichlet',0,0)
    cfl_desire = 0.9
    tfinal=1.5
    
    if not('output_problemC2' in os.listdir('./')):
        os.mkdir('output_problemC2')
    mu=0.001
    nonlinear_solver(velocityField1,tfinal,cfl_desire,flux_function_burger,mu,'output_problemC2')

#problemB()
#problemC1()
problemC2()
