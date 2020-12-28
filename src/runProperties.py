import numpy as np
import helpers as hp

class runproperties():
    def __init__(self):
        self.numSteps = -1
        self.dt = -1.0
        self.dt_ray = -1.0
        self.dt_bond = -1.0
        self.factories = []
        self.thermo_steps = 0
        self.thermo_options = {
            "step": True,
            "time": True,
            "atoms": True,
            "numbonds": True,
            "cpu": True,
            "cpuremain": True,
            "ke": True
        }
        self.file_steps = 0
        self.file_options = {
            "id": True,
            "type": True,
            "x": True,
            "y": True,
            "z": True,
            "ix": False,
            "iy": False,
            "iz": False,
            "vx": True,
            "vy": True,
            "vz": True,
            "fx": True,
            "fy": True,
            "fz": True,
            "omegax": True,
            "omegay": True,
            "omegaz": True,
            "radius": True,
            "density": True
        }
        

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
                hp.clear()
            elif opt == '2':
                self.fileOutput()
                hp.clear()
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
        while True:
            print("To Screen Options")
            print("1: Variables")
            print("2: Steps per Print")
            print("0: Go Back")
            opt = input("Screen Option: ")
            hp.clear()
            if opt == '1':
                while True:
                    print("Screen Variable Options")
                    print("1: Turn Variable On/Off")
                    print("2: Create Custom Variable")
                    opt = input("Screen Variable Option: ")
                    hp.clear()
                    if opt == '1':
                        keys = list(self.thermo_options.keys())
                        while True:
                            print("Select a variable to change")
                            for itr,key in enumerate(keys):
                                if self.thermo_options[key]:
                                    onOff = 'yes'
                                else:
                                    onOff = 'no'
                                print("%i: %s (%s)" % (itr+1, key, onOff))
                            key_itr = int(hp.getNum("Which key would you like to change (Press 0 to go back): "))
                            if key_itr == 0:
                                break
                            elif key_itr > itr:
                                print("Bad Option")
                                continue
                            else:
                                newOnOff = hp.getYesNo("New Value for %s" % (keys[key_itr]))
                                if newOnOff == 'yes':
                                    self.thermo_options[keys[key_itr]] = True
                                else:
                                    self.thermo_options[keys[key_itr]] = False
                                break
                        hp.clear()
                        break

                    elif opt == '2':
                        input("This has not been implemented yet... press enter to return")
                        break

            elif opt == '2':
                if self.dt < 0:
                    input("You must set your time step before you can set this option...\nPress enter to retrun...")
                    continue
                thermo_time = hp.getNum("Ammount of time between screen updates: ")
                self.thermo_steps = np.round(thermo_time/self.dt)
                continue
            elif opt == '0':
                return
            else:
                "Bad Option"        
        return

    def fileOutput(self):
        while True:
            print("To Screen Options")
            print("1: Variables")
            print("2: Steps per Print")
            print("0: Go Back")
            opt = input("Screen Option: ")
            hp.clear()
            if opt == '1':
                while True:
                    print("File Variable Options")
                    print("1: Turn Variable On/Off")
                    print("2: Create Custom Variable")
                    opt = input("File Variable Option: ")
                    hp.clear()
                    if opt == '1':
                        keys = list(self.file_options.keys())
                        while True:
                            print("Select a variable to change")
                            for itr,key in enumerate(keys):
                                if self.file_options[key]:
                                    onOff = 'yes'
                                else:
                                    onOff = 'no'
                                print("%i: %s (%s)" % (itr+1, key, onOff))
                            key_itr = int(hp.getNum("Which key would you like to change (Press 0 to go back): "))
                            if key_itr == 0:
                                break
                            elif key_itr > itr:
                                print("Bad Option")
                                continue
                            else:
                                newOnOff = hp.getYesNo("New Value for %s" % (keys[key_itr]))
                                if newOnOff == 'yes':
                                    self.file_options[keys[key_itr]] = True
                                else:
                                    self.file_options[keys[key_itr]] = False
                                break
                        break

                    elif opt == '2':
                        input("This has not been implemented yet... press enter to return")
                        break

            elif opt == '2':
                if self.dt < 0:
                    input("You must set your time step before you can set this option...\nPress enter to retrun...")
                    continue
                file_time = hp.getNum("Ammount of time between file updates: ")
                self.file_steps = np.round(file_time/self.dt)
                continue
            elif opt == '0':
                return
            else:
                "Bad Option"        
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
            print("1: Set time step")
            print("2: Set percentage of rayleigh time")
            print("0: Go Back")
            opt = input("Option to use: ")
            hp.clear()
            if opt == "2":
                while True:
                    per = hp.getNum("Percentage of Rayleigh Time: ")
                    if 0.0 < per and per < 1.0:
                        self.dt = per*dt_ray
                        return
                    else:
                        print("The value entered must be between 0.0 and 1.0")
            elif opt == "1":
                while True:
                    dt = hp.getNum("Set Time Step: ")
                    if dt > 0.0:
                        self.dt = dt
                        return
                    else:
                        print("The timestep must be greater than 0")
            elif opt == "0":
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
            opt = int(hp.getNum("Factory to edit: "))
            hp.clear()
            if opt < 1 or numFactories < opt:
                print("Bad Input")
            else:
                break
        keys = list(self.factories[opt-1].factoryOptions.keys())
        while True:
            print("Which options would you like to edit?")
            k = 1
            for key in keys:
                print("%i: %s" % (k, key))
                k += 1
            key_opt = int(hp.getNum("Option to edit: "))
            hp.clear()
            if key_opt < 1 or len(keys) < key_opt:
                print("Bad Input")
            else:
                break
        
        if keys[key_opt-1] == 'maxattempt':
            self.factories[opt-1].factoryOptions['maxattempt'] = \
            int(hp.getNum("New value for %s (%i) " % ('maxattempt', self.factories[opt-1].factoryOptions['maxattempt'])))
        elif keys[key_opt-1] == 'insert_every':
            if self.factories[opt-1].factoryOptions['insert_every'] == 'once':
                oldVal = 0
            else:
                oldVal = int(self.factories[opt-1].factoryOptions['insert_every'])
            newVal = int(hp.getNum("New value for %s (%i) " % ('insert_every', oldVal)))
            if newVal == 0:
                self.factories[opt-1].factoryOptions['insert_every'] = 'once'
            else:
                self.factories[opt-1].factoryOptions['insert_every'] = str(newVal)
        elif keys[key_opt-1] == 'overlapcheck':
            self.factories[opt-1].factoryOptions['overlapcheck'] = \
            hp.getYesNo("New value for %s (%s) " % ('overlapcheck', self.factories[opt-1].factoryOptions['overlapcheck']))
        elif keys[key_opt-1] == 'orientation':
            self.getOrientationOptions(opt-1)
        elif keys[key_opt-1] == 'all_in':
            self.factories[opt-1].factoryOptions['all_in'] = \
            hp.getYesNo("New value for %s (%s) " % ('all_in', self.factories[opt-1].factoryOptions['all_in']))
        elif keys[key_opt-1] == 'vel':
            self.getVelocityOptions(opt-1)
        elif keys[key_opt-1] == 'targetType':
            self.getTargetTypeOptions(opt-1)
        elif keys[key_opt-1] == 'ntry_mc':
            self.factories[opt-1].factoryOptions['ntry_mc'] = \
            int(hp.getNum("New value for %s (%i) " % ('ntry_mc', self.factories[opt-1].factoryOptions['ntry_mc'])))
        elif keys[key_opt-1] == 'check_dist_from_subdomain_border':
            self.factories[opt-1].factoryOptions['check_dist_from_subdomain_border'] = \
            hp.getYesNo("New value for %s (%s) " % ('check_dist_from_subdomain_border', self.factories[opt-1].factoryOptions['check_dist_from_subdomain_border']))

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
        if len(self.factories) == 0:
            print("No factories built yet...")
            return
        numFactories = len(self.factories)
        while True:
            print("Which factory would you like to set particle distribution for?")
            for k in range(numFactories):
                print("%i: %s"%(k+1,self.factories[k].name))
            opt = int(hp.getNum("Factory to edit: "))
            hp.clear()
            if opt < 1 or numFactories < opt:
                print("Bad Input")
            else:
                break
        factOpt = opt
        while True:
            print("Set Particle Probabilities")
            print("1: Manually")
            print("2: By Distribution")
            opt = input(" Select Type: ")
            hp.clear()
            if opt == '1':
                insertPers = list()
                sumPers = 0.0
                for k in range(len(atomProps.template)):
                    while True:
                        curStr = "Percentage for atom %s:"%(atomProps.template[k].name)
                        per = hp.getNum(curStr)
                        if per < 0 or 1 < per:
                            print("Atom Percentage must be between 0 and 1")
                        else:
                            sumPers += per
                            insertPers.append(per)
                            break
                for per in insertPers:
                    per /= sumPers
                
                self.factories[factOpt-1].atom_distribution = insertPers
                
                return
            elif opt == '2':
                input("This is not currently available... Press enter to return:")
                return
                for k in range(len(atomProps.template)):
                    while True:
                        print("Choose Distribution")
                        print("1: Guassian")
                        print("2: Uniform")
                        opt = input("Select Type: ")
                        hp.clear
                        if opt == '1':
                            return
                        elif opt == '2':
                            return
                        else:
                            print("Bad Input")
                    return
            else:
                print("Bad Input")
    
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
            f.shape.h1 = hp.getNum("Cylinder Start Height: ")
            f.shape.h2 = hp.getNum("Cylinder End Height: ")
            f.shape.radius = hp.getNum("Cylinder Radius: ")
            f.shape.height = hp.getNum("Cylinder Height: ")
        
        else:
            print("Bad Input")
        
        self.factories.append(f)
        
        return  

    def everythingDefined(self):
        return True
    
    def writeFactoryOptions(self, pt):
        curStr = "\n# Insertion Options"
        for k, p in enumerate(pt.template):
            if len(p.atom) > 1:
                print("Multisphere templates not yet implemented")
            else:
                curStr += "\nfix pts%i all particletemplate/sphere %i atom_type %i density constant %e radius constant %e" % (
                    k+1,
                    hp.getNewPrime(),
                    p.type,
                    p.density,
                    p.atom[0][-1]
                )
        # Now do factory construction
        for k, f in enumerate(self.factories):
            curStr += "\nfix pdd%i all particledistribution/discrete %i %i" % (
                k+1,
                hp.getNewPrime(),
                len(pt.template)
            )
            for kk, pd in enumerate(self.factories[k].atom_distribution):
                curStr += " pts%i %e" % (kk+1, pd)

        # Define factory region and factory options
        curStr += '\n'
        for k, f in enumerate(self.factories):
            curStr += self.getFactoryRegionStr(k,f)
            curStr += "\nfix ins%i all insert/pack seed %i distributiontemplate pdd%i " % (
                k+1,
                hp.getNewPrime(),
                k+1
            )
            curStr += self.getFactoryOptionsStr(f)

        return curStr

    def getFactoryOptionsStr(self, f):
        curStr = ''
        keys = list(f.factoryOptions.keys())
        chars = ['[',']','\'',',']
        t = 0
        for itr, key in enumerate(keys):
            if (itr+t) % 3 == 0:
                curStr += '&\n\t'
            
            curOption = str(f.factoryOptions[key])
            for c in chars:
                curOption = curOption.replace(c,'')

            if key == 'targetType':
                t+=1
                curStr += 'region %s ' % (f.name)
                curStr += curOption + ' '
            else:
                curStr += key + ' ' + curOption + ' '
        return curStr[:-1]

    def getFactoryRegionStr(self,k,f):
        if f.shape.name == 'box':
            return 'region %s block %e %e %e %e %e %e units box\n' % (
                f.name,
                f.shape.dimmensions[0],
                f.shape.dimmensions[1],
                f.shape.dimmensions[2],
                f.shape.dimmensions[3],
                f.shape.dimmensions[4],
                f.shape.dimmensions[5]
            )
        elif f.shape.name == 'cylinder':
            return 'region %s cylinder %s %e %e %e %e %e units box\n' % (
                f.name,
                f.shape.axis,
                f.shape.x1,
                f.shape.x2,
                f.shape.radius,
                f.shape.h1,
                f.shape.h2
            )
        else:
            return 'This factory type has not been added to the function: getFactoryRegionStr in runProperties.py'


    def writeThermoOptions(self):
        curStr = "thermo_style custom"
        keys = list(self.thermo_options.keys())
        for k in keys:
            if self.thermo_options[k]:
                curStr += ' ' + str(k)
        curStr += "\nthermo %i" %(self.thermo_steps)
        curStr += "\nthermo_modify lost ignore norm no"
        return curStr
    
    def writeDumpOptions(self):
        curStr = "dump dmp_part all custom %i post/dump_*.liggghts" % (self.file_steps)
        keys = list(self.file_options.keys())
        for k in keys:
            if self.file_options[k]:
                curStr += ' ' + str(k)
        return curStr

class factory():
    def __init__(self,_name):
        self.name = _name
        self.shape = None
        self.atom_distribution = []
        self.factoryOptions = {
            "maxattempt": int(1000),
            "insert_every": 'once',
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
        self.h1 = 0.0
        self.h2 = 0.0
        self.radius = 0.0
