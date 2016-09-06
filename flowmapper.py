"""
/***************************************************************************
 FlowMapper
                                 A QGIS plugin
 This plugin generates discreet flow lines between nodes
                              -------------------
        begin                : 2011-12-04
        copyright            : (C) 2011 by Cem GULLUOGLU
        email                : cempro@gmail.com
 ***************************************************************************/
"""

import sys
import os
#from os.path import isfile
from os.path import realpath
from os.path import isfile

import qgis.gui
from PyQt4 import QtCore, QtGui

#import ogr
from osgeo import ogr
import ogr

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from qgis.gui import *

# Initialize Qt resources from file resources.py
import resources

# Import the code for the dialog
from flowmapperdialog import FlowMapperDialog
import flowmapperdialog
from form2dialog import Form2Dialog
import form2dialog
from form3dialog import Form3Dialog
import form3dialog
from form6dialog import Form6Dialog
import form6dialog
from form4dialog import Form4Dialog
import form4dialog
from form7dialog import Form7Dialog
import form7dialog
from form5dialog import Form5Dialog
import form5dialog
import form_aboutdialog

# Import script that draws flow lines (kullan)
import flowpyv07
#import flowpyInterface (iptal)

class FlowMapper:
  
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/flowmapper/icon.png"), "Generate flow lines and nodes", self.iface.mainWindow())
        self.actionform2 = QAction(QIcon(":/plugins/flowmapper/icon2.png"), "Filter flow lines by magnitude", self.iface.mainWindow())
        self.actionform3 = QAction(QIcon(":/plugins/flowmapper/icon4.png"), "Filter flow lines by length", self.iface.mainWindow())
        self.actionform6 = QAction(QIcon(":/plugins/flowmapper/icon7.png"), "Filter flow lines by node and direction", self.iface.mainWindow())
        self.actionform4 = QAction(QIcon(":/plugins/flowmapper/icon5.png"), "Symbology for flow lines", self.iface.mainWindow())
        self.actionform7 = QAction(QIcon(":/plugins/flowmapper/icon8.png"), "Symbology for flow nodes", self.iface.mainWindow())
        self.actionform5 = QAction(QIcon(":/plugins/flowmapper/icon6.png"), "Export...", self.iface.mainWindow())
        self.actionabout = QAction(QIcon(":/plugins/flowmapper/icon3.png"), "About FlowMapper", self.iface.mainWindow())
        
		# connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        QObject.connect(self.actionform2, SIGNAL("triggered()"), self.form2)
        QObject.connect(self.actionform3, SIGNAL("triggered()"), self.form3)
        QObject.connect(self.actionform6, SIGNAL("triggered()"), self.form6)
        QObject.connect(self.actionform4, SIGNAL("triggered()"), self.form4)
        QObject.connect(self.actionform7, SIGNAL("triggered()"), self.form7)
        QObject.connect(self.actionform5, SIGNAL("triggered()"), self.form5)
        QObject.connect(self.actionabout, SIGNAL("triggered()"), self.about)
        
        # Add toolbar button and menu item to QGIS
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&FlowMapper", self.action)
        self.iface.addPluginToMenu("&FlowMapper", self.actionform2)
        self.iface.addPluginToMenu("&FlowMapper", self.actionform3)
        self.iface.addPluginToMenu("&FlowMapper", self.actionform6)
        self.iface.addPluginToMenu("&FlowMapper", self.actionform4)
        self.iface.addPluginToMenu("&FlowMapper", self.actionform7)
        self.iface.addPluginToMenu("&FlowMapper", self.actionform5)
        self.iface.addPluginToMenu("&FlowMapper", self.actionabout)
       
       
       
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&FlowMapper",self.action)
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("&FlowMapper", self.actionform2)
        self.iface.removeToolBarIcon(self.actionform2)
        self.iface.removePluginMenu("&FlowMapper", self.actionform3)
        self.iface.removeToolBarIcon(self.actionform3)
        self.iface.removePluginMenu("&FlowMapper", self.actionform6)
        self.iface.removeToolBarIcon(self.actionform6)
        self.iface.removePluginMenu("&FlowMapper", self.actionform4)
        self.iface.removeToolBarIcon(self.actionform4)
        self.iface.removePluginMenu("&FlowMapper", self.actionform7)
        self.iface.removeToolBarIcon(self.actionform5)
        self.iface.removePluginMenu("&FlowMapper", self.actionform5)
        self.iface.removeToolBarIcon(self.actionform5)        
        self.iface.removePluginMenu("&FlowMapper", self.actionabout)
        self.iface.removeToolBarIcon(self.actionabout)

    def OutputShp(self):
        dlg = FlowMapperDialog()
        #buttona basip file browser ile output shapefile LINES dosya adi vermek icin fonksiyon
        fd = QtGui.QFileDialog(dlg)
        global SaveShpName
        global SaveShpDirectory
        SaveShpName = fd.getSaveFileName(None, 'Shapefile(*.shp)', 'Type output shapefile name', '*.shp')

    def OutputShpNodes(self):
        dlg = FlowMapperDialog()
        #buttona basip file browser ile output shapefile NODES dosya adi vermek icin fonksiyon
        fd = QtGui.QFileDialog(dlg)
        global SaveShpNameNodes
        global SaveShpDirectoryNodes
        SaveShpNameNodes = fd.getSaveFileName(None, 'Shapefile(*.shp)', 'Type output shapefile name', '*.shp')
		
    def InputNodes(self):
        dlg = FlowMapperDialog()
        #buttona basip file browser ile input node coord. txt dosyasini sectirmek icin fonksiyon
        fd = QtGui.QFileDialog(dlg)
        global InputNodesName
        InputNodesName = fd.getOpenFileName(None, 'Text Files(*.txt)', 'Select txt file', '*.txt')

    def InputNodeNames(self):
        dlg = FlowMapperDialog()
        #buttona basip file browser ile input node coord. txt dosyasini sectirmek icin fonksiyon
        fd = QtGui.QFileDialog(dlg)
        global InputNodeNamesName
        InputNodeNamesName = fd.getOpenFileName(None, 'Text Files(*.txt)', 'Select txt file', '*.txt')        
                
    def InputMatrix(self):
        dlg = FlowMapperDialog()
        #buttona basip file browser ile flow matrix txt dosyasini sectirmek icin fonksiyon
        fd = QtGui.QFileDialog(dlg)
        global InputMatrixName
        InputMatrixName = fd.getOpenFileName(None, 'Text Files(*.txt)', 'Select txt file', '*.txt')

    def InputShpFilter(self):
        dlg = Form2Dialog()
        fd = QtGui.QFileDialog(dlg)
        global InputShpFilterName
        global InputShpFilterDirectory
        InputShpFilterName = fd.getOpenFileName(None, 'Shapefile(*.shp)', 'Select shapefile', '*.shp')
        #InputShpFilterDirectory = os.path.realpath(InputShpFilterName)
        InputShpFilterDirectory = InputShpFilterName
                
    def OutputShpFilter(self):
        dlg = Form2Dialog()
        fd = QtGui.QFileDialog(dlg)
        global OutputShpFilterName
        global OutputShpFilterDirectory
        OutputShpFilterName = fd.getSaveFileName(None, 'Shapefile(*.shp)', 'Type output shapefile name', '*.shp')
        #OutputShpFilterDirectory = os.path.realpath(OutputShpFilterName)
        OutputShpFilterDirectory = OutputShpFilterName

    def InputShpFilterLength(self):
        dlg = Form3Dialog()
        fd = QtGui.QFileDialog(dlg)
        global InputShpFilterLengthName
        global InputShpFilterLengthDirectory
        InputShpFilterLengthName = fd.getOpenFileName(None, 'Shapefile(*.shp)', 'Select shapefile', '*.shp')
        #InputShpFilterLengthDirectory = os.path.realpath(InputShpFilterLengthName)
        InputShpFilterLengthDirectory = InputShpFilterLengthName

    def InputShpSymbology(self):
        dlg = Form4Dialog()
        fd = QtGui.QFileDialog(dlg)
        global InputShpSymbologyName
        global InputShpSymbologyDirectory
        InputShpSymbologyName = fd.getOpenFileName(None, 'Shapefile(*.shp)', 'Select shapefile', '*.shp')
        #InputShpSymbologyDirectory = os.path.realpath(InputShpSymbologyName)
        InputShpSymbologyDirectory = InputShpSymbologyName

    def InputShpNodeSymbology(self):
        dlg = Form7Dialog()
        fd = QtGui.QFileDialog(dlg)
        global InputShpNodeSymbologyName
        global InputShpNodeSymbologyDirectory
        InputShpNodeSymbologyName = fd.getOpenFileName(None, 'Shapefile(*.shp)', 'Select shapefile', '*.shp')
        #InputShpNodeSymbologyDirectory = os.path.realpath(InputShpNodeSymbologyName)
        InputShpNodeSymbologyDirectory = InputShpNodeSymbologyName        
        
    def OutputShpFilterLength(self):
        dlg = Form3Dialog()
        fd = QtGui.QFileDialog(dlg)
        global OutputShpFilterLengthName
        global OutputShpFilterLengthDirectory
        OutputShpFilterLengthName = fd.getSaveFileName(None, 'Shapefile(*.shp)', 'Type output shapefile name', '*.shp')
        #OutputShpFilterLengthDirectory = os.path.realpath(OutputShpFilterLengthName)
        OutputShpFilterLengthDirectory = OutputShpFilterLengthName

    def InputShpNameExport(self):
        dlg = Form5Dialog()
        fd = QtGui.QFileDialog(dlg)
        global BrowseShapeLineEditNameExport
        global BrowseShapeLineEditDirectoryExport
        BrowseShapeLineEditNameExport = fd.getOpenFileName(None, 'Shapefile(*.shp)', 'Select shapefile', '*.shp')
        #BrowseShapeLineEditDirectoryExport = os.path.realpath(BrowseShapeLineEditNameExport)
        BrowseShapeLineEditDirectoryExport = BrowseShapeLineEditNameExport
    
    def OutputFileNameExport(self):
        dlg = Form5Dialog()
        fd = QtGui.QFileDialog(dlg)
        global BrowseFileLineEditNameExport
        global BrowseFileLineEditDirectoryExport
        BrowseFileLineEditNameExport = fd.getSaveFileName(None, '', 'Type output file name with extension', '*.shp')
        #BrowseFileLineEditDirectoryNameExport = os.path.realpath(BrowseFileLineEditNameExport)    
        BrowseFileLineEditDirectoryNameExport = BrowseFileLineEditNameExport

    def InputShpFilterNodeNames(self):
        dlg = Form6Dialog()
        fd = QtGui.QFileDialog(dlg)
        global InputShpFilterNodeNamesName
        global InputShpFilterNodeNamesDirectory
        InputShpFilterNodeNamesName = fd.getOpenFileName(None, 'Shapefile(*.shp)', 'Select shapefile', '*.shp')
        #InputShpFilterLengthDirectory = os.path.realpath(InputShpFilterLengthName)
        InputShpFilterNodeNamesDirectory = InputShpFilterNodeNamesName

    def OutputShpFilterNodeNames(self):
        dlg = Form6Dialog()
        fd = QtGui.QFileDialog(dlg)
        global OutputShpFilterNodeNamesName
        global OutputShpFilterNodeNamesDirectory
        OutputShpFilterNodeNamesName = fd.getSaveFileName(None, '', 'Type output file name with extension', '*.shp')
        #InputShpFilterLengthDirectory = os.path.realpath(InputShpFilterLengthName)
        OutputShpFilterNodeNamesDirectory = OutputShpFilterNodeNamesName
        
    def CalStatFilter(self):
        global CalStatNoOfFeatures
        global CalStatNoOfFeaturesZero
        global CalStatSumMagnitude
        global CalStatMaxFlow
        global CalStatMinFlow
        global CalStatMean
        global CalStatMeanNotZero        
        global CalStatStdDev
        global CalStatStdDevNotZero
        
        shp = ogr.Open(str(InputShpFilterDirectory),1)
        layer = shp.GetLayer(0)
        #get number of all features in shapefile
        CalStatNoOfFeatures = str(layer.GetFeatureCount())
        
#----------------------------------------------------------------------------------------------------        
        feature = layer.GetNextFeature()
        counterNotZero = 0
        CalStatSumMagnitude = 0
        CalStatList = []  
        while feature:
            magnitude = feature.GetField('magnitude')
            if magnitude > 0:
                CalStatList.append(int(magnitude))
                CalStatMinFlow = min(CalStatList)
                CalStatMaxFlow = max(CalStatList) 
                counterNotZero = counterNotZero + 1
            CalStatSumMagnitude = CalStatSumMagnitude + magnitude
            feature.Destroy()
            feature = layer.GetNextFeature()
        CalStatMean = str((CalStatSumMagnitude / int(CalStatNoOfFeatures)))
        CalStatMean = str(round(float(CalStatMean), 3))
        CalStatMeanNotZero = str(CalStatSumMagnitude / int(counterNotZero))
        CalStatMeanNotZero = str(round(float(CalStatMeanNotZero), 3))
        
        CalStatSumMagnitude = str(CalStatSumMagnitude)
        CalStatNoOfFeaturesZero = str(int(CalStatNoOfFeatures)-int(counterNotZero))
        CalStatMaxFlow = str(int(CalStatMaxFlow))
        CalStatMinFlow = str(int(CalStatMinFlow))
        
        layer.ResetReading()
        
        feature = layer.GetNextFeature()
        var = 0
        varNotZero = 0
              
        while feature:
            magnitude = feature.GetField('magnitude')
            var = var + ((magnitude - float(CalStatMean))**2)
            if magnitude > 0:
                varNotZero = varNotZero + ((magnitude - float(CalStatMeanNotZero))**2)
            feature.Destroy()
            feature = layer.GetNextFeature()
        CalStatStdDev = str((var / int(CalStatNoOfFeatures))**0.5)
        CalStatStdDev = str(round(float(CalStatStdDev), 3))
        CalStatStdDevNotZero = str((varNotZero / int(counterNotZero))**0.5)
        CalStatStdDevNotZero = str(round(float(CalStatStdDevNotZero), 3))
        
        layer.ResetReading()
        
        feature = layer.GetNextFeature()
        
        shp.Destroy()
#----------------------------------------------------------------------------------------------------

        #QMessageBox.information(self.iface.mainWindow(),"info" ,"Statistics calculated successfully !")
        
        #QMessageBox.information(self.iface.mainWindow(),"minflow" ,QString(str(CalStatMinFlow)))   
        #QMessageBox.information(self.iface.mainWindow(),"maxflow" ,QString(str(CalStatMaxFlow)))   
        #QMessageBox.information(self.iface.mainWindow(),"info" ,QString(str(CalStatSumMagnitude)))   
        #QMessageBox.information(self.iface.mainWindow(),"info" ,QString(str(CalStatStdDevNotZero)))               
        #QMessageBox.information(self.iface.mainWindow(),"info" ,QString(str(CalStatStdDev)))               
        #QMessageBox.information(self.iface.mainWindow(),"info" ,QString(str(CalStatMeanNotZero)))               
        #QMessageBox.information(self.iface.mainWindow(),"info" ,QString(str(CalStatMean)))   

    def CalStatFilterLength(self):
    
        global CalStatLengthMax
        global CalStatLengthMin
        global CalStatLengthMean
        global CalStatLengthMeanNotZero        
        global CalStatLengthStdDev
        global CalStatLengthStdDevNotZero
        
        shp = ogr.Open(str(InputShpFilterLengthDirectory),1)
        layer = shp.GetLayer(0)
        #get number of all features in shapefile
        CalStatLengthNoOfFeatures = str(layer.GetFeatureCount())
#----------------------------------------------------------------------------------------------------        
        feature = layer.GetNextFeature()
        counterNotZero = 0
        CalStatLengthSumLength = 0
        CalStatLengthList = []    
        while feature:
            length = feature.GetField('length_km')
            if length > 0:
                CalStatLengthList.append(length)
                CalStatLengthMin = min(CalStatLengthList)
                CalStatLengthMax = max(CalStatLengthList) 
                counterNotZero = counterNotZero + 1
            CalStatLengthSumLength = CalStatLengthSumLength + length
            feature.Destroy()
            feature = layer.GetNextFeature()
        CalStatLengthMean = str((CalStatLengthSumLength / int(CalStatLengthNoOfFeatures)))
        CalStatLengthMean = str(round(float(CalStatLengthMean), 3))
        CalStatLengthMeanNotZero = str(CalStatLengthSumLength / int(counterNotZero))
        CalStatLengthMeanNotZero = str(round(float(CalStatLengthMeanNotZero), 3))
        
        CalStatLengthSumLength = str(CalStatLengthSumLength)
        CalStatLengthNoOfFeaturesZero = str(int(CalStatLengthNoOfFeatures)-int(counterNotZero))
        CalStatLengthMin = str(round((CalStatLengthMin),3))
        CalStatLengthMax = str(round((CalStatLengthMax),3))
        
        layer.ResetReading()
        
        feature = layer.GetNextFeature()
        varLength = 0
        varLengthNotZero = 0
            
        while feature:
            length = feature.GetField('length_km')
            varLength = varLength + ((length - float(CalStatLengthMean))**2)
            if length > 0:
                varLengthNotZero = varLengthNotZero + ((length - float(CalStatLengthMeanNotZero))**2)
            feature.Destroy()
            feature = layer.GetNextFeature()
        CalStatLengthStdDev = str((varLength / int(CalStatLengthNoOfFeatures))**0.5)
        CalStatLengthStdDev = str(round(float(CalStatLengthStdDev), 3))
        CalStatLengthStdDevNotZero = str((varLengthNotZero / int(counterNotZero))**0.5)
        CalStatLengthStdDevNotZero = str(round(float(CalStatLengthStdDevNotZero), 3))

        layer.ResetReading()
        
        feature = layer.GetNextFeature()
        
        shp.Destroy()
