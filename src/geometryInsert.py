"""
Builds the geometries used in the simulation
"""
import os
import stl
import copy
import math
import numpy as np
import helpers as hp
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

## Main Geometry Class
class geometryInsert():
    ## Initialization
    def __init__(self):
        ## An array that holds the name of each figure name for plotting
        self.figureName = []

        ## An array that holds the name of each axis name for plotting
        self.axisName = []

        ## An array that holds the name for each stl geometry
        self.stlFiles = []

        ## An array that holds the name of each primitive geometry
        self.primitives = []

    ## Options to be shown to the user
    def getGeomOpts(self):
        # hp.clear()
        while True:
            print("Geometry Input")
            print("Number of Geometries: " + str(len(self.stlFiles)))
            print("1: Add Geometry")
            print("2: Build Geometry")
            print("3: Update Geometry")
            print("4: Render Geometries")
            print("5: Delete Geometry")
            print("0: Back to Main")
            opt = input("Option to use: ")
            hp.clear()
            if opt == "1":
                self.makeGeom()
                # self.makeSTL()
            elif opt == "2":
                print("Not Done")
            elif opt == "3":
                self.updateGeom()
            elif opt == "4":
                self.render()
            elif opt == "5":
                self.delGeom()
            elif opt == "0":
                break
            else:
                hp.clear()
                print("Bad Option")
        return True

    ## Asks the user what type of geometry they would like to add
    def makeGeom(self):
        while True:
            print("1: Geometry from file")
            print("2: Primitive Geometry")
            # print("3: Create Geometry")
            print("0: Go Back")
            opt = input("Geometry Options: ")
            hp.clear()
            if opt == '1':
                self.makeSTL()
            elif opt == '2':
                self.makePrimitive()
            elif opt == '0':
                return
            else:
                print("Bad Option")

    ## Creates the string that determins how many steps pass before each file write
    #
    #  @param file_steps The number of steps between each file write
    def writeDumpOptions(self,file_steps):
        curStr = ''
        for f in self.stlFiles:
            curStr += "\ndump dmp_%s all mesh/vtk %i post/stl_%s_*.vtk stress stresscomponents %s" % (
                f.name,
                file_steps,
                f.name,
                f.name
            )
        return curStr

    ## Creates the string to generate the geometry via a stl file
    #
    #  @param p2w The contact model being used (same as p2p)
    def writeGeometryProps(self,p2w):
        curStr = ''
        if len(self.stlFiles) > 0 or len(self.primitives) > 0:
            curStr = "\n# Insert Geometry and Factory"
        if len(self.stlFiles) > 0:
            meshNames = ''
            for mesh in self.stlFiles:
                meshNames += ' %s' % (mesh.name)
                curStr += "\nfix %s all mesh/surface/stress file %s type %i scale %e rotate axis %e %e %e angle %e move %e %e %e curvature_tolerant yes" % (
                    mesh.name,
                    mesh.fileLocation,
                    mesh.matType,
                    mesh.orgScale,
                    mesh.orgRotate[0],mesh.orgRotate[1],mesh.orgRotate[2],mesh.orgRotate[3],
                    mesh.orgMove[0],mesh.orgMove[1],mesh.orgMove[2]
                )
            curStr += "\nfix geo_walls all wall/gran model %s mesh n_meshes %i meshes%s" % (p2w, len(self.stlFiles), meshNames)

        for mesh in self.primitives:
            curStr += "\nfix %s all wall/gran model %s primitive type %i %s %e" %(
                mesh.name,
                p2w,
                mesh.matType,
                mesh.xyzPlane,
                mesh.value
            )
        return curStr

    ## Deletes a geometry
    def delGeom(self):
        hp.clear()
        numStlFiles = len(self.stlFiles)
        if numStlFiles == 0:
            print("No Files to Delete...")
            return
        while True:
            print("Available STLs to Delete:")
            for k in range(len(self.stlFiles)):
                print(str(k+1) + ": " + self.stlFiles[k].name)
            print("")
            print("0: Go Back")
            opt = input("Option to use: ")
            hp.clear()
            if opt == "0":
                return
            try:
                opt = int(opt)
            except:
                print("Option must be an integer...")
                continue
            if opt > numStlFiles:
                print("Bad Option")
                continue
            break
        self.stlFiles.pop(opt-1)

    ## Lets the user update a geometry
    def updateGeom(self):
        numStlFiles = len(self.stlFiles)
        if numStlFiles == 0:
            print("No Files to Update...")
            return
        while True:
            print("Available STLs to Update:")
            for k in range(len(self.stlFiles)):
                print(str(k+1) + ": " + self.stlFiles[k].name)
            print("")
            print("0: Go Back")
            opt = input("Option to use: ")
            hp.clear()
            if opt == "0":
                return
            try:
                opt = int(opt)
            except:
                print("Option must be an integer...")
                continue
            if opt > numStlFiles:
                print("Bad Option")
                continue
            break

        oldVal = self.stlFiles[opt-1].orgScale
        while True:
            scale = hp.getNum("Scaling to use for file (Was " + str(oldVal) + "): ")
            if scale < 0.0:
                print("scale must be greater than 0.0...")
            else:
                break
        
        oldVal = self.stlFiles[opt-1].orgMove
        mx = hp.getNum("Move Geom in x (Was " + str(oldVal[0]) + "): ")
        my = hp.getNum("Move Geom in y (Was " + str(oldVal[1]) + "): ")
        mz = hp.getNum("Move Geom in z (Was " + str(oldVal[2]) + "): ")
            
        oldVal = self.stlFiles[opt-1].orgRotate    
        rx = hp.getNum("Rotate Geom in x (Was " + str(oldVal[0]) + "): ")
        ry = hp.getNum("Rotate Geom in y (Was " + str(oldVal[1]) + "): ")
        rz = hp.getNum("Rotate Geom in z (Was " + str(oldVal[2]) + "): ")
        rv = hp.getNum("Rotate Geom by (Deg) (Was " + str(oldVal[3]) + "): ")
        
        newSTL = stlOb(
            name = self.stlFiles[opt-1].name,
            stlMesh = self.stlFiles[opt-1].orgMesh,
            move = (mx,my,mz),
            rotate = (rx,ry,rz,rv),
            scale = scale,
            fileLocation = self.stlFiles[opt-1].fileLocation,
            stlObject = self.stlFiles[opt-1].stlObject)
        self.stlFiles[opt-1] = newSTL   
        hp.clear()     

    ## Creates a primitive geometry
    def makePrimitive(self):
        while True:
            primName = input("Name of STL file: ")
            foundName = False
            for k in range(len(self.primitives)):
                if primName == self.primitives[k].name:
                    print("Error: Name must be unique")
                    foundName = True
                    break
            if not foundName:
                break
        while True:
            axis = input("Select axis for primitive (x or y or z): ")
            if axis in ['x','y','z']:
                break
            else:
                print("bad input")
        matType = int(hp.getNum("Material Type: "))
        walLocation = hp.getNum("Location of primitivie: ")

        myPrim = primOb(
        name = primName,
        matType = matType,
        xyzPlane = axis,
        value = walLocation
        )

        self.primitives.append(myPrim)

        return

    ## Creates a geometry from an stl file
    def makeSTL(self):
        # Get filename
        fileName = hp.getFileName(['stl', 'STL'], "Path to STL file:")
        while True:
            stlName = input("Name of STL file: ")
            foundName = False
            for k in range(len(self.stlFiles)):
                if stlName == self.stlFiles[k].name:
                    print("Error: Name must be unique")
                    foundName = True
                    break
            if not foundName:
                break
                
        while True:
            scale = hp.getNum("Scaling to use for file: ")
            if scale < 0.0:
                print("scale must be greater than 0.0...")
            break
        mx = hp.getNum("Move Geom in x: ")
        my = hp.getNum("Move Geom in y: ")
        mz = hp.getNum("Move Geom in z: ")

        rx = hp.getNum("Rotate Geom in x: ")
        ry = hp.getNum("Rotate Geom in y: ")
        rz = hp.getNum("Rotate Geom in z: ")
        rv = hp.getNum("Rotate Geom by (Deg): ")

        matType = int(hp.getNum("Material Type: "))

        if rv == 0:
            rx = 0.0
            ry = 0.0
            rz = 1.0

        self.addSTL(
            fileName = fileName, 
            scale = scale, 
            move = (mx,my,mz), 
            rotate = (rx,ry,rz,rv),
            name = stlName,
            matType = matType)
        hp.clear()

    ## Adds an stl geometry to the geometry list
    #
    #  @param fileName
    #  @param stlObject
    #  @param scale
    #  @param move
    #  @param rotate
    #  @param name
    #  @param matType
    def addSTL(self, 
        fileName = [], 
        stlObject = [], 
        scale = 1.0, 
        move = (0.0, 0.0, 0.0),
        rotate = (0.0, 0.0, 0.0, 0.0),
        name = 'stl',
        matType = 1
        ):
        if len(fileName) > 0 and len(stlObject) > 0:
            print("Cannot give both a filename and a stl object")
        if len(fileName) > 0:
            print("Reading in stl file: " + fileName)
            try:
                stlMesh = stl.mesh.Mesh.from_file(fileName)
            except:
                with open(fileName) as f:
                    stlMesh = stl.read_ascii_file(f)
        if name == 'stl':
            name+=str(len(self.stlFiles))
        newSTL = stlOb(
            name = name,
            matType = matType,
            stlMesh = stlMesh,
            move = move,
            rotate = rotate,
            scale = scale,
            fileLocation = fileName,
            stlObject = stlObject)
        self.stlFiles.append(newSTL)

    
    ## Renders all currently loaded/created meshes.
    #  We currently only plot the wire frames due to
    #  addcollection3d causing artifacts that make it
    #  not always show a connected polygon.
    #  @param bounds Is used to bound the image. If no
    #  bounds is given, we take the min/max of all
    #  currently drawn meshes as the bounds.
    def render(self, bounds = None):
        # Check that there is something to draw...
        if len(self.stlFiles) == 0:
            print("No STL files to render...")
            return
        # Get figure names and axes names
        self.figureName = plt.figure()
        self.axisName = mplot3d.Axes3D(self.figureName)
        
        # Check if we need to find the bounds
        if bounds == None:
            getBounds = True
            bounds = np.array([np.inf, -np.inf, np.inf, -np.inf, np.inf, -np.inf])
        else: 
            getBounds = False
        
        # Load the STL files and add the vectors to the plot
        for mesh in self.stlFiles:
            # axes.add_collection3d(
            #     mplot3d.art3d.Poly3DCollection(
            #         mesh.vectors, 
            #         linewidths = 1, 
            #         edgecolors = 'black',
            #         facecolors = 'blue')
            # )

            # Draw each triangle to generate a wire frame
            for vec in mesh.vectors:
                v0 = [vec[0,0], vec[1,0], vec[2,0], vec[0,0]]
                v1 = [vec[0,1], vec[1,1], vec[2,1], vec[0,1]]
                v2 = [vec[0,2], vec[1,2], vec[2,2], vec[0,2]]
                if getBounds:
                    curMinX = np.min(v0)
                    curMaxX = np.max(v0)
                    curMinY = np.min(v1)
                    curMaxY = np.max(v1)
                    curMinZ = np.min(v2)
                    curMaxZ = np.max(v2)
                    if curMinX < bounds[0]:
                        bounds[0] = curMinX
                    if curMinY < bounds[2]:
                        bounds[2] = curMinY
                    if curMinZ < bounds[4]:
                        bounds[4] = curMinZ
                    if curMinX > bounds[1]:
                        bounds[1] = curMaxX
                    if curMinY > bounds[3]:
                        bounds[3] = curMaxY
                    if curMinZ > bounds[5]:
                        bounds[5] = curMaxZ
                self.axisName.plot(v0,v1,v2, color = 'black', linewidth = 2)

        # Keep the aspect of the meshes correct
        db0 = bounds[1]-bounds[0]
        db1 = bounds[3]-bounds[2]
        db2 = bounds[5]-bounds[4]
        db = np.max(np.array([db0,db1,db2]))
        self.axisName.set_xlim(bounds[0], bounds[0] + db)
        self.axisName.set_ylim(bounds[2], bounds[2] + db)
        self.axisName.set_zlim(bounds[4], bounds[4] + db)
        plt.show()

