from particleTemplate import particle as pT
from geometryInsert import geometryInsert as gI
from simulationProps import properties as sP
import helpers as hp

props = sP()
geom = gI()
temp = pT()

temp.getPartTemp()

# geom.getGeomOpts()


# geom.addSTL(
#     fileName='tester/STL/ShearBox_BottomHalf.STL',
#     scale=0.001,name='bottomhalfSTL'
# )
# geom.addSTL(
#     fileName='tester/STL/ShearBox_BottomHalf.STL',
#     scale=0.001,name='tophalfSTL',move=(0.0,0.0,0.030)
# )
# geom.addSTL(
#     fileName='tester/STL/ShearBox_TopPlate.STL',
#     scale=0.001,name='bottomplateSTL'
# )
# geom.addSTL(
#     fileName='tester/STL/ShearBox_TopPlate.STL',
#     scale=0.001,name='topplateSTL',
#     move=(0.0,0.1014,0.100),rotate=(1.0,0.0,0.0,180.0)
# )
# geom.render()