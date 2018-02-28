# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 12:20:53 2018

@author: scott.downard
"""

from PIL import Image
import xlsxwriter
############################Output To Excel#######################################
def exportToexcel(data_dict,data_table, directory ,title = 'Test'):
    file_name = title + '.xlsx'
    workbook = xlsxwriter.Workbook(directory+'\\'+file_name)
    variable_format = workbook.add_format({'bold':1,'border':1,'align':'center','valign':'vcenter'})
    datasheet = workbook.add_worksheet('Data Page')
    row = 0
    col = 0
    for key in data_dict:
        row = 0
        datasheet.merge_range(row,col,row,col+3,key,variable_format)
        for typekey in data_dict[key]:
            row = 1
            datasheet.merge_range(row,col,row,col+1,typekey,variable_format)
            row += 1
            for metakey in data_dict[key][typekey]:
                if metakey == 'Data' or metakey == 'Time':
                    continue
                else:
                    datasheet.write(row,col,metakey)
                    datasheet.write(row,col+1,data_dict[key][typekey][metakey])
                    row += 1
            col +=2
    datapoints = workbook.add_worksheet('Data Points')
    row = 0
    col = 0
    for key in data_dict:
        row = 0
        datapoints.merge_range(row,col,row,col+2,key,variable_format)
        row += 1
        datapoints.write(row,col,"Acceleration (g's)",variable_format)
        datapoints.write(row,col+1,"Displacement (mm)",variable_format)
        datapoints.write(row,col+2,"Time (msec)",variable_format)
        row+=1
        for point in data_dict[key]['Acceleration']['Data']:
            datapoints.write(row,col,point)
            row += 1
        row=2
        for point in data_dict[key]['Displacement']['Data']:
            datapoints.write(row,col+1,point)
            row +=1
        row=2
        for point in data_dict[key]['Acceleration']['Time']:
            datapoints.write(row,col+2,point)
            row += 1
        col += 3
    dataTable = workbook.add_worksheet('Data Table')
    row = 0
    col = 0
    for key in data_table:
        row = 0
        dataTable.write(row,col,key,variable_format)
        row += 1
        for points in data_table[key]:
            dataTable.write(row,col,points,variable_format)
            row += 1
        col += 1
        
    workbook.close()
        
    










#column = 0
#file_name = ExcelFile + '.xlsx'
#workbook = xlsxwriter.Workbook(file_name)
#worksheet = workbook.add_worksheet('Summary')
##Create tables from data collected in python
#variable_format = workbook.add_format({'bold':1,'border':1,'align':'center','valign':'vcenter'})
#data_format = workbook.add_format({'border':1,'align':'center'})
#if filterSize is not 0:
#    
#    worksheet.merge_range(0,0,0,4,'Results',variable_format)
#    worksheet.write(1,0,'Test Number',variable_format)
#    worksheet.write(1,1,'Contact Time (mSec)',variable_format)
#    worksheet.write(1,2,'Bottom Out G (g)',variable_format)
#    worksheet.write(1,3,'Maximum Acceleration (g)',variable_format)
#    worksheet.write(1,4,'Maximum Displacement (mm)',variable_format)
#    row = 2
#    column = 0
#    count = 0
#    for i in file_list:
#        worksheet.write(row,column,'Test'+ str(i),variable_format)
#        worksheet.write(row,column+1,np.around(contactTime[count],3),data_format)
#        worksheet.write(row,column+2,np.around(bottomG[count],3),data_format)
#        worksheet.write(row,column+3,np.around(minAcceleration[count],3),data_format)
#        worksheet.write(row,column+4,np.around(maxDisplacement[count],3),data_format)
#        count += 1
#        row += 1
#
############################Insert Graphs into Excel###########################
#img1 = Image.open(DispGraph+'.jpg')
#imgwidth1, imgheight1 = img1.size
#img2 = Image.open(TimeGraph+'.jpg')
#imgwidth2, imgheight2 = img2.size
#img3 = Image.open('Average '+ DispGraph +'.jpg')
#imgwidth3, imgheight3 = img3.size
#worksheet.insert_image(0,column+6, DispGraph+'.jpg',{'x_scale':0.25,'y_scale':0.25})
#worksheet.insert_image(0,column+6, TimeGraph+'.jpg',{'x_scale': 0.25, 'y_scale': 0.25,'y_offset':imgheight1*0.25})
#worksheet.insert_image(0,column+6, 'Average '+ DispGraph +'.jpg',{'x_scale': 0.25, 'y_scale': 0.25,'y_offset':(imgheight1+imgheight2)*0.25})
#worksheet.insert_image(0,column+6, 'Average '+ TimeGraph +'.jpg',{'x_scale': 0.25, 'y_scale': 0.25,'y_offset':(imgheight1+imgheight2+imgheight3)*0.25})
#worksheet2 = workbook.add_worksheet('RAW_SAE'+str(filterSize))
#
#column = 0
#count = 0
#
#
#for testtype in total_data:
#    row = 0
#    worksheet2.merge_range(row,column,row,column+2,testtype,variable_format)
#    row += 1
#    for section in total_data[testtype]:
#        worksheet2.write(row,column,section,variable_format)
#        row += 1
#        for j in total_data[testtype][section][0]:
#            worksheet2.write(row,column,j)
#            row +=1
#        column += 1
#        row = 1
#
#if avg_check == True:
#    worksheet3 = workbook.add_worksheet('Average Plots')
#    numGroup = len(avgAccel)
#    row = 0
#    column = 0
#    
#    for key in avgAccel:
#        row = 0
#        worksheet3.merge_range(row,column,row,column + 2, key , variable_format) 
#        row += 1
#        worksheet3.write(row,column,'Acceleration',variable_format)
#        worksheet3.write(row,column+1,'Displacement',variable_format)
#        worksheet3.write(row,column+2,'Time',variable_format)
#        row += 1
#        for i in range(0,len(avgAccel[key])):
#            worksheet3.write(row,column,avgAccel[key][i])
#            worksheet3.write(row,column+1,avgDisp[key][i])
#            worksheet3.write(row,column+2,avgTime[key][i])
#            row += 1
#        column += 3
            