#----------------------------------------------------------------------------------------------------
        #QMessageBox.information(self.iface.mainWindow(),"info" ,"Statistics calculated successfully !")

    
    def CalStatSymbology(self):
        
        dlg = Form4Dialog() 
        
        global GradSymNoOfFeaturesSymbology
        GradSymNoOfFeaturesSymbology=""
        global GradSymNoOfFeaturesZeroSymbology
        GradSymNoOfFeaturesZeroSymbology=""
        global GradSymMinSymbology
        GradSymMinSymbology=""
        global GradSymMaxSymbology
        GradSymMaxSymbology=""
        global GradSymSumMagnitudeSymbology
        GradSymSumMagnitudeSymbology=""
        global GradSymMeanSymbology
        GradSymMeanSymbology=""
        global GradSymMeanNotZeroSymbology        
        GradSymMeanNotZeroSymbology=""
        global GradSymStdDevSymbology
        GradSymStdDevSymbology=""
        global GradSymStdDevNotZeroSymbology                    
        GradSymStdDevNotZeroSymbology=""
        global GradSymListSymbology
        GradSymListSymbology=""


        extension = os.path.splitext(str(InputShpSymbologyName))[1]
        if extension == ".shp" and ".shp" in InputShpSymbologyName and len(InputShpSymbologyName) > 4: 

        
            shp = ogr.Open(str(InputShpSymbologyName),1)
            layer = shp.GetLayer(0)
            GradSymNoOfFeaturesSymbology = str(layer.GetFeatureCount())
            
            feature = layer.GetNextFeature()
            counterNotZero = 0
            GradSymSumMagnitudeSymbology = 0
            GradSymListSymbology= []    
            
            while feature:
                magnitude = feature.GetField('magnitude')
                if magnitude > 0:
                    counterNotZero = counterNotZero + 1
                    GradSymListSymbology.append(int(magnitude))
                    GradSymMinSymbology = min(GradSymListSymbology)
                    GradSymMaxSymbology = max(GradSymListSymbology)
                GradSymSumMagnitudeSymbology = GradSymSumMagnitudeSymbology + magnitude
                feature.Destroy()
                feature = layer.GetNextFeature()
            GradSymMeanSymbology = str(round(float(GradSymSumMagnitudeSymbology / int(GradSymNoOfFeaturesSymbology)),3))
            GradSymMeanNotZeroSymbology = str(round(float(GradSymSumMagnitudeSymbology / int(counterNotZero)),3))
            GradSymSumMagnitudeSymbology = str(GradSymSumMagnitudeSymbology)
            GradSymNoOfFeaturesZeroSymbology = str(int(GradSymNoOfFeaturesSymbology)-int(counterNotZero))
            GradSymMinSymbology = str(GradSymMinSymbology)
            GradSymMaxSymbology = str(GradSymMaxSymbology)
            layer.ResetReading()
        
            GradSymVar = 0
            GradSymVarNotZero = 0
        
            feature = layer.GetNextFeature()
            while feature:
                magnitude = feature.GetField('magnitude')
                #feature = layer.GetNextFeature()
                GradSymVar = GradSymVar + ((magnitude - float(GradSymMeanSymbology))**2)
                if magnitude > 0:
                    GradSymVarNotZero = GradSymVarNotZero + ((magnitude - float(GradSymMeanNotZeroSymbology))**2)
                feature.Destroy()
                feature = layer.GetNextFeature()
            GradSymStdDevSymbology = str(round(((GradSymVar / int(GradSymNoOfFeaturesSymbology))**0.5), 3))
            GradSymStdDevNotZeroSymbology = str(round(((GradSymVarNotZero / int(counterNotZero))**0.5), 3))
            layer.ResetReading()
            
            shp.Destroy()

            
    def CalStatNodeSymbology(self):
        
        dlg = Form7Dialog() 
        
        global comboBoxSelectField_combotext
        
        global GradSymNoOfFeaturesNodeSymbology
        GradSymNoOfFeaturesNodeSymbology=""
        global GradSymNoOfFeaturesZeroNodeSymbology
        GradSymNoOfFeaturesZeroNodeSymbology=""
        global GradSymMinNodeSymbology
        GradSymMinNodeSymbology=""
        global GradSymMaxNodeSymbology
        GradSymMaxNodeSymbology=""
        global GradSymSumMagnitudeNodeSymbology
        GradSymSumMagnitudeNodeSymbology=""
        global GradSymMeanNodeSymbology
        GradSymMeanNodeSymbology=""
        global GradSymMeanNotZeroNodeSymbology        
        GradSymMeanNotZeroNodeSymbology=""
        global GradSymStdDevNodeSymbology
        GradSymStdDevNodeSymbology=""
        global GradSymStdDevNotZeroNodeSymbology                    
        GradSymStdDevNotZeroNodeSymbology=""
        global GradSymListNodeSymbology
        GradSymListNodeSymbology=""


        extension = os.path.splitext(str(InputShpNodeSymbologyName))[1]
        if extension == ".shp" and ".shp" in InputShpNodeSymbologyName and len(InputShpNodeSymbologyName) > 4: 

            shp = ogr.Open(str(InputShpNodeSymbologyName),1)
            layer = shp.GetLayer(0)
            GradSymNoOfFeaturesNodeSymbology = str(layer.GetFeatureCount())
            
            feature = layer.GetNextFeature()
            counterNotZero = 0
            GradSymSumMagnitudeNodeSymbology = 0
            GradSymListNodeSymbology= []    
            
            while feature:
                magnitude = feature.GetField(str(comboBoxSelectField_combotext))
                #magnitude = feature.GetField('magnitude')
                if magnitude > 0:
                    counterNotZero = counterNotZero + 1
                    GradSymListNodeSymbology.append(float(magnitude))
                    GradSymMinNodeSymbology = round(min(GradSymListNodeSymbology),3)
                    GradSymMaxNodeSymbology = round(max(GradSymListNodeSymbology),3)
                GradSymSumMagnitudeNodeSymbology = GradSymSumMagnitudeNodeSymbology + magnitude
                feature.Destroy()
                feature = layer.GetNextFeature()
            GradSymMeanNodeSymbology = str(round(float(GradSymSumMagnitudeNodeSymbology / int(GradSymNoOfFeaturesNodeSymbology)),3))
            GradSymMeanNotZeroNodeSymbology = str(round(float(GradSymSumMagnitudeNodeSymbology / int(counterNotZero)),3))
            GradSymSumMagnitudeNodeSymbology = str(GradSymSumMagnitudeNodeSymbology)
            GradSymNoOfFeaturesZeroNodeSymbology = str(int(GradSymNoOfFeaturesNodeSymbology)-int(counterNotZero))
            GradSymMinNodeSymbology = str(GradSymMinNodeSymbology)
            GradSymMaxNodeSymbology = str(GradSymMaxNodeSymbology)
            layer.ResetReading()
        
            GradSymVar = 0
            GradSymVarNotZero = 0
        
            feature = layer.GetNextFeature()
            while feature:
                magnitude = feature.GetField(str(comboBoxSelectField_combotext))
                #magnitude = feature.GetField('magnitude')
                #feature = layer.GetNextFeature()
                GradSymVar = GradSymVar + ((magnitude - float(GradSymMeanNodeSymbology))**2)
                if magnitude > 0:
                    GradSymVarNotZero = GradSymVarNotZero + ((magnitude - float(GradSymMeanNotZeroNodeSymbology))**2)
                feature.Destroy()
                feature = layer.GetNextFeature()
            GradSymStdDevNodeSymbology = str(round(((GradSymVar / int(GradSymNoOfFeaturesNodeSymbology))**0.5), 3))
            GradSymStdDevNotZeroNodeSymbology = str(round(((GradSymVarNotZero / int(counterNotZero))**0.5), 3))
            layer.ResetReading()
            
            shp.Destroy()    

            
    def form2(self):
        
        dlg = Form2Dialog() 
        #dlg.exec_()
        dlg.show()
        
        dlg.ui.CalStat.setEnabled(False)
        
        global text_magnitude
        text_magnitude = dlg.ui.Filter_LineEdit.text()

        
        #result = dlg2.exec_() 
        
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputFilter,QtCore.SIGNAL("clicked()"), self.InputShpFilter)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputFilter,QtCore.SIGNAL("clicked()"), dlg.SetTextBrowseInputShapeFilter)
        
        QtCore.QObject.connect(dlg.ui.BrowseShapeOutputFilter,QtCore.SIGNAL("clicked()"), self.OutputShpFilter)
        QtCore.QObject.connect(dlg.ui.BrowseShapeOutputFilter,QtCore.SIGNAL("clicked()"), dlg.SetTextBrowseOutputShapeFilter) 

        #get stats
        QtCore.QObject.connect(dlg.ui.CalStat,QtCore.SIGNAL("clicked()"), self.CalStatFilter)
        QtCore.QObject.connect(dlg.ui.CalStat,QtCore.SIGNAL("clicked()"), dlg.No_Of_Features)
        QtCore.QObject.connect(dlg.ui.CalStat,QtCore.SIGNAL("clicked()"), dlg.No_Of_FeaturesNotZero)
        QtCore.QObject.connect(dlg.ui.CalStat,QtCore.SIGNAL("clicked()"), dlg.Mean)
        QtCore.QObject.connect(dlg.ui.CalStat,QtCore.SIGNAL("clicked()"), dlg.MeanNotZero)
        QtCore.QObject.connect(dlg.ui.CalStat,QtCore.SIGNAL("clicked()"), dlg.MaxFlow)
        QtCore.QObject.connect(dlg.ui.CalStat,QtCore.SIGNAL("clicked()"), dlg.MinFlow)
        QtCore.QObject.connect(dlg.ui.CalStat,QtCore.SIGNAL("clicked()"), dlg.SumMagnitude)
        QtCore.QObject.connect(dlg.ui.CalStat,QtCore.SIGNAL("clicked()"), dlg.StdDev)
        QtCore.QObject.connect(dlg.ui.CalStat,QtCore.SIGNAL("clicked()"), dlg.StdDevNotZero)
        
        #dlg.exec_()         
        
        result = dlg.exec_() 
        # See if OK was pressed

        
        if result == 1:

            text_magnitude = dlg.ui.Filter_LineEdit.text()
            #QMessageBox.information(self.iface.mainWindow(),"cmd" , text_magnitude)
            Magnitude_combotext = dlg.ui.Magnitude_comboBox.currentText() 
            #QMessageBox.information(self.iface.mainWindow(),"cmd" , Magnitude_combotext)
            if Magnitude_combotext == "less than <":
                command1 = 'ogr2ogr -f "ESRI Shapefile" -where "magnitude >= '
            elif Magnitude_combotext == "<=":
                command1 = 'ogr2ogr -f "ESRI Shapefile" -where "magnitude > '                
            elif Magnitude_combotext == "equal to =":
                command1 = 'ogr2ogr -f "ESRI Shapefile" -where "magnitude <> '                
            elif Magnitude_combotext == ">=":
                command1 = 'ogr2ogr -f "ESRI Shapefile" -where "magnitude < '
            elif Magnitude_combotext == "greater than >=":
                command1 = 'ogr2ogr -f "ESRI Shapefile" -where "magnitude <= '                
            
            command2 = '"'
            #command3 = '\"'
            command = str(command1)+str(text_magnitude)+ str(command2)+" "+ str(OutputShpFilterName)+ " "+str(InputShpFilterName)
            #QMessageBox.information(self.iface.mainWindow(),"info" ,str(command))
            
            os.system(command)
            
            if dlg.ui.Add2MapcheckBox.isChecked() == False:
                message = "Flows "+str(Magnitude_combotext)+str(text_magnitude)+" filtered and "+str(OutputShpFilterName)+" created successfully !"
                QMessageBox.information(self.iface.mainWindow(),"info" ,message)
            else:    
                
                if dlg.ui.comboBoxSelectSymbology.currentText() == "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False: 
                    self.iface.addVectorLayer(str(OutputShpFilterName), str(OutputShpFilterName), "ogr")
                    SuccessMessage = str(OutputShpFilterName) + " created successfully !"
                    QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")                
                
                elif dlg.ui.comboBoxSelectSymbology.currentText() == "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True:
                    layer = QgsVectorLayer(str(OutputShpFilterName), str(OutputShpFilterName), 'ogr')
                    #Use the currently selected layer
                    #layer = qgis.utils.iface.mapCanvas().currentLayer()
                    registry = QgsSymbolLayerV2Registry.instance()
                    lineMeta = registry.symbolLayerMetadata("SimpleLine")
                    markerMeta = registry.symbolLayerMetadata("MarkerLine")
                    
                    symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
                    
                    #Line layer
                    lineLayer = lineMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'offset': '0', 'penstyle': 'solid', 'use_custom_dash': '0', 'joinstyle': 'bevel', 'capstyle': 'square'})
                    
                    #Marker layer
                    #markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'interval': '3', 'rotate': '1', 'placement': 'interval', 'offset': '0'})
                    markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'rotate': '1', 'placement': 'centralpoint', 'offset': '0'})
                    subSymbol = markerLayer.subSymbol()
                    
                    #Replace the default layer with our own SimpleMarker
                    subSymbol.deleteSymbolLayer(0)
                    triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer({'name': 'filled_arrowhead', 'color': '255,0,0', 'color_border': '0,0,0', 'offset': '0,0', 'size': '3', 'angle': '0'})
                    subSymbol.appendSymbolLayer(triangle)
                    
                    #Replace the default layer with our two custom layers
                    symbol.deleteSymbolLayer(0)
                    symbol.appendSymbolLayer(lineLayer)
                    symbol.appendSymbolLayer(markerLayer)
                    
                    #Replace the renderer of the current layer
                    renderer = QgsSingleSymbolRendererV2(symbol)
                    layer.setRendererV2(renderer)    
                    #
                    QgsMapLayerRegistry.instance().addMapLayer( layer ) 
                    
                    SuccessMessage = str(OutputShpFilterName) + " created successfully !"
                    #QMessageBox.information(self.iface.mainWindow(), "info", QString(SuccessMessage), QString('Close'))
                    QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")
                
                else:

                    global GradSymNoOfFeatures
                    global GradSymNoOfFeaturesZero
                    global GradSymMin
                    global GradSymMax
                    global GradSymSumMagnitude
                    global GradSymMean
                    global GradSymMeanNotZero        
                    global GradSymStdDev
                    global GradSymStdDevNotZero                    
                    global GradSymList 
                    
                    shp = ogr.Open(str(OutputShpFilterName),1)
                    layer = shp.GetLayer(0)
                    GradSymNoOfFeatures = str(layer.GetFeatureCount())
                    
                    feature = layer.GetNextFeature()
                    counterNotZero = 0
                    GradSymSumMagnitude = 0
                    GradSymList= []    
                    
                    while feature:
                        magnitude = feature.GetField('magnitude')
                        if magnitude > 0:
                            counterNotZero = counterNotZero + 1
                            GradSymList.append(int(magnitude))
                            GradSymMin = min(GradSymList)
                            GradSymMax = max(GradSymList)
                        GradSymSumMagnitude = GradSymSumMagnitude + magnitude
                        feature.Destroy()
                        feature = layer.GetNextFeature()
                    GradSymMean = str(round(float(GradSymSumMagnitude / int(GradSymNoOfFeatures)),3))
                    GradSymMeanNotZero = str(round(float(GradSymSumMagnitude / int(counterNotZero)),3))
                    GradSymSumMagnitude = str(GradSymSumMagnitude)
                    GradSymNoOfFeaturesZero = str(int(GradSymNoOfFeatures)-int(counterNotZero))
                    GradSymMin = str(GradSymMin)
                    GradSymMax = str(GradSymMax)
                    layer.ResetReading()

                    GradSymVar = 0
                    GradSymVarNotZero = 0

                    feature = layer.GetNextFeature()
                    while feature:
                        magnitude = feature.GetField('magnitude')
                        #feature = layer.GetNextFeature()
                        GradSymVar = GradSymVar + ((magnitude - float(GradSymMean))**2)
                        if magnitude > 0:
                            GradSymVarNotZero = GradSymVarNotZero + ((magnitude - float(GradSymMeanNotZero))**2)
                        feature.Destroy()
                        feature = layer.GetNextFeature()
                    GradSymStdDev = str(round(((GradSymVar / int(GradSymNoOfFeatures))**0.5), 3))
                    GradSymStdDevNotZero = str(round(((GradSymVarNotZero / int(counterNotZero))**0.5), 3))
                    layer.ResetReading()
                    
                    shp.Destroy()
                
                    registry = QgsSymbolLayerV2Registry.instance()
                    lineMeta = registry.symbolLayerMetadata("SimpleLine")
                    markerMeta = registry.symbolLayerMetadata("MarkerLine")
                
                    def validatedDefaultSymbol(geometryType):
                        symbol = QgsSymbolV2.defaultSymbol(geometryType)
                        if symbol is None:
                            if geometryType == QGis.Point:
                                symbol = QgsMarkerSymbolV2()
                            elif geometryType == QGis.Line:
                                symbol =  QgsLineSymbolV2()
                            elif geometryType == QGis.Polygon:
                                symbol = QgsFillSymbolV2()
                        return symbol
                    
                    #Create Symbology
                    def makeSymbologyForRange(layer, min ,max, label ,colour, alpha, width):
                        symbol = validatedDefaultSymbol(layer.geometryType())
                        
                        if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True: 
                            #Line layer
                            lineLayer = lineMeta.createSymbolLayer({'width': '0.5', 'color': '255,0,0', 'offset': '0', 'penstyle': 'solid', 'use_custom_dash': '0', 'joinstyle': 'bevel', 'capstyle': 'square'})
                            #Marker layer
                            markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'rotate': '1', 'placement': 'centralpoint', 'offset': '0'})
                            subSymbol = markerLayer.subSymbol()
                            #Replace the default layer with our own SimpleMarker
                            subSymbol.deleteSymbolLayer(0)
                            triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer({'name': 'filled_arrowhead', 'color': '255,0,0', 'color_border': '255,255,255', 'offset': '0,0', 'size': '3', 'outline_width': '0.5', 'angle': '0'})
                            subSymbol.appendSymbolLayer(triangle)
                            #Replace the default layer with our two custom layers
                            symbol.deleteSymbolLayer(0)
                            symbol.appendSymbolLayer(lineLayer)
                            symbol.appendSymbolLayer(markerLayer)
                            
                            symbol.setColor(colour)
                            symbol.setAlpha(alpha)
                            symbol.setWidth(width)
                            range = QgsRendererRangeV2(min, max, symbol, label)
                            
                        elif dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False:
                            symbol.setColor(colour)
                            symbol.setAlpha(alpha)
                            symbol.setWidth(width)
                            range = QgsRendererRangeV2(min, max, symbol, label)
                        
                        return range                    

                    vlayer = QgsVectorLayer(str(OutputShpFilterName), str(OutputShpFilterName), 'ogr')
                    myTargetField = 'magnitude'
                    
                    #Define base line symbol width and multiplier factor for graduated classes
                    global basesymbolwidth
                    global multipliersymbolwidth
                    if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True: 
                        global basesymbolwidth
                        global multipliersymbolwidth
                        basesymbolwidth = 3.0
                        multipliersymbolwidth = 2.0
                    elif dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False:
                        global basesymbolwidth
                        global multipliersymbolwidth
                        basesymbolwidth = 0.25                        
                        multipliersymbolwidth = 0.75                    

                    #Equal Interval
                    if dlg.ui.comboBoxSelectSymbology.currentText() == "Equal Interval":
                        GradSymNoOfClasses = dlg.ui.spinBoxClasses.value() 
                        GradSymInterval = round(((int(GradSymMax) - int(GradSymMin)) / float(GradSymNoOfClasses)),0)
                        myRangeList = []
                        for i in range(GradSymNoOfClasses):
                            if i == 0:
                                classlabel = str(GradSymMin)+" - "+str(int(GradSymMin)+GradSymInterval)
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), int(GradSymMin)+GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                            elif i == (GradSymNoOfClasses - 1):
                                classlabel = str(int(GradSymMin)+(GradSymInterval*i)+0.001)+" - "+str(GradSymMax)
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                            else:
                                classlabel = str(int(GradSymMin)+(GradSymInterval*i)+0.001)+" - "+str(int(GradSymMin)+GradSymInterval*(i+1))
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin)+(GradSymInterval*i)+0.001, int(GradSymMin)+GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                        vlayer.setRendererV2( myRenderer )
                        message = "Flows "+str(Magnitude_combotext)+str(text_magnitude)+" filtered and "+str(OutputShpFilterName)+" created successfully !"
                        QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 

                    #Defined Interval
                    elif dlg.ui.comboBoxSelectSymbology.currentText() == "Defined Interval":
                        GradSymInterval = int(dlg.ui.lineEditInterval.text())
                        GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                        myRangeList = []
                        for i in range(GradSymNoOfClasses):
                            if i == 0:
                                classlabel = str(GradSymMin)+" - "+str(GradSymInterval)
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                            elif i == (GradSymNoOfClasses - 1):
                                classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymMax)
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                            else:
                                classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                        vlayer.setRendererV2( myRenderer )
                        message = "Flows "+str(Magnitude_combotext)+str(text_magnitude)+" filtered and "+str(OutputShpFilterName)+" created successfully !"
                        QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                        
                    #Standard Deviation
                    elif dlg.ui.comboBoxSelectSymbology.currentText() == "Standard Deviation":
                        if dlg.ui.comboBoxSelectStdDev.currentText() == "1/4 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) / 4
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 0.25
                        elif dlg.ui.comboBoxSelectStdDev.currentText() == "1/2 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) / 2
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 0.5
                        elif dlg.ui.comboBoxSelectStdDev.currentText() == "1 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) 
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 1.0
                        elif dlg.ui.comboBoxSelectStdDev.currentText() == "2 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) * 2
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 2.0
                        myRangeList = []
                        for i in range(GradSymNoOfClasses):                            
                            if i == 0:                            
                                classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str(GradSymMin)+" - "+str(GradSymInterval)                            
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))                            
                            elif i == (GradSymNoOfClasses - 1):                            
                                classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str((GradSymInterval*i)+0.001)+" - "+str(GradSymMax)                            
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))                            
                            else:                            
                                classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))                            
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))                            
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )                            
                        vlayer.setRendererV2( myRenderer )                            
                        message = "Flows "+str(Magnitude_combotext)+str(text_magnitude)+" filtered and "+str(OutputShpFilterName)+" created successfully !"                            
                        QMessageBox.information(self.iface.mainWindow(),"info" ,message)                            
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer )                             
                    
                    #Equal Size Classes
                    elif dlg.ui.comboBoxSelectSymbology.currentText() == "Equal Size Classes":
                        GradSymNoOfClasses = dlg.ui.spinBoxClasses.value() 
                        GradSymNoOfFeaturesZero = int(GradSymNoOfFeaturesZero)
                        GradSymNoOfFeaturesInInterval = int(  round(((int(GradSymNoOfFeatures)-int(GradSymNoOfFeaturesZero))/float(GradSymNoOfClasses)),0) ) 
                        myRangeList = []
                        GradSymList.sort()
                        for i in range(GradSymNoOfClasses):
                            if i == 0:
                                classlabel = str(GradSymMin)+" - "+str(GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1])
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                            elif i == (GradSymNoOfClasses - 1):
                                classlabel = str(GradSymList[GradSymNoOfFeaturesInInterval*i])+" - "+str(GradSymMax)
                                myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                            else:
                                classlabel = str(GradSymList[GradSymNoOfFeaturesInInterval*i])+" - "+str(GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1])
                                myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                        vlayer.setRendererV2( myRenderer )
                        message = "Flows "+str(Magnitude_combotext)+str(text_magnitude)+" filtered and "+str(OutputShpFilterName)+" created successfully !"
                        QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                        

        
        
        
    def form3(self):
        
        dlg = Form3Dialog() 
        #dlg.exec_()
        dlg.show()

        dlg.ui.CalStatLength.setEnabled(False)
        
        global text_length
        text_length = dlg.ui.FilterLength_LineEdit.text()

        
        #result = dlg2.exec_() 
        
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputFilterLength,QtCore.SIGNAL("clicked()"), self.InputShpFilterLength)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputFilterLength,QtCore.SIGNAL("clicked()"), dlg.SetTextBrowseInputShapeFilterLength)
        
        QtCore.QObject.connect(dlg.ui.BrowseShapeOutputFilterLength,QtCore.SIGNAL("clicked()"), self.OutputShpFilterLength)
        QtCore.QObject.connect(dlg.ui.BrowseShapeOutputFilterLength,QtCore.SIGNAL("clicked()"), dlg.SetTextBrowseOutputShapeFilterLength)         

        #get stats for flowline lengths
        QtCore.QObject.connect(dlg.ui.CalStatLength,QtCore.SIGNAL("clicked()"), self.CalStatFilterLength)
        QtCore.QObject.connect(dlg.ui.CalStatLength,QtCore.SIGNAL("clicked()"), dlg.MeanLength)
        QtCore.QObject.connect(dlg.ui.CalStatLength,QtCore.SIGNAL("clicked()"), dlg.MeanLengthNotZero)
        QtCore.QObject.connect(dlg.ui.CalStatLength,QtCore.SIGNAL("clicked()"), dlg.MaxFlowLength)
        QtCore.QObject.connect(dlg.ui.CalStatLength,QtCore.SIGNAL("clicked()"), dlg.MinFlowLength)
        QtCore.QObject.connect(dlg.ui.CalStatLength,QtCore.SIGNAL("clicked()"), dlg.StdDevLength)
        QtCore.QObject.connect(dlg.ui.CalStatLength,QtCore.SIGNAL("clicked()"), dlg.StdDevLengthNotZero)        
        
        
        result = dlg.exec_() 
        
        if result == 1:
            
            text_length = dlg.ui.FilterLength_LineEdit.text()
            Length_combotext = str(dlg.ui.Length_comboBox.currentText()) 
            if Length_combotext == "shorter than <":
                command1 = 'ogr2ogr -f "ESRI Shapefile" -where "length_km >= '
            elif Length_combotext == "<=":
                command1 = 'ogr2ogr -f "ESRI Shapefile" -where "length_km > '                
            elif Length_combotext == "equal to =":
                command1 = 'ogr2ogr -f "ESRI Shapefile" -where "length_km <> '                
            elif Length_combotext == ">=":
                command1 = 'ogr2ogr -f "ESRI Shapefile" -where "length_km < '
            elif Length_combotext == "longer than >":
                command1 = 'ogr2ogr -f "ESRI Shapefile" -where "length_km <= '                

            command2 = '"'
            #command3 = '\"'
            command = str(command1)+str(text_length)+ str(command2)+" "+ str(OutputShpFilterLengthName)+ " "+str(InputShpFilterLengthName)
            #QMessageBox.information(self.iface.mainWindow(),"info" ,str(command))
                        
            os.system(command)
            
            if dlg.ui.Add2MapcheckBox.isChecked() == False:
                message = "Flows "+str(Length_combotext)+str(text_length)+" filtered and "+str(OutputShpFilterLengthName)+" created successfully !"
                QMessageBox.information(self.iface.mainWindow(),"info" ,message)
            else:    
                
                if dlg.ui.comboBoxSelectSymbology.currentText() == "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False: 
                    self.iface.addVectorLayer(str(OutputShpFilterLengthName), str(OutputShpFilterLengthName), "ogr")
                    SuccessMessage = str(OutputShpFilterLengthName) + " created successfully !"
                    QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")                

                elif dlg.ui.comboBoxSelectSymbology.currentText() == "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True:
                    layer = QgsVectorLayer(str(OutputShpFilterLengthName), str(OutputShpFilterLengthName), 'ogr')
                    #Use the currently selected layer
                    #layer = qgis.utils.iface.mapCanvas().currentLayer()
                    registry = QgsSymbolLayerV2Registry.instance()
                    lineMeta = registry.symbolLayerMetadata("SimpleLine")
                    markerMeta = registry.symbolLayerMetadata("MarkerLine")
                    
                    symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
                    
                    #Line layer
                    lineLayer = lineMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'offset': '0', 'penstyle': 'solid', 'use_custom_dash': '0', 'joinstyle': 'bevel', 'capstyle': 'square'})
                    
                    #Marker layer
                    #markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'interval': '3', 'rotate': '1', 'placement': 'interval', 'offset': '0'})
                    markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'rotate': '1', 'placement': 'centralpoint', 'offset': '0'})
                    subSymbol = markerLayer.subSymbol()
                    
                    #Replace the default layer with our own SimpleMarker
                    subSymbol.deleteSymbolLayer(0)
                    triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer({'name': 'filled_arrowhead', 'color': '255,0,0', 'color_border': '0,0,0', 'offset': '0,0', 'size': '3', 'angle': '0'})
                    subSymbol.appendSymbolLayer(triangle)
                    
                    #Replace the default layer with our two custom layers
                    symbol.deleteSymbolLayer(0)
                    symbol.appendSymbolLayer(lineLayer)
                    symbol.appendSymbolLayer(markerLayer)
                    
                    #Replace the renderer of the current layer
                    renderer = QgsSingleSymbolRendererV2(symbol)
                    layer.setRendererV2(renderer)    
                    #
                    QgsMapLayerRegistry.instance().addMapLayer( layer ) 
                    
                    SuccessMessage = str(OutputShpFilterLengthName) + " created successfully !"
                    #QMessageBox.information(self.iface.mainWindow(), "info", QString(SuccessMessage), QString('Close'))
                    QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")
                    
                else:

                    global GradSymNoOfFeatures
                    global GradSymNoOfFeaturesZero
                    global GradSymMin
                    global GradSymMax
                    global GradSymSumMagnitude
                    global GradSymMean
                    global GradSymMeanNotZero        
                    global GradSymStdDev
                    global GradSymStdDevNotZero                    
                    global GradSymList 
                    
                    shp = ogr.Open(str(OutputShpFilterLengthName),1)
                    layer = shp.GetLayer(0)
                    GradSymNoOfFeatures = str(layer.GetFeatureCount())
                    
                    feature = layer.GetNextFeature()
                    counterNotZero = 0
                    GradSymSumMagnitude = 0
                    GradSymList= []    
                    
                    while feature:
                        magnitude = feature.GetField('magnitude')
                        if magnitude > 0:
                            counterNotZero = counterNotZero + 1
                            GradSymList.append(int(magnitude))
                            GradSymMin = min(GradSymList)
                            GradSymMax = max(GradSymList)
                        GradSymSumMagnitude = GradSymSumMagnitude + magnitude
                        feature.Destroy()
                        feature = layer.GetNextFeature()
                    GradSymMean = str(round(float(GradSymSumMagnitude / int(GradSymNoOfFeatures)),3))
                    GradSymMeanNotZero = str(round(float(GradSymSumMagnitude / int(counterNotZero)),3))
                    GradSymSumMagnitude = str(GradSymSumMagnitude)
                    GradSymNoOfFeaturesZero = str(int(GradSymNoOfFeatures)-int(counterNotZero))
                    GradSymMin = str(GradSymMin)
                    GradSymMax = str(GradSymMax)
                    layer.ResetReading()

                    GradSymVar = 0
                    GradSymVarNotZero = 0

                    feature = layer.GetNextFeature()
                    while feature:
                        magnitude = feature.GetField('magnitude')
                        #feature = layer.GetNextFeature()
                        GradSymVar = GradSymVar + ((magnitude - float(GradSymMean))**2)
                        if magnitude > 0:
                            GradSymVarNotZero = GradSymVarNotZero + ((magnitude - float(GradSymMeanNotZero))**2)
                        feature.Destroy()
                        feature = layer.GetNextFeature()
                    GradSymStdDev = str(round(((GradSymVar / int(GradSymNoOfFeatures))**0.5), 3))
                    GradSymStdDevNotZero = str(round(((GradSymVarNotZero / int(counterNotZero))**0.5), 3))
                    layer.ResetReading()
                    
                    shp.Destroy()

                    registry = QgsSymbolLayerV2Registry.instance()
                    lineMeta = registry.symbolLayerMetadata("SimpleLine")
                    markerMeta = registry.symbolLayerMetadata("MarkerLine")
                    
                    def validatedDefaultSymbol(geometryType):
                        symbol = QgsSymbolV2.defaultSymbol(geometryType)
                        if symbol is None:
                            if geometryType == QGis.Point:
                                symbol = QgsMarkerSymbolV2()
                            elif geometryType == QGis.Line:
                                symbol =  QgsLineSymbolV2()
                            elif geometryType == QGis.Polygon:
                                symbol = QgsFillSymbolV2()
                        return symbol
                    
                    #Create Symbology
                    def makeSymbologyForRange(layer, min ,max, label ,colour, alpha, width):
                        symbol = validatedDefaultSymbol(layer.geometryType())
                        
                        if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True: 
                            #Line layer
                            lineLayer = lineMeta.createSymbolLayer({'width': '0.5', 'color': '255,0,0', 'offset': '0', 'penstyle': 'solid', 'use_custom_dash': '0', 'joinstyle': 'bevel', 'capstyle': 'square'})
                            #Marker layer
                            markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'rotate': '1', 'placement': 'centralpoint', 'offset': '0'})
                            subSymbol = markerLayer.subSymbol()
                            #Replace the default layer with our own SimpleMarker
                            subSymbol.deleteSymbolLayer(0)
                            triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer({'name': 'filled_arrowhead', 'color': '255,0,0', 'color_border': '255,255,255', 'offset': '0,0', 'size': '3', 'outline_width': '0.5', 'angle': '0'})
                            subSymbol.appendSymbolLayer(triangle)
                            #Replace the default layer with our two custom layers
                            symbol.deleteSymbolLayer(0)
                            symbol.appendSymbolLayer(lineLayer)
                            symbol.appendSymbolLayer(markerLayer)

                            symbol.setColor(colour)
                            symbol.setAlpha(alpha)
                            symbol.setWidth(width)
                            range = QgsRendererRangeV2(min, max, symbol, label)
                        
                        elif dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False:
                            symbol.setColor(colour)
                            symbol.setAlpha(alpha)
                            symbol.setWidth(width)
                            range = QgsRendererRangeV2(min, max, symbol, label)
                        
                        return range                    

                    vlayer = QgsVectorLayer(str(OutputShpFilterLengthName), str(OutputShpFilterLengthName), 'ogr')
                    myTargetField = 'magnitude'

                    #Define base line symbol width and multiplier factor for graduated classes
                    global basesymbolwidth
                    global multipliersymbolwidth
                    if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True: 
                        global basesymbolwidth
                        global multipliersymbolwidth
                        basesymbolwidth = 3.0
                        multipliersymbolwidth = 2.0
                    elif dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False:
                        global basesymbolwidth
                        global multipliersymbolwidth
                        basesymbolwidth = 0.25                        
                        multipliersymbolwidth = 0.75
                    
                    #Equal Interval
                    if dlg.ui.comboBoxSelectSymbology.currentText() == "Equal Interval":
                        GradSymNoOfClasses = dlg.ui.spinBoxClasses.value() 
                        GradSymInterval = round(((int(GradSymMax) - int(GradSymMin)) / float(GradSymNoOfClasses)),0)
                        myRangeList = []
                        for i in range(GradSymNoOfClasses):
                            if i == 0:
                                classlabel = str(GradSymMin)+" - "+str(int(GradSymMin)+GradSymInterval)
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), int(GradSymMin)+GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                            elif i == (GradSymNoOfClasses - 1):
                                classlabel = str(int(GradSymMin)+(GradSymInterval*i)+0.001)+" - "+str(GradSymMax)
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                            else:
                                classlabel = str(int(GradSymMin)+(GradSymInterval*i)+0.001)+" - "+str(int(GradSymMin)+GradSymInterval*(i+1))
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin)+(GradSymInterval*i)+0.001, int(GradSymMin)+(GradSymInterval*(i+1)), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                        vlayer.setRendererV2( myRenderer )
                        message = "Flows "+str(Length_combotext)+str(text_length)+" filtered and "+str(OutputShpFilterLengthName)+" created successfully !"
                        QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                    #Defined Interval
                    elif dlg.ui.comboBoxSelectSymbology.currentText() == "Defined Interval":
                        GradSymInterval = int(dlg.ui.lineEditInterval.text())
                        GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                        myRangeList = []
                        for i in range(GradSymNoOfClasses):
                            if i == 0:
                                classlabel = str(GradSymMin)+" - "+str(GradSymInterval)
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                            elif i == (GradSymNoOfClasses - 1):
                                classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymMax)
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                            else:
                                classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                        vlayer.setRendererV2( myRenderer )
                        message = "Flows "+str(Length_combotext)+str(text_length)+" filtered and "+str(OutputShpFilterLengthName)+" created successfully !"
                        QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                    #Standard Deviation
                    elif dlg.ui.comboBoxSelectSymbology.currentText() == "Standard Deviation":
                        if dlg.ui.comboBoxSelectStdDev.currentText() == "1/4 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) / 4
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 0.25
                        elif dlg.ui.comboBoxSelectStdDev.currentText() == "1/2 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) / 2
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 0.5
                        elif dlg.ui.comboBoxSelectStdDev.currentText() == "1 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) 
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 1.0
                        elif dlg.ui.comboBoxSelectStdDev.currentText() == "2 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) * 2
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 2.0
                        myRangeList = []
                        for i in range(GradSymNoOfClasses):                            
                            if i == 0:                            
                                classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str(GradSymMin)+" - "+str(GradSymInterval)                            
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))                            
                            elif i == (GradSymNoOfClasses - 1):                            
                                classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str((GradSymInterval*i)+0.001)+" - "+str(GradSymMax)                            
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))                            
                            else:                            
                                classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))                            
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))                            
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )                            
                        vlayer.setRendererV2( myRenderer )                            
                        message = "Flows "+str(Length_combotext)+str(text_length)+" filtered and "+str(OutputShpFilterLengthName)+" created successfully !"                            
                        QMessageBox.information(self.iface.mainWindow(),"info" ,message)                            
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer )                             
                    #Equal Size Classes
                    elif dlg.ui.comboBoxSelectSymbology.currentText() == "Equal Size Classes":
                        GradSymNoOfClasses = dlg.ui.spinBoxClasses.value() 
                        GradSymNoOfFeaturesZero = int(GradSymNoOfFeaturesZero)
                        GradSymNoOfFeaturesInInterval = int(  round(((int(GradSymNoOfFeatures)-int(GradSymNoOfFeaturesZero))/float(GradSymNoOfClasses)),0) ) 
                        myRangeList = []
                        GradSymList.sort()
                        for i in range(GradSymNoOfClasses):
                            if i == 0:
                                classlabel = str(GradSymMin)+" - "+str(GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1])
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                            elif i == (GradSymNoOfClasses - 1):
                                classlabel = str(GradSymList[GradSymNoOfFeaturesInInterval*i])+" - "+str(GradSymMax)
                                myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                            else:
                                classlabel = str(GradSymList[GradSymNoOfFeaturesInInterval*i])+" - "+str(GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1])
                                myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                        vlayer.setRendererV2( myRenderer )
                        message = "Flows "+str(Length_combotext)+str(text_length)+" filtered and "+str(OutputShpFilterLengthName)+" created successfully !"
                        QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 

    def SelectColorSymbology_1(self):
        dlg = Form4Dialog() 
        global color_name_1
        global r1 
        global g1 
        global b1
        color = QtGui.QColorDialog.getColor()
        color_name_1 = str(color.name())
        if color.isValid():
            r1 = color.red()
            g1 = color.green()
            b1 = color.blue()
        #QMessageBox.information(self.iface.mainWindow(),"info" ,QString(r1))
        #QMessageBox.information(self.iface.mainWindow(),"info" ,QString(g1))
        #QMessageBox.information(self.iface.mainWindow(),"info" ,QString(b1))
        
        
    def SelectColorSymbology_2(self):
        dlg = Form4Dialog() 
        global color_name_2
        global r2
        global g2 
        global b2
        color = QtGui.QColorDialog.getColor()
        color_name_2 = str(color.name())
        if color.isValid():
            r2 = color.red()
            g2 = color.green()
            b2 = color.blue()
            
    def SelectColorSymbology_3(self):
        dlg = Form4Dialog() 
        global color_name_3
        global r3, g3, b3
        color = QtGui.QColorDialog.getColor()
        color_name_3 = str(color.name())
        if color.isValid():
            r3 = color.red()
            g3 = color.green()
            b3 = color.blue()
            
    def SelectColorSymbology_4(self):
        dlg = Form4Dialog() 
        global color_name_4
        global r4, g4, b4
        color = QtGui.QColorDialog.getColor()
        color_name_4 = str(color.name())
        if color.isValid():
            r4 = color.red()
            g4 = color.green()
            b4 = color.blue()
            
    def SelectColorSymbology_5(self):
        dlg = Form4Dialog() 
        global color_name_5
        global r5, g5, b5
        color = QtGui.QColorDialog.getColor()
        color_name_5 = str(color.name())
        if color.isValid():
            r5 = color.red()
            g5 = color.green()
            b5 = color.blue()
            
    def SelectColorSymbology_6(self):
        dlg = Form4Dialog() 
        global color_name_6
        global r6, g6, b6
        color = QtGui.QColorDialog.getColor()
        color_name_6 = str(color.name())
        if color.isValid():
            r6 = color.red()
            g6 = color.green()
            b6 = color.blue()
            
    def SelectColorSymbology_7(self):
        dlg = Form4Dialog() 
        global color_name_7
        global r7, g7, b7
        color = QtGui.QColorDialog.getColor()
        color_name_7 = str(color.name())
        if color.isValid():
            r7 = color.red()
            g7 = color.green()
            b7 = color.blue()
            
    def SelectColorSymbology_8(self):
        dlg = Form4Dialog() 
        global color_name_8
        global r8, g8, b8
        color = QtGui.QColorDialog.getColor()
        color_name_8 = str(color.name())
        if color.isValid():
            r8 = color.red()
            g8 = color.green()
            b8 = color.blue()
            

    def form4(self):

        dlg = Form4Dialog() 
        dlg.show()
        
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputSymbology,QtCore.SIGNAL("clicked()"), self.InputShpSymbology)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputSymbology,QtCore.SIGNAL("clicked()"), dlg.SetTextBrowseInputShapeSymbology)
        
        #get stats for flow line symbology
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputSymbology,QtCore.SIGNAL("clicked()"), self.CalStatSymbology)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputSymbology,QtCore.SIGNAL("clicked()"), dlg.MeanSymbology)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputSymbology,QtCore.SIGNAL("clicked()"), dlg.MaxSymbology)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputSymbology,QtCore.SIGNAL("clicked()"), dlg.MinSymbology)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputSymbology,QtCore.SIGNAL("clicked()"), dlg.StdDevSymbology)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputSymbology,QtCore.SIGNAL("clicked()"), dlg.NoOfFeaturesSymbology)
        
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_1,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_1)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_1,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_1)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_2,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_2)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_2,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_2)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_3,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_3)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_3,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_3)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_4,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_4)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_4,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_4)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_5,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_5)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_5,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_5)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_6,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_6)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_6,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_6)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_7,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_7)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_7,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_7)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_8,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_8)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_8,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_8)
        
        result = dlg.exec_() 
        
        if result == 1:
            if dlg.ui.comboBoxSelectSymbology.currentText() == "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False:
                self.iface.addVectorLayer(str(InputShpSymbologyName), str(InputShpSymbologyName), "ogr")
                SuccessMessage = str(InputShpSymbologyName) + " created successfully !"
                QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")                

            elif dlg.ui.comboBoxSelectSymbology.currentText() == "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True:
                layer = QgsVectorLayer(str(InputShpSymbologyName), str(InputShpSymbologyName), 'ogr')
                #Use the currently selected layer
                #layer = qgis.utils.iface.mapCanvas().currentLayer()
                registry = QgsSymbolLayerV2Registry.instance()
                lineMeta = registry.symbolLayerMetadata("SimpleLine")
                markerMeta = registry.symbolLayerMetadata("MarkerLine")
                
                symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
                
                #Line layer
                lineLayer = lineMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'offset': '0', 'penstyle': 'solid', 'use_custom_dash': '0', 'joinstyle': 'bevel', 'capstyle': 'square'})
                
                #Marker layer
                #markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'interval': '3', 'rotate': '1', 'placement': 'interval', 'offset': '0'})
                markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'rotate': '1', 'placement': 'centralpoint', 'offset': '0'})
                subSymbol = markerLayer.subSymbol()
                
                #Replace the default layer with our own SimpleMarker
                subSymbol.deleteSymbolLayer(0)
                triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer({'name': 'filled_arrowhead', 'color': '255,0,0', 'color_border': '0,0,0', 'offset': '0,0', 'size': '3', 'angle': '0'})
                subSymbol.appendSymbolLayer(triangle)
                
                #Replace the default layer with our two custom layers
                symbol.deleteSymbolLayer(0)
                symbol.appendSymbolLayer(lineLayer)
                symbol.appendSymbolLayer(markerLayer)
                
                #Replace the renderer of the current layer
                renderer = QgsSingleSymbolRendererV2(symbol)
                layer.setRendererV2(renderer)    
                #
                QgsMapLayerRegistry.instance().addMapLayer( layer ) 
                
                SuccessMessage = str(InputShpSymbologyName) + " created successfully !"
                #QMessageBox.information(self.iface.mainWindow(), "info", QString(SuccessMessage), QString('Close'))
                QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")
                 
            else:

                global GradSymNoOfFeatures
                global GradSymNoOfFeaturesZero
                global GradSymMin
                global GradSymMax
                global GradSymSumMagnitude
                global GradSymMean
                global GradSymMeanNotZero        
                global GradSymStdDev
                global GradSymStdDevNotZero                    
                global GradSymList 
                
                shp = ogr.Open(str(InputShpSymbologyName),1)
                layer = shp.GetLayer(0)
                GradSymNoOfFeatures = str(layer.GetFeatureCount())
                
                feature = layer.GetNextFeature()
                counterNotZero = 0
                GradSymSumMagnitude = 0
                GradSymList= []    
                
                while feature:
                    magnitude = feature.GetField('magnitude')
                    if magnitude > 0:
                        counterNotZero = counterNotZero + 1
                        GradSymList.append(int(magnitude))
                        GradSymMin = min(GradSymList)
                        GradSymMax = max(GradSymList)
                    GradSymSumMagnitude = GradSymSumMagnitude + magnitude
                    feature.Destroy()
                    feature = layer.GetNextFeature()
                GradSymMean = str(round(float(GradSymSumMagnitude / int(GradSymNoOfFeatures)),3))
                GradSymMeanNotZero = str(round(float(GradSymSumMagnitude / int(counterNotZero)),3))
                GradSymSumMagnitude = str(GradSymSumMagnitude)
                GradSymNoOfFeaturesZero = str(int(GradSymNoOfFeatures)-int(counterNotZero))
                GradSymMin = str(GradSymMin)
                GradSymMax = str(GradSymMax)
                layer.ResetReading()

                GradSymVar = 0
                GradSymVarNotZero = 0

                feature = layer.GetNextFeature()
                while feature:
                    magnitude = feature.GetField('magnitude')
                    #feature = layer.GetNextFeature()
                    GradSymVar = GradSymVar + ((magnitude - float(GradSymMean))**2)
                    if magnitude > 0:
                        GradSymVarNotZero = GradSymVarNotZero + ((magnitude - float(GradSymMeanNotZero))**2)
                    feature.Destroy()
                    feature = layer.GetNextFeature()
                GradSymStdDev = str(round(((GradSymVar / int(GradSymNoOfFeatures))**0.5), 3))
                GradSymStdDevNotZero = str(round(((GradSymVarNotZero / int(counterNotZero))**0.5), 3))
                layer.ResetReading()
                
                shp.Destroy()
                
                registry = QgsSymbolLayerV2Registry.instance()
                lineMeta = registry.symbolLayerMetadata("SimpleLine")
                markerMeta = registry.symbolLayerMetadata("MarkerLine")
            
                def validatedDefaultSymbol(geometryType):
                    symbol = QgsSymbolV2.defaultSymbol(geometryType)
                    if symbol is None:
                        if geometryType == QGis.Point:
                            symbol = QgsMarkerSymbolV2()
                        elif geometryType == QGis.Line:
                            symbol =  QgsLineSymbolV2()
                        elif geometryType == QGis.Polygon:
                            symbol = QgsFillSymbolV2()
                    return symbol
                
                #Create Symbology
                def makeSymbologyForRange(layer, min ,max, label ,colour, alpha, width):
                    symbol = validatedDefaultSymbol(layer.geometryType())
                        
                    if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True: 
                        #Line layer
                        lineLayer = lineMeta.createSymbolLayer({'width': '0.5', 'color': '255,0,0', 'offset': '0', 'penstyle': 'solid', 'use_custom_dash': '0', 'joinstyle': 'bevel', 'capstyle': 'square'})
                        #Marker layer
                        markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'rotate': '1', 'placement': 'centralpoint', 'offset': '0'})
                        subSymbol = markerLayer.subSymbol()
                        #Replace the default layer with our own SimpleMarker
                        subSymbol.deleteSymbolLayer(0)
                        triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer({'name': 'filled_arrowhead', 'color': '255,0,0', 'color_border': '255,255,255', 'offset': '0,0', 'size': '3', 'outline_width': '0.5', 'angle': '0'})
                        subSymbol.appendSymbolLayer(triangle)
                        #Replace the default layer with our two custom layers
                        symbol.deleteSymbolLayer(0)
                        symbol.appendSymbolLayer(lineLayer)
                        symbol.appendSymbolLayer(markerLayer)
                    
                        symbol.setColor(colour)
                        symbol.setAlpha(alpha)
                        symbol.setWidth(width)
                        range = QgsRendererRangeV2(min, max, symbol, label)
                    
                    elif dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False:
                        symbol.setColor(colour)
                        symbol.setAlpha(alpha)
                        symbol.setWidth(width)
                        range = QgsRendererRangeV2(min, max, symbol, label)
                    
                    return range                    

                vlayer = QgsVectorLayer(str(InputShpSymbologyName), str(InputShpSymbologyName), 'ogr')
                myTargetField = 'magnitude'
                
                #Define base line symbol width and multiplier factor for graduated classes
                global basesymbolwidth
                global multipliersymbolwidth
                if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True: 
                    global basesymbolwidth
                    global multipliersymbolwidth
                    basesymbolwidth = 3.0
                    multipliersymbolwidth = 2.0
                elif dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False:
                    global basesymbolwidth
                    global multipliersymbolwidth
                    basesymbolwidth = 0.25                        
                    multipliersymbolwidth = 0.80                    
                
                #Equal Interval
                if dlg.ui.comboBoxSelectSymbology.currentText() == "Equal Interval":
                    GradSymNoOfClasses = dlg.ui.spinBoxClasses.value() 
                    GradSymInterval = round(((int(GradSymMax) - int(GradSymMin)) / float(GradSymNoOfClasses)),0)
                    myRangeList = []
                    for i in range(GradSymNoOfClasses):
                        if i == 0:
                            classlabel = str(GradSymMin)+" - "+str(int(GradSymMin)+GradSymInterval)
                            myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), int(GradSymMin)+GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                        elif i == (GradSymNoOfClasses - 1):
                            classlabel = str(int(GradSymMin)+(GradSymInterval*i)+0.001)+" - "+str(GradSymMax)
                            myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                        else:
                            classlabel = str(int(GradSymMin)+(GradSymInterval*i)+0.001)+" - "+str(int(GradSymMin)+GradSymInterval*(i+1))
                            myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin)+(GradSymInterval*i)+0.001, int(GradSymMin)+GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                    myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                    vlayer.setRendererV2( myRenderer )
                    message = "Equal interval representation created and ready to be added into map canvas !"
                    QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                    QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                #Defined Interval
                elif dlg.ui.comboBoxSelectSymbology.currentText() == "Defined Interval":
                    GradSymInterval = int(dlg.ui.lineEditInterval.text())
                    GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                    myRangeList = []
                    for i in range(GradSymNoOfClasses):
                        if i == 0:
                            classlabel = str(GradSymMin)+" - "+str(GradSymInterval)
                            myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                        elif i == (GradSymNoOfClasses - 1):
                            classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymMax)
                            myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                        else:
                            classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))
                            myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                    myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                    vlayer.setRendererV2( myRenderer )
                    message = "Defined interval representation created and ready to be added into map canvas !"
                    QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                    QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                #Standard Deviation
                elif dlg.ui.comboBoxSelectSymbology.currentText() == "Standard Deviation":
                    if dlg.ui.comboBoxSelectStdDev.currentText() == "1/4 Std. Dev.":
                        GradSymInterval = float(GradSymStdDevNotZero) / 4
                        GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                        classlabelStdDev = 0.25
                    elif dlg.ui.comboBoxSelectStdDev.currentText() == "1/2 Std. Dev.":
                        GradSymInterval = float(GradSymStdDevNotZero) / 2
                        GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                        classlabelStdDev = 0.5
                    elif dlg.ui.comboBoxSelectStdDev.currentText() == "1 Std. Dev.":
                        GradSymInterval = float(GradSymStdDevNotZero) 
                        GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                        classlabelStdDev = 1.0
                    elif dlg.ui.comboBoxSelectStdDev.currentText() == "2 Std. Dev.":
                        GradSymInterval = float(GradSymStdDevNotZero) * 2
                        GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                        classlabelStdDev = 2.0
                    myRangeList = []
                    for i in range(GradSymNoOfClasses):                            
                        if i == 0:                            
                            classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str(GradSymMin)+" - "+str(GradSymInterval)                            
                            myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))                            
                        elif i == (GradSymNoOfClasses - 1):                            
                            classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str((GradSymInterval*i)+0.001)+" - "+str(GradSymMax)                            
                            myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))                            
                        else:                            
                            classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))                            
                            myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))                            
                    myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )                            
                    vlayer.setRendererV2( myRenderer )                            
                    message = "Standard deviation interval representation created and ready to be added into map canvas !"
                    QMessageBox.information(self.iface.mainWindow(),"info" ,message)                            
                    QgsMapLayerRegistry.instance().addMapLayer( vlayer )                             
                #Equal Size Classes
                elif dlg.ui.comboBoxSelectSymbology.currentText() == "Equal Size Classes":
                    GradSymNoOfClasses = dlg.ui.spinBoxClasses.value() 
                    GradSymNoOfFeaturesZero = int(GradSymNoOfFeaturesZero)
                    GradSymNoOfFeaturesInInterval = int(  round(((int(GradSymNoOfFeatures)-int(GradSymNoOfFeaturesZero))/float(GradSymNoOfClasses)),0) ) 
                    myRangeList = []
                    GradSymList.sort()
                    for i in range(GradSymNoOfClasses):
                        if i == 0:
                            classlabel = str(GradSymMin)+" - "+str(GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1])
                            myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                        elif i == (GradSymNoOfClasses - 1):
                            classlabel = str(GradSymList[GradSymNoOfFeaturesInInterval*i])+" - "+str(GradSymMax)
                            myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                        else:
                            classlabel = str(GradSymList[GradSymNoOfFeaturesInInterval*i])+" - "+str(GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1])
                            myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                    myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                    vlayer.setRendererV2( myRenderer )
                    message = "Equal size classes representation created and ready to be added into map canvas !"
                    QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                    QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                #Manual Interval
                elif dlg.ui.comboBoxSelectSymbology.currentText() == "Manual Interval":
                    
                    if dlg.ui.spinBoxClasses.value() >= 1 :
                        Interval_1 =  int(dlg.ui.lineEditManualInterval_1.text())
                    if dlg.ui.spinBoxClasses.value() >= 2 :
                        Interval_2 =  int(dlg.ui.lineEditManualInterval_2.text())
                    if dlg.ui.spinBoxClasses.value() >= 3 :
                        Interval_3 =  int(dlg.ui.lineEditManualInterval_3.text())
                    if dlg.ui.spinBoxClasses.value() >= 4 :
                        Interval_4 =  int(dlg.ui.lineEditManualInterval_4.text())
                    if dlg.ui.spinBoxClasses.value() >= 5 :
                        Interval_5 =  int(dlg.ui.lineEditManualInterval_5.text())
                    if dlg.ui.spinBoxClasses.value() >= 6 :
                        Interval_6 =  int(dlg.ui.lineEditManualInterval_6.text())
                    if dlg.ui.spinBoxClasses.value() >= 7 :
                        Interval_7 =  int(dlg.ui.lineEditManualInterval_7.text())
                    if dlg.ui.spinBoxClasses.value() >= 8 :
                        Interval_8 =  int(dlg.ui.lineEditManualInterval_8.text())
                    Thickness_1 = dlg.ui.doubleSpinBoxThickness_1.text()
                    Thickness_1 = float(Thickness_1.replace(",",".")) 
                    Thickness_2 = dlg.ui.doubleSpinBoxThickness_2.text()
                    Thickness_2 = float(Thickness_2.replace(",",".")) 
                    Thickness_3 = dlg.ui.doubleSpinBoxThickness_3.text()
                    Thickness_3 = float(Thickness_3.replace(",",".")) 
                    Thickness_4 = dlg.ui.doubleSpinBoxThickness_4.text()
                    Thickness_4 = float(Thickness_4.replace(",",".")) 
                    Thickness_5 = dlg.ui.doubleSpinBoxThickness_5.text()
                    Thickness_5 = float(Thickness_5.replace(",",".")) 
                    Thickness_6 = dlg.ui.doubleSpinBoxThickness_6.text()
                    Thickness_6 = float(Thickness_6.replace(",",".")) 
                    Thickness_7 = dlg.ui.doubleSpinBoxThickness_7.text()
                    Thickness_7 = float(Thickness_7.replace(",",".")) 
                    Thickness_8 = dlg.ui.doubleSpinBoxThickness_8.text()
                    Thickness_8 = float(Thickness_8.replace(",",".")) 
                    
                    myRangeList = []
                    
                    if dlg.ui.spinBoxClasses.value() >= 1 :
                        classlabel1 = str(GradSymMin)+" - "+str(Interval_1)
                        myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), int(Interval_1), classlabel1 , QColor(r1, g1, b1), 1, Thickness_1 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 2 :                                                                                                          
                        classlabel2 = str(Interval_1)+" - "+str(Interval_2)                                                                                          
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_1), int(Interval_2), classlabel2 , QColor(r2, g2, b2), 1, Thickness_2 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 3 :                                                                                                          
                        classlabel3 = str(Interval_2)+" - "+str(Interval_3)                                                                                          
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_2), int(Interval_3), classlabel3 , QColor(r3, g3, b3), 1, Thickness_3 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 4 :                                                                                                          
                        classlabel4 = str(Interval_3)+" - "+str(Interval_4)                                                                                          
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_3), int(Interval_4), classlabel4 , QColor(r4, g4, b4), 1, Thickness_4 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 5 :                                                                                                          
                        classlabel5 = str(Interval_4)+" - "+str(Interval_5)                                                                                          
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_4), int(Interval_5), classlabel5 , QColor(r5, g5, b5), 1, Thickness_5 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 6 :                                                                                                          
                        classlabel6 = str(Interval_5)+" - "+str(Interval_6)                                                                                          
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_5), int(Interval_6), classlabel6 , QColor(r6, g6, b6), 1, Thickness_6 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 7 :                                                                                                          
                        classlabel7 = str(Interval_6)+" - "+str(Interval_7)                                                                                          
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_6), int(Interval_7), classlabel7 , QColor(r7, g7, b7), 1, Thickness_7 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 8 :                                                                                                          
                        classlabel8 = str(Interval_7)+" - "+str(Interval_8)                                                                                          
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_7), int(Interval_8), classlabel8 , QColor(r8, g8, b8), 1, Thickness_8 * float(1)  ))                      
                        
                    #elif i == (GradSymNoOfClasses - 1):
                    #        classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymMax)
                    #        myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i/1.25 ))
                    #else:
                    #        classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))
                    #        myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i/1.25 ))
                    myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                    vlayer.setRendererV2( myRenderer )
                    message = "Defined interval representation created and ready to be added into map canvas !"
                    QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                    QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                     

    def form7(self):
        
        global comboBoxSelectField_combotext
        
        dlg = Form7Dialog() 
        dlg.show()

        QtCore.QObject.connect(dlg.ui.BrowseShapeInputNodeSymbology,QtCore.SIGNAL("clicked()"), self.InputShpNodeSymbology)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputNodeSymbology,QtCore.SIGNAL("clicked()"), dlg.SetTextBrowseInputShapeNodeSymbology)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputNodeSymbology,QtCore.SIGNAL("clicked()"), self.PopulateFieldNames)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputNodeSymbology,QtCore.SIGNAL("clicked()"), dlg.SetTextPopulateFieldNamesList)     
        
        #get stats for flow node symbology                 
        QtCore.QObject.connect(dlg.ui.CalStatField,QtCore.SIGNAL("clicked()"), self.CalStatNodeSymbology)
        QtCore.QObject.connect(dlg.ui.CalStatField,QtCore.SIGNAL("clicked()"), dlg.MeanSymbology)
        QtCore.QObject.connect(dlg.ui.CalStatField,QtCore.SIGNAL("clicked()"), dlg.MaxSymbology)
        QtCore.QObject.connect(dlg.ui.CalStatField,QtCore.SIGNAL("clicked()"), dlg.MinSymbology)
        QtCore.QObject.connect(dlg.ui.CalStatField,QtCore.SIGNAL("clicked()"), dlg.StdDevSymbology)
        QtCore.QObject.connect(dlg.ui.CalStatField,QtCore.SIGNAL("clicked()"), dlg.NoOfFeaturesSymbology)
        
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_1,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_1)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_1,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_1)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_2,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_2)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_2,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_2)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_3,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_3)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_3,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_3)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_4,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_4)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_4,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_4)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_5,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_5)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_5,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_5)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_6,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_6)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_6,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_6)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_7,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_7)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_7,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_7)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_8,QtCore.SIGNAL("clicked()"), self.SelectColorSymbology_8)
        QtCore.QObject.connect(dlg.ui.PushButtonColorSelect_8,QtCore.SIGNAL("clicked()"), dlg.PushButtonColorSelectSymbology_8)
        
        result = dlg.exec_() 
        
        if result == 1: 

            #add to map canvas based on selected symbology options 

