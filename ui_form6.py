# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_form6.ui'
#
# Created: Mon Nov 25 01:18:34 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

##----------------------------------------------------------------##        
import flowmapper
##----------------------------------------------------------------## 

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(600, 290)
        Form.setMinimumSize(QtCore.QSize(600, 290))
        Form.setMaximumSize(QtCore.QSize(600, 290))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/flowmapper/icon7.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(Form)
        self.buttonBox.setGeometry(QtCore.QRect(420, 250, 160, 24))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.BrowseShapeInputFilterNodeNames = QtGui.QPushButton(Form)
        self.BrowseShapeInputFilterNodeNames.setGeometry(QtCore.QRect(510, 10, 80, 24))
        self.BrowseShapeInputFilterNodeNames.setObjectName(_fromUtf8("BrowseShapeInputFilterNodeNames"))
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 91, 20))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.BrowseShapeLineEdit = QtGui.QLineEdit(Form)
        self.BrowseShapeLineEdit.setEnabled(False)
        self.BrowseShapeLineEdit.setGeometry(QtCore.QRect(200, 10, 301, 20))
        self.BrowseShapeLineEdit.setText(_fromUtf8(""))
        self.BrowseShapeLineEdit.setObjectName(_fromUtf8("BrowseShapeLineEdit"))
        self.label_01 = QtGui.QLabel(Form)
        self.label_01.setGeometry(QtCore.QRect(10, 10, 180, 20))
        self.label_01.setObjectName(_fromUtf8("label_01"))
        self.nodeFilteringType_comboBox = QtGui.QComboBox(Form)
        self.nodeFilteringType_comboBox.setGeometry(QtCore.QRect(200, 70, 191, 22))
        self.nodeFilteringType_comboBox.setObjectName(_fromUtf8("nodeFilteringType_comboBox"))
        self.nodeFilteringType_comboBox.addItem(_fromUtf8(""))
        self.nodeFilteringType_comboBox.addItem(_fromUtf8(""))
        self.nodeFilteringType_comboBox.addItem(_fromUtf8(""))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(110, 40, 481, 20))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.comboBoxSelectSymbology = QtGui.QComboBox(Form)
        self.comboBoxSelectSymbology.setEnabled(True)
        self.comboBoxSelectSymbology.setGeometry(QtCore.QRect(460, 180, 120, 22))
        self.comboBoxSelectSymbology.setObjectName(_fromUtf8("comboBoxSelectSymbology"))
        self.comboBoxSelectSymbology.addItem(_fromUtf8(""))
        self.comboBoxSelectSymbology.addItem(_fromUtf8(""))
        self.comboBoxSelectSymbology.addItem(_fromUtf8(""))
        self.comboBoxSelectSymbology.addItem(_fromUtf8(""))
        self.comboBoxSelectSymbology.addItem(_fromUtf8(""))
        self.label_19 = QtGui.QLabel(Form)
        self.label_19.setGeometry(QtCore.QRect(10, 210, 81, 20))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.Add2MapcheckBox = QtGui.QCheckBox(Form)
        self.Add2MapcheckBox.setEnabled(True)
        self.Add2MapcheckBox.setGeometry(QtCore.QRect(10, 180, 231, 17))
        self.Add2MapcheckBox.setChecked(True)
        self.Add2MapcheckBox.setObjectName(_fromUtf8("Add2MapcheckBox"))
        self.lineEditInterval = QtGui.QLineEdit(Form)
        self.lineEditInterval.setEnabled(False)
        self.lineEditInterval.setGeometry(QtCore.QRect(280, 210, 51, 20))
        self.lineEditInterval.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEditInterval.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEditInterval.setObjectName(_fromUtf8("lineEditInterval"))
        self.comboBoxSelectStdDev = QtGui.QComboBox(Form)
        self.comboBoxSelectStdDev.setEnabled(False)
        self.comboBoxSelectStdDev.setGeometry(QtCore.QRect(460, 210, 120, 22))
        self.comboBoxSelectStdDev.setObjectName(_fromUtf8("comboBoxSelectStdDev"))
        self.comboBoxSelectStdDev.addItem(_fromUtf8(""))
        self.comboBoxSelectStdDev.addItem(_fromUtf8(""))
        self.comboBoxSelectStdDev.addItem(_fromUtf8(""))
        self.comboBoxSelectStdDev.addItem(_fromUtf8(""))
        self.label_20 = QtGui.QLabel(Form)
        self.label_20.setGeometry(QtCore.QRect(380, 210, 81, 20))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.label_21 = QtGui.QLabel(Form)
        self.label_21.setGeometry(QtCore.QRect(200, 210, 81, 20))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.spinBoxClasses = QtGui.QSpinBox(Form)
        self.spinBoxClasses.setEnabled(False)
        self.spinBoxClasses.setGeometry(QtCore.QRect(90, 210, 51, 22))
        self.spinBoxClasses.setMinimum(2)
        self.spinBoxClasses.setProperty(_fromUtf8("value"), 2)
        self.spinBoxClasses.setObjectName(_fromUtf8("spinBoxClasses"))
        self.NodeNames_comboBox = QtGui.QComboBox(Form)
        self.NodeNames_comboBox.setGeometry(QtCore.QRect(200, 100, 191, 22))
        self.NodeNames_comboBox.setObjectName(_fromUtf8("NodeNames_comboBox"))
        self.label_18 = QtGui.QLabel(Form)
        self.label_18.setGeometry(QtCore.QRect(10, 100, 111, 20))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_18.setFont(font)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.ShowDirectioncheckBox = QtGui.QCheckBox(Form)
        self.ShowDirectioncheckBox.setEnabled(True)
        self.ShowDirectioncheckBox.setGeometry(QtCore.QRect(280, 180, 121, 17))
        self.ShowDirectioncheckBox.setChecked(True)
        self.ShowDirectioncheckBox.setObjectName(_fromUtf8("ShowDirectioncheckBox"))
        self.BrowseShapeLineEdit_2 = QtGui.QLineEdit(Form)
        self.BrowseShapeLineEdit_2.setEnabled(False)
        self.BrowseShapeLineEdit_2.setGeometry(QtCore.QRect(200, 140, 301, 20))
        self.BrowseShapeLineEdit_2.setText(_fromUtf8(""))
        self.BrowseShapeLineEdit_2.setObjectName(_fromUtf8("BrowseShapeLineEdit_2"))
        self.BrowseShapeOutputFilterNodeNames = QtGui.QPushButton(Form)
        self.BrowseShapeOutputFilterNodeNames.setGeometry(QtCore.QRect(510, 140, 80, 24))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BrowseShapeOutputFilterNodeNames.sizePolicy().hasHeightForWidth())
        self.BrowseShapeOutputFilterNodeNames.setSizePolicy(sizePolicy)
        self.BrowseShapeOutputFilterNodeNames.setObjectName(_fromUtf8("BrowseShapeOutputFilterNodeNames"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 180, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(Form)
        
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Form.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Form.reject)
        QtCore.QMetaObject.connectSlotsByName(Form)

##-----------------------------------------------------------------------------------------------##        
##-----------------------------------------------------------------------------------------------##
        QtCore.QObject.connect(self.nodeFilteringType_comboBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.set_nodeFilteringType_comboText)

        QtCore.QObject.connect(self.Add2MapcheckBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.comboBoxSelectSymbology.setEnabled)
        QtCore.QObject.connect(self.Add2MapcheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.reset_enable_disable_state)
        QtCore.QObject.connect(self.comboBoxSelectSymbology, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.enable_disable)
##-----------------------------------------------------------------------------------------------##        
##-----------------------------------------------------------------------------------------------##

        
        Form.setTabOrder(self.BrowseShapeLineEdit, self.BrowseShapeInputFilterNodeNames)
        Form.setTabOrder(self.BrowseShapeInputFilterNodeNames, self.nodeFilteringType_comboBox)
        Form.setTabOrder(self.nodeFilteringType_comboBox, self.NodeNames_comboBox)
        Form.setTabOrder(self.NodeNames_comboBox, self.BrowseShapeLineEdit_2)
        Form.setTabOrder(self.BrowseShapeLineEdit_2, self.BrowseShapeOutputFilterNodeNames)
        Form.setTabOrder(self.BrowseShapeOutputFilterNodeNames, self.Add2MapcheckBox)
        Form.setTabOrder(self.Add2MapcheckBox, self.ShowDirectioncheckBox)
        Form.setTabOrder(self.ShowDirectioncheckBox, self.comboBoxSelectSymbology)
        Form.setTabOrder(self.comboBoxSelectSymbology, self.spinBoxClasses)
        Form.setTabOrder(self.spinBoxClasses, self.lineEditInterval)
        Form.setTabOrder(self.lineEditInterval, self.comboBoxSelectStdDev)
        Form.setTabOrder(self.comboBoxSelectStdDev, self.buttonBox)

##-----------------------------------------------------------------------------------------------##        
##-----------------------------------------------------------------------------------------------##           
    def set_nodeFilteringType_comboText(self):
        flowmapper.nodeFilteringType_combotext = self.nodeFilteringType_comboBox.currentText() 
        
    def reset_enable_disable_state(self):
        self.comboBoxSelectSymbology.setCurrentIndex(0)
        self.spinBoxClasses.setEnabled(False)
        self.lineEditInterval.setEnabled(False)
        self.comboBoxSelectStdDev.setEnabled(False)

        if self.Add2MapcheckBox.isChecked() == True:
            self.ShowDirectioncheckBox.setEnabled(True)
            self.ShowDirectioncheckBox.setChecked(True)
        elif self.Add2MapcheckBox.isChecked() == False:
            self.ShowDirectioncheckBox.setEnabled(False)
            self.ShowDirectioncheckBox.setChecked(False)          
    
    def enable_disable(self):
        if self.comboBoxSelectSymbology.currentText() == "Single Symbol":
            self.spinBoxClasses.setEnabled(False)
            self.lineEditInterval.setEnabled(False)
            self.comboBoxSelectStdDev.setEnabled(False)
            if self.Add2MapcheckBox.isChecked() == True:
                self.ShowDirectioncheckBox.setEnabled(True)
                self.ShowDirectioncheckBox.setChecked(True)
            elif self.Add2MapcheckBox.isChecked() == False:
                self.ShowDirectioncheckBox.setEnabled(False)
                self.ShowDirectioncheckBox.setChecked(False)            
            
        elif self.comboBoxSelectSymbology.currentText() == "Equal Size Classes":
            self.spinBoxClasses.setEnabled(True)
            self.lineEditInterval.setEnabled(False)
            self.comboBoxSelectStdDev.setEnabled(False)
            if self.Add2MapcheckBox.isChecked() == True:
                self.ShowDirectioncheckBox.setEnabled(True)
                self.ShowDirectioncheckBox.setChecked(True)
            elif self.Add2MapcheckBox.isChecked() == False:
                self.ShowDirectioncheckBox.setEnabled(False)
                self.ShowDirectioncheckBox.setChecked(False)
            
        elif self.comboBoxSelectSymbology.currentText() == "Equal Interval":
            self.spinBoxClasses.setEnabled(True)
            self.lineEditInterval.setEnabled(False)
            self.comboBoxSelectStdDev.setEnabled(False)  
            if self.Add2MapcheckBox.isChecked() == True:            
                self.ShowDirectioncheckBox.setEnabled(True)            
                self.ShowDirectioncheckBox.setChecked(True)            
            elif self.Add2MapcheckBox.isChecked() == False:            
                self.ShowDirectioncheckBox.setEnabled(False)            
                self.ShowDirectioncheckBox.setChecked(False)            
            
        elif self.comboBoxSelectSymbology.currentText() == "Defined Interval":
            self.spinBoxClasses.setEnabled(False)
            self.lineEditInterval.setEnabled(True)
            self.comboBoxSelectStdDev.setEnabled(False) 
            if self.Add2MapcheckBox.isChecked() == True:
                self.ShowDirectioncheckBox.setEnabled(True)
                self.ShowDirectioncheckBox.setChecked(True)
            elif self.Add2MapcheckBox.isChecked() == False:
                self.ShowDirectioncheckBox.setEnabled(False)
                self.ShowDirectioncheckBox.setChecked(False)
            
        elif self.comboBoxSelectSymbology.currentText() == "Standard Deviation":
            self.spinBoxClasses.setEnabled(False)
            self.lineEditInterval.setEnabled(False)
            self.comboBoxSelectStdDev.setEnabled(True)  
            if self.Add2MapcheckBox.isChecked() == True:
                self.ShowDirectioncheckBox.setEnabled(True)
                self.ShowDirectioncheckBox.setChecked(True)
            elif self.Add2MapcheckBox.isChecked() == False:
                self.ShowDirectioncheckBox.setEnabled(False)            
                self.ShowDirectioncheckBox.setChecked(False)    

    def uncheck_ShowDirectioncheckBox(self):
        self.ShowDirectioncheckBox.setChecked(False)
        
##-----------------------------------------------------------------------------------------------##        
##-----------------------------------------------------------------------------------------------##
        
    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Filter flow lines by node and direction", None, QtGui.QApplication.UnicodeUTF8))
        self.BrowseShapeInputFilterNodeNames.setText(QtGui.QApplication.translate("Form", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Filter flow lines :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_01.setText(QtGui.QApplication.translate("Form", "Select shapefile storing flow lines :", None, QtGui.QApplication.UnicodeUTF8))
        self.nodeFilteringType_comboBox.setItemText(0, QtGui.QApplication.translate("Form", "both incoming to & outgoing from", None, QtGui.QApplication.UnicodeUTF8))
        self.nodeFilteringType_comboBox.setItemText(1, QtGui.QApplication.translate("Form", "only incoming to", None, QtGui.QApplication.UnicodeUTF8))
        self.nodeFilteringType_comboBox.setItemText(2, QtGui.QApplication.translate("Form", "only outgoing from", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "* Input shapefile must be created with Flow Mapper or include \"name_x1y1\" & \"name_x2y2\" fields.", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxSelectSymbology.setItemText(0, QtGui.QApplication.translate("Form", "Single Symbol", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxSelectSymbology.setItemText(1, QtGui.QApplication.translate("Form", "Equal Size Classes", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxSelectSymbology.setItemText(2, QtGui.QApplication.translate("Form", "Equal Interval", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxSelectSymbology.setItemText(3, QtGui.QApplication.translate("Form", "Defined Interval", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxSelectSymbology.setItemText(4, QtGui.QApplication.translate("Form", "Standard Deviation", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("Form", "No. of classes :", None, QtGui.QApplication.UnicodeUTF8))
        self.Add2MapcheckBox.setText(QtGui.QApplication.translate("Form", "Add shapefile to map canvas after filtering", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditInterval.setText(QtGui.QApplication.translate("Form", "100", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxSelectStdDev.setItemText(0, QtGui.QApplication.translate("Form", "1/4 Std. Dev.", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxSelectStdDev.setItemText(1, QtGui.QApplication.translate("Form", "1/2 Std. Dev.", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxSelectStdDev.setItemText(2, QtGui.QApplication.translate("Form", "1 Std. Dev.", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxSelectStdDev.setItemText(3, QtGui.QApplication.translate("Form", "2 Std. Dev.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("Form", "Class interval :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("Form", "Class interval :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("Form", "Select node name :", None, QtGui.QApplication.UnicodeUTF8))
        self.ShowDirectioncheckBox.setText(QtGui.QApplication.translate("Form", "Show flow direction", None, QtGui.QApplication.UnicodeUTF8))
        self.BrowseShapeOutputFilterNodeNames.setText(QtGui.QApplication.translate("Form", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Output location for filtered shapefile :", None, QtGui.QApplication.UnicodeUTF8))

import resources
