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

