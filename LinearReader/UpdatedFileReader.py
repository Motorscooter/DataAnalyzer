# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 14:39:22 2018

@author: scott.downard
"""

import os
import struct
import numpy as np

def readFiles(dirList):
    filedict = {}
    new_float_data = []
    new_data = []
    time = []
    for file in dirList:
# =============================================================================
# Opens current file and reads text data to pull needed information
        with open(file,'rb') as fup:
        
            textfilestr = fup.read()
            textfilestr = textfilestr.decode('latin-1') #Decode text from binary file
            vs = textfilestr.find('VERTSCALE')     #Vertical scaling factor
            vo = textfilestr.find('VERTOFFSET')    #Vertical offset from 0
            vu = textfilestr.find('VERTUNITS')     #Vertical units
            hs = textfilestr.find('HORZSCALE')     #horizontal scaling factor
            ho = textfilestr.find('HORZOFFSET')    #horizontal offset from 0
            hu = textfilestr.find('HORZUNITS')     #horizontal units
            hups = textfilestr.find('HUNITPERSEC') #number of horizontal units per second
            rl = textfilestr.find('RECLEN')        #Number of datapoints in file
            xdc = textfilestr.find('XDCRSENS')     #Used to find grab the correct number of points in datapoint line
            cr = textfilestr.find('CLOCK_RATE')    #Sample rate
            ss = textfilestr.find('SUBSAMP_SKIP')  #Used to grab correct number of points in Sample Rate
            name = textfilestr.find('Sample')      #Reads BuildSheet Number
            filedict[name] = {}
            filedict[name]['VertScale'] = float(textfilestr[vs+10:vo - 1])
            filedict[name]['VertOffset'] = float(textfilestr[vo+11:vu - 1])
            filedict[name]['VertUnits'] = textfilestr[vu+10:hs - 1]
            filedict[name]['HorzScale'] = float(textfilestr[hs+10:hups - 1])
            filedict[name]['HorzUnitsPerSec'] = float(textfilestr[hups+12:ho - 1])
            filedict[name]['HorzOffset'] = float(textfilestr[ho+11:hu - 1])
            filedict[name]['HorzUnits'] = (textfilestr[hu+10:rl - 1])
            filedict[name]['NumofPoints'] = int(textfilestr[rl+7:xdc-1])
            filedict[name]['Sample Rate'] = float(textfilestr[cr+11:ss-1])
        fup.close()            
# =============================================================================
# =============================================================================
# The file is closed and then opened to read binary data.
        with open(file, 'rb') as fup:
            datacount = filedict[name]['NumofPoints']            
            size = fup.read()
            data = struct.unpack('h'*datacount,size[len(size)-(datacount*2):])
            list_data = list(data)
            for i in list_data:
                new_float_data.append(float(i))
            for i in new_float_data:
                new_data.append(i *  filedict[name]['VertScale'] + filedict[name]['VertOffset'])
            filedict[name]['Data'] = new_data
            timecount = filedict[name]['HorzOffset']           
            for i in range(0,filedict[name]['NumofPoints']):
                time.append(timecount)
                timecount += filedict['HorzScale']
            filedict[name]['Time'] = time
        fup.close()
        return filedict
# =============================================================================