## Primitive Geometry Class
#
#  @param name Unique name of the primitive geometry
#  @param matType Material type that should be used
#  @param xyzPlane What plane the primitive should be in
#  @param value The x, y, or z value that the primtive should be placed at
class primOb():
    ## Initialization
    def __init__(
        self,
        name,
        matType,
        xyzPlane,
        value
        ):
        ## Unique name of the primitive geometry
        self.name = name
        
        ## Material type that should be used
        self.matType = matType
        
        ## What plane the primitive should be in
        self.xyzPlane = xyzPlane

        ## The x, y, or z value that the primtive should be placed at
        self.value = value

## STL Geometry Class
#
#  @param stlMesh The stl mesh
#  @param move How the stl file should be moved
#  @param rotate How the stl file should be rotated
#  @param scale How the stl file should be scaled
#  @param name The name of the stl geometry
#  @param matType The material type that should be used for the geometry
#  @param fileLocation Where is the stl file located
#  @param stlObject A custome stl geometry created by the user
class stlOb():
    ## Initialization
    def __init__(
        self, 
        stlMesh, 
        move = (0.0, 0.0, 0.0), 
        rotate = (0.0, 0.0, 0.0, 0.0),
        scale = 1.0,
        name = None,
        matType = int(1),
        fileLocation = "",
        stlObject = []
        ):
        
        ## The original mesh
        self.orgMesh = copy.deepcopy(stlMesh)
        # Scale the mesh by scale
        stlMesh.vectors *= scale
        # Rotate the mesh
        stlMesh.rotate((rotate[0],rotate[1],rotate[2]), theta = math.radians(rotate[3]))
        # Move the mesh
        stlMesh.x += move[0]
        stlMesh.y += move[1]
        stlMesh.z += move[2]

        # Save everything along with original parameters
        ## Original Node locations
        self.vectors = stlMesh.vectors

        ## The name of the stl
        self.name = name

        ## The material type
        self.matType = matType

        ## The original move values
        self.orgMove = move

        ## The original rotate values
        self.orgRotate = rotate

        ## The original scale value
        self.orgScale = scale

        ## The file location for the stl file
        self.fileLocation = fileLocation

        ## The stl object
        self.stlObject = stlObject
