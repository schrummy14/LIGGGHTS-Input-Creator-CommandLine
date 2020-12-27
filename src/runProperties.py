import numpy as np
import helpers as hp

class runproperties():
    def __init__(self):
        self.numSteps = -1
        self.dt = -1.0
        self.dt_ray = -1.0
        self.dt_bond = -1.0
        self.factories = []
        

    def getRunProps(self, simProps, atomProps):
         while True:
            if self.dt > 0:
                dtTooLarge = False
                dtTooLarge |= self.dt/self.dt_ray > 0.25
                if dtTooLarge:
                    print("Warning: Time step is set larger than is recommended...")
                    print("Rayleigh Time Step:",self.dt_ray)
                    print("Current Time Step:", self.dt)
            
            print("Set Run Time Properties")
            print("1: Screen Output")
            print("2: File Output")
            print("3: Time Step")
            print("4: Build Factory")
            print("0: Go Back")

            opt = input("Option to use: ")
            hp.clear()
            if opt == '1':
                self.screenOutput()
                # hp.clear()
            elif opt == '2':
                self.fileOutput()
                # hp.clear()
            elif opt == '3':
                self.timeStep(simProps, atomProps)
                hp.clear()
            elif opt == '4':
                self.buildFactory(atomProps)
            elif opt == '0':
                return self.everythingDefined()
            else:
                print("Bad Option")

    def screenOutput(self):
        return
    def fileOutput(self):
        return
    def timeStep(self, sp, ap):
        # Get atom props
        numTemplates = len(ap.template)
        minR = None
        minDensity = None
        for k in range(numTemplates):
            curTemp = ap.template[k]
            curDensity = curTemp.density
            if minDensity is None or curDensity < minDensity:
                minDensity = curDensity
            for atom in curTemp.atom:
                curR = atom[-1]
                if minR is None or curR < minR:
                    minR = curR
        # Get material properties
        maxY = None
        maxG = None
        maxP = None
        for k in range(sp.numMaterials):
            Y = sp.contactProps['youngsModulus'][k]
            if maxY is None or Y > maxY:
                maxY = Y
            P = sp.contactProps['poissonsRatio'][k]
            if maxP is None or P > maxP:
                maxP = P
            G = Y/(2.0*(1.0+P))
            if maxG is None or G > maxG:
                maxG = G
        
        # Calculate Rayleigh Time
        dt_ray = np.pi*minR*np.sqrt(minDensity/maxG)/(0.1631*maxP+0.8766)
        self.dt_ray = dt_ray
        
        while True:
            print("Set time step of simulation")
            print("Rayleigh Time:", dt_ray)
            print("1: Set percentage of rayleigh time")
            print("2: Set time step")
            print("0: Go Back")
            opt = input("Option to use: ")
            hp.clear()
            if opt == "1":
                while True:
                    per = hp.getNum("Percentage of Rayleigh Time: ")
                    if 0.0 < per and per < 1.0:
                        self.dt = per*dt_ray
                        return
                    else:
                        print("The value entered must be between 0.0 and 1.0")
            elif opt == "2":
                while True:
                    dt = hp.getNum("Set Time Step: ")
                    if dt > 0.0:
                        self.dt = dt
                        return
                    else:
                        print("The timestep must be greater than 0")
            elif opt == "5":
                return 
            else:
                hp.clear()
                print("Bad Input")
        return
    

    def buildFactory(self, atomProps):
        while True:
            print("Set Factory Options")
            print("1: Factory Dimmenstions")
            print("2: Particle Distribution")
            print("3: Factory Options")
            print("4: Delete Factory")
            print("0: Go Back")
            opt = input("Option to use: ")
            hp.clear()
            if opt == '1':
                self.getFactoryType()
                hp.clear()
            elif opt == '2':
                self.setParticleDistribution(atomProps)
                hp.clear()
            elif opt == '3':
                self.setFactoryOptions()
                hp.clear()
            elif opt == '4':
                self.deleteFactory()
            elif opt == '0':
                return
            else:
                print("Bad Input")

    def deleteFactory(self):
        numFactories = len(self.factories)
        if numFactories == 0:
            print("You have no factories to delete... Returning")
            return
        hp.clear()
        while True:
            print("Which factory would you like to delete?")
            for k in range(numFactories):
                print("%i: %s"%(k+1,self.factories[k].name))
            opt = hp.getNum("Factory to delete: ")
            hp.clear()
            if opt < 1 or numFactories < opt:
                print("Bad Input")
            else:
                break

    def setFactoryOptions(self):
        numFactories = len(self.factories)
        if numFactories == 0:
            print("You have no factories created... Returning")
            return
        hp.clear()
        while True:
            print("Which factory would you like to edit?")
            for k in range(numFactories):
                print("%i: %s"%(k+1,self.factories[k].name))
            opt = hp.getNum("Factory to edit: ")
            hp.clear()
            if opt < 1 or numFactories < opt:
                print("Bad Input")
            else:
                break
        keys = self.factories[opt-1].factoryOptions.keys()
        while True:
            print("Which options would you like to edit?")
            k = 1
            for key in keys:
                print("%i: %s" % (k, key))
                k += 1
            key_opt = hp.getNum("Option to edit: ")
            hp.clear()
            if key_opt < 1 or len(keys) < key_opt:
                print("Bad Input")
            else:
                break
        
        if key[key_opt-1] == 'maxattempt':
            self.factories[opt-1].factoryOptions['maxattempt'] = \
            int(hp.getNum("New value for %s (%i)" % ('maxattempt', self.factories[opt-1].factoryOptions['maxattempt'])))
        elif key[key_opt-1] == 'insert_every':
            self.factories[opt-1].factoryOptions['insert_every'] = \
            int(hp.getNum("New value for %s (%i)" % ('insert_every', self.factories[opt-1].factoryOptions['insert_every'])))
        elif key[key_opt-1] == 'overlapcheck':
            self.factories[opt-1].factoryOptions['overlapcheck'] = \
            hp.getYesNo("New value for %s (%s)" % ('overlapcheck', self.factories[opt-1].factoryOptions['overlapcheck']))
        elif key[key_opt-1] == 'orientation':
            self.getOrientationOptions(opt-1)
        elif key[key_opt-1] == 'all_in':
            self.factories[opt-1].factoryOptions['all_in'] = \
            hp.getYesNo("New value for %s (%s)" % ('all_in', self.factories[opt-1].factoryOptions['all_in']))
        elif key[key_opt-1] == 'vel':
            self.getVelocityOptions(opt-1)
        elif key[key_opt-1] == 'targetType':
            self.getTargetTypeOptions(opt-1)
        elif key[key_opt-1] == 'ntry_mc':
            self.factories[opt-1].factoryOptions['ntry_mc'] = \
            int(hp.getNum("New value for %s (%i)" % ('ntry_mc', self.factories[opt-1].factoryOptions['ntry_mc'])))
        elif key[key_opt-1] == 'check_dist_from_subdomain_border':
            self.factories[opt-1].factoryOptions['check_dist_from_subdomain_border'] = \
            hp.getYesNo("New value for %s (%s)" % ('check_dist_from_subdomain_border', self.factories[opt-1].factoryOptions['check_dist_from_subdomain_border']))

        return

    def getOrientationOptions(self, fact):
        input("Can only use random orientation at this time. Press enter to return")
        return

    def getVelocityOptions(self, fact):
        hp.clear()
        while True:
            print("Velocity Type")
            print("1: Constant")
            opt = input("Select Velocity Type: ")
            hp.clear()
            if opt == '1':
                self.factories[fact].factoryOptions['vel'][0] = 'constant'
                vx = hp.getNum("Velocity in x direction: ")
                vy = hp.getNum("Velocity in y direction: ")
                vz = hp.getNum("Velocity in z direction: ")
                self.factories[fact].factoryOptions['vel'][1] = [vx,vy,vz]
                return
            else:
                print("Bad Input")
        return

    def getTargetTypeOptions(self, fact):
        hp.clear()
        while True:
            print("Insertion Types")
            print("1: Volume Fraction")
            opt = input("Select Insertion Type: ")
            hp.clear()
            if opt == '1':
                self.factories[fact].factoryOptions['targetType'][0] = 'volumefraction_region'
                self.factories[fact].factoryOptions['targetType'][1] = hp.getNum("volume fraction target: ")
            else:
                print("Bad Input")
        return

    def setParticleDistribution(self, atomProps):
        if len(atomProps.template) == 0:
            print("No Atoms Defined: You must create atom templates first...")
            return
        while True:
            print("Set Particle Probabilities")
            print("1: Manually")
            print("2: By Distribution")
            opt = input(" Select Type: ")
            hp.clear()
            if opt == '1':
                for k in range(len(atomProps.template)):
                    while True:
                        curStr = "Percentage for atom %s:"%(atomProps.template[k].name)
                        per = hp.getNum(curStr)
                        if per < 0 or 1 < per:
                            print("Atom Percentage must be between 0 and 1")
                        else:
                            break
                return
            elif opt == '2':
                for k in range(len(atomProps.template)):
                    return
    
    def getFactoryType(self):
        print("Select Factory Shape")
        print("1: Box")
        print("2: Cylinder")
        opt = input("Option to use: ")
        hp.clear()
        if opt == '1':
            f = factory(input("Factory Name: "))
            f.shape = box_factory()
            f.shape.dimmensions[0] = hp.getNum("Box xMin: ")
            f.shape.dimmensions[1] = hp.getNum("Box xMax: ")
            f.shape.dimmensions[2] = hp.getNum("Box yMin: ")
            f.shape.dimmensions[3] = hp.getNum("Box yMax: ")
            f.shape.dimmensions[4] = hp.getNum("Box zMin: ")
            f.shape.dimmensions[5] = hp.getNum("Box zMax: ")

        elif opt == '2':
            f = factory(input("Factory Name: "))
            f.shape = cylinder_factory()
            while True:
                opt = input("Which axis is the cylinder along: ")
                if not opt in ['x','y','z']:
                    print("Bad Option: Cylinder can only be in the x or y or z direction")
                else:
                    break
            f.shape.axis = opt
            f.shape.x1 = hp.getNum("x1 Position: ")
            f.shape.x2 = hp.getNum("x2 Position: ")
            f.shape.radius = hp.getNum("Cylinder Radius: ")
            f.shape.height = hp.getNum("Cylinder Height: ")
        
        else:
            print("Bad Input")
        
        self.factories.append(f)
        
        return
            

    def everythingDefined(self):
        return True

class factory():
    def __init__(self,_name):
        self.name = _name
        self.shape = None
        self.atom_distribution = []
        self.factoryOptions = {
            "maxattempt": int(1000),
            "insert_every": int(0), # 0 means once
            "overlapcheck": "yes",
            "orientation": "random",
            "all_in": "yes",
            "vel": ["constant", [0,0,0]],
            "targetType": ["volumefraction_region", 0.6],
            "ntry_mc": int(1000000),
            "check_dist_from_subdomain_border": "no"
        }

class box_factory():
    def __init__(self):
        self.name = 'box'
        self.dimmensions = [0,0,0,0,0,0]
class cylinder_factory():
    def __init__(self):
        self.name = 'cylinder'
        self.x1 = 0.0
        self.x2 = 0.0
        self.axis = 'xyz'
        self.height = 0.0
        self.radius = 0.0
