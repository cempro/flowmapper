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
from os.path import isfile

from PyQt4 import QtCore, QtGui
from ui_flowmapper import Ui_FlowMapper
import flowmapper
# create the dialog for zoom to point

class FlowMapperDialog(QtGui.QDialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_FlowMapper()
        self.ui.setupUi(self)

    def SetTextBrowseShape(self):
        self.ui.BrowseShapeLineEdit.setText(flowmapper.SaveShpName)
        
    def SetTextBrowseShapeNodes(self):
        self.ui.BrowseShapeNodesLineEdit.setText(flowmapper.SaveShpNameNodes)        

    def SetTextBrowseNodes(self):
        if isfile(flowmapper.InputNodesName):
            self.ui.BrowseNodesLineEdit.setText(flowmapper.InputNodesName)
            
    def SetTextBrowseNodeNames(self):
        if isfile(flowmapper.InputNodeNamesName):
            self.ui.BrowseNodeNamesLineEdit.setText(flowmapper.InputNodeNamesName)     
            
    def SetTextBrowseMatrix(self):
        if isfile(flowmapper.InputMatrixName):
            self.ui.BrowseMatrixLineEdit.setText(flowmapper.InputMatrixName)



        
