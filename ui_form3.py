# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_form3.ui'
#
# Created: Sat Dec 28 23:33:02 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(600, 400)
        Form.setMinimumSize(QtCore.QSize(600, 400))
        Form.setMaximumSize(QtCore.QSize(600, 400))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/flowmapper/icon4.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(Form)
        self.buttonBox.setGeometry(QtCore.QRect(420, 360, 160, 24))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.BrowseShapeInputFilterLength = QtGui.QPushButton(Form)
        self.BrowseShapeInputFilterLength.setGeometry(QtCore.QRect(510, 10, 80, 24))
        self.BrowseShapeInputFilterLength.setObjectName(_fromUtf8("BrowseShapeInputFilterLength"))
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 250, 101, 20))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 210, 180, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.BrowseShapeLineEdit = QtGui.QLineEdit(Form)
        self.BrowseShapeLineEdit.setEnabled(False)
        self.BrowseShapeLineEdit.setGeometry(QtCore.QRect(198, 10, 301, 20))
        self.BrowseShapeLineEdit.setText(_fromUtf8(""))
        self.BrowseShapeLineEdit.setObjectName(_fromUtf8("BrowseShapeLineEdit"))
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 110, 141, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.BrowseShapeOutputFilterLength = QtGui.QPushButton(Form)
        self.BrowseShapeOutputFilterLength.setGeometry(QtCore.QRect(510, 210, 80, 24))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BrowseShapeOutputFilterLength.sizePolicy().hasHeightForWidth())
        self.BrowseShapeOutputFilterLength.setSizePolicy(sizePolicy)
        self.BrowseShapeOutputFilterLength.setObjectName(_fromUtf8("BrowseShapeOutputFilterLength"))
        self.MeanLength_LineEdit = QtGui.QLineEdit(Form)
        self.MeanLength_LineEdit.setGeometry(QtCore.QRect(160, 110, 65, 20))
        self.MeanLength_LineEdit.setText(_fromUtf8(""))
        self.MeanLength_LineEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.MeanLength_LineEdit.setReadOnly(True)
        self.MeanLength_LineEdit.setObjectName(_fromUtf8("MeanLength_LineEdit"))
        self.FilterLength_LineEdit = QtGui.QLineEdit(Form)
        self.FilterLength_LineEdit.setEnabled(True)
        self.FilterLength_LineEdit.setGeometry(QtCore.QRect(220, 250, 60, 20))
        self.FilterLength_LineEdit.setObjectName(_fromUtf8("FilterLength_LineEdit"))
        self.label_01 = QtGui.QLabel(Form)
        self.label_01.setGeometry(QtCore.QRect(10, 10, 180, 20))
        self.label_01.setObjectName(_fromUtf8("label_01"))
        self.CalStatLength = QtGui.QPushButton(Form)
        self.CalStatLength.setEnabled(True)
        self.CalStatLength.setGeometry(QtCore.QRect(270, 70, 321, 24))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.CalStatLength.setFont(font)
        self.CalStatLength.setObjectName(_fromUtf8("CalStatLength"))
        self.BrowseShapeLineEdit_2 = QtGui.QLineEdit(Form)
        self.BrowseShapeLineEdit_2.setEnabled(False)
        self.BrowseShapeLineEdit_2.setGeometry(QtCore.QRect(200, 210, 301, 20))
        self.BrowseShapeLineEdit_2.setText(_fromUtf8(""))
        self.BrowseShapeLineEdit_2.setObjectName(_fromUtf8("BrowseShapeLineEdit_2"))
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 140, 101, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.StdDevLength_LineEdit = QtGui.QLineEdit(Form)
        self.StdDevLength_LineEdit.setGeometry(QtCore.QRect(160, 140, 65, 20))
        self.StdDevLength_LineEdit.setText(_fromUtf8(""))
        self.StdDevLength_LineEdit.setReadOnly(True)
        self.StdDevLength_LineEdit.setObjectName(_fromUtf8("StdDevLength_LineEdit"))
        self.MeanNotZeroLength_LineEdit = QtGui.QLineEdit(Form)
        self.MeanNotZeroLength_LineEdit.setGeometry(QtCore.QRect(500, 110, 65, 20))
        self.MeanNotZeroLength_LineEdit.setText(_fromUtf8(""))
        self.MeanNotZeroLength_LineEdit.setReadOnly(True)
        self.MeanNotZeroLength_LineEdit.setObjectName(_fromUtf8("MeanNotZeroLength_LineEdit"))
        self.label_9 = QtGui.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(270, 110, 221, 20))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.StdDevNotZeroLength_LineEdit = QtGui.QLineEdit(Form)
        self.StdDevNotZeroLength_LineEdit.setGeometry(QtCore.QRect(500, 140, 65, 20))
        self.StdDevNotZeroLength_LineEdit.setText(_fromUtf8(""))
        self.StdDevNotZeroLength_LineEdit.setReadOnly(True)
        self.StdDevNotZeroLength_LineEdit.setObjectName(_fromUtf8("StdDevNotZeroLength_LineEdit"))
        self.label_10 = QtGui.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(270, 140, 161, 20))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.MaxFlowLength_LineEdit = QtGui.QLineEdit(Form)
        self.MaxFlowLength_LineEdit.setGeometry(QtCore.QRect(160, 170, 65, 20))
        self.MaxFlowLength_LineEdit.setText(_fromUtf8(""))
        self.MaxFlowLength_LineEdit.setReadOnly(True)
        self.MaxFlowLength_LineEdit.setObjectName(_fromUtf8("MaxFlowLength_LineEdit"))
        self.label_11 = QtGui.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(10, 170, 131, 20))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(290, 250, 71, 20))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.MinFlowLength_LineEdit = QtGui.QLineEdit(Form)
        self.MinFlowLength_LineEdit.setGeometry(QtCore.QRect(500, 170, 65, 20))
        self.MinFlowLength_LineEdit.setText(_fromUtf8(""))
        self.MinFlowLength_LineEdit.setReadOnly(True)
        self.MinFlowLength_LineEdit.setObjectName(_fromUtf8("MinFlowLength_LineEdit"))
        self.label_13 = QtGui.QLabel(Form)
        self.label_13.setGeometry(QtCore.QRect(270, 170, 221, 20))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(230, 110, 16, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.Length_comboBox = QtGui.QComboBox(Form)
        self.Length_comboBox.setGeometry(QtCore.QRect(110, 250, 101, 22))
        self.Length_comboBox.setObjectName(_fromUtf8("Length_comboBox"))
        self.Length_comboBox.addItem(_fromUtf8(""))
        self.Length_comboBox.addItem(_fromUtf8(""))
        self.Length_comboBox.addItem(_fromUtf8(""))
        self.Length_comboBox.addItem(_fromUtf8(""))
        self.Length_comboBox.addItem(_fromUtf8(""))
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(230, 140, 16, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_14 = QtGui.QLabel(Form)
        self.label_14.setGeometry(QtCore.QRect(230, 170, 16, 20))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_15 = QtGui.QLabel(Form)
        self.label_15.setGeometry(QtCore.QRect(570, 170, 16, 20))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_16 = QtGui.QLabel(Form)
        self.label_16.setGeometry(QtCore.QRect(570, 140, 16, 20))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.label_17 = QtGui.QLabel(Form)
        self.label_17.setGeometry(QtCore.QRect(570, 110, 16, 20))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(200, 40, 391, 20))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.comboBoxSelectSymbology = QtGui.QComboBox(Form)
        self.comboBoxSelectSymbology.setEnabled(True)
        self.comboBoxSelectSymbology.setGeometry(QtCore.QRect(460, 290, 120, 22))
        self.comboBoxSelectSymbology.setObjectName(_fromUtf8("comboBoxSelectSymbology"))
        self.comboBoxSelectSymbology.addItem(_fromUtf8(""))
        self.comboBoxSelectSymbology.addItem(_fromUtf8(""))
        self.comboBoxSelectSymbology.addItem(_fromUtf8(""))
        self.comboBoxSelectSymbology.addItem(_fromUtf8(""))
        self.comboBoxSelectSymbology.addItem(_fromUtf8(""))
        self.label_19 = QtGui.QLabel(Form)
        self.label_19.setGeometry(QtCore.QRect(10, 320, 81, 20))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.Add2MapcheckBox = QtGui.QCheckBox(Form)
        self.Add2MapcheckBox.setEnabled(True)
        self.Add2MapcheckBox.setGeometry(QtCore.QRect(10, 290, 231, 17))
        self.Add2MapcheckBox.setChecked(True)
        self.Add2MapcheckBox.setObjectName(_fromUtf8("Add2MapcheckBox"))
        self.lineEditInterval = QtGui.QLineEdit(Form)
        self.lineEditInterval.setEnabled(False)
        self.lineEditInterval.setGeometry(QtCore.QRect(280, 320, 51, 20))
        self.lineEditInterval.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEditInterval.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEditInterval.setObjectName(_fromUtf8("lineEditInterval"))
        self.comboBoxSelectStdDev = QtGui.QComboBox(Form)
        self.comboBoxSelectStdDev.setEnabled(False)
        self.comboBoxSelectStdDev.setGeometry(QtCore.QRect(460, 320, 120, 22))
        self.comboBoxSelectStdDev.setObjectName(_fromUtf8("comboBoxSelectStdDev"))
        self.comboBoxSelectStdDev.addItem(_fromUtf8(""))
        self.comboBoxSelectStdDev.addItem(_fromUtf8(""))
        self.comboBoxSelectStdDev.addItem(_fromUtf8(""))
        self.comboBoxSelectStdDev.addItem(_fromUtf8(""))
        self.label_20 = QtGui.QLabel(Form)
        self.label_20.setGeometry(QtCore.QRect(380, 320, 81, 20))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.label_21 = QtGui.QLabel(Form)
        self.label_21.setGeometry(QtCore.QRect(200, 320, 81, 20))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.spinBoxClasses = QtGui.QSpinBox(Form)
        self.spinBoxClasses.setEnabled(False)
        self.spinBoxClasses.setGeometry(QtCore.QRect(90, 320, 51, 22))
        self.spinBoxClasses.setMinimum(2)
        self.spinBoxClasses.setProperty(_fromUtf8("value"), 2)
        self.spinBoxClasses.setObjectName(_fromUtf8("spinBoxClasses"))
        self.ShowDirectioncheckBox = QtGui.QCheckBox(Form)
        self.ShowDirectioncheckBox.setEnabled(True)
        self.ShowDirectioncheckBox.setGeometry(QtCore.QRect(280, 290, 121, 17))
        self.ShowDirectioncheckBox.setChecked(True)
        self.ShowDirectioncheckBox.setObjectName(_fromUtf8("ShowDirectioncheckBox"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Form.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Form.reject)
##-----------------------------------------------------------------------------------------------##
##-----------------------------------------------------------------------------------------------##
        QtCore.QObject.connect(self.Add2MapcheckBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.comboBoxSelectSymbology.setEnabled)
        QtCore.QObject.connect(self.Add2MapcheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.reset_enable_disable_state)
        QtCore.QObject.connect(self.comboBoxSelectSymbology, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.enable_disable)
##-----------------------------------------------------------------------------------------------##        
##-----------------------------------------------------------------------------------------------##        
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        Form.setTabOrder(self.BrowseShapeLineEdit, self.BrowseShapeInputFilterLength)
        Form.setTabOrder(self.BrowseShapeInputFilterLength, self.CalStatLength)
        Form.setTabOrder(self.CalStatLength, self.MeanLength_LineEdit)
        Form.setTabOrder(self.MeanLength_LineEdit, self.StdDevLength_LineEdit)
        Form.setTabOrder(self.StdDevLength_LineEdit, self.MaxFlowLength_LineEdit)
        Form.setTabOrder(self.MaxFlowLength_LineEdit, self.MeanNotZeroLength_LineEdit)
        Form.setTabOrder(self.MeanNotZeroLength_LineEdit, self.StdDevNotZeroLength_LineEdit)
        Form.setTabOrder(self.StdDevNotZeroLength_LineEdit, self.MinFlowLength_LineEdit)
        Form.setTabOrder(self.MinFlowLength_LineEdit, self.BrowseShapeLineEdit_2)
        Form.setTabOrder(self.BrowseShapeLineEdit_2, self.BrowseShapeOutputFilterLength)
        Form.setTabOrder(self.BrowseShapeOutputFilterLength, self.Length_comboBox)
        Form.setTabOrder(self.Length_comboBox, self.FilterLength_LineEdit)
        Form.setTabOrder(self.FilterLength_LineEdit, self.Add2MapcheckBox)
        Form.setTabOrder(self.Add2MapcheckBox, self.ShowDirectioncheckBox)
        Form.setTabOrder(self.ShowDirectioncheckBox, self.comboBoxSelectSymbology)
        Form.setTabOrder(self.comboBoxSelectSymbology, self.spinBoxClasses)
        Form.setTabOrder(self.spinBoxClasses, self.lineEditInterval)
        Form.setTabOrder(self.lineEditInterval, self.comboBoxSelectStdDev)
        Form.setTabOrder(self.comboBoxSelectStdDev, self.buttonBox)

##-----------------------------------------------------------------------------------------------##        
##-----------------------------------------------------------------------------------------------##
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
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Filter flow lines by length", None, QtGui.QApplication.UnicodeUTF8))
        self.BrowseShapeInputFilterLength.setText(QtGui.QApplication.translate("Form", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Delete flow lines", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Output location for filtered shapefile :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Average length of flow lines :", None, QtGui.QApplication.UnicodeUTF8))
        self.BrowseShapeOutputFilterLength.setText(QtGui.QApplication.translate("Form", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.FilterLength_LineEdit.setText(QtGui.QApplication.translate("Form", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_01.setText(QtGui.QApplication.translate("Form", "Select shapefile storing flow lines :", None, QtGui.QApplication.UnicodeUTF8))
        self.CalStatLength.setText(QtGui.QApplication.translate("Form", "Calculate Statistics...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Form", "Standard deviation :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Form", "Avg. length of flow lines excluding zero flows :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Form", "Std. Dev. excluding zero flows :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Form", "Maximum flow line length :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("Form", "kilometers", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("Form", "Minimum flow line length excluding zero flows :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Form", "km.", None, QtGui.QApplication.UnicodeUTF8))
        self.Length_comboBox.setItemText(0, QtGui.QApplication.translate("Form", "shorter than <", None, QtGui.QApplication.UnicodeUTF8))
        self.Length_comboBox.setItemText(1, QtGui.QApplication.translate("Form", "<=", None, QtGui.QApplication.UnicodeUTF8))
        self.Length_comboBox.setItemText(2, QtGui.QApplication.translate("Form", "equal to =", None, QtGui.QApplication.UnicodeUTF8))
        self.Length_comboBox.setItemText(3, QtGui.QApplication.translate("Form", ">=", None, QtGui.QApplication.UnicodeUTF8))
        self.Length_comboBox.setItemText(4, QtGui.QApplication.translate("Form", "longer than >", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Form", "km.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("Form", "km.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("Form", "km.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("Form", "km.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("Form", "km.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "* Input shapefile must be created with Flow Mapper or include \"length_km\" field.", None, QtGui.QApplication.UnicodeUTF8))
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
        self.ShowDirectioncheckBox.setText(QtGui.QApplication.translate("Form", "Show flow direction", None, QtGui.QApplication.UnicodeUTF8))

import resources