##----------Single Symbology/START----------------------------------------------
            if dlg.ui.comboBoxSelectSymbology.currentText() == "Single Symbol" and dlg.ui.DifNodeSymbologycheckBox.isChecked() == False:
                self.iface.addVectorLayer(str(InputShpNodeSymbologyName), str(InputShpNodeSymbologyName), "ogr")            
                message = "Single symbol representation created and added into map canvas !"
                QMessageBox.information(self.iface.mainWindow(),"info" ,message, "Close")
            elif dlg.ui.comboBoxSelectSymbology.currentText() == "Single Symbol" and dlg.ui.DifNodeSymbologycheckBox.isChecked() == True:            
                def validatedDefaultSymbol(geometryType):
                    symbol = QgsSymbolV2.defaultSymbol(geometryType)
                    if symbol is None:
                        if geometryType == QGis.Point:
                            symbol = QgsMarkerSymbolV2()
                        elif geometryType == QGis.Line:
                            symbol =  QgsLineSymbolV2()
                        elif geometryType == QGis.Polygon:
                            symbol = QgsFillSymbolV2()
                    return symbol
                
                #Create Symbology
                def makeSymbologyForRange(layer, min ,max, label ,colour, alpha, size):
                    symbol = validatedDefaultSymbol(layer.geometryType())
                    symbol.setColor(colour)
                    symbol.setAlpha(alpha)
                    symbol.setSize(size)
                    range = QgsRendererRangeV2(min, max, symbol, label)
                    return range

                vlayer = QgsVectorLayer(str(InputShpNodeSymbologyName), str(InputShpNodeSymbologyName), 'ogr')
                myTargetField = 'indicator'
                myRangeList = []
                classlabel1 = "nodes gaining flows (incoming>outgoing)"
                classlabel2 = "nodes losing flows (incoming<outgoing)"
                classlabel3 = "neutral nodes (incoming=outgoing)"
                myRangeList.append(makeSymbologyForRange( vlayer, 0.9, 2, classlabel1 , QColor(0, 192, 0), 1, 2 ))
                myRangeList.append(makeSymbologyForRange( vlayer, -2, -0.9, classlabel2 , QColor(255, 0, 0), 1, 2 ))
                myRangeList.append(makeSymbologyForRange( vlayer, 0, 0, classlabel3 , QColor(128, 128, 128), 1, 2 ))                
                
                myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                vlayer.setRendererV2( myRenderer )
                message = "Flow nodes are differentiated by flow gain or flow loss and added into map canvas !"
                QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
