# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_about.ui'
#
# Created: Sat Nov 15 17:25:20 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FormAbout(object):
    def setupUi(self, FormAbout):
        FormAbout.setObjectName(_fromUtf8("FormAbout"))
        FormAbout.setEnabled(True)
        FormAbout.resize(430, 230)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FormAbout.sizePolicy().hasHeightForWidth())
        FormAbout.setSizePolicy(sizePolicy)
        FormAbout.setMinimumSize(QtCore.QSize(430, 230))
        FormAbout.setMaximumSize(QtCore.QSize(430, 230))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/flowmapper/icon3.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormAbout.setWindowIcon(icon)
        FormAbout.setSizeGripEnabled(False)
        FormAbout.setModal(True)
        self.pushButton = QtGui.QPushButton(FormAbout)
        self.pushButton.setGeometry(QtCore.QRect(320, 190, 91, 24))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label_05 = QtGui.QLabel(FormAbout)
        self.label_05.setGeometry(QtCore.QRect(40, 10, 231, 21))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setItalic(False)
        font.setBold(True)
        self.label_05.setFont(font)
        self.label_05.setObjectName(_fromUtf8("label_05"))
        self.label_6 = QtGui.QLabel(FormAbout)
        self.label_6.setGeometry(QtCore.QRect(40, 30, 250, 21))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(FormAbout)
        self.label_7.setGeometry(QtCore.QRect(40, 150, 351, 21))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_7.setFont(font)
        self.label_7.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_10 = QtGui.QLabel(FormAbout)
        self.label_10.setGeometry(QtCore.QRect(40, 80, 191, 21))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(FormAbout)
        self.label_11.setGeometry(QtCore.QRect(40, 100, 371, 21))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(FormAbout)
        self.label_12.setGeometry(QtCore.QRect(40, 50, 211, 21))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_12.setFont(font)
        self.label_12.setOpenExternalLinks(True)
        self.label_12.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(FormAbout)
        self.label_13.setGeometry(QtCore.QRect(40, 120, 81, 21))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label = QtGui.QLabel(FormAbout)
        self.label.setGeometry(QtCore.QRect(10, 10, 25, 25))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/flowmapper/icon.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_8 = QtGui.QLabel(FormAbout)
        self.label_8.setGeometry(QtCore.QRect(40, 170, 51, 21))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_8.setFont(font)
        self.label_8.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(FormAbout)
        self.label_9.setGeometry(QtCore.QRect(100, 190, 131, 21))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_9.setFont(font)
        self.label_9.setOpenExternalLinks(True)
        self.label_9.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_14 = QtGui.QLabel(FormAbout)
        self.label_14.setGeometry(QtCore.QRect(100, 170, 101, 21))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_14.setFont(font)
        self.label_14.setOpenExternalLinks(True)
        self.label_14.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_14.setObjectName(_fromUtf8("label_14"))

        self.retranslateUi(FormAbout)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), FormAbout.reject)
        QtCore.QMetaObject.connectSlotsByName(FormAbout)

    def retranslateUi(self, FormAbout):
        FormAbout.setWindowTitle(QtGui.QApplication.translate("FormAbout", "About FlowMapper", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("FormAbout", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.label_05.setText(QtGui.QApplication.translate("FormAbout", "FlowMapper Plugin for QGIS v2.0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("FormAbout", "v0.4.1  major rel. Dec. 2013 (rev. May. 2016)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("FormAbout", "Developed under GNU General Public License v2 by Dr. Cem GULLUOGLU", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("FormAbout", "MIDDLE EAST TECHNICAL UNIVERSITY", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("FormAbout", "Geodetic & Geographic Information Technologies Interdisciplinary Programme", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("FormAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://plugins.qgis.org/plugins/FlowMapper\"><span style=\" text-decoration: underline; color:#0000ff;\">http://plugins.qgis.org/plugins/FlowMapper</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("FormAbout", "Ankara / TURKEY", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("FormAbout", "Contact :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("FormAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"mailto:cemgulluoglu@gmail.com?subject=About FlowMapper\"><span style=\" text-decoration: underline; color:#0000ff;\">cemgulluoglu@gmail.com</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("FormAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"mailto:cempro@gmail.com?subject=About FlowMapper\"><span style=\" text-decoration: underline; color:#0000ff;\">cempro@gmail.com</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import resources
