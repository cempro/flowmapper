"""
/***************************************************************************
 FlowMapperDialog
                                 A QGIS plugin
 This plugin generates discreet flow lines between nodes
                             -------------------
        begin                : 2011-12-04
        copyright            : (C) 2011 by Cem GULLUOGLU
        email                : cempro@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import sys
import os
from os.path import isfile

from PyQt4 import QtCore, QtGui
from ui_form3 import Ui_Form
import flowmapper
# create the dialog for zoom to point

class Form3Dialog(QtGui.QDialog):
    
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def SetTextBrowseInputShapeFilterLength(self):
        self.ui.BrowseShapeLineEdit.setText(flowmapper.InputShpFilterLengthName)
        
        #InputShpFilterLengthDirectory = os.path.realpath(flowmapper.InputShpFilterLengthName)
        InputShpFilterLengthDirectory = flowmapper.InputShpFilterLengthName
        if len(flowmapper.InputShpFilterLengthName) > 0:
            extension = os.path.splitext(str(InputShpFilterLengthDirectory))[1]
            if extension == ".shp":
                self.ui.CalStatLength.setEnabled(True)
        
    def SetTextBrowseOutputShapeFilterLength(self):
        self.ui.BrowseShapeLineEdit_2.setText(flowmapper.OutputShpFilterLengthName)
    
    def MeanLength(self):
        self.ui.MeanLength_LineEdit.setText(flowmapper.CalStatLengthMean)
    
    def MeanLengthNotZero(self):
        self.ui.MeanNotZeroLength_LineEdit.setText(flowmapper.CalStatLengthMeanNotZero)
        
    def MaxFlowLength(self):
        self.ui.MaxFlowLength_LineEdit.setText(flowmapper.CalStatLengthMax)

    def MinFlowLength(self):
        self.ui.MinFlowLength_LineEdit.setText(flowmapper.CalStatLengthMin)
        
    def StdDevLength(self):
        self.ui.StdDevLength_LineEdit.setText(flowmapper.CalStatLengthStdDev)
    
    def StdDevLengthNotZero(self):
        self.ui.StdDevNotZeroLength_LineEdit.setText(flowmapper.CalStatLengthStdDevNotZero)
        
        
        