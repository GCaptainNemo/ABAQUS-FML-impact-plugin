from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class _rsgTmp069_DB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Laminates Builder',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        TabBook_1 = FXTabBook(p=self, tgt=None, sel=0,
            opts=TABBOOK_NORMAL,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)
        tabItem = FXTabItem(p=TabBook_1, text='Geometry', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_4 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        l = FXLabel(p=TabItem_4, text='Default Unit(mm)', opts=JUSTIFY_LEFT)
        if isinstance(TabItem_4, FXHorizontalFrame):
            FXVerticalSeparator(p=TabItem_4, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        else:
            FXHorizontalSeparator(p=TabItem_4, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        VFrame_4 = FXVerticalFrame(p=TabItem_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        HFrame_2 = FXHorizontalFrame(p=VFrame_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        fileName = os.path.join(thisDir, 'Geometry.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_2, text='', ic=icon)
        VFrame_3 = FXVerticalFrame(p=HFrame_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_1 = FXGroupBox(p=VFrame_3, text='Whole', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='Long       ', tgt=form.Long_WholeKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='Width      ', tgt=form.Width_WholeKw, sel=0)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='Mesh size', tgt=form.Mesh_Size_WholeKw, sel=0)
        GroupBox_3 = FXGroupBox(p=VFrame_3, text='Center Area', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_3, ncols=12, labelText='Long       ', tgt=form.Long_CenterKw, sel=0)
        AFXTextField(p=GroupBox_3, ncols=12, labelText='Width      ', tgt=form.Width_CenterKw, sel=0)
        AFXTextField(p=GroupBox_3, ncols=12, labelText='Mesh Size', tgt=form.Mesh_Size_CenterKw, sel=0)
        if isinstance(VFrame_4, FXHorizontalFrame):
            FXVerticalSeparator(p=VFrame_4, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        else:
            FXHorizontalSeparator(p=VFrame_4, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        HFrame_3 = FXHorizontalFrame(p=VFrame_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        fileName = os.path.join(thisDir, 'Impact.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_3, text='', ic=icon)
        VFrame_5 = FXVerticalFrame(p=HFrame_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_4 = FXGroupBox(p=VFrame_5, text='Impact Head', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_4, ncols=12, labelText='Radius          ', tgt=form.RadiusKw, sel=0)
        AFXTextField(p=GroupBox_4, ncols=12, labelText='Speed(mm/s)', tgt=form.SpeedKw, sel=0)
        AFXTextField(p=GroupBox_4, ncols=12, labelText='Mesh Size     ', tgt=form.Mesh_Size_ImpactKw, sel=0)
        AFXTextField(p=GroupBox_4, ncols=12, labelText='Total time(s): ', tgt=form.Total_TimeKw, sel=0)
        tabItem = FXTabItem(p=TabBook_1, text='Assign', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_1 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        HFrame_18 = FXHorizontalFrame(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        fileName = os.path.join(thisDir, 'rotation.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_18, text='', ic=icon)
        fileName = os.path.join(thisDir, 'Stack.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_18, text='', ic=icon)
        HFrame_19 = FXHorizontalFrame(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_14 = FXGroupBox(p=HFrame_19, text='Model type', opts=FRAME_GROOVE)
        FXRadioButton(p=GroupBox_14, text='1/4 model', tgt=form.GroupBox14Kw1, sel=118)
        FXRadioButton(p=GroupBox_14, text='1/2 model', tgt=form.GroupBox14Kw1, sel=119)
        GroupBox_15 = FXGroupBox(p=HFrame_19, text='Material', opts=FRAME_GROOVE)
        ComboBox_1 = AFXComboBox(p=GroupBox_15, ncols=0, nvis=1, text='Metal:', tgt=form.Metal_nameKw, sel=0)
        ComboBox_1.setMaxVisible(10)
        ComboBox_2 = AFXComboBox(p=GroupBox_15, ncols=0, nvis=1, text='FRP:   ', tgt=form.polymer_nameKw, sel=0)
        ComboBox_2.setMaxVisible(10)
        ComboBox_1.appendItem(text='AZ31-JC')
        ComboBox_2.appendItem(text='AZ31-JC')
        ComboBox_1.appendItem(text='CFRP-T700')
        ComboBox_2.appendItem(text='CFRP-T700')
        vf = FXVerticalFrame(TabItem_1, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        table = AFXTable(vf, 11, 5, 11, 5, form.StackKw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        table.setPopupOptions(AFXTable.POPUP_COPY|AFXTable.POPUP_PASTE|AFXTable.POPUP_INSERT_ROW|AFXTable.POPUP_DELETE_ROW|AFXTable.POPUP_CLEAR_CONTENTS)
        table.setLeadingRows(1)
        table.setLeadingColumns(1)
        table.setColumnWidth(1, 100)
        table.setColumnType(1, AFXTable.BOOL)
        table.setColumnJustify(1, AFXTable.CENTER)
        table.setColumnWidth(2, 100)
        table.setColumnType(2, AFXTable.BOOL)
        table.setColumnJustify(2, AFXTable.CENTER)
        table.setColumnWidth(3, 120)
        table.setColumnType(3, AFXTable.FLOAT)
        table.setColumnWidth(4, 100)
        table.setColumnType(4, AFXTable.FLOAT)
        table.setLeadingRowLabels('Metal\tFRP\tThickness(mm)\tRotation Angle( FRP Only )')
        table.setStretchableColumn( table.getNumColumns()-1 )
        table.showHorizontalGrid(True)
        table.showVerticalGrid(True)
        GroupBox_13 = FXGroupBox(p=TabItem_1, text='Attention', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        l = FXLabel(p=GroupBox_13, text='Metal or FRP can only be chosen one', opts=JUSTIFY_LEFT)
        l.setFont( getAFXFont(FONT_BOLD) )
        l = FXLabel(p=GroupBox_13, text='There must be two layers at least', opts=JUSTIFY_LEFT)
        l.setFont( getAFXFont(FONT_BOLD) )
