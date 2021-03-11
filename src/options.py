"""
Options for properties provided by user
"""

import pickle
import numpy as np
import helpers as hp
from runProperties import runproperties as rP
from particleTemplate import particle as pT
from simulationProps import properties as sP
from geometryInsert import geometryInsert as gI

## The main options class
class Options():
    ## Initialization
    def __init__(self):
        ## Boolean for simulation properties
        self.hasUnits = False
        ## Boolean for region properties
        self.hasRegions = False
        ## Boolean for particle creation
        self.hasParticles = False
        ## Boolean for geometry creation
        self.hasGeometries = False
        ## Boolean for factory creation
        self.hasFactory = False
        ## Boolean for run creation
        self.hasRunSetup = False
        ## Geometry Class
        self.geom = gI()
        ## Simulation Property Class
        self.simProps = sP()
        ## Particle Class
        self.partTemp = pT()
        ## Run Property Class
        self.runProps = rP()
        ## Selected Option
        self.opt = -1

    ## Main options provided to the user
    def printOptions(self):
        hp.clear()
        while True:
            print("LIGGGHTS INPUT SCRIPT OPTIONS")

            hp.print2screenOptions("1: Set Simulation Properties", self.hasUnits)
            hp.print2screenOptions("2: Define Particle(s)", self.hasParticles)
            hp.print2screenOptions("3: Define Geometries", self.hasGeometries)
            # hp.print2screenOptions("4: Define Particle Insertion", self.hasFactory)
            hp.print2screenOptions("5: Define Run", self.hasRunSetup)
            print()
            print("8: Save/Load")
            print("9: Write Input File")
            print("0: Exit")

            self.getOption()

            if self.opt == "0":
                return


    ## Gets option from user and calls needed class
    def getOption(self):
        self.opt = input("Options to use: ")
        hp.clear()
        if self.opt == '1':
            self.hasUnits = self.simProps.getSimPropOpts()
        elif self.opt == '2':
            self.hasParticles = self.partTemp.getPartTemp()
        elif self.opt == '3':
            self.hasGeometries = self.geom.getGeomOpts()
        # elif self.opt == '4':
        #     self.hasParticles = self.partTemp.getPartTemp(self.simProps)
        elif self.opt == '5':
            self.hasRunSetup = self.runProps.getRunProps(self.simProps, self.partTemp)
            
        elif self.opt == '8':
            self.saveLoad()

        elif self.opt == '9':
            self.writeLiggghts()

    ## Creates the input file
    def writeLiggghts(self):
        hp.clear()
        with open('in.liggghts','w') as f:
            write("# This is an automatically created file provided by the LIGGGHTS-Input-Creator",f)
            write("shell mkdir post",f)
            write("shell mkdir restart",f)
            write("\n# Set Atom Style",f)
            write("atom_style %s"%(self.simProps.atomType),f)
            write("atom_modify map array",f)
            if np.min(self.simProps.contactProps['youngsModulus']) < 1.0e6:
                write('soft_particles yes',f)
            if np.max(self.simProps.contactProps['youngsModulus']) > 1.0e9:
                write('hard_particles yes',f)

            write("\n# Boundaries",f)
            write("boundary %s %s %s"%(self.simProps.boundaries['x'][-1], self.simProps.boundaries['y'][-1], self.simProps.boundaries['z'][-1]),f)
            write("newton off\ncommunicate single vel yes\nunits si",f)

            write("\n# Create Simulation Region",f)
            xMin = self.simProps.boundaries['x'][0]
            yMin = self.simProps.boundaries['y'][0]
            zMin = self.simProps.boundaries['z'][0]
            xMax = self.simProps.boundaries['x'][1]
            yMax = self.simProps.boundaries['y'][1]
            zMax = self.simProps.boundaries['z'][1]
            write("region domain block %e %e %e %e %e %e units box"%(xMin,xMax,yMin,yMax,zMin,zMax),f)
            write("create_box %i domain"%(self.simProps.numMaterials),f)

            write("\n# Define Contact/Fiber Models",f)
            write("pair_style %s"%(self.simProps.contactModel['p2p']),f)
            if self.simProps.numBondTypes > 0:
                write("bond_style %s"%(self.simProps.bondModel['p2p']),f)

            write("\n# Set Comunication Settings",f)
            write("neighbor %e bin"%(1.0*self.partTemp.getMinRadius()),f)
            write("neigh_modify delay 0",f)

            write("\n# Set Coefficients for Contact/Fiber Model",f)
            write("pair_coeff * *",f)

            if self.simProps.numBondTypes > 0:
                write(self.simProps.writeBondCoefs(),f) # write("bond_coeff %s"%(self.simProps.bondModel['p2p']),f)

            write("\n# Set Material Properties",f)
            write(self.simProps.writeMaterialProps(),f)

            # write("\n# Insert Geometry and Factory",f)
            write(self.geom.writeGeometryProps(self.simProps.contactModel['p2w'][11:-1]),f)

            # Add Gravity
            if np.abs(self.simProps.gravity[0]) > 0.0:
                write("\n# Add Gravity",f)
                write("fix grav_fix all gravity %e vector %e %e %e" % (self.simProps.gravity[0], self.simProps.gravity[1], self.simProps.gravity[2], self.simProps.gravity[3]), f)

            write("\n# Set Integration Type and Time Step", f)
            write("fix integr all nve/sphere",f)
            write("timestep %e" % (self.runProps.dt), f)

            # Add Insertion Options
            write(self.runProps.writeFactoryOptions(self.partTemp),f)

            write('\n# Add thermo and dump options',f)
            write(self.runProps.writeThermoOptions(),f)

            # Run 1 to make sure dump files are not empty
            write('\nrun 1',f)
            write(self.geom.writeDumpOptions(self.runProps.file_steps),f)
            write(self.runProps.writeDumpOptions(),f)

            # Run the simulation!
            write('\n# Set simulation run time',f)
            write('run %i'%(self.runProps.numSteps),f)

    ## Saves/Loads a configuration file
    def saveLoad(self):
        hp.clear()
        while True:
            print("1: Save Session")
            print("2: Load Session")
            print("0: Main Menu")
            opt = input("Option to use: ")
            hp.clear()
            if opt == "1":
                with open("currentSession.obj", 'wb') as f:
                    pickle.dump(self,f)
                    return
            elif opt == "2":
                try:
                    with open("currentSession.obj",'rb') as f:
                        temp = pickle.load(f)
                        curObs = [k for k in vars(temp)]
                        for var in curObs:
                            vars(self)[var] = vars(temp)[var]
                    # self = temp
                    return
                except:
                    print("Cannot Load File... Returning")
                    break
            elif opt == "0":
                return
            else:
                hp.clear()
                print("Not a valid input...")

## writes a string to file
#
#  @param curStr The string that will be written to file
#  @param fid The file that the string is being written to
def write(curStr,fid):
    fid.write(curStr + '\n')
