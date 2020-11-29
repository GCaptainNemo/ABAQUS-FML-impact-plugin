from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class _rsgTmp001_Form(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='Test',
            objectName='impact_kernel', registerQuery=False)
        pickedDefault = ''
        self.Long_WholeKw = AFXFloatKeyword(self.cmd, 'Long_Whole', True, 170)
        self.Width_WholeKw = AFXFloatKeyword(self.cmd, 'Width_Whole', True, 90)
        self.Mesh_Size_WholeKw = AFXFloatKeyword(self.cmd, 'Mesh_Size_Whole', True, 1.2)
        self.Long_CenterKw = AFXFloatKeyword(self.cmd, 'Long_Center', True, 40)
        self.Width_CenterKw = AFXFloatKeyword(self.cmd, 'Width_Center', True, 40)
        self.Mesh_Size_CenterKw = AFXFloatKeyword(self.cmd, 'Mesh_Size_Center', True, 0.3)
        self.RadiusKw = AFXFloatKeyword(self.cmd, 'Radius', True, 6.5)
        self.SpeedKw = AFXFloatKeyword(self.cmd, 'Speed', True, 3200)
        self.Mesh_Size_ImpactKw = AFXFloatKeyword(self.cmd, 'Mesh_Size_Impact', True, 1)
        self.Total_TimeKw = AFXFloatKeyword(self.cmd, 'Total_Time', True, 0.01)
        if not self.radioButtonGroups.has_key('GroupBox14'):
            self.GroupBox14Kw1 = AFXIntKeyword(None, 'GroupBox14Dummy', True)
            self.GroupBox14Kw2 = AFXStringKeyword(self.cmd, 'GroupBox14', True)
            self.radioButtonGroups['GroupBox14'] = (self.GroupBox14Kw1, self.GroupBox14Kw2, {})
        self.radioButtonGroups['GroupBox14'][2][1] = '1/4 model'
        if not self.radioButtonGroups.has_key('GroupBox14'):
            self.GroupBox14Kw1 = AFXIntKeyword(None, 'GroupBox14Dummy', True)
            self.GroupBox14Kw2 = AFXStringKeyword(self.cmd, 'GroupBox14', True)
            self.radioButtonGroups['GroupBox14'] = (self.GroupBox14Kw1, self.GroupBox14Kw2, {})
        self.radioButtonGroups['GroupBox14'][2][2] = '1/2 model'
        self.Metal_nameKw = AFXStringKeyword(self.cmd, 'Metal_name', True)
        self.polymer_nameKw = AFXStringKeyword(self.cmd, 'polymer_name', True)
        self.StackKw = AFXTableKeyword(self.cmd, 'Stack', True)
        self.StackKw.setColumnType(0, AFXTABLE_TYPE_BOOL)
        self.StackKw.setColumnType(1, AFXTABLE_TYPE_BOOL)
        self.StackKw.setColumnType(2, AFXTABLE_TYPE_FLOAT)
        self.StackKw.setColumnType(3, AFXTABLE_TYPE_FLOAT)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import _rsgTmp001_DB
        return _rsgTmp001_DB._rsgTmp001_DB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def deactivate(self):
    
        try:
            osutils.remove(os.path.join('c:\\Users\\wang1\\abaqus_plugins\\impact_xiugai', '_rsgTmp001_DB.py'), force=True )
            osutils.remove(os.path.join('c:\\Users\\wang1\\abaqus_plugins\\impact_xiugai', '_rsgTmp001_DB.pyc'), force=True )
        except:
            pass
        try:
            osutils.remove(os.path.join('c:\\Users\\wang1\\abaqus_plugins\\impact_xiugai', '_rsgTmp001_Form.py'), force=True )
            osutils.remove(os.path.join('c:\\Users\\wang1\\abaqus_plugins\\impact_xiugai', '_rsgTmp001_Form.pyc'), force=True )
        except:
            pass
        AFXForm.deactivate(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getCommandString(self):

        cmds = 'import impact_kernel\n'
        cmds += AFXForm.getCommandString(self)
        return cmds

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False
