import numpy as np
import helpers as hp
import matplotlib.pyplot as plt

class particle():
    def __init__(self):
        self.template = []
        self.renderLines = 16
        
    def getPartTemp(self):
        while True:
            print("Number of Templates Defined: " + str(len(self.template)))
            print("1: Define Particle Template")
            print("2: Update Particle Template")
            print("3: Delete Particle Template")
            # print("4: Optimize to stl")
            print("4: Load Template")
            print("5: Show Template")
            print("0: Go Back")

            opt = input("Option to use: ")
            hp.clear()
            if opt == '1':
                self.defineTemplate()
                hp.clear()
            elif opt == '2':
                self.updateTemplate()
                hp.clear()
            elif opt == '3':
                self.deleteTemplate()
                hp.clear()
            elif opt == '4':
                if (self.loadTemplate()):
                    hp.clear()
            elif opt == '5':
                self.showTemplate()
                hp.clear()
            elif opt == '0':
                return self.everythingDefined()
            else:
                print("Bad Option")

    def updateTemplate(self):
        hp.clear()
        while True:
            numTemplates = len(self.template)
            print("Select template to update (Total: %i)" % (numTemplates))

            for k in range(numTemplates):
                curTemp = self.template[k]
                curStr = "%i: Template Name [%s] with %i sphere(s)" % (k+1, curTemp.name, len(curTemp.atom))
                print(curStr)
            print("0: Go Back")

            opt = input("Option to use: ")
            hp.clear()
            if opt == "0":
                return
            try:
                opt = int(opt)
            except ValueError:
                print("Error: Input must be an integer")
                continue
            if int(opt) < 1 or int(opt) > numTemplates:
                print("Error: Input out of range")
            

    
    def loadTemplate(self):
        fileName = hp.getFileName('ANY_TYPE', "Select Particle Template From File")
        print("Loading file: " + fileName)
        with open(fileName, 'r') as f:
            lines = f.readlines()
        
        mol = molecule()
        mol.name = input("Name of particle: ")

        k = 0
        for line in lines:
            if k == 0:
                k+=1
                density = getNum(line.strip())
                if density is False:
                    return False
                mol.density = density
            else:
                singleAtom = getArray(line.strip(),4)
                if singleAtom[3] is np.False_:
                    return False
                mol.atom.append(singleAtom)
        self.template.append(mol)
        return True

    
    def deleteTemplate(self):
        hp.clear()
        while True:
            numTemplates = len(self.template)
            print("Select template to delete (Total: %i)" % (numTemplates))

            for k in range(numTemplates):
                curTemp = self.template[k]
                curStr = "%i: Template Name [%s] with %i sphere(s)" % (k+1, curTemp.name, len(curTemp.atom))
                print(curStr)
            print("0: Go Back")

            opt = input("Option to use: ")
            hp.clear()
            if opt == "0":
                return
            try:
                opt = int(opt)
            except ValueError:
                print("Error: Input must be an integer")
                continue
            if int(opt) < 1 or int(opt) > numTemplates:
                print("Error: Input out of range")
            self.template.pop(opt-1)

    def showTemplate(self):
        hp.clear()
        numTemplates = len(self.template)
        if numTemplates == 0:
            print("No templates to render...")
            return
        while True:
            for k in range(numTemplates):
                curTemp = self.template[k]
                curStr = "%i: Template Name [%s] with %i sphere(s)" % (k+1, curTemp.name, len(curTemp.atom))
                print(curStr)
            print("0: Go Back")

            opt = input("Option to use: ")
            hp.clear()
            if opt == "0":
                return
            try:
                opt = int(opt)
            except ValueError:
                print("Error: Input must be an integer")
                continue
            if int(opt) < 1 or int(opt) > numTemplates:
                print("Error: Input out of range")
            temp = self.template[int(opt)-1]

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            u = np.linspace(0.0,2.0*np.pi,self.renderLines)
            v = np.linspace(0.0,np.pi,self.renderLines)
            cosu = np.cos(u)
            sinu = np.sin(u)
            cosv = np.cos(v)
            sinv = np.sin(v)
            oneSizeU = np.ones(np.size(u))
            bounds = None
            for atom in temp.atom:
                x = atom[3]*np.outer(cosu, sinv) + atom[0]
                y = atom[3]*np.outer(sinu, sinv) + atom[1]
                z = atom[3]*np.outer(oneSizeU, cosv) + atom[2]
                ax.plot_surface(x,y,z,color='yellow')
                if bounds == None:
                    bounds = [
                        atom[0]-atom[3], atom[0]+atom[3],
                        atom[1]-atom[3], atom[1]+atom[3],
                        atom[2]-atom[3], atom[2]+atom[3]
                    ]
                else:
                    bounds = [
                        min([atom[0]-atom[3], bounds[0]]), max([atom[0]+atom[3], bounds[1]]),
                        min([atom[1]-atom[3], bounds[2]]), max([atom[1]+atom[3], bounds[3]]),
                        min([atom[2]-atom[3], bounds[4]]), max([atom[2]+atom[3], bounds[5]])
                    ]
            dB = max([bounds[1]-bounds[0], bounds[3]-bounds[2], bounds[5]-bounds[4]])
            ax.set_xlim3d([bounds[0], bounds[0] + dB])
            ax.set_ylim3d([bounds[2], bounds[2] + dB])
            ax.set_zlim3d([bounds[4], bounds[4] + dB])
            plt.show()

    def getMaxRadius(self):
        maxR = 0.0
        numTemplates = len(self.template)
        for k in range(numTemplates):
            temp = self.template[k]
            for atom in temp.atom:
                if atom[-1] > maxR:
                    maxR = atom[-1]
        return maxR

    def getMinRadius(self):
        minR = 1.0e9
        numTemplates = len(self.template)
        for k in range(numTemplates):
            temp = self.template[k]
            for atom in temp.atom:
                if atom[-1] < minR:
                    minR = atom[-1]
        return minR
        
    def defineTemplate(self):
        hp.clear()
        while True:
            numAtoms = int(hp.getNum("Number of spheres in template: "))
            if numAtoms < 1:
                print("Error: Must have at least one sphere in template")
            else:
                break
        mol = molecule()
        mol.name = input("Name of Particle: ")
        mol.density = hp.getNum("Density of Particle: ")
        for k in range(numAtoms):
            print("Sphere ", k+1)
            x = hp.getNum("x pos: ")
            y = hp.getNum("y pos: ")
            z = hp.getNum("z pos: ")
            r = hp.getNum("Radius of sphere: ")
            mol.atom.append([x,y,z,r])
        self.template.append(mol)
        hp.clear()

    
    def everythingDefined(self):
        return True

class molecule():
    def __init__(self):
        self.name = ""
        self.density = 0.0
        self.atom = []

def getNum(curStr):
    try:
        num = float(curStr)
    except ValueError:
        print("Error: Bad file input")
        print("Tried to make a single number from")
        print(curStr)
        return False
    return num


def getArray(curStr, arrSize):
    curStr = curStr.replace(',', ' ')
    curStr = curStr.strip()
    arrList = curStr.split()
    if len(arrList) != arrSize:
        return np.full(arrSize,False)
    arrValue = []
    for v in arrList:
        val = getNum(v)
        if val is False:
            return np.full(arrSize,False)
        arrValue.append(val)
    return arrValue
