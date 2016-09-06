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
from ui_form2 import Ui_Form
import flowmapper
# create the dialog for zoom to point

class Form2Dialog(QtGui.QDialog):
    
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def SetTextBrowseInputShapeFilter(self):
        self.ui.BrowseShapeLineEdit.setText(flowmapper.InputShpFilterName)
        
        #InputShpFilterDirectory = os.path.realpath(flowmapper.InputShpFilterName)
        InputShpFilterDirectory = flowmapper.InputShpFilterName
        if len(flowmapper.InputShpFilterName) > 0:
            extension = os.path.splitext(str(InputShpFilterDirectory))[1]
            if extension == ".shp":
                self.ui.CalStat.setEnabled(True)
        
    def SetTextBrowseOutputShapeFilter(self):
        self.ui.BrowseShapeLineEdit_2.setText(flowmapper.OutputShpFilterName)
    
    def No_Of_Features(self):
        self.ui.No_Of_Features_LineEdit.setText(flowmapper.CalStatNoOfFeatures)

    def No_Of_FeaturesNotZero(self):
        self.ui.No_Of_ZeroFlowFeatures_LineEdit.setText(flowmapper.CalStatNoOfFeaturesZero)
        
    def Mean(self):
        self.ui.Mean_LineEdit.setText(flowmapper.CalStatMean)
    
    def MeanNotZero(self):
        self.ui.MeanNotZero_LineEdit.setText(flowmapper.CalStatMeanNotZero)
        
    def MaxFlow(self):
        self.ui.MaxFlow_LineEdit.setText(flowmapper.CalStatMaxFlow)

    def MinFlow(self):
        self.ui.MinFlow_LineEdit.setText(flowmapper.CalStatMinFlow)
        
    def SumMagnitude(self):
        self.ui.SumMagnitude_LineEdit.setText(flowmapper.CalStatSumMagnitude)
    
    def StdDev(self):
        self.ui.StdDev_LineEdit.setText(flowmapper.CalStatStdDev)
    
    def StdDevNotZero(self):
        self.ui.StdDevNotZero_LineEdit.setText(flowmapper.CalStatStdDevNotZero)
    
    
    
        
 