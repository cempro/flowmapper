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
from ui_form5 import Ui_Form
import flowmapper
# create the dialog for zoom to point

class Form5Dialog(QtGui.QDialog):
    
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
    def BrowseShapeLineEditExport(self):
        self.ui.BrowseShapeLineEdit.setText(flowmapper.BrowseShapeLineEditNameExport)
    def BrowseFileLineEditExport(self):
        self.ui.BrowseFileLineEdit.setText(flowmapper.BrowseFileLineEditNameExport)