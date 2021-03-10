"""
Simulation Properties
"""

import types
import numpy as np
import helpers as hp

## Particle and Geometry Interaction Property Class
class properties():
    ## Initialization
    def __init__(self):
        ## Type of atoms in the simulation
        self.atomType = "sphere"
        ## Use JKR contact
        self.jkr_flag = False
        ## How many materials in the simulation
        self.numMaterials = 0
        ## Number of bond types in the simulation
        self.numBondTypes = 0
        ## Max bonds per atom
        self.maxBondsPerAtom = 0
        ## Gravity in the simulation
        self.gravity = [0.0, 0.0, 0.0, 0.0]
        ## The contact model for the simulation
        self.contactModel = {
            "p2p": "",
            "p2w": ""
        }
        ## The bond model to be used
        self.bondModel = {
            "p2p": ""
        }
        ## Boundaries in the simulation
        self.boundaries = {
            "x": [0.0, 0.0, "f"],
            "y": [0.0, 0.0, "f"],
            "z": [0.0, 0.0, "f"]
        }
        ## The contact properties
        self.contactProps = {
            "kn": [],
            "kt": [],
            "gammaN": [],
            "gammaT": [],
            "characteristicVelocity": 0.0,
            "youngsModulus": [],
            "poissonsRatio": [],
            "coefRestitution": [],
            "coefFriction": [],
            "coefAdhesion": [],
            "jkrResolution": 0.0
        }
        ## The bond properties
        self.bondProps = {
            "YoungsModulus": [],
            "PoissonsRatio": [],
            "NormalBreak": [],
            "TanBreak": [],
            "BreakType": [],
            "TempBreak": []
        }
        ## Cohesion model properties
        self.cohesionProps = {
            "minSeparationDistanceRatio": 0.0,
            "maxSeparationDistanceRatio": 0.0,
            "surfaceLiquidContentInitial": 0.0,
            "surfaceTension": 0.0,
            "fluidViscosity": 0.0,
            "contactAngle": [],
            "cohesionEnergyDensity": [],
            "maxLiquidContent": []
        }
        ## Rolling model properties
        self.rollingProps = {
            "adhesionHysteresis": [],
            "coefficientRollingFriction": [],
            "coefficientRollingViscousDamping": [],
            "coeffRollingStiffness": 0.0
        }
    ## Creates a string containing the bond coefficient properties
    def writeBondCoefs(self):
        return ''
    ## Creates a string containing the material properties
    def writeMaterialProps(self):
        curStr = "fix m1 all property/global youngsModulus peratomtype"
        for k in range(self.numMaterials):
            curStr += ' %e'%(self.contactProps['youngsModulus'][k])

        curStr += "\nfix m2 all property/global poissonsRatio peratomtype"
        for k in range(self.numMaterials):
            curStr += ' %e'%(self.contactProps['poissonsRatio'][k])

        curStr += "\nfix m3 all property/global coefficientFriction peratomtypepair %i"%(self.numMaterials)
        cof = self.buildTypeMatrix(self.contactProps['coefFriction'])
        for k in range(self.numMaterials):
            for m in range(self.numMaterials):
                curStr += " %e"%(cof[k][m])

        curStr += "\nfix m4 all property/global coefficientRestitution peratomtypepair %i"%(self.numMaterials)
        cof = self.buildTypeMatrix(self.contactProps['coefRestitution'])
        for k in range(self.numMaterials):
            for m in range(self.numMaterials):
                curStr += " %e"%(cof[k][m])

        fixNum = 5
        if self.jkr_flag:
            curStr += "\nfix m%i all property/global workOfAdhesion peratomtypepair %i"%(fixNum,self.numMaterials)
            cof = self.buildTypeMatrix(self.contactProps['coefAdhesion'])
            for k in range(self.numMaterials):
                for m in range(self.numMaterials):
                    curStr += " %e"%(cof[k][m])
            fixNum += 1
            curStr += "\nfix m%i all property/global resolutionJKR scalar %e" % (fixNum, self.contactProps['jkrResolution'])
            fixNum += 1

        if len(self.rollingProps['coefficientRollingFriction']) > 0:
            curStr += "\nfix m%i all property/global coefficientRollingFriction peratomtypepair %i"%(fixNum,self.numMaterials)
            cof = self.buildTypeMatrix(self.rollingProps['coefficientRollingFriction'])
            for k in range(self.numMaterials):
                for m in range(self.numMaterials):
                    curStr += " %e"%(cof[k][m])
            fixNum += 1
        
        if len(self.rollingProps['adhesionHysteresis']) > 0:
            curStr += "\nfix m%i all property/global adhesionHysteresis peratomtypepair %i"%(fixNum,self.numMaterials)
            cof = self.buildTypeMatrix(self.rollingProps['adhesionHysteresis'])
            for k in range(self.numMaterials):
                for m in range(self.numMaterials):
                    curStr += " %e"%(cof[k][m])
            fixNum += 1

        return curStr
    ## Builds the interaction matrix
    #
    #  @param arr The values to be used in the matrix
    def buildTypeMatrix(self,arr):
        cof = np.zeros([self.numMaterials,self.numMaterials])
        km = 0
        for k in range(self.numMaterials):
            for m in range(k,self.numMaterials):
                cof[k][m] = arr[km]
                km += 1
        return cof + cof.T - np.diag(cof.diagonal())

    ## Provides the simulation options to the user to edit
    def getSimPropOpts(self):
        hp.clear()
        while True:
            print("Simulation Property Input")
            print("1: Set Atom Style")
            print("2: Set Boundaries")
            print("3: Set Material Properties")
            print("4: Back to Main")
            opt = input("Option to use: ")
            hp.clear()
            if opt == "1":
                self.setAtomStyle()
                hp.clear()
            elif opt == "2":
                self.setSimBoundaries()
                hp.clear()
            elif opt == "3":
                self.setMaterialProps()
                hp.clear()
            elif opt == "4":
                break
            else:
                print("Bad Input...")
        curObs = [k for k in vars(self)]
        notSet = False
        for ob in curObs:
            # print(ob)
            if type(vars(self)[ob]) is int:
                if vars(self)[ob] == 0:
                    print("Simulation Property [" + ob + "] Still Needs To Be Set...")
                    notSet |= True
            elif type(vars(self)[ob]) is bool:
                continue
            elif len(vars(self)[ob]) == 0:
                print("Simulation Property [" + ob + "] Still Needs To Be Set...")
                notSet |= True
        if notSet:
            return False
        else:
            return True

    ## Allows the user to set the atom style
    def setAtomStyle(self):
        hp.clear()
        while True:
            print("Select Atom Style From List")
            print("1: Granular")
            print("2: Granular Bond")
            opt = input("Option to use: ")
            if opt == "1":
                self.atomType = "granular"
                self.numBondTypes = -1
                self.maxBondsPerAtom = -1
                # hp.clear()
                break
            elif opt == "2":
                self.numBondTypes = hp.getNum("Number of Bond Types: ")
                self.maxBondsPerAtom = hp.getNum("Max Bonds Per Atom: ")
                self.atomType = "hybrid granular bond/gran"
                # hp.clear()
                break
            else:
                print("Bad Option...")
        hp.clear()
        
    ## Has the user set the boundary type and size
    def setSimBoundaries(self):
        hp.clear()
        while True:
            print("Select Boundary Info")
            print("1: Boundary Types")
            print("2: Boundary Size")
            print("3: Gravity")
            print("0: Go Back")
            opt = input("Option to use: ")
            hp.clear()
            if opt == "1":
                print("Boundaries can be (f)ixed or (p)eriodic")
                self.boundaries["x"][2] = getBoundaryType("Boundary Type X: ")
                self.boundaries["y"][2] = getBoundaryType("Boundary Type Y: ")
                self.boundaries["z"][2] = getBoundaryType("Boundary Type Z: ")
                hp.clear()
            elif opt == "2":
                self.boundaries["x"][0] = hp.getNum("Min X Boundary: ")
                self.boundaries["x"][1] = hp.getNum("Max X Boundary: ")
                self.boundaries["y"][0] = hp.getNum("Min Y Boundary: ")
                self.boundaries["y"][1] = hp.getNum("Max Y Boundary: ")
                self.boundaries["z"][0] = hp.getNum("Min Z Boundary: ")
                self.boundaries["z"][1] = hp.getNum("Max Z Boundary: ")
                hp.clear()
            elif opt == "3":
                self.gravity[0] = hp.getNum("Set Gravity Magnitude: ")
                print("Gravity Direction")
                self.gravity[1] = hp.getNum("X - Direction: ")
                self.gravity[2] = hp.getNum("Y - Direction: ")
                self.gravity[3] = hp.getNum("Z - Direction: ")
                hp.clear()
            elif opt == "0":
                hp.clear()
                return
            else:
                print("Bad Input...")

    ## Allows the user to set the material properties
    def setMaterialProps(self):
        hp.clear()
        while True:
            print("Set Material Properties")
            print("1: Number of Materials")
            print("2: Contact Model")
            print("3: Bond Model")
            print("4: Material Properties")
            print("0: Back")

            opt = input("Option to use: ")
            hp.clear()
            if opt == "1":
                self.numMaterials = int(hp.getNum("Number of Materials: "))
                hp.clear()
            elif opt == "2":
                self.contactModel["p2p"] = self.getContactModel()
                hp.clear()
            elif opt == "3":
                self.bondModel = "gran"
                hp.clear()
            elif opt == "4":
                self.getMaterialProps()
                hp.clear()
            elif opt == "0":
                hp.clear()
                return

    ## Has the user set the properties for the simulation
    def getMaterialProps(self):
        conMod = self.contactModel["p2p"]
        self.contactModel["p2w"] = conMod

        print("Setting Properties for the Physics Model")
        modelId = conMod.find("model")
        cohesionId = conMod.find("cohesion")
        rollingId = conMod.find("rolling_friction")

        self.getContactProps(conMod[modelId:cohesionId])
        self.getCohesionProps(conMod[cohesionId:rollingId])
        self.getRollingProps(conMod[rollingId:])

    ## Has the user set the contact properties
    #
    #  @param contactMod A string that contains the contact model
    def getContactProps(self, contactMod):
        if contactMod == -1:
            return
        numAtomTypes = self.numMaterials
        contactMod = contactMod[contactMod.find(" "):].strip()

        if len(contactMod) == 0:
            return

        self.contactProps["youngsModulus"] = []
        for k in range(numAtomTypes):
            curStr = "Contact Young's Modulus for Type %i: " % (k+1)
            self.contactProps["youngsModulus"].append(hp.getNum(curStr))
        
        self.contactProps["poissonsRatio"] = []
        for k in range(numAtomTypes):
            curStr = "Contact Poisson's Ratio for Type %i: " % (k+1)
            self.contactProps["poissonsRatio"].append(hp.getNum(curStr))

        self.contactProps["coefRestitution"] = []
        for k1 in range(numAtomTypes):
            for k2 in range(k1,numAtomTypes):
                curStr = "Coefficient of Restitution Between Types %i and %i: " % (k1+1, k2+1)
                self.contactProps["coefRestitution"].append(hp.getNum(curStr))
        
        self.contactProps["coefFriction"] = []
        for k1 in range(numAtomTypes):
            for k2 in range(k1,numAtomTypes):
                curStr = "Coefficient of Friction Between Types %i and %i: " % (k1+1, k2+1)
                self.contactProps["coefFriction"].append(hp.getNum(curStr))

        if contactMod[:contactMod.find(" ")].strip() == "hooke" or contactMod[:contactMod.find(" ")].strip() == "hooke/stiffness":
            curStr = "Characteristic Velocity: "
            self.contactProps["characteristicVelocity"] = hp.getNum(curStr)

        if contactMod[:contactMod.find(" ")].strip() == "hertz/stiffness" or contactMod[:contactMod.find(" ")].strip() == "hooke/stiffness":
            self.contactProps["kn"] = []
            self.contactProps["kt"] = []
            self.contactProps["gamman"] = []
            self.contactProps["gammat"] = []
            for k1 in range(numAtomTypes):
                for k2 in range(k1,numAtomTypes):
                    curStr = "Normal Stiffness Between Types %i and %i: " % (k1+1, k2+1)
                    self.contactProps["kn"].append(hp.getNum(curStr))
            for k1 in range(numAtomTypes):
                for k2 in range(k1,numAtomTypes):
                    curStr = "Tangential Stiffness Between Types %i and %i: " % (k1+1, k2+1)
                    self.contactProps["kt"].append(hp.getNum(curStr))
            for k1 in range(numAtomTypes):
                for k2 in range(k1,numAtomTypes):
                    curStr = "Normal Damping Between Types %i and %i: " % (k1+1, k2+1)
                    self.contactProps["gamman"].append(hp.getNum(curStr))
            for k1 in range(numAtomTypes):
                for k2 in range(k1,numAtomTypes):
                    curStr = "Tangential Damping Between Types %i and %i: " % (k1+1, k2+1)
                    self.contactProps["gammat"].append(hp.getNum(curStr))
        
        if contactMod[:contactMod.find(" ")].strip() == 'jkr':
            self.contactProps["coefAdhesion"] = []
            for k1 in range(numAtomTypes):
                for k2 in range(k1,numAtomTypes):
                    curStr = "Coefficient of Adhesion Between Types %i and %i: " % (k1+1, k2+1)
                    self.contactProps["coefAdhesion"].append(hp.getNum(curStr))
            self.contactProps["jkrResolution"] = hp.getNum("Reselution in JKR interpolation table (1.0e-4): ")

    ## Has the user set the cohesion properties
    #
    #  @param cohesionMod A string that contains the cohesion model
    def getCohesionProps(self, cohesionMod):
        if cohesionMod == -1:
            return
        numAtomTypes = self.numMaterials
        cohesionMod = cohesionMod[cohesionMod.find(" "):].strip()

        if len(cohesionMod) == 0:
            return

        if cohesionMod == "easo/capillary/viscous" or cohesionMod == "washino/capillary/viscous":
            curStr = "Min Seperation Distance Ratio (Recommended = 1.01): "
            self.cohesionProps["minSeparationDistanceRatio"] = hp.getNum(curStr)

            curStr = "Max Seperation Distance Ratio (Recommended = 1.1): "
            self.cohesionProps["maxSeparationDistanceRatio"] = hp.getNum(curStr)

            curStr = "Initial Surface Liquid Content (%): "
            self.cohesionProps["surfaceLiquidContentInitial"] = hp.getNum(curStr)

            curStr = "Surface Tension (N/m): "
            self.cohesionProps["surfaceTension"] = hp.getNum(curStr)

            curStr = "Fluid Viscosity (Pascal-Second): "
            self.cohesionProps["fluidViscosity"] = hp.getNum(curStr)

            for k in range(numAtomTypes):
                curStr = "Contact Angle Between Type %i and Fluid: " % (k+1)
                self.cohesionProps["contactAngle"].append(hp.getNum(curStr))
            
            if cohesionMod == "":
                for k in range(numAtomTypes):
                    curStr = "Max Liquid Content of Type %i (0.0 to turn off): " % (k+1)
                    self.cohesionProps["maxLiquidContent"].append(hp.getNum(curStr))
        
        elif cohesionMod == "sjkr" or cohesionMod == "sjkr2":
            for k1 in range(numAtomTypes):
                for k2 in range(k1,numAtomTypes):
                    curStr = "Cohesion Energy Density Between Type %i and %i: " % (k1+1, k2+1)
                    self.cohesionProps["cohesionEnergyDensity"].append(hp.getNum(curStr))

    ## Has the user set the rolling properties
    #
    #  @param rollMod A string that contains the rolling model
    def getRollingProps(self, rollMod):
        if rollMod == -1:
            return
        numAtomTypes = self.numMaterials
        rollMod = rollMod[rollMod.find(" "):].strip()

        if len(rollMod) == 0:
            return

        self.rollingProps["coefficientRollingFriction"] = []
        for k1 in range(numAtomTypes):
            for k2 in range(k1,numAtomTypes):
                curStr = "Coef Rolling Friction Between Type %i and %i: " % (k1+1,k2+1)
                self.rollingProps["coefficientRollingFriction"].append(hp.getNum(curStr))
        if rollMod == "cdt" or rollMod == "epsd2":
            pass
        elif rollMod == "cdt_jkr":
            self.rollingProps["adhesionHysteresis"] = []
            for k1 in range(numAtomTypes):
                for k2 in range(k1,numAtomTypes):
                    curStr = "Coef Adhesion Hysteresis Between Type %i and %i: " % (k1+1,k2+1)
                    self.rollingProps["adhesionHysteresis"].append(hp.getNum(curStr))
        elif rollMod == "epsd" or rollMod == "epsd3":
            self.rollingProps["coefficientRollingViscousDamping"] = []
            for k1 in range(numAtomTypes):
                for k2 in range(k1,numAtomTypes):
                    curStr = "Coef Rolling Damping Between Type %i and %i: " % (k1+1,k2+1)
                    self.rollingProps["coefficientRollingViscousDamping"].append(hp.getNum(curStr))
            if rollMod == "epsd3":
                curStr = "Coef Rolling Stiffness: "
                self.rollingProps["coeffRollingStiffness"] = hp.getNum(curStr)
            
    ## Has the user choose the interaction model
    def getContactModel(self):
        conMod = "gran model "
        haveBeen = 0
        hp.clear()
        while True:        
            print("Current option:", conMod)
            print("Current Contact Models")
            print("1: Contact Model")
            print("2: Cohesion Model")
            print("3: Rolling Model")
            print("0: Go Back")
            
            opt = input("Option to use: ")
            hp.clear()
            if opt == "1" and haveBeen == 0:
                conMod += self.getContacts()
                haveBeen += 1
                hp.clear()
            elif opt == "2" and haveBeen == 1:
                conMod += self.getCohesions()
                haveBeen += 1
                hp.clear()
            elif opt == "3" and haveBeen == 2:
                conMod += self.getRolling()
                haveBeen += 1
                hp.clear()
            elif opt == "0":
                hp.clear()
                return conMod
            else:
                print("Bad Input: Must go in the order Contact Model -> Cohesion Model -> Rolling Model")
    
    ## Has the user choose the contact model
    def getContacts(self):
        hp.clear()
        while True:
            print("Current Contact Models")
            print("1: Hertz")
            print("2: Hooke")
            print("3: Hertz Stiffness")
            print("4: Hooke Stiffness")
            print("5: JKR")
            print("0: Go Back")
            opt = input("Option to use: ")
            hp.clear()
            if opt == "1":
                return "hertz tangential history "
            elif opt == "2":
                return "hooke tangential history "
            elif opt == "3":
                return "hertz/stiffness tangential history "
            elif opt == "4":
                return "hooke/stiffness tangential history "
            elif opt == "5":
                self.jkr_flag = True
                return "jkr tangential jkr_tan "
            elif opt == "0":
                return ""
            else:
                hp.clear()
                print("Bad Input")

    ## Has the user choose the cohesion model
    def getCohesions(self):
        hp.clear()
        if self.jkr_flag:
            print("Cannot have a cohesion model with jkr")
            input("Press enter to continue:")
            return ""
        while True:
            print("Current Cohession Models")
            print("1: easo/capillary/viscous")
            print("2: sjkr")
            print("3: sjkr2")
            print("4: washino/capillary/viscous")
            print("0: None")
            opt = input("Option to use: ")
            hp.clear()
            if opt == "1":
                return "cohesion easo/capillary/viscous "
            elif opt == "2":
                return "cohesion sjkr "
            elif opt == "3":
                return "cohesion sjkr2 "
            elif opt == "4":
                return "cohesion washino/capillary/viscous "
            elif opt == "0":
                return ""
            else:
                hp.clear()
                print("Bad Input")

    ## Has the user choose the rolling model
    def getRolling(self):
        hp.clear()
        while True:
            print("Current Rolling Models")
            if self.jkr_flag:
                print("1: cdt_jkr")
            else:
                print("1: cdt")
                print("2: epsd")
                print("3: epsd2")
                print("4: epsd3")
            print("0: None")
            opt = input("Option to use: ")
            hp.clear()
            if self.jkr_flag:
                if opt == "1":
                    return "rolling_friction cdt_jkr "
                elif opt == "0":
                    return ""
                else:
                    hp.clear()
                    print("Bad Input")
            else:    
                if opt == "1":
                    return "rolling_friction cdt "
                elif opt == "2":
                    return "rolling_friction epsd "
                elif opt == "3":
                    return "rolling_friction epsd2 "
                elif opt == "4":
                    return "rolling_friction epsd3 "
                elif opt == "0":
                    return ""
                else:
                    hp.clear()
                    print("Bad Input")

## Function to get the type of boundary from the user
#
#  @param outStr String that the user sees
def getBoundaryType(outStr):
    while True:
        b = input(outStr)
        if b in ['p','f']:
            return b
        print("Bad Input: Must be either p or f")
