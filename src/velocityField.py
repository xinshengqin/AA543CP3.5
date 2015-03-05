#!/usr/bin/python
import numpy as np
import sys
from mesh import *


class velocityField(object):

    def __init__(self, mesh, IC,IC_para1,IC_para2, BC='periodic',u_xmin=None,u_xmax=None):
        #IC should be a function object that can compute initial condition at t = 0, given relative position in 1D mesh.
        #BC should be a string indicating the BC type. It should be one from 'periodic','dirichlet','neumann'. 
        #If 'dirichlet' BC is shosen, u_xmin and u_xmax should be specified as the constant value at boundary.
        self.mesh=mesh
        self.u_xmin=u_xmin
        self.u_xmax=u_xmax
        self.u0=[]#note finally u will be a list who has 2 more elements than self.mesh

        #apply IC

        for i in range(len(mesh.coordinates)):

            ui=IC(mesh.startPoint,mesh.endPoint,IC_para1,IC_para2,mesh.coordinates[i])

            self.u0.append(ui)

        self.BC=BC

        if BC=='periodic':
            self.u0.insert(0,self.u0[-1])
            self.u0.append(self.u0[1])
        elif BC=='dirichlet':
            self.u0.insert(0,u_xmin)
            self.u0.append(u_xmax)
        elif BC=='neumann':
            self.u0.insert(0,self.u0[0])#du/dx=0 on boundary
            self.u0.append(self.u0[-1])
        else:
            print "Wrong input for choosing BC. Program exit."
            sys.exit()
        self.mx=len(self.u0)#number of grid points, include ghost points
        self.u=np.array(self.u0,ndmin=2)
            
    def applyBC(self,i):#apply BC to velocity field at time step i. i start from 0 
        if self.BC=='periodic':
            self.u[i,self.mx-1]=self.u[i,1]
            self.u[i,0]=self.u[i,self.mx-2]
        elif self.BC=='dirichlet':
            self.u[i,self.mx-1]=self.u_xmax
            self.u[i,0]=self.u_xmin
        elif self.BC=='neumann':
            self.u[i,self.mx-1]=self.u[i,self.mx-2]
            self.u[i,0]=self.u[i,1]
        else:
            print "Wrong input for choosing BC. Program exit."
            sys.exit()


   
    def plot_pointVsIndex(self):
        index = np.linspace(1,len(self.mesh.coordinates),len(self.mesh.coordinates))

        plt.figure()
        plt.plot(index,self.mesh.coordinates,'ro-')
        plt.xlabel('index i')
        plt.ylabel('point coordinate')
        plt.savefig('pointVsIndex.png', bbox_inches='tight')
        plt.close()

    def plot_gapSpaceVsIndex(self):
        index = np.linspace(1,len(self.mesh.coordinates)-1,len(self.mesh.coordinates)-1)

        plt.figure()
        plt.plot(index,self.mesh.gapSpaceDistribution,'ro-')
        plt.xlabel('index i')
        plt.ylabel('gap space after between point i and i+1')
        plt.savefig('gapSpaceVsIndex.png', bbox_inches='tight')
        plt.close()

    def plot_uVsIndex(self):
        index = np.linspace(0,len(self.mesh.coordinates)+1,len(self.mesh.coordinates)+2)

        plt.figure()
        plt.plot(index,self.u0,'ro-')
        plt.xlabel('index i')
        plt.ylabel('velocity u')
        plt.savefig('velocityVsIndex.png', bbox_inches='tight')
        plt.close()
        
    def plot_uVsX(self,i,filename):
        i=int(i)
        x=self.mesh.coordinates
        u=self.u[i,1:-1]#truncate the left-most and right-most ghost cell

        plt.figure()
        plt.plot(x,u,'ro-')
        plt.xlabel('x')
        plt.ylabel('velocity u')
        plt.savefig(filename+'.png', bbox_inches='tight')
        plt.close()
        




def IC_gaussian(xmin,xmax,xpeak,width,x):
    return ( 1+np.exp(-10/width*pow(((x-xpeak)*(xmax+xmin)/(xmax-xmin)),2)))
def IC_stepFunction(xmin,xmax,xpeak,width,x):
    center=0#default center coordinate of the step function is 0
    if x<xmin or x>xmax:
        return 0
    elif x<(center-float(width)/2) or x>(center+float(width)/2):
        return 0
    else:
        return float(xpeak) 