##----------Single Symbology/END------------------------------------------------
            
            else:
                global GradSymNoOfFeaturesNodeSymbology
                global GradSymNoOfFeaturesZeroNodeSymbology
                global GradSymMinNodeSymbology
                global GradSymMaxNodeSymbology
                global GradSymSumMagnitudeNodeSymbology
                global GradSymMeanNodeSymbology
                global GradSymMeanNotZeroNodeSymbology     
                global GradSymStdDevNodeSymbology
                global GradSymStdDevNotZeroNodeSymbology                   
                global GradSymListNodeSymbology
                
                shp = ogr.Open(str(InputShpNodeSymbologyName),1)
                layer = shp.GetLayer(0)
                GradSymNoOfFeaturesNodeSymbology = str(layer.GetFeatureCount())
                
                feature = layer.GetNextFeature()
                counterNotZero = 0
                GradSymSumMagnitudeNodeSymbology = 0
                GradSymListNodeSymbology= []    
                
                while feature:
                    #magnitude = feature.GetField('magnitude')
                    magnitude = feature.GetField(str(comboBoxSelectField_combotext))
                    if magnitude > 0:
                        counterNotZero = counterNotZero + 1
                        GradSymListNodeSymbology.append(int(magnitude))
                        GradSymMinNodeSymbology = min(GradSymListNodeSymbology)
                        GradSymMaxNodeSymbology = max(GradSymListNodeSymbology)
                    GradSymSumMagnitudeNodeSymbology = GradSymSumMagnitudeNodeSymbology + magnitude
                    feature.Destroy()
                    feature = layer.GetNextFeature()
                GradSymMeanNodeSymbology = str(round(float(GradSymSumMagnitudeNodeSymbology / int(GradSymNoOfFeaturesNodeSymbology)),3))
                GradSymMeanNotZeroNodeSymbology = str(round(float(GradSymSumMagnitudeNodeSymbology / int(counterNotZero)),3))
                GradSymSumMagnitudeNodeSymbology = str(GradSymSumMagnitudeNodeSymbology)
                GradSymNoOfFeaturesZeroNodeSymbology = str(int(GradSymNoOfFeaturesNodeSymbology)-int(counterNotZero))
                GradSymMinNodeSymbology = str(GradSymMinNodeSymbology)
                GradSymMaxNodeSymbology = str(GradSymMaxNodeSymbology)
                layer.ResetReading()

                GradSymVarNodeSymbology = 0
                GradSymVarNotZeroNodeSymbology = 0

                feature = layer.GetNextFeature()
                while feature:
                    #magnitude = feature.GetField('magnitude')
                    magnitude = feature.GetField(str(comboBoxSelectField_combotext))
                    #feature = layer.GetNextFeature()
                    GradSymVarNodeSymbology = GradSymVarNodeSymbology + ((magnitude - float(GradSymMeanNodeSymbology))**2)
                    if magnitude > 0:
                        GradSymVarNotZeroNodeSymbology = GradSymVarNotZeroNodeSymbology + ((magnitude - float(GradSymMeanNotZeroNodeSymbology))**2)
                    feature.Destroy()
                    feature = layer.GetNextFeature()
                GradSymStdDevNodeSymbology = str(round(((GradSymVarNodeSymbology / int(GradSymNoOfFeaturesNodeSymbology))**0.5), 3))
                GradSymStdDevNotZeroNodeSymbology = str(round(((GradSymVarNotZeroNodeSymbology / int(counterNotZero))**0.5), 3))
                layer.ResetReading()
                
                shp.Destroy()

                def validatedDefaultSymbol(geometryType):
                    symbol = QgsSymbolV2.defaultSymbol(geometryType)
                    if symbol is None:
                        if geometryType == QGis.Point:
                            symbol = QgsMarkerSymbolV2()
                        elif geometryType == QGis.Line:
                            symbol =  QgsLineSymbolV2()
                        elif geometryType == QGis.Polygon:
                            symbol = QgsFillSymbolV2()
                    return symbol
                
                #registry = QgsSymbolLayerV2Registry.instance()
                #markerMeta = registry.symbolLayerMetadata("SimpleMarker")
                #markerMeta2 = registry.symbolLayerMetadata("SimpleMarker")
                
                #Create Symbology
                def makeSymbologyForRange(layer, min ,max, label ,colour, alpha, size):
                    symbol = validatedDefaultSymbol(layer.geometryType())
                        
                    if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.DifNodeSymbologycheckBox.isChecked() == True:                        
                    #    markerLayer = markerMeta.createSymbolLayer({'name': 'circle', 'color': '128,128,128', 'color_border': '0,0,0', 'offset': '0,0', 'size': '2', 'outline_width': '0.1', 'angle': '0'})                        
                    #    markerLayer2 = markerMeta.createSymbolLayer({'name': 'circle', 'color': '255,0,0', 'color_border': '0,0,0', 'offset': '0,0', 'size': '1', 'outline_width': '0.1', 'angle': '0'})
                    #    #subSymbol = markerLayer.subSymbol()
                    #    
                    #    ##Replace the default layer with our own SimpleMarker
                    #    #subSymbol.deleteSymbolLayer(0)
                    #    #triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer({'name': 'filled_arrowhead', 'color': '255,0,255', 'color_border': '255,255,255', 'offset': '0,0', 'size': '3', 'outline_width': '0.5', 'angle': '0'})
                    #    #subSymbol.appendSymbolLayer(triangle)
                    #    
                    #    #Replace the default layer with our two custom layers
                    #    symbol.deleteSymbolLayer(0)
                    #    symbol.appendSymbolLayer(markerLayer1)
                    #    symbol.appendSymbolLayer(markerLayer2)
                    #
                    #    symbol.setColor(colour)
                    #    symbol.setAlpha(alpha)
                    #    symbol.setSize(size)
                    #    
                    #    range = QgsRendererRangeV2(min, max, symbol2, label)
                        pass
                        
                    if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol":
                        symbol.setColor(colour)
                        symbol.setAlpha(alpha)
                        symbol.setSize(size)
                        range = QgsRendererRangeV2(min, max, symbol, label)
                        return range                    
                    
                vlayer = QgsVectorLayer(str(InputShpNodeSymbologyName), str(InputShpNodeSymbologyName), 'ogr')
                
                #myTargetField = 'magnitude'
                myTargetField = str(comboBoxSelectField_combotext)
                
                #Define base line symbol width and multiplier factor for graduated classes
                global basesymbolwidth
                global multipliersymbolwidth

                if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol":
                    global basesymbolwidth
                    global multipliersymbolwidth
                    basesymbolwidth = 3.0                        
                    multipliersymbolwidth = 2.0
                
                #Equal Interval
                if dlg.ui.comboBoxSelectSymbology.currentText() == "Equal Interval":
                    GradSymNoOfClasses = dlg.ui.spinBoxClasses.value() 
                    GradSymInterval = round(((int(GradSymMaxNodeSymbology) - int(GradSymMinNodeSymbology)) / float(GradSymNoOfClasses)),0)
                    myRangeList = []
                    for i in range(GradSymNoOfClasses):
                        if i == 0:
                            classlabel = str(GradSymMinNodeSymbology)+" - "+str(int(GradSymMinNodeSymbology)+GradSymInterval)
                            #myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMinNodeSymbology), int(GradSymMinNodeSymbology)+GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                            myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMinNodeSymbology), int(GradSymMinNodeSymbology)+GradSymInterval, classlabel , QColor(192,192,192), 1, basesymbolwidth ))                            
                        elif i == (GradSymNoOfClasses - 1):
                            classlabel = str(int(GradSymMinNodeSymbology)+(GradSymInterval*i)+0.001)+" - "+str(GradSymMaxNodeSymbology)
                            #myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMaxNodeSymbology), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i*multipliersymbolwidth ))
                            myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMaxNodeSymbology), classlabel , QColor(192,192,192), 1, (i+1)*multipliersymbolwidth ))
                        else:
                            classlabel = str(int(GradSymMinNodeSymbology)+(GradSymInterval*i)+0.001)+" - "+str(int(GradSymMinNodeSymbology)+GradSymInterval*(i+1))
                            #myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMinNodeSymbology)+(GradSymInterval*i)+0.001, int(GradSymMinNodeSymbology)+GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i*multipliersymbolwidth ))
                            myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMinNodeSymbology)+(GradSymInterval*i)+0.001, int(GradSymMinNodeSymbology)+GradSymInterval*(i+1), classlabel , QColor(192,192,192), 1, (i+1)*multipliersymbolwidth ))
                    myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                    vlayer.setRendererV2( myRenderer )
                    message = "Equal interval representation created and ready to be added into map canvas !"
                    QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                    QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                
                #Defined Interval
                elif dlg.ui.comboBoxSelectSymbology.currentText() == "Defined Interval":
                    GradSymInterval = int(dlg.ui.lineEditInterval.text())
                    GradSymNoOfClasses = int((int(GradSymMaxNodeSymbology) - int(GradSymMinNodeSymbology)) / GradSymInterval) + 1
                    myRangeList = []
                    for i in range(GradSymNoOfClasses):
                        if i == 0:
                            classlabel = str(GradSymMinNodeSymbology)+" - "+str(GradSymInterval)
                            #myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMinNodeSymbology), GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                            myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMinNodeSymbology), GradSymInterval, classlabel , QColor(192,192,192), 1, basesymbolwidth ))
                        elif i == (GradSymNoOfClasses - 1):
                            classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymMaxNodeSymbology)
                            #myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMaxNodeSymbology), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                            myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMaxNodeSymbology), classlabel , QColor(192,192,192), 1, (i+1)*multipliersymbolwidth ))
                        else:
                            classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))
                            #myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                            myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(192,192,192), 1, (i+1)*multipliersymbolwidth ))
                    myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                    vlayer.setRendererV2( myRenderer )
                    message = "Defined interval representation created and ready to be added into map canvas !"
                    QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                    QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                
                #Standard Deviation
                elif dlg.ui.comboBoxSelectSymbology.currentText() == "Standard Deviation":
                    if dlg.ui.comboBoxSelectStdDev.currentText() == "1/4 Std. Dev.":
                        GradSymInterval = float(GradSymStdDevNotZeroNodeSymbology) / 4
                        GradSymNoOfClasses = int((int(GradSymMaxNodeSymbology) - int(GradSymMinNodeSymbology)) / GradSymInterval) + 1
                        classlabelStdDev = 0.25
                    elif dlg.ui.comboBoxSelectStdDev.currentText() == "1/2 Std. Dev.":
                        GradSymInterval = float(GradSymStdDevNotZeroNodeSymbology) / 2
                        GradSymNoOfClasses = int((int(GradSymMaxNodeSymbology) - int(GradSymMinNodeSymbology)) / GradSymInterval) + 1
                        classlabelStdDev = 0.5
                    elif dlg.ui.comboBoxSelectStdDev.currentText() == "1 Std. Dev.":
                        GradSymInterval = float(GradSymStdDevNotZeroNodeSymbology) 
                        GradSymNoOfClasses = int((int(GradSymMaxNodeSymbology) - int(GradSymMinNodeSymbology)) / GradSymInterval) + 1
                        classlabelStdDev = 1.0
                    elif dlg.ui.comboBoxSelectStdDev.currentText() == "2 Std. Dev.":
                        GradSymInterval = float(GradSymStdDevNotZeroNodeSymbology) * 2
                        GradSymNoOfClasses = int((int(GradSymMaxNodeSymbology) - int(GradSymMinNodeSymbology)) / GradSymInterval) + 1
                        classlabelStdDev = 2.0
                    myRangeList = []
                    for i in range(GradSymNoOfClasses):                            
                        if i == 0:                            
                            classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str(GradSymMinNodeSymbology)+" - "+str(GradSymInterval)                            
                            #myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMinNodeSymbology), GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))                            
                            myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMinNodeSymbology), GradSymInterval, classlabel , QColor(192,192,192), 1, basesymbolwidth ))                            
                        elif i == (GradSymNoOfClasses - 1):                            
                            classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str((GradSymInterval*i)+0.001)+" - "+str(GradSymMaxNodeSymbology)                            
                            #myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMaxNodeSymbology), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))                            
                            myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMaxNodeSymbology), classlabel , QColor(192,192,192), 1, (i+1)*multipliersymbolwidth ))                            
                        else:                            
                            classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))                            
                            #myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))                            
                            myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(192,192,192), 1, (i+1)*multipliersymbolwidth ))                            
                    myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )                            
                    vlayer.setRendererV2( myRenderer )                            
                    message = "Standard deviation interval representation created and ready to be added into map canvas !"
                    QMessageBox.information(self.iface.mainWindow(),"info" ,message)                            
                    QgsMapLayerRegistry.instance().addMapLayer( vlayer )                             
                
                #Equal Size Classes
                elif dlg.ui.comboBoxSelectSymbology.currentText() == "Equal Size Classes":
                    GradSymNoOfClasses = dlg.ui.spinBoxClasses.value() 
                    GradSymNoOfFeaturesZeroNodeSymbology = int(GradSymNoOfFeaturesZeroNodeSymbology)
                    GradSymNoOfFeaturesInInterval = int(  round(((int(GradSymNoOfFeaturesNodeSymbology)-int(GradSymNoOfFeaturesZeroNodeSymbology))/float(GradSymNoOfClasses)),0) ) 
                    myRangeList = []
                    GradSymListNodeSymbology.sort()
                    for i in range(GradSymNoOfClasses):
                        if i == 0:
                            classlabel = str(GradSymMinNodeSymbology)+" - "+str(GradSymListNodeSymbology[(GradSymNoOfFeaturesInInterval*(i+1))-1])
                            #myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMinNodeSymbology), GradSymListNodeSymbology[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                            myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMinNodeSymbology), GradSymListNodeSymbology[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(192,192,192), 1, basesymbolwidth ))
                        elif i == (GradSymNoOfClasses - 1):
                            classlabel = str(GradSymListNodeSymbology[GradSymNoOfFeaturesInInterval*i])+" - "+str(GradSymMaxNodeSymbology)
                            #myRangeList.append(makeSymbologyForRange( vlayer, GradSymListNodeSymbology[GradSymNoOfFeaturesInInterval*i], int(GradSymMaxNodeSymbology), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                            myRangeList.append(makeSymbologyForRange( vlayer, GradSymListNodeSymbology[GradSymNoOfFeaturesInInterval*i], int(GradSymMaxNodeSymbology), classlabel , QColor(192,192,192), 1, (i+1)*multipliersymbolwidth ))
                        else:
                            classlabel = str(GradSymListNodeSymbology[GradSymNoOfFeaturesInInterval*i])+" - "+str(GradSymListNodeSymbology[(GradSymNoOfFeaturesInInterval*(i+1))-1])
                            #myRangeList.append(makeSymbologyForRange( vlayer, GradSymListNodeSymbology[GradSymNoOfFeaturesInInterval*i], GradSymListNodeSymbology[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                            myRangeList.append(makeSymbologyForRange( vlayer, GradSymListNodeSymbology[GradSymNoOfFeaturesInInterval*i], GradSymListNodeSymbology[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(192,192,192), 1, (i+1)*multipliersymbolwidth ))
                    myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                    vlayer.setRendererV2( myRenderer )
                    message = "Equal size classes representation created and ready to be added into map canvas !"
                    QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                    QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                #Manual Interval
                elif dlg.ui.comboBoxSelectSymbology.currentText() == "Manual Interval":
                    
                    if dlg.ui.spinBoxClasses.value() >= 1 :
                        Interval_1 =  int(dlg.ui.lineEditManualInterval_1.text())
                    if dlg.ui.spinBoxClasses.value() >= 2 :
                        Interval_2 =  int(dlg.ui.lineEditManualInterval_2.text())
                    if dlg.ui.spinBoxClasses.value() >= 3 :
                        Interval_3 =  int(dlg.ui.lineEditManualInterval_3.text())
                    if dlg.ui.spinBoxClasses.value() >= 4 :
                        Interval_4 =  int(dlg.ui.lineEditManualInterval_4.text())
                    if dlg.ui.spinBoxClasses.value() >= 5 :
                        Interval_5 =  int(dlg.ui.lineEditManualInterval_5.text())
                    if dlg.ui.spinBoxClasses.value() >= 6 :
                        Interval_6 =  int(dlg.ui.lineEditManualInterval_6.text())
                    if dlg.ui.spinBoxClasses.value() >= 7 :
                        Interval_7 =  int(dlg.ui.lineEditManualInterval_7.text())
                    if dlg.ui.spinBoxClasses.value() >= 8 :
                        Interval_8 =  int(dlg.ui.lineEditManualInterval_8.text())
                    Size_1 = dlg.ui.doubleSpinBoxSize_1.text()
                    Size_1 = float(Size_1.replace(",",".")) 
                    Size_2 = dlg.ui.doubleSpinBoxSize_2.text()
                    Size_2 = float(Size_2.replace(",",".")) 
                    Size_3 = dlg.ui.doubleSpinBoxSize_3.text()
                    Size_3 = float(Size_3.replace(",",".")) 
                    Size_4 = dlg.ui.doubleSpinBoxSize_4.text()
                    Size_4 = float(Size_4.replace(",",".")) 
                    Size_5 = dlg.ui.doubleSpinBoxSize_5.text()
                    Size_5 = float(Size_5.replace(",",".")) 
                    Size_6 = dlg.ui.doubleSpinBoxSize_6.text()
                    Size_6 = float(Size_6.replace(",",".")) 
                    Size_7 = dlg.ui.doubleSpinBoxSize_7.text()
                    Size_7 = float(Size_7.replace(",",".")) 
                    Size_8 = dlg.ui.doubleSpinBoxSize_8.text()
                    Size_8 = float(Size_8.replace(",",".")) 
                    
                    myRangeList = []
                    
                    if dlg.ui.spinBoxClasses.value() >= 1 :
                        classlabel1 = str(GradSymMinNodeSymbology)+" - "+str(Interval_1)
                        myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMinNodeSymbology), int(Interval_1), classlabel1 , QColor(r1, g1, b1), 1, Size_1 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 2 :                                                                                                  
                        classlabel2 = str(Interval_1)+" - "+str(Interval_2)                                                                                  
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_1), int(Interval_2), classlabel2 , QColor(r2, g2, b2), 1, Size_2 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 3 :                                                                                                  
                        classlabel3 = str(Interval_2)+" - "+str(Interval_3)                                                                                  
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_2), int(Interval_3), classlabel3 , QColor(r3, g3, b3), 1, Size_3 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 4 :                                                                                                  
                        classlabel4 = str(Interval_3)+" - "+str(Interval_4)                                                                                  
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_3), int(Interval_4), classlabel4 , QColor(r4, g4, b4), 1, Size_4 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 5 :                                                                                                  
                        classlabel5 = str(Interval_4)+" - "+str(Interval_5)                                                                                  
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_4), int(Interval_5), classlabel5 , QColor(r5, g5, b5), 1, Size_5 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 6 :                                                                                                  
                        classlabel6 = str(Interval_5)+" - "+str(Interval_6)                                                                                  
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_5), int(Interval_6), classlabel6 , QColor(r6, g6, b6), 1, Size_6 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 7 :                                                                                                  
                        classlabel7 = str(Interval_6)+" - "+str(Interval_7)                                                                                  
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_6), int(Interval_7), classlabel7 , QColor(r7, g7, b7), 1, Size_7 * float(1) ))
                    if dlg.ui.spinBoxClasses.value() >= 8 :                                                                                                  
                        classlabel8 = str(Interval_7)+" - "+str(Interval_8)                                                                                  
                        myRangeList.append(makeSymbologyForRange( vlayer, int(Interval_7), int(Interval_8), classlabel8 , QColor(r8, g8, b8), 1, Size_8 * float(1)  ))                      
                        
                    #elif i == (GradSymNoOfClasses - 1):
                    #        classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymMaxNodeSymbology)
                    #        myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMaxNodeSymbology), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i/1.25 ))
                    #else:
                    #        classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))
                    #        myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i/1.25 ))
                    myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                    vlayer.setRendererV2( myRenderer )
                    message = "Defined interval representation created and ready to be added into map canvas !"
                    QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                    QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 

