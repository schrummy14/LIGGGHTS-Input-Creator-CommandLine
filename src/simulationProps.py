import types
import helpers as hp
class properties():
    def __init__(self):
        self.atomType = "sphere"
        self.numMaterials = 0
        self.numBondTypes = 0
        self.maxBondsPerAtom = 0
        self.contactModel = {
            "p2p": "",
            "p2w": ""
        }
        self.bondModel = {
            "p2p": ""
        }
        self.boundaries = {
            "x": [0.0, 0.0, "f"],
            "y": [0.0, 0.0, "f"],
            "z": [0.0, 0.0, "f"]
        }

        self.contactProps = {
            "kn": [],
            "kt": [],
            "gammaN": [],
            "gammaT": [],
            "characteristicVelocity": 0.0,
            "youngsModulus": [],
            "poissonsRatio": [],
            "coefRestitution": [],
            "coefFriction": []
        }

        self.bondProps = {
            "YoungsModulus": 0.0,
            "PoissonsRatio": 0.0
        }
        
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

        self.rollingProps = {
            "coefficientRollingFriction": [],
            "coefficientRollingViscousDamping": [],
            "coeffRollingStiffness": 0.0
        }

   
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
        for ob in curObs:
            if type(vars(self)[ob]) is int:
                if vars(self)[ob] == 0:
                    print("Simulation Property [" + ob + "] Still Needs To Be Set...")
                    return False    
            elif len(vars(self)[ob]) == 0:
                print("Simulation Property [" + ob + "] Still Needs To Be Set...")
                return False
        return True

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
        
    def setSimBoundaries(self):
        hp.clear()
        while True:
            print("Select Boundary Info")
            print("1: Boundary Types")
            print("2: Boundary Size")
            print("3: Go Back")
            opt = input("Option to use: ")
            hp.clear()
            if opt == "1":
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
                hp.clear()
                return
            else:
                print("Bad Input...")

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

    def getContactProps(self, contactMod):
        if contactMod == -1:
            return
        numAtomTypes = self.numMaterials
        contactMod = contactMod[contactMod.find(" "):].strip()

        if len(contactMod) == 0:
            return

        for k in range(numAtomTypes):
            curStr = "Contact Young's Modulus for Type %i: " % (k+1)
            self.contactProps["youngsModulus"].append(hp.getNum(curStr))
        
        for k in range(numAtomTypes):
            curStr = "Contact Poisson's Ratio for Type %i: " % (k+1)
            self.contactProps["poissonsRatio"].append(hp.getNum(curStr))

        for k1 in range(numAtomTypes):
            for k2 in range(k1,numAtomTypes):
                curStr = "Coefficient of Restitution Between Types %i and %i: " % (k1+1, k2+1)
                self.contactProps["coefRestitution"].append(hp.getNum(curStr))
        
        for k1 in range(numAtomTypes):
            for k2 in range(k1,numAtomTypes):
                curStr = "Coefficient of Friction Between Types %i and %i: " % (k1+1, k2+1)
                self.contactProps["coefFriction"].append(hp.getNum(curStr))

        if contactMod == "hooke" or contactMod == "hooke/stiffness":
            curStr = "Characteristic Velocity: "
            self.contactProps["characteristicVelocity"] = hp.getNum(curStr)

        if contactMod == "hertz/stiffness" or contactMod == "hooke/stiffness":
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


    def getRollingProps(self, rollMod):
        if rollMod == -1:
            return
        numAtomTypes = self.numMaterials
        rollMod = rollMod[rollMod.find(" "):].strip()

        if len(rollMod) == 0:
            return

        for k1 in range(numAtomTypes):
            for k2 in range(k1,numAtomTypes):
                curStr = "Coef Rolling Friction Between Type %i and %i: " % (k1+1,k2+1)
                self.rollingProps["coefficientRollingFriction"].append(hp.getNum(curStr))
        if rollMod == "cdt" or rollMod == "epsd2":
            pass
        elif rollMod == "epsd" or rollMod == "epsd3":
            for k1 in range(numAtomTypes):
                for k2 in range(k1,numAtomTypes):
                    curStr = "Coef Rolling Damping Between Type %i and %i: " % (k1+1,k2+1)
                    self.rollingProps["coefficientRollingViscousDamping"].append(hp.getNum(curStr))
            if rollMod == "epsd3":
                curStr = "Coef Rolling Stiffness: "
                self.rollingProps["coeffRollingStiffness"] = hp.getNum(curStr)
            
    def getContactModel(self):
        conMod = "gran model "
        haveBeen = 0
        hp.clear()
        while True:        
            print("Current Contact Models")
            print("1: Contact Model")
            print("2: Cohesion Model")
            print("3: Rolling Model")
            print("0: Go Back")
            
            opt = input("Option to use: ")
            hp.clear()
            if opt == "1" and haveBeen < 1:
                conMod += self.getContacts()
                haveBeen += 1
                hp.clear()
            elif opt == "2" and haveBeen < 2:
                conMod += self.getCohesions()
                haveBeen += 1
                hp.clear()
            elif opt == "3" and haveBeen < 3:
                conMod += self.getRolling()
                haveBeen += 1
                hp.clear()
            elif opt == "0":
                hp.clear()
                return conMod
            else:
                print("Bad Input")
    
    def getContacts(self):
        hp.clear()
        while True:
            print("Current Contact Models")
            print("1: Hertz")
            print("2: Hooke")
            print("3: Hertz Stiffness")
            print("4: Hooke Stiffness")
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
            elif opt == "0":
                return 
            else:
                hp.clear()
                print("Bad Input")

    def getCohesions(self):
        hp.clear()
        while True:
            print("Current Cohession Models")
            print("1: easo/capillary/viscous")
            print("2: sjkr")
            print("3: sjkr2")
            print("4: washino/capillary/viscous")
            print("0: Go Back")
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
                return 
            else:
                hp.clear()
                print("Bad Input")


    def getRolling(self):
        hp.clear()
        while True:
            print("Current Rolling Models")
            print("1: cdt")
            print("2: epsd")
            print("3: epsd2")
            print("4: epsd3")
            print("0: Go Back")
            opt = input("Option to use: ")
            hp.clear()
            if opt == "1":
                return "rolling_friction cdt "
            elif opt == "2":
                return "rolling_friction epsd "
            elif opt == "3":
                return "rolling_friction epsd2 "
            elif opt == "4":
                return "rolling_friction epsd3 "
            elif opt == "5":
                return 
            else:
                hp.clear()
                print("Bad Input")
                



def getBoundaryType(outStr):
    while True:
        b = input(outStr)
        if b in ['p','f']:
            return b
        print("Bad Input: Must be either p or f")