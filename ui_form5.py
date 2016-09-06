# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\cem\.qgis\python\plugins\FlowMapper\ui_form5.ui'
#
# Created: Tue Jan 29 03:48:26 2013
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
        Form.resize(520, 185)
        Form.setMinimumSize(QtCore.QSize(520, 185))
        Form.setMaximumSize(QtCore.QSize(520, 185))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/flowmapper/icon6.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(Form)
        self.buttonBox.setGeometry(QtCore.QRect(350, 150, 160, 24))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.BrowseShapeInputExport = QtGui.QPushButton(Form)
        self.BrowseShapeInputExport.setGeometry(QtCore.QRect(430, 10, 79, 24))
        self.BrowseShapeInputExport.setObjectName(_fromUtf8("BrowseShapeInputExport"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 91, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.BrowseShapeLineEdit = QtGui.QLineEdit(Form)
        self.BrowseShapeLineEdit.setEnabled(False)
        self.BrowseShapeLineEdit.setGeometry(QtCore.QRect(130, 10, 291, 20))
        self.BrowseShapeLineEdit.setText(_fromUtf8(""))
        self.BrowseShapeLineEdit.setObjectName(_fromUtf8("BrowseShapeLineEdit"))
        self.BrowseFileOutputExport = QtGui.QPushButton(Form)
        self.BrowseFileOutputExport.setGeometry(QtCore.QRect(430, 110, 79, 24))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BrowseFileOutputExport.sizePolicy().hasHeightForWidth())
        self.BrowseFileOutputExport.setSizePolicy(sizePolicy)
        self.BrowseFileOutputExport.setObjectName(_fromUtf8("BrowseFileOutputExport"))
        self.label_01 = QtGui.QLabel(Form)
        self.label_01.setGeometry(QtCore.QRect(10, 10, 111, 20))
        self.label_01.setObjectName(_fromUtf8("label_01"))
        self.BrowseFileLineEdit = QtGui.QLineEdit(Form)
        self.BrowseFileLineEdit.setEnabled(False)
        self.BrowseFileLineEdit.setGeometry(QtCore.QRect(130, 110, 291, 20))
        self.BrowseFileLineEdit.setText(_fromUtf8(""))
        self.BrowseFileLineEdit.setObjectName(_fromUtf8("BrowseFileLineEdit"))
        self.FileType_comboBox = QtGui.QComboBox(Form)
        self.FileType_comboBox.setGeometry(QtCore.QRect(130, 70, 151, 22))
        self.FileType_comboBox.setObjectName(_fromUtf8("FileType_comboBox"))
        self.FileType_comboBox.addItem(_fromUtf8(""))
        self.FileType_comboBox.addItem(_fromUtf8(""))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(130, 40, 391, 20))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 70, 91, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Form.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Form.reject)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.BrowseShapeLineEdit, self.BrowseShapeInputExport)
        Form.setTabOrder(self.BrowseShapeInputExport, self.BrowseFileLineEdit)
        Form.setTabOrder(self.BrowseFileLineEdit, self.BrowseFileOutputExport)
        Form.setTabOrder(self.BrowseFileOutputExport, self.FileType_comboBox)
        Form.setTabOrder(self.FileType_comboBox, self.buttonBox)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Export...", None, QtGui.QApplication.UnicodeUTF8))
        self.BrowseShapeInputExport.setText(QtGui.QApplication.translate("Form", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Output file name :", None, QtGui.QApplication.UnicodeUTF8))
        self.BrowseFileOutputExport.setText(QtGui.QApplication.translate("Form", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_01.setText(QtGui.QApplication.translate("Form", "Select input shapefile :", None, QtGui.QApplication.UnicodeUTF8))
        self.FileType_comboBox.setItemText(0, QtGui.QApplication.translate("Form", "Google Earth KML", None, QtGui.QApplication.UnicodeUTF8))
        self.FileType_comboBox.setItemText(1, QtGui.QApplication.translate("Form", "MapInfo TAB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "* Input shapefile must have geographic coordinates for proper KML conversion.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Convert to :", None, QtGui.QApplication.UnicodeUTF8))

import resources
