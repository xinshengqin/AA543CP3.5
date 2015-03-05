#!/usr/bin/python
import sys
import matplotlib.pyplot as plt
import numpy

class mesh(object):
    def __init__(self, xmin, xmax, n, ratio = None, xclusteredPoint = None):
        #The four input arguments are coordinates of left end point, coordinates of right end point,
        #number of points and the ratio of maximum grid spacing to minimum grid spacing.
        self.startPoint = float(xmin)
        self.endPoint = float(xmax)
        if type(n) != int:
            print "The number of points is not an integer. Please modify the input."
            sys.exit()
        else:
            self.numberOfPoints = n
        #Create uniform mesh
        if ratio == None:
            self.Nonuniform = False 
            self.coordinates,self.gapSpaceDistribution = self.createUniformMesh()
            self.minimumDeltaX=self.gapSpaceDistribution[0]
        #Create nonuniform mesh
        elif ratio != None and xclusteredPoint != None:
            self.Nonuniform = True
            self.ratio = float(ratio)
            if xclusteredPoint < self.startPoint or xclusteredPoint > self.endPoint:
                print "The specified clustered point is out of range. Please modify the input."
                sys.exit()
            else:
                self.xclusteredPoint = float(xclusteredPoint)
            self.n1 = int((self.xclusteredPoint-self.startPoint)/(self.endPoint-self.startPoint)*self.numberOfPoints) #Number of grid points to the left of
            #cluster point
            self.n2 = self.numberOfPoints - self.n1
            self.nmax = max(self.n1,self.n2)
            self.b = (2*self.nmax-3*self.ratio-1)/(self.ratio-1)
            self.coordinates, self.gapSpaceDistribution, self.minimumDeltax= self.createNonuniformMesh()
        else:
            print "Wrong input."


    def createUniformMesh(self):
        print "Creating uniform Mesh"
        delta_x = (self.endPoint - self.startPoint)/(self.numberOfPoints-1)
        list_of_point_coords = []
        for i in range(self.numberOfPoints-1):
            list_of_point_coords.append(self.startPoint + delta_x*i)
        list_of_point_coords.append(self.endPoint)
        print "The list of point coords is: {}".format( list_of_point_coords )
        gapSpaceDistribution = [] 
        for i in range(self.numberOfPoints-1):
            gapSpaceDistribution.append(delta_x)
        print "The gap space distribution is: {}.".format(gapSpaceDistribution) 
        print "Mesh generation complete."
        return list_of_point_coords,gapSpaceDistribution



    def createNonuniformMesh(self):
        print "Creating nonuniform Mesh"
        list_of_point_coords = []
        for i in range(self.n1):
            print "insert coordinate of point {} to the left of cluster point into list.".format(self.n1+1-i)
            list_of_point_coords.append(self.polynomial_minus(self.n1+1-i))
        for i in range(self.n2):
            print "insert coordinate of point {} to the right of cluster point into list.".format(i+1)
            list_of_point_coords.append(self.polynomial_plus(i+1))
        print "The list of point coords before scaling is: {}".format( list_of_point_coords )
        length_raw = list_of_point_coords[-1] - list_of_point_coords[0] 
        length_target = self.endPoint - self.startPoint 
        minimumDeltaX=(3+self.b)*length_target/length_raw
        list_of_point_coords_0 = list_of_point_coords[0]
        for i in range(len(list_of_point_coords)):
            list_of_point_coords[i] = self.startPoint + ( list_of_point_coords[i] - list_of_point_coords_0) * length_target/length_raw
        print "The list of point coords after scaling is: {}".format( list_of_point_coords )
        gapSpaceDistribution = []
        for i in range(self.numberOfPoints-1):
            gapSpaceDistribution.append(list_of_point_coords[i+1]-list_of_point_coords[i])
        print "The gap space distribution is: {}.".format(gapSpaceDistribution) 
        print "Mesh generation complete."
        return list_of_point_coords,gapSpaceDistribution,minimumDeltaX
          
    def polynomial(self,index):
        return pow(index,2)+self.b*index

    def polynomial_plus(self,index):
        return self.xclusteredPoint + ( self.polynomial(index) - self.polynomial(1) )
        
    def polynomial_minus(self,index):
        return self.xclusteredPoint - ( self.polynomial(index) - self.polynomial(1) )

    def plot_pointVsIndex(self):
        index = numpy.linspace(1,self.numberOfPoints,self.numberOfPoints)

        plt.figure()
        plt.plot(index,self.coordinates,'ro')
        plt.xlabel('index i')
        plt.ylabel('point coordinate')
        plt.savefig('pointVsIndex.png', bbox_inches='tight')
        plt.close()

    def plot_gapSpaceVsIndex(self):
        index = numpy.linspace(1,self.numberOfPoints-1,self.numberOfPoints-1)

        plt.figure()
        plt.plot(index,self.gapSpaceDistribution,'ro')
        plt.xlabel('index i')
        plt.ylabel('gap space after between point i and i+1')
        plt.savefig('gapSpaceVsIndex.png', bbox_inches='tight')
        plt.close()

    def plot_gapSpaceVsX(self):
        x = self.coordinates
        x.pop()

        plt.figure()
        plt.plot(x,self.gapSpaceDistribution,'ro')
        plt.xlabel('point coordinate')
        plt.ylabel('gap space between this point and next point')
        plt.savefig('gapSpaceVsX.png', bbox_inches='tight')
        plt.close()
        

    def printAllDataMembers(self):
        print "startPoint: {}".format(self.startPoint)
        print "endPoint: {}".format(self.endPoint)
        print "number of Points: {}".format(self.numberOfPoints)
        if self.Nonuniform == True:
            print "ratio: {}".format(self.ratio)
            print "coordinates of cluster point: {}".format(self.xclusteredPoint)
            print "number of points to the left of cluster point: {}".format(self.n1)
            print "number of points to the right of cluster point: {}".format(self.n2)
            print "max of n1 and n2: {}".format(self.nmax)
            print "parameter b for polynomial function: {}".format(self.b)

###################################################
#testing part

def test_uniformMesh():
    mesh2 = mesh(-0.5,0.5,101)
    mesh2.plot_pointVsIndex()
    mesh2.plot_gapSpaceVsIndex()
    print type(mesh2.coordinates)

def test_nonuniformMesh():
    mesh1 = mesh(0.2,2,101,5,1.5)
    mesh1.plot_pointVsIndex()
    mesh1.plot_gapSpaceVsIndex()

#test_uniformMesh()
#test_nonuniformMesh()