#---------------Differentiate flow nodes and add to map canvas/START----------------------------------------------                    

                if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.DifNodeSymbologycheckBox.isChecked() == True:            
                    #Create Symbology
                    def makeSymbologyForRange(layer, min ,max, label ,colour, alpha, size):
                        symbol = validatedDefaultSymbol(layer.geometryType())
                        symbol.setColor(colour)
                        symbol.setAlpha(alpha)
                        symbol.setSize(size)
                        range = QgsRendererRangeV2(min, max, symbol, label)
                        return range
    
                    vlayer = QgsVectorLayer(str(InputShpNodeSymbologyName), str(InputShpNodeSymbologyName), 'ogr')
                    myTargetField = 'indicator'
                    myRangeList = []
                    classlabel1 = "nodes gaining flows (incoming>outgoing)"
                    classlabel2 = "nodes losing flows (incoming<outgoing)"
                    classlabel3 = "neutral nodes (incoming=outgoing)"
                    myRangeList.append(makeSymbologyForRange( vlayer, 0.9, 2, classlabel1 , QColor(0, 192, 0), 1, 2 ))
                    myRangeList.append(makeSymbologyForRange( vlayer, -2, -0.9, classlabel2 , QColor(255, 0, 0), 1, 2 ))
                    myRangeList.append(makeSymbologyForRange( vlayer, 0, 0, classlabel3 , QColor(128, 128, 128), 1, 2 ))                
                    
                    myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                    vlayer.setRendererV2( myRenderer )
                    message = "Flow nodes are differentiated by flow gain or flow loss and added into map canvas !"
                    QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                    QgsMapLayerRegistry.instance().addMapLayer( vlayer )   
