# Flowpy -- takes a square interaction matrix, a corresponding set of point coordinates, and
# and creates a shapefile of flow lines from them. You can choose magnitudes as "raw" two way flow,
# net flow, or gross flow.

# Flowpy is initially written by Alan Glennon (19 Oct. 2009) in Python 2.6 and requires ogr to run.
# initially coded by Alan GLENNON (19 Oct. 2009)
# further developed and coded by Cem GULLUOGLU (between 2011 & 2013)

import codecs

def shapefilemaker(typeofcalculation,CreateShpNodes,IncludeNodeNames,fulldirectorystring,outputfilename,outputfilenamenodes,fulldirODinput,fulldirPTinput,fulldirPTNamesinput,combotext):
        
        #import flowmapper
        
        import ogr, os, sys
        import math
        #directory location of output file
        #os.chdir(fulldirectorystring)
        #location of input file
        odmatrixfilename = fulldirODinput
        nodefilename = fulldirPTinput
        nodenamesfilename = fulldirPTNamesinput

        # type of flow calculation -- 1 is two way flow; 2 is gross flow; 3 is net flow

        try: 
            odmatrix = open(odmatrixfilename, 'r')
            nodes = open(nodefilename, 'r')
            #names = codecs.open(nodenamesfilename, 'r', encoding='utf-8')
            names = open(nodenamesfilename, 'r')
        except IOError, e:
            print 'file open error:', e

        numberofnodes = 0
        for line in nodes:
                numberofnodes += 1
        nodes.close

        # interaction file is read. Output result is myodmatrix[rows][columns]
        rows = 0
        myodmatrix = [] #stores flow magnitudes between input nodes
        for icounter in xrange(numberofnodes):
                        myodmatrix.append([])
                        for jcounter in xrange(numberofnodes):
                                myodmatrix[icounter].append(icounter+jcounter)

        for eachLine in odmatrix:
                        separatestrings = eachLine.split()
                        columns = 0
                        while columns < numberofnodes:
                            onevalue = float(separatestrings[columns])
                            myodmatrix[rows][columns] = onevalue
                            columns += 1
                        rows += 1
        odmatrix.close

        
        # points file is read. Output result is mypoints[ptrows][ptcolumns]
        ptrows = 0
        mypoints = [] #stores coordinates of input nodes
        for kcounter in xrange(numberofnodes):
                        mypoints.append([])
                        for lcounter in xrange(2):
                                mypoints[kcounter].append(kcounter+lcounter)

        nodesagain = open(nodefilename,'r')
        
        for eachLine2 in nodesagain:
                        separatestrings2 = eachLine2.split()
                        ptcolumns = 0
                        while ptcolumns < 2:
                                onevalue2 = float(separatestrings2[ptcolumns])
                                mypoints[ptrows][ptcolumns] = onevalue2
                                ptcolumns += 1
                        ptrows += 1
        nodesagain.close

        
        # read node names (input txt file optional)
        mypointnames = [] #stores names of input nodes (attribute)
        for eachLine3 in names:
                        mypointnames.append(eachLine3.split())
                        #mypointnames.append(eachLine3.strip())
        names.close
        
        ##############################################################################################################
        #f = open("C:\\_.txt","w")
        #for item in mypointnames:
        #    f.write("%s\n" % item)
        #f.close
        ##############################################################################################################

        if CreateShpNodes == 1:
            #create flow NODES/start########################################################################################
            # get the driver
            driver2 = ogr.GetDriverByName('ESRI Shapefile')
            # create a new data source and layer
            if os.path.exists(outputfilenamenodes):
                driver2.DeleteDataSource(outputfilenamenodes)
                
            ds2 = driver2.CreateDataSource(outputfilenamenodes)
            layer2 = ds2.CreateLayer('node', geom_type=ogr.wkbPoint)
            fieldDefn20 = ogr.FieldDefn('name', ogr.OFTString)
            fieldDefn21 = ogr.FieldDefn('incoming', ogr.OFTReal)
            fieldDefn22 = ogr.FieldDefn('outgoing', ogr.OFTReal)
            fieldDefn23 = ogr.FieldDefn('gross', ogr.OFTReal)
            fieldDefn24 = ogr.FieldDefn('net', ogr.OFTReal)
            fieldDefn25 = ogr.FieldDefn('in/out', ogr.OFTReal)
            fieldDefn26 = ogr.FieldDefn('out/in', ogr.OFTReal)
            fieldDefn27 = ogr.FieldDefn('indicator', ogr.OFTReal)
            layer2.CreateField(fieldDefn20)
            layer2.CreateField(fieldDefn21)
            layer2.CreateField(fieldDefn22)
            layer2.CreateField(fieldDefn23)
            layer2.CreateField(fieldDefn24)
            layer2.CreateField(fieldDefn25)
            layer2.CreateField(fieldDefn26)            
            layer2.CreateField(fieldDefn27)            
            
            counterA = 0
            sumincoming = 0
            while counterA < numberofnodes:
                linester2 = ogr.Geometry(ogr.wkbPoint)
                linester2.SetPoint(0, mypoints[counterA][0],mypoints[counterA][1])
                featureDefn2 = layer2.GetLayerDefn()
                feature2 = ogr.Feature(featureDefn2)
                feature2.SetGeometry(linester2)

                #set node names/start
                if IncludeNodeNames == 1:
                    name = str(mypointnames[counterA])
                    name = name[2:-2]
                    feature2.SetField('name',name)
                elif IncludeNodeNames == 0:
                    name = "Node_"+str(counterA+1)
                    feature2.SetField('name',name)
                #set node names/end                

                myodmatrixA=myodmatrix[counterA]
                sumoutgoing=sum(myodmatrixA)
                feature2.SetField('outgoing',sumoutgoing)
                
                counterB = 0
                while counterB < numberofnodes:
            
                    myodmatrixB = myodmatrix[counterB][counterA]
                    sumincoming=sumincoming+int(myodmatrixB)
                    counterB += 1
                feature2.SetField('incoming',sumincoming)

                gross = sumincoming + sumoutgoing
                feature2.SetField('gross',gross)
                net = sumincoming - sumoutgoing
                net_abs = abs(net)
                feature2.SetField('net',net_abs)
                
                #START#patched to avoid DIV by ZERO bug while calculating flow node attributes
                if sumoutgoing == 0:
                    feature2.SetField('in/out',0)
                else:
                    in_DIV_out = sumincoming / sumoutgoing
                    feature2.SetField('in/out',in_DIV_out)
                			
                if sumincoming == 0:
                    feature2.SetField('out/in',0)
                else:
                    out_DIV_in = sumoutgoing / sumincoming 
                    feature2.SetField('out/in',out_DIV_in)                
                #END#patched to avoid DIV by ZERO bug while calculating flow node attributes
                                
                
                #set node indicator: +1 receives flow, -1 gives flow, 0 incoming = outgoing
                if net < 0:
                    indicator = -1
                elif net > 0:
                    indicator = 1
                elif net == 0:
                    indicator = 0
                feature2.SetField('indicator',indicator)
                    
                sumincoming = 0
                
                layer2.CreateFeature(feature2)
                counterA += 1

            linester2.Destroy()
            feature2.Destroy()
            ds2.Destroy()
            #create flow NODES/end########################################################################################
            
        
        #START setup creation of shapefile LINES
        # get the driver
        driver = ogr.GetDriverByName('ESRI Shapefile')
        # create a new data source and layer
        if os.path.exists(outputfilename):
            driver.DeleteDataSource(outputfilename)
            
        ds = driver.CreateDataSource(outputfilename)
        if ds is None:
            print 'Could not create file'
            sys.exit(1)
        layer = ds.CreateLayer('flow', geom_type=ogr.wkbLineString)
        fieldDefn = ogr.FieldDefn('magnitude', ogr.OFTReal)
        
        fieldDefn2 = ogr.FieldDefn('length_km', ogr.OFTReal)
        fieldDefn3 = ogr.FieldDefn('coord_x1', ogr.OFTReal)
        fieldDefn4 = ogr.FieldDefn('coord_y1', ogr.OFTReal)
        fieldDefn5 = ogr.FieldDefn('coord_x2', ogr.OFTReal)
        fieldDefn6 = ogr.FieldDefn('coord_y2', ogr.OFTReal)
        fieldDefn7 = ogr.FieldDefn('name_x1y1', ogr.OFTString)
        fieldDefn8 = ogr.FieldDefn('name_x2y2', ogr.OFTString)
        
        layer.CreateField(fieldDefn)
        layer.CreateField(fieldDefn2)
        layer.CreateField(fieldDefn3)
        layer.CreateField(fieldDefn4)
        layer.CreateField(fieldDefn5)
        layer.CreateField(fieldDefn6)
        layer.CreateField(fieldDefn7)
        layer.CreateField(fieldDefn8)
        
        #END setup creation of shapefile

        #START two way flow calculation. 
        if typeofcalculation == 1:
            counter1 = 0
            counter2 = 0
            while counter2 < numberofnodes:
                    while counter1 < numberofnodes:
                            linester = ogr.Geometry(ogr.wkbLineString)
                            linester.AddPoint(mypoints[counter2][0],mypoints[counter2][1])
                            linester.AddPoint(mypoints[counter1][0],mypoints[counter1][1])
                            featureDefn = layer.GetLayerDefn()
                            feature = ogr.Feature(featureDefn)
                            feature.SetGeometry(linester)
                            feature.SetField('magnitude',myodmatrix[counter2][counter1])
                            
                            x1 = mypoints[counter2][0]
                            y1 = mypoints[counter2][1]
                            x2 = mypoints[counter1][0]
                            y2 = mypoints[counter1][1]
                            
                            feature.SetField('coord_x1',x1)
                            feature.SetField('coord_y1',y1)
                            feature.SetField('coord_x2',x2)
                            feature.SetField('coord_y2',y2)  
                            
                            if IncludeNodeNames == 1:
                                Namex1y1 = str(mypointnames[counter2])
                                Namex1y1 = Namex1y1[2:-2]
                                feature.SetField('name_x1y1',Namex1y1)
                                Namex2y2 = str(mypointnames[counter1])
                                Namex2y2 = Namex2y2[2:-2]
                                feature.SetField('name_x2y2',Namex2y2)
                            elif IncludeNodeNames == 0:
                                Namex1y1 = "Node_"+str(counter2+1)
                                feature.SetField('name_x1y1',Namex1y1)
                                Namex2y2 = "Node_"+str(counter1+1)
                                feature.SetField('name_x2y2',Namex2y2)
                                
                                
                            if combotext == "Cartesian":
                                length_m = (((x1-x2)**2)+((y1-y2)**2))**0.5
                                feature.SetField('length_km',length_m / (1000))
                            
                            else:
                                lon1 = float(x1)
                                lat1 = float(y1)
                                lon2 = float(x2)
                                lat2 = float(y2)
                                length_km = math.atan2(math.sqrt((math.cos((math.atan(1.0)/45.0)*lat2)*math.sin((math.atan(1.0)/45.0)*lon2-(math.atan(1.0)/45.0)*lon1))**2 + (math.cos((math.atan(1.0)/45.0)*lat1)*math.sin((math.atan(1.0)/45.0)*lat2)-math.sin((math.atan(1.0)/45.0)*lat1)*math.cos((math.atan(1.0)/45.0)*lat2)*math.cos((math.atan(1.0)/45.0)*lon2-(math.atan(1.0)/45.0)*lon1))**2), math.sin((math.atan(1.0)/45.0)*lat1)*math.sin((math.atan(1.0)/45.0)*lat2) + math.cos((math.atan(1.0)/45.0)*lat1)*math.cos((math.atan(1.0)/45.0)*lat2)*math.cos((math.atan(1.0)/45.0)*lon2-(math.atan(1.0)/45.0)*lon1)) * 6367.9375
                                feature.SetField('length_km',length_km)
                            
                            
                            layer.CreateFeature(feature)
                            counter1 = counter1 + 1
                    counter2 = counter2 + 1
                    counter1 = 0
        #FINISH two way flow calculation


        #START gross flow calculations
        if typeofcalculation == 2:
            g = 0
            h = 0
            while g < numberofnodes:
                while h < numberofnodes:
                            if (g <= h):
                                    linester = ogr.Geometry(ogr.wkbLineString)
                                    linester.AddPoint(mypoints[g][0], mypoints[g][1])
                                    linester.AddPoint(mypoints[h][0], mypoints[h][1])
                                    if h==g: 
                                        grossmagnitude = (myodmatrix[g][h] + myodmatrix[h][g])/2
                                    else: 
                                        grossmagnitude = (myodmatrix[g][h] + myodmatrix[h][g])
                                    featureDefn = layer.GetLayerDefn()
                                    feature = ogr.Feature(featureDefn)
                                    feature.SetGeometry(linester)
                                    feature.SetField('magnitude',grossmagnitude)

                                    x1 = mypoints[h][0]                                        
                                    y1 = mypoints[h][1]
                                    x2 = mypoints[g][0]                                        
                                    y2 = mypoints[g][1]                                        
                                    
                                    feature.SetField('coord_x1',x1)
                                    feature.SetField('coord_y1',y1)
                                    feature.SetField('coord_x2',x2)
                                    feature.SetField('coord_y2',y2)                                    
                                    
                                    if IncludeNodeNames == 1:
                                        Namex1y1 = str(mypointnames[h])
                                        Namex1y1 = Namex1y1[2:-2]
                                        feature.SetField('name_x1y1',Namex1y1)
                                        Namex2y2 = str(mypointnames[g])
                                        Namex2y2 = Namex2y2[2:-2]
                                        feature.SetField('name_x2y2',Namex2y2)
                                    
                                    elif IncludeNodeNames == 0:
                                        Namex1y1 = "Node_"+str(h+1)
                                        feature.SetField('name_x1y1',Namex1y1)
                                        Namex2y2 = "Node_"+str(g+1)
                                        feature.SetField('name_x2y2',Namex2y2)
                                    
                                    if combotext == "Cartesian":
                                        length_m = (((x1-x2)**2)+((y1-y2)**2))**0.5
                                        feature.SetField('length_km',length_m / (1000))
                                    
                                    else:
                                        lon1 = float(x1)
                                        lat1 = float(y1)
                                        lon2 = float(x2)
                                        lat2 = float(y2)
                                        length_km = math.atan2(math.sqrt((math.cos((math.atan(1.0)/45.0)*lat2)*math.sin((math.atan(1.0)/45.0)*lon2-(math.atan(1.0)/45.0)*lon1))**2 + (math.cos((math.atan(1.0)/45.0)*lat1)*math.sin((math.atan(1.0)/45.0)*lat2)-math.sin((math.atan(1.0)/45.0)*lat1)*math.cos((math.atan(1.0)/45.0)*lat2)*math.cos((math.atan(1.0)/45.0)*lon2-(math.atan(1.0)/45.0)*lon1))**2), math.sin((math.atan(1.0)/45.0)*lat1)*math.sin((math.atan(1.0)/45.0)*lat2) + math.cos((math.atan(1.0)/45.0)*lat1)*math.cos((math.atan(1.0)/45.0)*lat2)*math.cos((math.atan(1.0)/45.0)*lon2-(math.atan(1.0)/45.0)*lon1)) * 6367.9375
                                        feature.SetField('length_km',length_km)
                                    
                                    layer.CreateFeature(feature)
                            h += 1
                h = 0
                g += 1
        #FINISH gross flow calculations

        #START net flow calculations
        if typeofcalculation == 3:
            g = 0
            h = 0
            while g < numberofnodes:
                while h < numberofnodes:
                            if (g <= h):
                                    if h==g: 
                                        netmagnitude = (myodmatrix[g][h] + myodmatrix[h][g])/2
                                    else: 
                                        netmagnitude = (myodmatrix[g][h] - myodmatrix[h][g])
                                    if netmagnitude < 0:
                                        linester = ogr.Geometry(ogr.wkbLineString)
                                        linester.AddPoint(mypoints[h][0], mypoints[h][1])
                                        linester.AddPoint(mypoints[g][0], mypoints[g][1])
                                        featureDefn = layer.GetLayerDefn()
                                        feature = ogr.Feature(featureDefn)
                                        feature.SetGeometry(linester)
                                        feature.SetField('magnitude',netmagnitude * (-1))

                                        x1 = mypoints[h][0]                                        
                                        y1 = mypoints[h][1]
                                        x2 = mypoints[g][0]                                        
                                        y2 = mypoints[g][1]                                        
                                        
                                        feature.SetField('coord_x1',x1)
                                        feature.SetField('coord_y1',y1)
                                        feature.SetField('coord_x2',x2)
                                        feature.SetField('coord_y2',y2)
                                        
                                        if IncludeNodeNames == 1:
                                            Namex1y1 = str(mypointnames[h])
                                            Namex1y1 = Namex1y1[2:-2]
                                            feature.SetField('name_x1y1',Namex1y1)
                                            Namex2y2 = str(mypointnames[g])
                                            Namex2y2 = Namex2y2[2:-2]
                                            feature.SetField('name_x2y2',Namex2y2)
                                        
                                        elif IncludeNodeNames == 0:
                                            Namex1y1 = "Node_"+str(h+1)
                                            feature.SetField('name_x1y1',Namex1y1)
                                            Namex2y2 = "Node_"+str(g+1)
                                            feature.SetField('name_x2y2',Namex2y2)
                                        
                                        if combotext == "Cartesian":
                                            length_m = (((x1-x2)**2)+((y1-y2)**2))**0.5
                                            feature.SetField('length_km',length_m / (1000))
                                        
                                        else:
                                            lon1 = float(x1)
                                            lat1 = float(y1)
                                            lon2 = float(x2)
                                            lat2 = float(y2)
                                            length_km = math.atan2(math.sqrt((math.cos((math.atan(1.0)/45.0)*lat2)*math.sin((math.atan(1.0)/45.0)*lon2-(math.atan(1.0)/45.0)*lon1))**2 + (math.cos((math.atan(1.0)/45.0)*lat1)*math.sin((math.atan(1.0)/45.0)*lat2)-math.sin((math.atan(1.0)/45.0)*lat1)*math.cos((math.atan(1.0)/45.0)*lat2)*math.cos((math.atan(1.0)/45.0)*lon2-(math.atan(1.0)/45.0)*lon1))**2), math.sin((math.atan(1.0)/45.0)*lat1)*math.sin((math.atan(1.0)/45.0)*lat2) + math.cos((math.atan(1.0)/45.0)*lat1)*math.cos((math.atan(1.0)/45.0)*lat2)*math.cos((math.atan(1.0)/45.0)*lon2-(math.atan(1.0)/45.0)*lon1)) * 6367.9375
                                            feature.SetField('length_km',length_km)
                                        
                                        layer.CreateFeature(feature)
                                    
                                    else:
                                        linester = ogr.Geometry(ogr.wkbLineString)
                                        linester.AddPoint(mypoints[g][0], mypoints[g][1])
                                        linester.AddPoint(mypoints[h][0], mypoints[h][1])
                                        featureDefn = layer.GetLayerDefn()
                                        feature = ogr.Feature(featureDefn)
                                        feature.SetGeometry(linester)
                                        feature.SetField('magnitude',netmagnitude)
                                        
                                        x1 = mypoints[g][0]
                                        y1 = mypoints[g][1]
                                        x2 = mypoints[h][0]
                                        y2 = mypoints[h][1]
                                        
                                        feature.SetField('coord_x1',x1)
                                        feature.SetField('coord_y1',y1)
                                        feature.SetField('coord_x2',x2)
                                        feature.SetField('coord_y2',y2)
                                        
                                        if IncludeNodeNames == 1:
                                            Namex1y1 = str(mypointnames[g])
                                            Namex1y1 = Namex1y1[2:-2]
                                            feature.SetField('name_x1y1',Namex1y1)
                                            Namex2y2 = str(mypointnames[h])
                                            Namex2y2 = Namex2y2[2:-2]
                                            feature.SetField('name_x2y2',Namex2y2)
                                            
                                        elif IncludeNodeNames == 0:
                                            Namex1y1 = "Node_"+str(g+1)
                                            feature.SetField('name_x1y1',Namex1y1)
                                            Namex2y2 = "Node_"+str(h+1)
                                            feature.SetField('name_x2y2',Namex2y2)                                            
                                        
                                        if combotext == "Cartesian":
                                            length_m = (((x1-x2)**2)+((y1-y2)**2))**0.5
                                            feature.SetField('length_km',length_m / (1000))
                                            
                                        else:
                                            lon1 = float(x1)
                                            lat1 = float(y1)
                                            lon2 = float(x2)
                                            lat2 = float(y2)
                                            length_km = math.atan2(math.sqrt((math.cos((math.atan(1.0)/45.0)*lat2)*math.sin((math.atan(1.0)/45.0)*lon2-(math.atan(1.0)/45.0)*lon1))**2 + (math.cos((math.atan(1.0)/45.0)*lat1)*math.sin((math.atan(1.0)/45.0)*lat2)-math.sin((math.atan(1.0)/45.0)*lat1)*math.cos((math.atan(1.0)/45.0)*lat2)*math.cos((math.atan(1.0)/45.0)*lon2-(math.atan(1.0)/45.0)*lon1))**2), math.sin((math.atan(1.0)/45.0)*lat1)*math.sin((math.atan(1.0)/45.0)*lat2) + math.cos((math.atan(1.0)/45.0)*lat1)*math.cos((math.atan(1.0)/45.0)*lat2)*math.cos((math.atan(1.0)/45.0)*lon2-(math.atan(1.0)/45.0)*lon1)) * 6367.9375
                                            feature.SetField('length_km',length_km)

                                        layer.CreateFeature(feature)
                            h += 1
                h = 0
                g += 1
        #FINISH net flow calculations

        # shapefile cleanup
        # destroy the geometry and feature and close the data source
        linester.Destroy()
        feature.Destroy()
        ds.Destroy()

