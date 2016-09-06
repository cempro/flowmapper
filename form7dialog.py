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
from ui_form7 import Ui_Form
import flowmapper

class Form7Dialog(QtGui.QDialog):
    
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
    def SetTextBrowseInputShapeNodeSymbology(self):
        self.ui.BrowseShapeLineEdit.setText(flowmapper.InputShpNodeSymbologyName)

        InputShpNodeSymbologyDirectory = flowmapper.InputShpNodeSymbologyName
        if len(flowmapper.InputShpNodeSymbologyName) > 0:
            extension = os.path.splitext(str(InputShpNodeSymbologyDirectory))[1]
            if extension == ".shp":
                self.ui.CalStatField.setEnabled(True)        
        
    def SetTextPopulateFieldNamesList(self):
        self.ui.comboBoxSelectField.clear()
        if ".shp" in flowmapper.InputShpNodeSymbologyName and len(flowmapper.InputShpNodeSymbologyName) > 4: 
            for item in flowmapper.FieldNamesListcomboBox:
                self.ui.comboBoxSelectField.addItem(item)
            self.ui.comboBoxSelectField.setCurrentIndex(0)
        
    def MeanSymbology(self):
        self.ui.lineEditMeanSymbology.setText(flowmapper.GradSymMeanNodeSymbology)
        
    def MaxSymbology(self):
        self.ui.lineEditMaxSymbology.setText(flowmapper.GradSymMaxNodeSymbology)

    def MinSymbology(self):
        self.ui.lineEditMinSymbology.setText(flowmapper.GradSymMinNodeSymbology)
        
    def StdDevSymbology(self):
        self.ui.lineEditStdDevSymbology.setText(flowmapper.GradSymStdDevNodeSymbology)

    def NoOfFeaturesSymbology(self):
        self.ui.lineEditNoOfFeaturesSymbology.setText(flowmapper.GradSymNoOfFeaturesNodeSymbology)        
        
    def PushButtonColorSelectSymbology_1(self):
        self.ui.PushButtonColorSelect_1.setStyleSheet("QPushButton {background-color: "+flowmapper.color_name_1+" }")        
    def PushButtonColorSelectSymbology_2(self):
        self.ui.PushButtonColorSelect_2.setStyleSheet("QPushButton {background-color: "+flowmapper.color_name_2+" }")   
    def PushButtonColorSelectSymbology_3(self):
        self.ui.PushButtonColorSelect_3.setStyleSheet("QPushButton {background-color: "+flowmapper.color_name_3+" }")        
    def PushButtonColorSelectSymbology_4(self):
        self.ui.PushButtonColorSelect_4.setStyleSheet("QPushButton {background-color: "+flowmapper.color_name_4+" }")        
    def PushButtonColorSelectSymbology_5(self):
        self.ui.PushButtonColorSelect_5.setStyleSheet("QPushButton {background-color: "+flowmapper.color_name_5+" }")       
    def PushButtonColorSelectSymbology_6(self):
        self.ui.PushButtonColorSelect_6.setStyleSheet("QPushButton {background-color: "+flowmapper.color_name_6+" }")
    def PushButtonColorSelectSymbology_7(self):
        self.ui.PushButtonColorSelect_7.setStyleSheet("QPushButton {background-color: "+flowmapper.color_name_7+" }")
    def PushButtonColorSelectSymbology_8(self):
        self.ui.PushButtonColorSelect_8.setStyleSheet("QPushButton {background-color: "+flowmapper.color_name_8+" }")        