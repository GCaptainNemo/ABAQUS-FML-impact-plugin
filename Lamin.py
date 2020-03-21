from abaqus import *
from abaqusConstants import *
# coding=utf-8
import __main__

import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior


def Test(Long_Whole, Width_Whole, Mesh_Size_Whole, Long_Center, Width_Center,
         Mesh_Size_Center, Radius, Speed,
         Mesh_Size_Impact, Metal_name, polymer_name, Stack, Friction_Coef,
         Total_Time, SDVn, SDVd):
    Long_Half = Long_Whole / 2.0
    Long_Quarter = Long_Half / 2.0
    Width_Half = Width_Whole / 2.0
    Width_Quarter = Width_Half / 2.0

    Long_Center_Half = Long_Center / 2.0
    Long_Center_Quarter = Long_Center / 4.0

    Width_Center_Half = Width_Center / 2.0
    Width_Center_Quarter = Width_Center / 4.0

    L_W_L_C_Q = Long_Quarter + Long_Center_Quarter
    W_W_W_C_Q = Width_Quarter + Width_Center_Quarter

    Speed = -1.0 * Speed
    Layers = len(Stack)

    Thick_Layer = []
    Thick_Layer_Half = []

    tmp_list = []
    tmp_num = 0
    Thick_Whole = 0

    for i in range(0, Layers):
        tmp_num = 0
        Thick_Whole = Thick_Whole + Stack[i][2]
        if i > 0:
            for j in range(0, i):
                tmp_num = tmp_num + Stack[j][2]
        Thick_Layer.append(tmp_num + Stack[i][2])
        Thick_Layer_Half.append(tmp_num + Stack[i][2] / 2.0)

    Thick_Half = Thick_Whole / 2.0
    Thick_Layer_Half = tuple(Thick_Layer_Half)
    Thick_Layer = tuple(Thick_Layer)

    ####Part()
    ##Create Plate
    # Sktech
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    s.setPrimaryObject(option=STANDALONE)

    s.rectangle(point1=(0.0, 0.0), point2=(Long_Half, Width_Half))  ##--

    p = mdb.models['Model-1'].Part(name='Plate', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Plate']
    # Extrusion
    p.BaseSolidExtrude(sketch=s, depth=Thick_Whole)  # --

    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']

    ##Partition
    # Layer Sketch
    f = p.faces.findAt((Long_Quarter, 0, Thick_Half))  ##--
    e = p.edges.findAt((Long_Half, 0, Thick_Half))  ##--
    t = p.MakeSketchTransform(sketchPlane=f, sketchUpEdge=e, sketchPlaneSide=SIDE1, origin=(0, 0, 0))

    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=100, gridSpacing=5, transform=t)
    s.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)

    for i in range(0, Layers - 1):
        s.Line(point1=(0, Thick_Layer[i]), point2=(Long_Half, Thick_Layer[i]))  ##--
    p.PartitionFaceBySketch(sketchUpEdge=e, faces=f, sketch=s)

    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']

    # Layer Partition
    e = p.edges
    c = p.cells
    for i in range(0, Layers - 1):
        p.PartitionCellByExtrudeEdge(line=e.findAt((0, Width_Quarter / 3.0, Thick_Whole)),
                                     cells=c.findAt((Long_Quarter, Width_Half, Thick_Whole)),
                                     edges=p.edges.findAt((Long_Quarter, 0, Thick_Layer[i])), sense=FORWARD)  ####---

    # Focus Area Sketch
    f = p.faces.findAt((Long_Quarter, Width_Quarter, Thick_Whole))  ##--
    e = p.edges.findAt((Long_Half, Width_Quarter, Thick_Whole))  ##--
    t = p.MakeSketchTransform(sketchPlane=f, sketchUpEdge=e, sketchPlaneSide=SIDE1, origin=(0, 0, Thick_Whole))  # -

    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=150, gridSpacing=3, transform=t)
    s.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)

    s.Line(point1=(0.0, Width_Center_Half), point2=(Long_Center_Half, Width_Center_Half))  ##--
    s.Line(point1=(Long_Center_Half, Width_Center_Half), point2=(Long_Center_Half, 0))  ##--

    p.PartitionFaceBySketch(sketchUpEdge=e, faces=f, sketch=s)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']

    p.ReferencePoint(point=(0, 0, Thick_Whole))  # --
    mdb.models['Model-1'].parts['Plate'].features.changeKey(fromName='RP', toName='Plate')

    # Focus Area Partition
    c = p.cells
    e = p.edges
    pickedEdges = (e.findAt((Long_Center_Quarter, Width_Center_Half, Thick_Whole)),
                   e.findAt((Long_Center_Half, Width_Center_Quarter, Thick_Whole)))  ##--
    tmp_num = float(Stack[0][2]) / 4.0
    p.PartitionCellByExtrudeEdge(line=e.findAt((0.0, 0.0, tmp_num)), cells=c, edges=pickedEdges,
                                 sense=REVERSE)  #######---

    ##Create Impact Head
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=30.0)
    g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -15.0), point2=(0.0, 15.0))

    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(Radius, 0.0), point2=(0.0, Radius), direction=COUNTERCLOCKWISE)  # -
    s.Line(point1=(0.0, Radius), point2=(0.0, 0.0))  # -
    s.Line(point1=(0.0, 0.0), point2=(Radius, 0.0))  # -

    p = mdb.models['Model-1'].Part(name='Impact Head', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Impact Head']
    p.BaseSolidRevolve(sketch=s, angle=90.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']

    p.ReferencePoint(point=(0.0, 0.0, Radius))  # -
    mdb.models['Model-1'].parts['Impact Head'].features.changeKey(fromName='RP', toName='Impact Head')
    r = p.referencePoints
    refPoints = (r[2],)
    p.Set(referencePoints=refPoints, name='Impact Head')

    ##Create Support Up
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    s.setPrimaryObject(option=STANDALONE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(38.0, 0.0), point2=(0.0, 38.0), direction=COUNTERCLOCKWISE)

    s.Line(point1=(38.0, 0.0), point2=(60.0, 0.0))  # C
    s.Line(point1=(60.0, 0.0), point2=(60.0, 60.0))  # C
    s.Line(point1=(60.0, 60.0), point2=(0.0, 60.0))  # C
    s.Line(point1=(0.0, 60.0), point2=(0.0, 38.0))  # C

    p = mdb.models['Model-1'].Part(name='Support Up', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Support Up']
    p.BaseSolidExtrude(sketch=s, depth=1.0)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']

    p.ReferencePoint(point=(60.0, 30.0, 1.0))
    mdb.models['Model-1'].parts['Support Up'].features.changeKey(fromName='RP', toName='Support Up')
    r = p.referencePoints
    refPoints = (r[2],)
    p.Set(referencePoints=refPoints, name='Support Up')

    ##Creative Support_Down
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    s.setPrimaryObject(option=STANDALONE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(38.0, 0.0), point2=(0.0, 38.0), direction=COUNTERCLOCKWISE)

    s.Line(point1=(38.0, 0.0), point2=(60.0, 0.0))
    s.Line(point1=(60.0, 0.0), point2=(60.0, 60.0))
    s.Line(point1=(60.0, 60.0), point2=(0.0, 60.0))
    s.Line(point1=(0.0, 60.0), point2=(0.0, 38.0))

    p = mdb.models['Model-1'].Part(name='Support Down', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Support Down']
    p.BaseSolidExtrude(sketch=s, depth=1.0)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']

    p.ReferencePoint(point=(60.0, 30.0, 0.0))
    mdb.models['Model-1'].parts['Support Down'].features.changeKey(fromName='RP', toName='Support Down')
    r = p.referencePoints
    refPoints = (r[2],)
    p.Set(referencePoints=refPoints, name='Support Down')

    ###Assemble()
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['Impact Head']
    a.Instance(name='Impact Head', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['Plate']
    a.Instance(name='Plate', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['Support Down']
    a.Instance(name='Support Down', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['Support Up']
    a.Instance(name='Support Up', part=p, dependent=ON)

    a.translate(instanceList=('Support Up',), vector=(0.0, 0.0, Thick_Whole))  # -

    a.translate(instanceList=('Support Down',), vector=(0.0, 0.0, -1.0))

    a.rotate(instanceList=('Impact Head',), axisPoint=(0.0, 0.0, 0.0), axisDirection=(1.0, 0.0, 0.0), angle=-180.0)
    a.rotate(instanceList=('Impact Head',), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=90.0)

    a.translate(instanceList=('Impact Head',), vector=(0.0, 0.0, Radius + Thick_Whole))  ##--

    ##Property()
    ## Material Property
    # Rigid
    mdb.models['Model-1'].Material(name='Rigid')
    mdb.models['Model-1'].materials['Rigid'].Density(table=((1.019e-05, ), ))
    mdb.models['Model-1'].materials['Rigid'].Elastic(table=((1, 0.3), ))
    #

    ##Section
    mdb.models['Model-1'].HomogeneousSolidSection(name='Rigid', material='Rigid', thickness=None)
    mdb.models['Model-1'].HomogeneousSolidSection(name=Metal_name, material=Metal_name, thickness=None)
    mdb.models['Model-1'].HomogeneousSolidSection(name=polymer_name, material=polymer_name, thickness=None)

    ##Assign
    p = mdb.models['Model-1'].parts['Impact Head']
    cells = p.cells.getSequenceFromMask(mask=('[#1 ]',), )
    region = regionToolset.Region(cells=cells)
    p.SectionAssignment(region=region, sectionName='Rigid', offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)

    p = mdb.models['Model-1'].parts['Support Down']
    cells = p.cells.getSequenceFromMask(mask=('[#1 ]',), )
    region = regionToolset.Region(cells=cells)
    p = mdb.models['Model-1'].parts['Support Down']
    p.SectionAssignment(region=region, sectionName='Rigid', offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)

    p = mdb.models['Model-1'].parts['Support Up']
    cells = p.cells.getSequenceFromMask(mask=('[#1 ]',), )
    region = regionToolset.Region(cells=cells)
    # p = mdb.models['Model-1'].parts['Support Up']
    p.SectionAssignment(region=region, sectionName='Rigid', offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)

    p = mdb.models['Model-1'].parts['Plate']
    c = p.cells
    for i in range(0, Layers):
        if (Stack[i][0] == True and Stack[i][1] == False):
            cells = c.findAt(((Long_Center_Quarter, Width_Center_Quarter, Thick_Layer_Half[i]),))  ####-
            region = regionToolset.Region(cells=cells)
            p.SectionAssignment(region=region, sectionName=Metal_name, offset=0.0,
                                offsetType=MIDDLE_SURFACE, offsetField='',
                                thicknessAssignment=FROM_SECTION)

            cells = c.findAt(((L_W_L_C_Q, W_W_W_C_Q, Thick_Layer_Half[i]),))  ####-
            region = regionToolset.Region(cells=cells)
            p.SectionAssignment(region=region, sectionName=Metal_name, offset=0.0,
                                offsetType=MIDDLE_SURFACE, offsetField='',
                                thicknessAssignment=FROM_SECTION)
            print(Thick_Layer_Half[i])

    for i in range(0, Layers):
        if (Stack[i][0] == False and Stack[i][1] == True):
            cells = c.findAt(((Long_Center_Quarter, Width_Center_Quarter, Thick_Layer_Half[i]),))  ####-
            region = regionToolset.Region(cells=cells)
            p.SectionAssignment(region=region, sectionName=polymer_name, offset=0.0,
                                offsetType=MIDDLE_SURFACE, offsetField='',
                                thicknessAssignment=FROM_SECTION)
            ##Orientation
            mdb.models['Model-1'].parts['Plate'].MaterialOrientation(region=region,
                                                                     orientationType=SYSTEM, axis=AXIS_3,
                                                                     localCsys=None,
                                                                     fieldName='',
                                                                     additionalRotationType=ROTATION_ANGLE,
                                                                     additionalRotationField='', angle=Stack[i][3],
                                                                     stackDirection=STACK_3)  # -

            cells = c.findAt(((L_W_L_C_Q, W_W_W_C_Q, Thick_Layer_Half[i]),))  ####-
            region = regionToolset.Region(cells=cells)
            p.SectionAssignment(region=region, sectionName=polymer_name, offset=0.0,
                                offsetType=MIDDLE_SURFACE, offsetField='',
                                thicknessAssignment=FROM_SECTION)
            ##Orientation
            mdb.models['Model-1'].parts['Plate'].MaterialOrientation(region=region,
                                                                     orientationType=SYSTEM, axis=AXIS_3,
                                                                     localCsys=None,
                                                                     fieldName='',
                                                                     additionalRotationType=ROTATION_ANGLE,
                                                                     additionalRotationField='', angle=Stack[i][3],
                                                                     stackDirection=STACK_3)  # -
            print(Thick_Layer_Half[i])
    ###Step()
    mdb.models['Model-1'].ExplicitDynamicsStep(name='Step-1', previous='Initial', timePeriod=Total_Time)  # -

    a = mdb.models['Model-1'].rootAssembly
    r1 = a.instances['Impact Head'].referencePoints
    refPoints1 = (r1[2],)
    region = regionToolset.Region(referencePoints=refPoints1)
    mdb.models['Model-1'].Velocity(name='Predefined Field-1', region=region,
                                   field='', distributionType=MAGNITUDE, velocity1=0.0, velocity2=0.0,
                                   velocity3=Speed, omega=0.0)  # -

    mdb.models['Model-1'].FieldOutputRequest(name='F-Output-2',
                                             createStepName='Step-1', variables=(
        'SDEG', 'DMICRT', 'CSDMG', 'CSQUADSCRT', 'SDV', 'FV', 'MFR', 'UVARM',
        'EMSF', 'DENSITY', 'DENSITYVAVG', 'STATUS', 'RHOE', 'RHOP', 'BURNF',
        'DBURNF', 'TIEDSTATUS', 'TIEADJUST'))

    regionDef = mdb.models['Model-1'].rootAssembly.instances['Impact Head'].sets['Impact Head']
    mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-2',
                                               createStepName='Step-1', variables=('S11', 'S22', 'S33', 'S12', 'S13',
                                                                                   'S23', 'SP', 'TRESC', 'PRESS',
                                                                                   'INV3', 'MISES', 'TSHR13', 'TSHR23',
                                                                                   'CTSHR13', 'CTSHR23', 'TRIAX',
                                                                                   'VS11', 'VS22', 'VS33', 'VS12',
                                                                                   'VS13',
                                                                                   'VS23', 'PS11', 'PS22', 'PS33',
                                                                                   'PS12', 'PS13', 'PS23', 'SFABRIC11',
                                                                                   'SFABRIC22', 'SFABRIC33',
                                                                                   'SFABRIC12', 'SFABRIC13',
                                                                                   'SFABRIC23',
                                                                                   'SSAVG1', 'SSAVG2', 'SSAVG3',
                                                                                   'SSAVG4', 'SSAVG5', 'SSAVG6', 'U1',
                                                                                   'U2',
                                                                                   'U3', 'UR1', 'UR2', 'UR3', 'UT',
                                                                                   'UR', 'UCOM1', 'UCOM2', 'UCOM3',
                                                                                   'V1',
                                                                                   'V2', 'V3', 'VR1', 'VR2', 'VR3',
                                                                                   'VT', 'VR', 'VCOM1', 'VCOM2',
                                                                                   'VCOM3',
                                                                                   'A1', 'A2', 'A3', 'AR1', 'AR2',
                                                                                   'AR3', 'AT', 'AR', 'ACOM1', 'ACOM2',
                                                                                   'ACOM3', 'RBANG', 'RBROT', 'SDV',
                                                                                   'FV', 'MFR', 'UVARM', 'DT', 'DMASS',
                                                                                   'EMSF', 'DENSITY', 'STATUS', 'RHOE',
                                                                                   'RHOP', 'BURNF', 'DBURNF'),
                                               region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

    ###Interaction()
    ##Rigid
    a = mdb.models['Model-1'].rootAssembly
    region1 = a.instances['Impact Head'].sets['Impact Head']
    c = a.instances['Impact Head'].cells
    cells = c.getSequenceFromMask(mask=('[#1 ]',), )
    region2 = regionToolset.Region(cells=cells)
    mdb.models['Model-1'].RigidBody(name='Impact Head Rigid', refPointRegion=region1, bodyRegion=region2)

    a = mdb.models['Model-1'].rootAssembly
    region1 = a.instances['Support Up'].sets['Support Up']
    c = a.instances['Support Up'].cells
    cells = c.getSequenceFromMask(mask=('[#1 ]',), )
    region2 = regionToolset.Region(cells=cells)
    mdb.models['Model-1'].RigidBody(name='Support Up Rigid', refPointRegion=region1, bodyRegion=region2)

    a = mdb.models['Model-1'].rootAssembly
    region1 = a.instances['Support Down'].sets['Support Down']
    c = a.instances['Support Down'].cells
    cells = c.getSequenceFromMask(mask=('[#1 ]',), )
    region2 = regionToolset.Region(cells=cells)
    mdb.models['Model-1'].RigidBody(name='Support Down Rigid', refPointRegion=region1, bodyRegion=region2)

    mdb.models['Model-1'].ContactProperty('Cohesive')
    mdb.models['Model-1'].interactionProperties['Cohesive'].CohesiveBehavior(
        repeatedContacts=ON, eligibility=INITIAL_NODES, defaultPenalties=OFF,
        table=((2050.0, 720.0, 720.0),))
    mdb.models['Model-1'].interactionProperties['Cohesive'].Damage(
        criterion=QUAD_TRACTION, initTable=((140.0, 300.0, 300.0),),
        useEvolution=ON, evolutionType=ENERGY, useMixedMode=ON,
        mixedModeType=POWER_LAW, exponent=2.0, evolTable=((2.0, 3.0, 3.0),))

    mdb.models['Model-1'].ContactProperty('General')
    mdb.models['Model-1'].interactionProperties['General'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF,
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0,
        table=((0.3,),), shearStressLimit=None, maximumElasticSlip=FRACTION,
        fraction=0.005, elasticSlipStiffness=None)
    mdb.models['Model-1'].interactionProperties['General'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON,
        constraintEnforcementMethod=DEFAULT)

    p = mdb.models['Model-1'].parts['Plate']
    s = p.faces
    tmp_list = []
    for i in range(0, Layers - 1):
        tmp_list.append(s.findAt(((Long_Center_Quarter, Width_Center_Quarter, Thick_Layer[i]),)))  ##-
        tmp_list.append(s.findAt(((L_W_L_C_Q, Width_Center_Quarter + Width_Quarter, Thick_Layer[i]),)))  ##-
    sideFaces = tuple(tmp_list)
    p.Surface(side1Faces=sideFaces, name='Inter_Up')

    mdb.models['Model-1'].ContactExp(name='Int-1', createStepName='Initial')

    ups = mdb.models['Model-1'].rootAssembly.instances['Plate'].surfaces['Inter_Up']
    mdb.models['Model-1'].interactions['Int-1'].includedPairs.setValuesInStep(
        stepName='Initial', useAllstar=OFF, addPairs=((ALLSTAR, SELF), (
            ALLSTAR, ups), (ups, SELF)))

    tmp_list = [(GLOBAL, SELF, 'General')]
    for i in range(0, Layers - 1):
        tmp_str = 'Up_' + str(i)
        p.Surface(side1Faces=s.findAt(((Long_Center_Quarter, Width_Center_Quarter, Thick_Layer[i]),),
                                      ((L_W_L_C_Q, W_W_W_C_Q, Thick_Layer[i]),)), name=tmp_str)  ##-
        up = mdb.models['Model-1'].rootAssembly.instances['Plate'].surfaces[tmp_str]
        tmp_str = 'Down_' + str(i)
        p.Surface(side2Faces=s.findAt(((Long_Center_Quarter, Width_Center_Quarter, Thick_Layer[i]),),
                                      ((L_W_L_C_Q, W_W_W_C_Q, Thick_Layer[i]),)), name=tmp_str)  ##-
        down = mdb.models['Model-1'].rootAssembly.instances['Plate'].surfaces[tmp_str]
        tmp_list.append((up, down, 'Cohesive'))

    cofaces = tuple(tmp_list)
    mdb.models['Model-1'].interactions['Int-1'].contactPropertyAssignments.appendInStep(
        stepName='Initial', assignments=cofaces)

    ###Load()
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.instances['Impact Head'].referencePoints
    refPoints1 = (r1[2],)
    region = regionToolset.Region(referencePoints=refPoints1)
    mdb.models['Model-1'].XsymmBC(name='Head_1', createStepName='Initial', region=region, localCsys=None)
    mdb.models['Model-1'].YsymmBC(name='Head_2', createStepName='Initial', region=region, localCsys=None)

    r1 = a.instances['Support Up'].referencePoints
    refPoints1 = (r1[2],)
    r2 = a.instances['Support Down'].referencePoints
    refPoints2 = (r2[2],)
    region = regionToolset.Region(referencePoints=(refPoints1, refPoints2,))
    mdb.models['Model-1'].EncastreBC(name='Support', createStepName='Initial', region=region, localCsys=None)

    f1 = a.instances['Plate'].faces
    j = 1
    for i in range(0, Layers):
        tmp_str = 'SY_X_' + str(j)
        j = j + 1
        faces1 = f1.findAt(((0, Width_Center_Quarter, Thick_Layer_Half[i]),))
        region = regionToolset.Region(faces=faces1)
        mdb.models['Model-1'].XsymmBC(name=tmp_str, createStepName='Initial', region=region, localCsys=None)

        tmp_str = 'SY_X_' + str(j)
        j = j + 1
        faces1 = f1.findAt(((0, W_W_W_C_Q, Thick_Layer_Half[i]),))
        region = regionToolset.Region(faces=faces1)
        mdb.models['Model-1'].XsymmBC(name=tmp_str, createStepName='Initial', region=region, localCsys=None)

    j = 1
    for i in range(0, Layers):
        tmp_str = 'SY_Y_' + str(j)
        j = j + 1
        faces1 = f1.findAt(((Long_Center_Quarter, 0, Thick_Layer_Half[i]),))
        region = regionToolset.Region(faces=faces1)
        mdb.models['Model-1'].YsymmBC(name=tmp_str, createStepName='Initial', region=region, localCsys=None)

        tmp_str = 'SY_Y_' + str(j)
        j = j + 1
        faces1 = f1.findAt(((L_W_L_C_Q, 0, Thick_Layer_Half[i]),))
        region = regionToolset.Region(faces=faces1)
        mdb.models['Model-1'].YsymmBC(name=tmp_str, createStepName='Initial', region=region, localCsys=None)

    j = 1
    for i in range(0, Layers):
        tmp_str = 'Other_' + str(j)
        j = j + 1
        faces1 = f1.findAt(((Long_Half, Width_Quarter, Thick_Layer_Half[i]),))
        region = regionToolset.Region(faces=faces1)
        mdb.models['Model-1'].EncastreBC(name=tmp_str, createStepName='Initial', region=region, localCsys=None)

        tmp_str = 'Other_' + str(j)
        j = j + 1
        faces1 = f1.findAt(((Long_Quarter, Width_Half, Thick_Layer_Half[i]),))
        region = regionToolset.Region(faces=faces1)
        mdb.models['Model-1'].EncastreBC(name=tmp_str, createStepName='Initial', region=region, localCsys=None)

    ###Mesh()
    p = mdb.models['Model-1'].parts['Impact Head']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]',), )
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE, algorithm=NON_DEFAULT)
    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT,
                              elemDeletion=OFF)
    pickedRegions = (pickedRegions,)
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    p.seedPart(size=Mesh_Size_Impact, deviationFactor=0.1, minSizeFactor=0.1)  # -
    p.generateMesh()

    p = mdb.models['Model-1'].parts['Support Down']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]',), )
    p.setMeshControls(regions=pickedRegions, technique=SWEEP, algorithm=MEDIAL_AXIS)
    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT,
                              kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF,
                              hourglassControl=DEFAULT, distortionControl=DEFAULT, elemDeletion=OFF)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT)
    pickedRegions = (pickedRegions,)
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    p.seedPart(size=2.0, deviationFactor=0.1, minSizeFactor=0.1)  # -#
    p.generateMesh()

    p = mdb.models['Model-1'].parts['Support Up']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]',), )
    p.setMeshControls(regions=pickedRegions, technique=SWEEP, algorithm=MEDIAL_AXIS)
    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT,
                              kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF,
                              hourglassControl=DEFAULT, distortionControl=DEFAULT, elemDeletion=OFF)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT)
    pickedRegions = (pickedRegions,)
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    p.seedPart(size=2.0, deviationFactor=0.1, minSizeFactor=0.1)  # -#
    p.generateMesh()

    p = mdb.models['Model-1'].parts['Plate']
    c = p.cells
    e = p.edges
    tmp_list = []
    for i in range(0, Layers):
        tmp_list.append(c.findAt((Long_Quarter, Width_Quarter, Thick_Layer_Half[i]), ))  # -
    pickedRegions = tuple(tmp_list)
    p.setMeshControls(regions=pickedRegions, algorithm=MEDIAL_AXIS)
    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT,
                              kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF,
                              hourglassControl=ENHANCED, distortionControl=DEFAULT, elemDeletion=ON)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT)

    tmp_list = []
    for i in range(0, Layers):
        tmp_list.append(c.findAt((Long_Half, Width_Half, Thick_Layer_Half[i]), ))  #
        tmp_list.append(c.findAt((Long_Center_Quarter, Width_Center_Quarter, Thick_Layer_Half[i]), ))

    pickedRegions = tuple(tmp_list)
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))

    tmp_list = [e.findAt((Long_Center_Quarter, 0, 0), ), e.findAt((0, Width_Center_Quarter, 0), )]

    for i in range(0, Layers):
        tmp_list.append(e.findAt((Long_Center_Quarter, 0, Thick_Layer[i]), ))  #
        tmp_list.append(e.findAt((0, Width_Center_Quarter, Thick_Layer[i]), ))  #

    pickedEdges = tuple(tmp_list)
    p.seedEdgeBySize(edges=pickedEdges, size=Mesh_Size_Center, deviationFactor=0.1, constraint=FINER)  # -

    tmp_list = [e.findAt((L_W_L_C_Q, 0, 0), ), e.findAt((0, W_W_W_C_Q, 0), )]
    for i in range(0, Layers):
        tmp_list.append(e.findAt((L_W_L_C_Q, 0, Thick_Layer[i]), ))  #
        tmp_list.append(e.findAt((0, W_W_W_C_Q, Thick_Layer[i]), ))  #

    pickedEdges = tuple(tmp_list)
    p.seedEdgeBySize(edges=pickedEdges, size=Mesh_Size_Whole, deviationFactor=0.1, constraint=FINER)  # -
    p.generateMesh()