#---------------Differentiate flow nodes and add to map canvas/END----------------------------------------------                                        
                
                    self.iface.legendInterface().addGroup(str(InputShpNodeSymbologyName),0,9000)
                    self.iface.legendInterface().moveLayer (qgis.utils.iface.legendInterface().layers()[1],0)
                    self.iface.legendInterface().moveLayer (qgis.utils.iface.legendInterface().layers()[0],0)
                    self.iface.legendInterface().moveLayer (qgis.utils.iface.legendInterface().layers()[1],0)

            
    def form5(self):
        dlg = Form5Dialog()
        #dlg.show()
                
        #browse for file penceresini acmak icin SaveShp e signal yollar
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputExport,QtCore.SIGNAL("clicked()"), self.InputShpNameExport)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputExport,QtCore.SIGNAL("clicked()"), dlg.BrowseShapeLineEditExport)
        QtCore.QObject.connect(dlg.ui.BrowseFileOutputExport,QtCore.SIGNAL("clicked()"), self.OutputFileNameExport)
        QtCore.QObject.connect(dlg.ui.BrowseFileOutputExport,QtCore.SIGNAL("clicked()"), dlg.BrowseFileLineEditExport)
		
        result = dlg.exec_()
        if result == 1:

            #SaveDirectory = os.path.realpath(BrowseFileLineEditNameExport)
            SaveDirectory = BrowseFileLineEditNameExport
            
            if dlg.ui.FileType_comboBox.currentText() == "Google Earth KML":        
                
                command1_shp2kml = 'ogr2ogr -f "KML" '
                command = str(command1_shp2kml)+" "+str(BrowseFileLineEditNameExport)+" "+str(BrowseShapeLineEditNameExport)
                os.system(command)
                message = str(BrowseFileLineEditNameExport)+" "+'created succesfully !'
                QMessageBox.information(self.iface.mainWindow(),"info" ,message)

            elif dlg.ui.FileType_comboBox.currentText() == "MapInfo TAB":        
                command1_shp2tab = 'ogr2ogr -f "MapInfo File" '
                command = str(command1_shp2tab)+" "+str(BrowseFileLineEditNameExport)+" "+str(BrowseShapeLineEditNameExport)
                os.system(command)
                message = str(BrowseFileLineEditNameExport)+" "+'created succesfully !'
                QMessageBox.information(self.iface.mainWindow(),"info" ,message)

    
    
    def PopulateNodeNames(self):
        
        global NodeNamesListcomboBox

        extension = os.path.splitext(str(InputShpFilterNodeNamesName))[1]
        if extension == ".shp" and ".shp" in InputShpFilterNodeNamesName and len(InputShpFilterNodeNamesName) > 4:
        #if ".shp" in InputShpFilterNodeNamesName and len(InputShpFilterNodeNamesName) > 4: 
        
            shp = ogr.Open(str(InputShpFilterNodeNamesName),1)
            layer = shp.GetLayer(0)
            nodenameList = [] 
            feature = layer.GetNextFeature()
            while feature:
                if nodeFilteringType_combotext == "both incoming to & outgoing from":
                    nodename_from = feature.GetField('name_x1y1')
                    nodename_to = feature.GetField('name_x2y2')
                    if nodename_from not in nodenameList:
                        nodenameList.append(nodename_from)
                    if nodename_to not in nodenameList:
                        nodenameList.append(nodename_to)
                elif nodeFilteringType_combotext == "only incoming to":
                    nodename = feature.GetField('name_x2y2')                
                    if nodename not in nodenameList:
                        nodenameList.append(nodename)
                elif nodeFilteringType_combotext == "only outgoing from":
                    nodename = feature.GetField('name_x1y1')                
                    if nodename not in nodenameList:
                        nodenameList.append(nodename)
                feature.Destroy()
                feature = layer.GetNextFeature()
                
            layer.ResetReading()
            #shp.destroy()
            
            nodenameList.sort()
            NodeNamesListcomboBox = nodenameList
            
            #QMessageBox.information(self.iface.mainWindow(),"info" ,str(NodeNamesListcomboBox))
            #QMessageBox.information(self.iface.mainWindow(),"info" ,str(len(nodenameList)))
            #QMessageBox.information(self.iface.mainWindow(),"info" ,str(nodeFilteringType_combotext))

    def PopulateFieldNames(self):
    
        global FieldNamesListcomboBox
        
        extension = os.path.splitext(str(InputShpNodeSymbologyName))[1]
        if extension == ".shp" and ".shp" in InputShpNodeSymbologyName and len(InputShpNodeSymbologyName) > 4:        

            shp = ogr.Open(str(InputShpNodeSymbologyName),1)      
            layer = shp.GetLayer(0)
            fieldnameList = []
            layerDefinition = layer.GetLayerDefn()
            
            for i in range(layerDefinition.GetFieldCount()):
                #print layerDefinition.GetFieldDefn(i).GetName()
                ListItemName = layerDefinition.GetFieldDefn(i).GetName()
                ListItemType = layerDefinition.GetFieldDefn(i).GetType()
                #QMessageBox.information(self.iface.mainWindow(),"info" ,str(ListItemType))
                #Type 4 stands for string type fields
                #if int(ListItemType) != 4 and str(ListItemName) <> "indicator" and str(ListItemName) <> "Indicator" and str(ListItemName) <> "INDICATOR" :
                if int(ListItemType) != 4:             
                    fieldnameList.append(ListItemName)
            
            layer.ResetReading()
            #shp.destroy()
            
            FieldNamesListcomboBox = fieldnameList
            
    def form6(self):
        
        dlg = Form6Dialog() 
        dlg.show()
        #result = dlg2.exec_() 

        global nodeFilteringType_combotext
        nodeFilteringType_combotext = str(dlg.ui.nodeFilteringType_comboBox.currentText()) 
        global InputShpFilterNodeNamesName
        InputShpFilterNodeNamesName = "" 
        
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputFilterNodeNames,QtCore.SIGNAL("clicked()"), self.InputShpFilterNodeNames)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputFilterNodeNames,QtCore.SIGNAL("clicked()"), dlg.SetTextBrowseInputShapeFilterNodeNames)
        QtCore.QObject.connect(dlg.ui.BrowseShapeOutputFilterNodeNames,QtCore.SIGNAL("clicked()"), self.OutputShpFilterNodeNames)
        QtCore.QObject.connect(dlg.ui.BrowseShapeOutputFilterNodeNames,QtCore.SIGNAL("clicked()"), dlg.SetTextBrowseOutputShapeFilterNodeNames)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputFilterNodeNames,QtCore.SIGNAL("clicked()"), self.PopulateNodeNames)
        QtCore.QObject.connect(dlg.ui.BrowseShapeInputFilterNodeNames,QtCore.SIGNAL("clicked()"), dlg.SetTextPopulateNodeNamesList)     
        QtCore.QObject.connect(dlg.ui.nodeFilteringType_comboBox,QtCore.SIGNAL("currentIndexChanged(int)"), self.PopulateNodeNames)
        QtCore.QObject.connect(dlg.ui.nodeFilteringType_comboBox,QtCore.SIGNAL("currentIndexChanged(int)"), dlg.SetTextPopulateNodeNamesList)
        
        #in order to populate combobox with push button rather than browse...
        #QtCore.QObject.connect(dlg.ui.PopulateNodeNamesButton,QtCore.SIGNAL("clicked()"), self.PopulateNodeNames)     
        #QtCore.QObject.connect(dlg.ui.PopulateNodeNamesButton,QtCore.SIGNAL("clicked()"), dlg.SetTextPopulateNodeNamesList)     
        
        #dlg.exec_()         
        result = dlg.exec_() 
        
        if result == 1:
            
            text = dlg.ui.NodeNames_comboBox.currentText()
            if nodeFilteringType_combotext == "both incoming to & outgoing from":
                command_pt1 = 'ogr2ogr -f "ESRI Shapefile" -where "name_x1y1 = '
                command_pt2 = ' or name_x2y2 = '
                command_pt3 = '"'
                command_pt4 = "'"
                command = str(command_pt1)+str(command_pt4)+str(text)+str(command_pt4)+str(command_pt2)+str(command_pt4)+str(text)+str(command_pt4)+str(command_pt3)+" "+str(OutputShpFilterNodeNamesName)+" "+str(InputShpFilterNodeNamesName) 
            elif nodeFilteringType_combotext == "only incoming to":
                command1 = 'ogr2ogr -f "ESRI Shapefile" -where "name_x2y2 = ' 
                command2 = '"'
                command3 = "'"
                command = str(command1) + str(command3) + str(text)+ str(command3) + str(command2)+" "+ str(OutputShpFilterNodeNamesName)+" "+str(InputShpFilterNodeNamesName)
            elif nodeFilteringType_combotext == "only outgoing from":
                command1 = 'ogr2ogr -f "ESRI Shapefile" -where "name_x1y1 = '                
                command2 = '"'
                command3 = "'"
                command = str(command1) + str(command3) + str(text)+ str(command3) + str(command2)+" "+ str(OutputShpFilterNodeNamesName)+" "+str(InputShpFilterNodeNamesName)
            
            #QMessageBox.information(self.iface.mainWindow(),"info" ,str(command))
            os.system(str(command))
            
            if dlg.ui.Add2MapcheckBox.isChecked() == False:
                message = "Flows "+str(nodeFilteringType_combotext)+" "+str(text)+" filtered and "+str(OutputShpFilterNodeNamesName)+" created successfully !"
                QMessageBox.information(self.iface.mainWindow(),"info" ,message)
            else:    
                
                if dlg.ui.comboBoxSelectSymbology.currentText() == "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False: 
                    self.iface.addVectorLayer(str(OutputShpFilterNodeNamesName), str(OutputShpFilterNodeNamesName), "ogr")        

                    self.iface.addVectorLayer(str(OutputShpFilterNodeNamesName), str(OutputShpFilterNodeNamesName), "ogr")
                    SuccessMessage = "Flows "+str(nodeFilteringType_combotext)+" "+str(text)+" filtered and "+str(OutputShpFilterNodeNamesName)+" created successfully !"
                    QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")                
                
                elif dlg.ui.comboBoxSelectSymbology.currentText() == "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True:
                    layer = QgsVectorLayer(str(OutputShpFilterNodeNamesName), str(OutputShpFilterNodeNamesName), 'ogr')
                    #Use the currently selected layer
                    #layer = qgis.utils.iface.mapCanvas().currentLayer()
                    registry = QgsSymbolLayerV2Registry.instance()
                    lineMeta = registry.symbolLayerMetadata("SimpleLine")
                    markerMeta = registry.symbolLayerMetadata("MarkerLine")
                    
                    symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
                    
                    #Line layer
                    lineLayer = lineMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'offset': '0', 'penstyle': 'solid', 'use_custom_dash': '0', 'joinstyle': 'bevel', 'capstyle': 'square'})
                    
                    #Marker layer
                    #markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'interval': '3', 'rotate': '1', 'placement': 'interval', 'offset': '0'})
                    markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'rotate': '1', 'placement': 'centralpoint', 'offset': '0'})
                    subSymbol = markerLayer.subSymbol()
                    
                    #Replace the default layer with our own SimpleMarker
                    subSymbol.deleteSymbolLayer(0)
                    triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer({'name': 'filled_arrowhead', 'color': '255,0,0', 'color_border': '0,0,0', 'offset': '0,0', 'size': '3', 'angle': '0'})
                    subSymbol.appendSymbolLayer(triangle)
                    
                    #Replace the default layer with our two custom layers
                    symbol.deleteSymbolLayer(0)
                    symbol.appendSymbolLayer(lineLayer)
                    symbol.appendSymbolLayer(markerLayer)
                    
                    #Replace the renderer of the current layer
                    renderer = QgsSingleSymbolRendererV2(symbol)
                    layer.setRendererV2(renderer)    
                    #
                    QgsMapLayerRegistry.instance().addMapLayer( layer ) 
                    
                    SuccessMessage = "Flows "+str(nodeFilteringType_combotext)+" "+str(text)+" filtered and "+str(OutputShpFilterNodeNamesName)+" created successfully !"
                    #QMessageBox.information(self.iface.mainWindow(), "info", QString(SuccessMessage), QString('Close'))
                    QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")
                
                else:

                    global GradSymNoOfFeatures
                    global GradSymNoOfFeaturesZero
                    global GradSymMin
                    global GradSymMax
                    global GradSymSumMagnitude
                    global GradSymMean
                    global GradSymMeanNotZero        
                    global GradSymStdDev
                    global GradSymStdDevNotZero                    
                    global GradSymList 
                    
                    shp = ogr.Open(str(OutputShpFilterNodeNamesName),1)
                    layer = shp.GetLayer(0)
                    GradSymNoOfFeatures = str(layer.GetFeatureCount())
                    
                    feature = layer.GetNextFeature()
                    counterNotZero = 0
                    GradSymSumMagnitude = 0
                    GradSymList= []    
                    
                    while feature:
                        magnitude = feature.GetField('magnitude')
                        if magnitude > 0:
                            counterNotZero = counterNotZero + 1
                            GradSymList.append(int(magnitude))
                            GradSymMin = min(GradSymList)
                            GradSymMax = max(GradSymList)
                        GradSymSumMagnitude = GradSymSumMagnitude + magnitude
                        feature.Destroy()
                        feature = layer.GetNextFeature()
                    GradSymMean = str(round(float(GradSymSumMagnitude / int(GradSymNoOfFeatures)),3))
                    GradSymMeanNotZero = str(round(float(GradSymSumMagnitude / int(counterNotZero)),3))
                    GradSymSumMagnitude = str(GradSymSumMagnitude)
                    GradSymNoOfFeaturesZero = str(int(GradSymNoOfFeatures)-int(counterNotZero))
                    GradSymMin = str(GradSymMin)
                    GradSymMax = str(GradSymMax)
                    layer.ResetReading()

                    GradSymVar = 0
                    GradSymVarNotZero = 0

                    feature = layer.GetNextFeature()
                    while feature:
                        magnitude = feature.GetField('magnitude')
                        #feature = layer.GetNextFeature()
                        GradSymVar = GradSymVar + ((magnitude - float(GradSymMean))**2)
                        if magnitude > 0:
                            GradSymVarNotZero = GradSymVarNotZero + ((magnitude - float(GradSymMeanNotZero))**2)
                        feature.Destroy()
                        feature = layer.GetNextFeature()
                    GradSymStdDev = str(round(((GradSymVar / int(GradSymNoOfFeatures))**0.5), 3))
                    GradSymStdDevNotZero = str(round(((GradSymVarNotZero / int(counterNotZero))**0.5), 3))
                    layer.ResetReading()
                    
                    shp.Destroy()
                
                    registry = QgsSymbolLayerV2Registry.instance()
                    lineMeta = registry.symbolLayerMetadata("SimpleLine")
                    markerMeta = registry.symbolLayerMetadata("MarkerLine")
                
                    def validatedDefaultSymbol(geometryType):
                        symbol = QgsSymbolV2.defaultSymbol(geometryType)
                        if symbol is None:
                            if geometryType == QGis.Point:
                                symbol = QgsMarkerSymbolV2()
                            elif geometryType == QGis.Line:
                                symbol =  QgsLineSymbolV2()
                            elif geometryType == QGis.Polygon:
                                symbol = QgsFillSymbolV2()
                        return symbol
                    
                    #Create Symbology
                    def makeSymbologyForRange(layer, min ,max, label ,colour, alpha, width):
                        symbol = validatedDefaultSymbol(layer.geometryType())
                        
                        if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True: 
                            #Line layer
                            lineLayer = lineMeta.createSymbolLayer({'width': '0.5', 'color': '255,0,0', 'offset': '0', 'penstyle': 'solid', 'use_custom_dash': '0', 'joinstyle': 'bevel', 'capstyle': 'square'})
                            #Marker layer
                            markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'rotate': '1', 'placement': 'centralpoint', 'offset': '0'})
                            subSymbol = markerLayer.subSymbol()
                            #Replace the default layer with our own SimpleMarker
                            subSymbol.deleteSymbolLayer(0)
                            triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer({'name': 'filled_arrowhead', 'color': '255,0,0', 'color_border': '255,255,255', 'offset': '0,0', 'size': '3', 'outline_width': '0.5', 'angle': '0'})
                            subSymbol.appendSymbolLayer(triangle)
                            #Replace the default layer with our two custom layers
                            symbol.deleteSymbolLayer(0)
                            symbol.appendSymbolLayer(lineLayer)
                            symbol.appendSymbolLayer(markerLayer)
                            
                            symbol.setColor(colour)
                            symbol.setAlpha(alpha)
                            symbol.setWidth(width)
                            range = QgsRendererRangeV2(min, max, symbol, label)
                            
                        elif dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False:
                            symbol.setColor(colour)
                            symbol.setAlpha(alpha)
                            symbol.setWidth(width)
                            range = QgsRendererRangeV2(min, max, symbol, label)
                        
                        return range                    

                    vlayer = QgsVectorLayer(str(OutputShpFilterNodeNamesName), str(OutputShpFilterNodeNamesName), 'ogr')
                    myTargetField = 'magnitude'
                    
                    #Define base line symbol width and multiplier factor for graduated classes
                    global basesymbolwidth
                    global multipliersymbolwidth
                    if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True: 
                        global basesymbolwidth
                        global multipliersymbolwidth
                        basesymbolwidth = 3.0
                        multipliersymbolwidth = 2.0
                    elif dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False:
                        global basesymbolwidth
                        global multipliersymbolwidth
                        basesymbolwidth = 0.25                        
                        multipliersymbolwidth = 0.75                    

                    #Equal Interval
                    if dlg.ui.comboBoxSelectSymbology.currentText() == "Equal Interval":
                        GradSymNoOfClasses = int(dlg.ui.spinBoxClasses.value())
                        GradSymInterval = round(((int(GradSymMax) - int(GradSymMin)) / float(GradSymNoOfClasses)),0)
                        myRangeList = []
                        for i in range(GradSymNoOfClasses):
                            if i == 0:
                                classlabel = str(GradSymMin)+" - "+str(int(GradSymMin)+GradSymInterval)
                                #myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), int(GradSymMin)+GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                                if nodeFilteringType_combotext == "both incoming to & outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), int(GradSymMin)+GradSymInterval, classlabel , QColor(192, 192, 192), 1, basesymbolwidth ))
                                elif nodeFilteringType_combotext == "only incoming to":
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), int(GradSymMin)+GradSymInterval, classlabel , QColor(0, 255, 127), 1, basesymbolwidth ))
                                elif nodeFilteringType_combotext == "only outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), int(GradSymMin)+GradSymInterval, classlabel , QColor(255, 0, 0), 1, basesymbolwidth ))
                            elif i == (GradSymNoOfClasses - 1):
                                classlabel = str(int(GradSymMin)+(GradSymInterval*i)+0.001)+" - "+str(GradSymMax)
                                #myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i*multipliersymbolwidth ))
                                if nodeFilteringType_combotext == "both incoming to & outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only incoming to":
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(192*i/GradSymNoOfClasses), 127-(127*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(255-(192*i/GradSymNoOfClasses), 0, 0), 1, (i+1)*multipliersymbolwidth ))
                            else:
                                classlabel = str(int(GradSymMin)+(GradSymInterval*i)+0.001)+" - "+str(int(GradSymMin)+GradSymInterval*(i+1))
                                #myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin)+(GradSymInterval*i)+0.001, int(GradSymMin)+GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i*multipliersymbolwidth ))
                                if nodeFilteringType_combotext == "both incoming to & outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin)+(GradSymInterval*i)+0.001, int(GradSymMin)+GradSymInterval*(i+1), classlabel , QColor(192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only incoming to":
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin)+(GradSymInterval*i)+0.001, int(GradSymMin)+GradSymInterval*(i+1), classlabel , QColor(0, 255-(192*i/GradSymNoOfClasses), 127-(127*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin)+(GradSymInterval*i)+0.001, int(GradSymMin)+GradSymInterval*(i+1), classlabel , QColor(255-(192*i/GradSymNoOfClasses), 0, 0), 1, (i+1)*multipliersymbolwidth ))
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                        vlayer.setRendererV2( myRenderer )
                        message = "Flows "+str(nodeFilteringType_combotext)+" "+str(text)+" filtered and "+str(OutputShpFilterNodeNamesName)+" created successfully !"
                        QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 

                    #Defined Interval
                    elif dlg.ui.comboBoxSelectSymbology.currentText() == "Defined Interval":
                        GradSymInterval = int(dlg.ui.lineEditInterval.text())
                        GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                        myRangeList = []
                        for i in range(GradSymNoOfClasses):
                            if i == 0:
                                classlabel = str(GradSymMin)+" - "+str(GradSymInterval)
                                #myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                                if nodeFilteringType_combotext == "both incoming to & outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(192, 192, 192), 1, basesymbolwidth ))
                                elif nodeFilteringType_combotext == "only incoming to":                                              
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(0, 255, 127), 1, basesymbolwidth ))
                                elif nodeFilteringType_combotext == "only outgoing from":                                            
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(255, 0, 0), 1, basesymbolwidth ))
                            elif i == (GradSymNoOfClasses - 1):
                                classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymMax)
                                #myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i*multipliersymbolwidth ))
                                if nodeFilteringType_combotext == "both incoming to & outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only incoming to":                                                        
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(192*i/GradSymNoOfClasses), 127-(127*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only outgoing from":                                                      
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(255-(192*i/GradSymNoOfClasses), 0, 0), 1, (i+1)*multipliersymbolwidth ))
                            else:
                                classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))
                                #myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i*multipliersymbolwidth ))
                                if nodeFilteringType_combotext == "both incoming to & outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only incoming to":                                                              
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(192*i/GradSymNoOfClasses), 127-(127*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only outgoing from":                                                            
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(255-(192*i/GradSymNoOfClasses), 0, 0), 1, (i+1)*multipliersymbolwidth ))
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                        vlayer.setRendererV2( myRenderer )
                        message = "Flows "+str(nodeFilteringType_combotext)+" "+str(text)+" filtered and "+str(OutputShpFilterNodeNamesName)+" created successfully !"
                        QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                        
                    #Standard Deviation
                    elif dlg.ui.comboBoxSelectSymbology.currentText() == "Standard Deviation":
                        if dlg.ui.comboBoxSelectStdDev.currentText() == "1/4 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) / 4
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 0.25
                        elif dlg.ui.comboBoxSelectStdDev.currentText() == "1/2 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) / 2
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 0.5
                        elif dlg.ui.comboBoxSelectStdDev.currentText() == "1 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) 
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 1.0
                        elif dlg.ui.comboBoxSelectStdDev.currentText() == "2 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) * 2
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 2.0
                        myRangeList = []
                        for i in range(GradSymNoOfClasses):                            
                            if i == 0:                            
                                classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str(GradSymMin)+" - "+str(GradSymInterval)                            
                                #myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))                            
                                if nodeFilteringType_combotext == "both incoming to & outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(192, 192, 192), 1, basesymbolwidth ))
                                elif nodeFilteringType_combotext == "only incoming to":                                              
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(0, 255, 127), 1, basesymbolwidth ))
                                elif nodeFilteringType_combotext == "only outgoing from":                                            
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(255, 0, 0), 1, basesymbolwidth ))
                            elif i == (GradSymNoOfClasses - 1):                            
                                classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str((GradSymInterval*i)+0.001)+" - "+str(GradSymMax)                            
                                #myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i*multipliersymbolwidth ))                            
                                if nodeFilteringType_combotext == "both incoming to & outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only incoming to":                                                        
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(192*i/GradSymNoOfClasses), 127-(127*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only outgoing from":                                                      
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(255-(192*i/GradSymNoOfClasses), 0, 0), 1, (i+1)*multipliersymbolwidth ))
                            else:                            
                                classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))                            
                                #myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i*multipliersymbolwidth ))                            
                                if nodeFilteringType_combotext == "both incoming to & outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only incoming to":                                                              
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(192*i/GradSymNoOfClasses), 127-(127*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only outgoing from":                                                            
                                    myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(255-(192*i/GradSymNoOfClasses), 0, 0), 1, (i+1)*multipliersymbolwidth ))
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )                            
                        vlayer.setRendererV2( myRenderer )                            
                        message = "Flows "+str(nodeFilteringType_combotext)+" "+str(text)+" filtered and "+str(OutputShpFilterNodeNamesName)+" created successfully !"
                        QMessageBox.information(self.iface.mainWindow(),"info" ,message)                            
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer )                             

                    #Equal Size Classes
                    elif dlg.ui.comboBoxSelectSymbology.currentText() == "Equal Size Classes":
                        GradSymNoOfClasses = dlg.ui.spinBoxClasses.value() 
                        GradSymNoOfFeaturesZero = int(GradSymNoOfFeaturesZero)
                        GradSymNoOfFeaturesInInterval = int(  round(((int(GradSymNoOfFeatures)-int(GradSymNoOfFeaturesZero))/float(GradSymNoOfClasses)),0) ) 
                        myRangeList = []
                        GradSymList.sort()
                        for i in range(GradSymNoOfClasses):
                            if i == 0:
                                classlabel = str(GradSymMin)+" - "+str(GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1])
                                #myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                                if nodeFilteringType_combotext == "both incoming to & outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(192, 192, 192), 1, basesymbolwidth ))
                                elif nodeFilteringType_combotext == "only incoming to":                                                                                   
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255, 127), 1, basesymbolwidth ))
                                elif nodeFilteringType_combotext == "only outgoing from":                                                                                 
                                    myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(255, 0, 0), 1, basesymbolwidth ))
                            elif i == (GradSymNoOfClasses - 1):
                                classlabel = str(GradSymList[GradSymNoOfFeaturesInInterval*i])+" - "+str(GradSymMax)
                                #myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i*multipliersymbolwidth ))
                                if nodeFilteringType_combotext == "both incoming to & outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], int(GradSymMax), classlabel , QColor(192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only incoming to":                                                                           
                                    myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], int(GradSymMax), classlabel , QColor(0, 255-(192*i/GradSymNoOfClasses), 127-(127*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only outgoing from":                                                                         
                                    myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], int(GradSymMax), classlabel , QColor(255-(192*i/GradSymNoOfClasses), 0, 0), 1, (i+1)*multipliersymbolwidth ))
                            else:
                                classlabel = str(GradSymList[GradSymNoOfFeaturesInInterval*i])+" - "+str(GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1])
                                #myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, i*multipliersymbolwidth ))
                                if nodeFilteringType_combotext == "both incoming to & outgoing from":
                                    myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses), 192-(192*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only incoming to":                                                                                                                
                                    myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255-(192*i/GradSymNoOfClasses), 127-(127*i/GradSymNoOfClasses)), 1, (i+1)*multipliersymbolwidth ))
                                elif nodeFilteringType_combotext == "only outgoing from":                                                                                                              
                                    myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(255-(192*i/GradSymNoOfClasses), 0, 0), 1, (i+1)*multipliersymbolwidth ))                            
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                        vlayer.setRendererV2( myRenderer )
                        message = "Flows "+str(nodeFilteringType_combotext)+" "+str(text)+" filtered and "+str(OutputShpFilterNodeNamesName)+" created successfully !"
                        QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                        
        
        
    def about(self):
        dlg = form_aboutdialog.Form_AboutDialog() 
        #dlg.show()
        dlg.exec_() 
        #result = dlg3.exec_() 

        # run method that performs all the real work
    
    def run(self):
        # create and show the dialog
        dlg = FlowMapperDialog()
        # show the dialog
        dlg.show()
        
        #browse for file penceresini acmak icin SaveShp e signal yollar
        QtCore.QObject.connect(dlg.ui.BrowseShape,QtCore.SIGNAL("clicked()"), self.OutputShp)
        QtCore.QObject.connect(dlg.ui.BrowseShape,QtCore.SIGNAL("clicked()"), dlg.SetTextBrowseShape)
        QtCore.QObject.connect(dlg.ui.BrowseNodes,QtCore.SIGNAL("clicked()"), self.InputNodes)
        QtCore.QObject.connect(dlg.ui.BrowseNodes,QtCore.SIGNAL("clicked()"), dlg.SetTextBrowseNodes)
        QtCore.QObject.connect(dlg.ui.BrowseNodeNames,QtCore.SIGNAL("clicked()"), self.InputNodeNames)
        QtCore.QObject.connect(dlg.ui.BrowseNodeNames,QtCore.SIGNAL("clicked()"), dlg.SetTextBrowseNodeNames)        
        QtCore.QObject.connect(dlg.ui.BrowseShapeNodes,QtCore.SIGNAL("clicked()"), self.OutputShpNodes)
        QtCore.QObject.connect(dlg.ui.BrowseShapeNodes,QtCore.SIGNAL("clicked()"), dlg.SetTextBrowseShapeNodes)
        QtCore.QObject.connect(dlg.ui.BrowseMatrix,QtCore.SIGNAL("clicked()"), self.InputMatrix)
        QtCore.QObject.connect(dlg.ui.BrowseMatrix,QtCore.SIGNAL("clicked()"), dlg.SetTextBrowseMatrix)
        		
        result = dlg.exec_()
        if result == 1:
            
            global SaveShpName
            global SaveShpNameNodes
            global InputNodeNamesName
            global InputNodesName
            
            if dlg.ui.IncludeNodeNamescheckBox.isChecked() == False:
                IncludeNodeNames = 0            
                InputNodeNamesName = InputNodesName
            else:
                IncludeNodeNames = 1
                
            if dlg.ui.CreateFlowNodescheckBox.isChecked() == False:
                CreateShpNodes = 0            
                SaveShpNameNodes = "NULL"
            else:
                CreateShpNodes = 1            
                
            #combotext_temp = InputNodeNamesName
            #combotext_temp2 = IncludeNodeNames
            #QMessageBox.information(self.iface.mainWindow(), "InputNodeNamesName", QString(combotext_temp))
            #QMessageBox.information(self.iface.mainWindow(), "InputNodeNamesName", QString(combotext_temp2))
            
            if dlg.ui.TwowayRadioButton.isChecked():
                FlowType = 1
            elif dlg.ui.GrossRadioButton.isChecked():
                FlowType = 2
            elif dlg.ui.NetRadioButton.isChecked():
                FlowType = 3
            
            global combotext
            combotext = str(dlg.ui.comboBox.currentText()) 
            #QMessageBox.information(self.iface.mainWindow(), "info", QString(combotext))

            #SaveDirectory = os.path.realpath(SaveShpName)
            SaveDirectory = SaveShpName
            flowpyv07.shapefilemaker(FlowType,CreateShpNodes,IncludeNodeNames,str(SaveDirectory), str(SaveShpName),str(SaveShpNameNodes),str(InputMatrixName),str(InputNodesName),str(InputNodeNamesName),str(combotext))
                
            if dlg.ui.Add2MapcheckBox.isChecked() == False:
                SuccessMessage = str(SaveShpName) + " created successfully !"
                QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")
            
            else:    
                
                if dlg.ui.comboBoxSelectSymbology.currentText() == "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False: 
                    self.iface.addVectorLayer(str(SaveShpName), str(SaveShpName), "ogr")
                    SuccessMessage = str(SaveShpName) + " created successfully !"
                    QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")                
                
                elif dlg.ui.comboBoxSelectSymbology.currentText() == "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True:
                    layer = QgsVectorLayer(str(SaveShpName), str(SaveShpName), 'ogr')
                    #Use the currently selected layer
                    #layer = qgis.utils.iface.mapCanvas().currentLayer()
                    registry = QgsSymbolLayerV2Registry.instance()
                    lineMeta = registry.symbolLayerMetadata("SimpleLine")
                    markerMeta = registry.symbolLayerMetadata("MarkerLine")
                    
                    symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
                    
                    #Line layer
                    lineLayer = lineMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'offset': '0', 'penstyle': 'solid', 'use_custom_dash': '0', 'joinstyle': 'bevel', 'capstyle': 'square'})
                    
                    #Marker layer
                    #markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'interval': '3', 'rotate': '1', 'placement': 'interval', 'offset': '0'})
                    markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'rotate': '1', 'placement': 'centralpoint', 'offset': '0'})
                    subSymbol = markerLayer.subSymbol()
                    
                    #Replace the default layer with our own SimpleMarker
                    subSymbol.deleteSymbolLayer(0)
                    triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer({'name': 'filled_arrowhead', 'color': '255,0,0', 'color_border': '0,0,0', 'offset': '0,0', 'size': '3', 'angle': '0'})
                    subSymbol.appendSymbolLayer(triangle)
                    
                    #Replace the default layer with our two custom layers
                    symbol.deleteSymbolLayer(0)
                    symbol.appendSymbolLayer(lineLayer)
                    symbol.appendSymbolLayer(markerLayer)
                    
                    #Replace the renderer of the current layer
                    renderer = QgsSingleSymbolRendererV2(symbol)
                    layer.setRendererV2(renderer)    
                    #
                    QgsMapLayerRegistry.instance().addMapLayer( layer ) 
                    
                    SuccessMessage = str(SaveShpName) + " created successfully !"
                    #QMessageBox.information(self.iface.mainWindow(), "info", QString(SuccessMessage), QString('Close'))
                    QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")
					
                else:
                    
                    global GradSymNoOfFeatures
                    global GradSymNoOfFeaturesZero
                    global GradSymMin
                    global GradSymMax
                    global GradSymSumMagnitude
                    global GradSymMean
                    global GradSymMeanNotZero        
                    global GradSymStdDev
                    global GradSymStdDevNotZero                    
                    global GradSymList 
                    
                    shp = ogr.Open(str(SaveShpName),1)
                    layer = shp.GetLayer(0)
                    GradSymNoOfFeatures = str(layer.GetFeatureCount())
                    
                    feature = layer.GetNextFeature()
                    counterNotZero = 0
                    GradSymSumMagnitude = 0
                    GradSymList= []    
                    
                    while feature:
                        magnitude = feature.GetField('magnitude')
                        if magnitude > 0:
                            counterNotZero = counterNotZero + 1
                            GradSymList.append(int(magnitude))
                            GradSymMin = min(GradSymList)
                            GradSymMax = max(GradSymList)
                        GradSymSumMagnitude = GradSymSumMagnitude + magnitude
                        feature.Destroy()
                        feature = layer.GetNextFeature()
                    GradSymMean = str(round(float(GradSymSumMagnitude / int(GradSymNoOfFeatures)),3))
                    GradSymMeanNotZero = str(round(float(GradSymSumMagnitude / int(counterNotZero)),3))
                    GradSymSumMagnitude = str(GradSymSumMagnitude)
                    GradSymNoOfFeaturesZero = str(int(GradSymNoOfFeatures)-int(counterNotZero))
                    GradSymMin = str(GradSymMin)
                    GradSymMax = str(GradSymMax)
                    layer.ResetReading()

                    GradSymVar = 0
                    GradSymVarNotZero = 0

                    feature = layer.GetNextFeature()
                    while feature:
                        magnitude = feature.GetField('magnitude')
                        #feature = layer.GetNextFeature()
                        GradSymVar = GradSymVar + ((magnitude - float(GradSymMean))**2)
                        if magnitude > 0:
                            GradSymVarNotZero = GradSymVarNotZero + ((magnitude - float(GradSymMeanNotZero))**2)
                        feature.Destroy()
                        feature = layer.GetNextFeature()
                    GradSymStdDev = str(round(((GradSymVar / int(GradSymNoOfFeatures))**0.5), 3))
                    GradSymStdDevNotZero = str(round(((GradSymVarNotZero / int(counterNotZero))**0.5), 3))
                    layer.ResetReading()
                    
                    shp.Destroy()
                    
                    registry = QgsSymbolLayerV2Registry.instance()
                    lineMeta = registry.symbolLayerMetadata("SimpleLine")
                    markerMeta = registry.symbolLayerMetadata("MarkerLine")
                    
                    def validatedDefaultSymbol(geometryType):
                        symbol = QgsSymbolV2.defaultSymbol(geometryType)
                        if symbol is None:
                            if geometryType == QGis.Point:
                                symbol = QgsMarkerSymbolV2()
                            elif geometryType == QGis.Line:
                                symbol =  QgsLineSymbolV2()
                            elif geometryType == QGis.Polygon:
                                symbol = QgsFillSymbolV2()
                        return symbol
                    
                    #Create Symbology
                    def makeSymbologyForRange(layer, min ,max, label ,colour, alpha, width):
                        symbol = validatedDefaultSymbol(layer.geometryType())
                        
                        if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True: 
                            #Line layer
                            lineLayer = lineMeta.createSymbolLayer({'width': '0.5', 'color': '255,0,0', 'offset': '0', 'penstyle': 'solid', 'use_custom_dash': '0', 'joinstyle': 'bevel', 'capstyle': 'square'})
                            #Marker layer
                            markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': '255,0,0', 'rotate': '1', 'placement': 'centralpoint', 'offset': '0'})
                            subSymbol = markerLayer.subSymbol()
                            #Replace the default layer with our own SimpleMarker
                            subSymbol.deleteSymbolLayer(0)
                            triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer({'name': 'filled_arrowhead', 'color': '255,0,0', 'color_border': '255,255,255', 'offset': '0,0', 'size': '3', 'outline_width': '0.5', 'angle': '0'})
                            subSymbol.appendSymbolLayer(triangle)
                            #Replace the default layer with our two custom layers
                            symbol.deleteSymbolLayer(0)
                            symbol.appendSymbolLayer(lineLayer)
                            symbol.appendSymbolLayer(markerLayer)
                            
                            symbol.setColor(colour)
                            symbol.setAlpha(alpha)
                            symbol.setWidth(width)
                            range = QgsRendererRangeV2(min, max, symbol, label)
                            
                        elif dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False:
                            symbol.setColor(colour)
                            symbol.setAlpha(alpha)
                            symbol.setWidth(width)
                            range = QgsRendererRangeV2(min, max, symbol, label)
                        
                        return range

                    vlayer = QgsVectorLayer(str(SaveShpName), str(SaveShpName), 'ogr')
                    myTargetField = 'magnitude'
                    
                    #Define base line symbol width and multiplier factor for graduated classes
                    global basesymbolwidth
                    global multipliersymbolwidth
                    if dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == True: 
                        global basesymbolwidth
                        global multipliersymbolwidth
                        basesymbolwidth = 3.0
                        multipliersymbolwidth = 2.0
                    elif dlg.ui.comboBoxSelectSymbology.currentText() <> "Single Symbol" and dlg.ui.ShowDirectioncheckBox.isChecked() == False:
                        global basesymbolwidth
                        global multipliersymbolwidth
                        basesymbolwidth = 0.25                        
                        multipliersymbolwidth = 0.75                    
                    
                    #Equal Interval
                    if dlg.ui.comboBoxSelectSymbology.currentText() == "Equal Interval":
                        GradSymNoOfClasses = dlg.ui.spinBoxClasses.value() 
                        GradSymInterval = round(((int(GradSymMax) - int(GradSymMin)) / float(GradSymNoOfClasses)),0)
                        myRangeList = []
                        for i in range(GradSymNoOfClasses):
                            if i == 0:
                                classlabel = str(GradSymMin)+" - "+str(int(GradSymMin)+GradSymInterval)
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), int(GradSymMin)+GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                            elif i == (GradSymNoOfClasses - 1):
                                classlabel = str(int(GradSymMin)+(GradSymInterval*i)+0.001)+" - "+str(GradSymMax)
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                            else:
                                classlabel = str(int(GradSymMin)+(GradSymInterval*i)+0.001)+" - "+str(int(GradSymMin)+GradSymInterval*(i+1))
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin)+(GradSymInterval*i)+0.001, int(GradSymMin)+GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                        vlayer.setRendererV2( myRenderer )
                        SuccessMessage = str(SaveShpName) + " created successfully !"
                        QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer )                     

                    #Defined Interval
                    elif dlg.ui.comboBoxSelectSymbology.currentText() == "Defined Interval":
                        GradSymInterval = int(dlg.ui.lineEditInterval.text())
                        GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                        myRangeList = []
                        for i in range(GradSymNoOfClasses):
                            if i == 0:
                                classlabel = str(GradSymMin)+" - "+str(GradSymInterval)
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                            elif i == (GradSymNoOfClasses - 1):
                                classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymMax)
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                            else:
                                classlabel = str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                        vlayer.setRendererV2( myRenderer )
                        SuccessMessage = str(SaveShpName) + " created successfully !"
                        QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
                    
                    #Standard Deviation
                    elif dlg.ui.comboBoxSelectSymbology.currentText() == "Standard Deviation":
                        if dlg.ui.comboBoxSelectStdDev.currentText() == "1/4 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) / 4
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 0.25
                        elif dlg.ui.comboBoxSelectStdDev.currentText() == "1/2 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) / 2
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 0.5
                        elif dlg.ui.comboBoxSelectStdDev.currentText() == "1 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) 
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 1.0
                        elif dlg.ui.comboBoxSelectStdDev.currentText() == "2 Std. Dev.":
                            GradSymInterval = float(GradSymStdDevNotZero) * 2
                            GradSymNoOfClasses = int((int(GradSymMax) - int(GradSymMin)) / GradSymInterval) + 1
                            classlabelStdDev = 2.0
                        myRangeList = []
                        for i in range(GradSymNoOfClasses):                            
                            if i == 0:                            
                                classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str(GradSymMin)+" - "+str(GradSymInterval)                            
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymInterval, classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))                            
                            elif i == (GradSymNoOfClasses - 1):                            
                                classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str((GradSymInterval*i)+0.001)+" - "+str(GradSymMax)                            
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))                            
                            else:                            
                                classlabel = str((i+1)*classlabelStdDev)+" Std. Dev. "+str((GradSymInterval*i)+0.001)+" - "+str(GradSymInterval*(i+1))                            
                                myRangeList.append(makeSymbologyForRange( vlayer, (GradSymInterval*i)+0.001, GradSymInterval*(i+1), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))                            
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )                            
                        vlayer.setRendererV2( myRenderer )                            
                        SuccessMessage = str(SaveShpName) + " created successfully !"                            
                        QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")                            
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer )                             
                    
                    #Equal Size Classes
                    elif dlg.ui.comboBoxSelectSymbology.currentText() == "Equal Size Classes":
                        GradSymNoOfClasses = dlg.ui.spinBoxClasses.value() 
                        GradSymNoOfFeaturesZero = int(GradSymNoOfFeaturesZero)
                        GradSymNoOfFeaturesInInterval = int( round(((int(GradSymNoOfFeatures)-int(GradSymNoOfFeaturesZero))/float(GradSymNoOfClasses)),0) ) 
                        myRangeList = []
                        GradSymList.sort()
                        for i in range(GradSymNoOfClasses):
                            if i == 0:
                                classlabel = str(GradSymMin)+" - "+str(GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1])
                                myRangeList.append(makeSymbologyForRange( vlayer, int(GradSymMin), GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, basesymbolwidth ))
                            elif i == (GradSymNoOfClasses - 1):
                                classlabel = str(GradSymList[GradSymNoOfFeaturesInInterval*i])+" - "+str(GradSymMax)
                                myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], int(GradSymMax), classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                            else:
                                classlabel = str(GradSymList[GradSymNoOfFeaturesInInterval*i])+" - "+str(GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1])
                                myRangeList.append(makeSymbologyForRange( vlayer, GradSymList[GradSymNoOfFeaturesInInterval*i], GradSymList[(GradSymNoOfFeaturesInInterval*(i+1))-1], classlabel , QColor(0, 255-(255*i/GradSymNoOfClasses), 255*i/GradSymNoOfClasses), 1, (i+1)*multipliersymbolwidth ))
                        myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                        vlayer.setRendererV2( myRenderer )
                        SuccessMessage = str(SaveShpName) + " created successfully !"
                        QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")
                        QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
    
            #add nodes shapefile to map canvas based on checkbox state
            if dlg.ui.CreateFlowNodescheckBox.isChecked() == True and dlg.ui.AddNodes2MapcheckBox.isChecked() == False:
                SuccessMessage = str(SaveShpNameNodes) + " created successfully !"
                QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")
            
            elif dlg.ui.CreateFlowNodescheckBox.isChecked() == True and dlg.ui.AddNodes2MapcheckBox.isChecked() == True and dlg.ui.DifNodeSymbologycheckBox.isChecked() == False:
                SuccessMessage = str(SaveShpNameNodes) + " created successfully !"
                QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")
                self.iface.addVectorLayer(str(SaveShpNameNodes), str(SaveShpNameNodes), "ogr")            
            
            elif dlg.ui.CreateFlowNodescheckBox.isChecked() == True and dlg.ui.AddNodes2MapcheckBox.isChecked() == True and dlg.ui.DifNodeSymbologycheckBox.isChecked() == True:    
                #SuccessMessage = str(SaveShpNameNodes) + " created successfully !"
                #QMessageBox.information(self.iface.mainWindow(), "info", SuccessMessage, "Close")
                #self.iface.addVectorLayer(str(SaveShpNameNodes), str(SaveShpNameNodes), "ogr")
            
                registry = QgsSymbolLayerV2Registry.instance()
                markerMeta = registry.symbolLayerMetadata("MarkerLine")
                
                def validatedDefaultSymbol(geometryType):
                    symbol = QgsSymbolV2.defaultSymbol(geometryType)
                    if symbol is None:
                        if geometryType == QGis.Point:
                            symbol = QgsMarkerSymbolV2()
                        elif geometryType == QGis.Line:
                            symbol =  QgsLineSymbolV2()
                        elif geometryType == QGis.Polygon:
                            symbol = QgsFillSymbolV2()
                    return symbol
                
                #Create Symbology
                def makeSymbologyForRange(layer, min ,max, label ,colour, alpha, size):
                    symbol = validatedDefaultSymbol(layer.geometryType())
                    symbol.setColor(colour)
                    symbol.setAlpha(alpha)
                    symbol.setSize(size)
                    range = QgsRendererRangeV2(min, max, symbol, label)
                    return range

                vlayer = QgsVectorLayer(str(SaveShpNameNodes), str(SaveShpNameNodes), 'ogr')
                myTargetField = 'indicator'
                
                myRangeList = []
                    
                classlabel1 = "nodes gaining flows (incoming>outgoing)"
                classlabel2 = "nodes losing flows (incoming<outgoing)"
                classlabel3 = "neutral nodes (incoming=outgoing)"
                
                myRangeList.append(makeSymbologyForRange( vlayer, 0.9, 2, classlabel1 , QColor(0, 192, 0), 1, 2 ))
                myRangeList.append(makeSymbologyForRange( vlayer, -2, -0.9, classlabel2 , QColor(255, 0, 0), 1, 2 ))
                myRangeList.append(makeSymbologyForRange( vlayer, 0, 0, classlabel3 , QColor(128, 128, 128), 1, 2 ))                
                
                myRenderer = QgsGraduatedSymbolRendererV2( myTargetField, myRangeList )
                vlayer.setRendererV2( myRenderer )
                message = str(SaveShpNameNodes) + " created successfully !"
                QMessageBox.information(self.iface.mainWindow(),"info" ,message)
                QgsMapLayerRegistry.instance().addMapLayer( vlayer ) 
            
    #execfile("somefile.py")


