import pickle
import helpers as hp
from runProperties import run 
from particleTemplate import particle as pT
from simulationProps import properties as sP
from geometryInsert import geometryInsert as gI
class Options():
    def __init__(self):
        self.hasUnits = False
        self.hasRegions = False
        self.hasParticles = False
        self.hasGeometries = False
        self.hasFactory = False
        self.hasRunSetup = False
        self.geom = gI()
        self.simProps = sP()
        self.partTemp = pT()
        self.runProps = run()
        self.opt = -1

    def printOptions(self):
        hp.clear()
        while True:
            print("LIGGGHTS INPUT SCRIPT OPTIONS")

            hp.print2screenOptions("1: Set Simulation Properties", self.hasUnits)
            hp.print2screenOptions("2: Define Particle(s)", self.hasParticles)
            hp.print2screenOptions("3: Define Geometries", self.hasGeometries)
            hp.print2screenOptions("4: Define Particle Insertion", self.hasFactory)
            hp.print2screenOptions("5: Define Run", self.hasRunSetup)
            print()
            print("8: Save/Load")
            print("9: Write Input File")
            print("0: Exit")
            
            self.getOption()

            if self.opt == "0":
                return



    def getOption(self):
        self.opt = input("Options to use: ")
        hp.clear()
        if self.opt == '1':
            print("Getting Simulation Porps")
            self.hasUnits = self.simProps.getSimPropOpts()
        elif self.opt == '2':
            self.hasParticles = self.partTemp.getPartTemp()
        elif self.opt == '3':
            print("Defining Geometries")
            self.hasGeometries = self.geom.getGeomOpts()
        elif self.opt == '4':
            print("Defining Particle Insertion")
            self.hasParticles = self.partTemp.getPartTemp(self.simProps)
        elif self.opt == '5':
            self.hasRunSetup = self.runProps.getRunProps(self.simProps)
            
        elif self.opt == '8':
            self.saveLoad()


    def saveLoad(self):
        hp.clear()
        while True:
            print("1: Save Session")
            print("2: Load Session")
            print("3: Main Menu")
            opt = input("Option to use: ")
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
            elif opt == "3":
                return
            else:
                hp.clear()
                print("Not a valid input...")

