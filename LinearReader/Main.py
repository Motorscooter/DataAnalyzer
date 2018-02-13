# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 14:26:01 2018

@author: scott.downard
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import Mainwindow
from LinearReader import *
from exporttoexcel import *
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column, row
from bokeh.models import Legend, ColumnDataSource
from bokeh.models.widgets import Panel, Tabs, DataTable, TableColumn
import bokeh.io as bk
import numpy as np
import pandas as pd
class LinearApp(QtWidgets.QMainWindow, Mainwindow.Ui_mainwindow):

    
    def __init__(self,parent=None):
        filterlist = ['Raw','60','180']
        super(LinearApp, self).__init__(parent)
        self.setupUi(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Test Name','Group #'])
        self.filterBox.addItems(filterlist)
        self.openFile.clicked.connect(self.browse_folder)
        self.graphbtn.clicked.connect(self.graph)
        self.export_2.clicked.connect(self.exportexcel)
    def browse_folder(self):
#        self.listWidget.clear()
        
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self,"Pick a Folder")
        if self.directory:
            self.tableWidget.clear()
            self.test_list = []
            group_list = []
            self.data_dict = fileRead(self.directory)            
            for keys in self.data_dict:
                self.test_list.append(keys)
             
            for i in range(len(self.test_list)):
                group_list.append(str(i+1))
            self.tableWidget.setRowCount(len(self.test_list))
            i = 0
            for k in self.test_list:
                self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem("Test_"+str(k))) 
                comboBox = QtWidgets.QComboBox()
                comboBox.addItems(group_list)
                comboBox.setCurrentIndex(i)
                self.tableWidget.setCellWidget(i,1,comboBox)               
                i +=1
 
        
    def exportexcel(self):
        i = 0
        savedirectory = QtWidgets.QFileDialog.getExistingDirectory(self,"Save Excel File")
        for keys in self.data_dict:
            self.data_dict[keys]['Acceleration']['Title'] = self.test_name[i]
            i += 1
        exportToexcel(self.data_dict,savedirectory,self.titlebox.text())
        
        
    def graph(self):
        if self.directory:
            
            group_list = []
            self.test_name = []
            color_list = ['black','red','blue','green','purple','grey','orange',
              'yellow','darkgreen','magenta','gold','aquamarine']
            group_color = []
            filtersize = self.filterBox.currentText()
            plotTitle = self.titlebox.text()
            for i in range(len(self.test_list)):
                self.test_name.append(self.tableWidget.item(i,0).text())
                group_list.append(self.tableWidget.cellWidget(i,1).currentText())
            self.final_data = {i:group_list.count(i) for i in group_list}
            for key in self.final_data:
                self.final_data[key] = {}
            for i in group_list:
                group_color.append(color_list[int(i)])
            for i in range(len(self.test_list)):
                if filtersize == 'Raw':
                    continue
                else:
                    self.data_dict[self.test_list[i]]['Acceleration']['Data'] = filterProcessing(self.data_dict[self.test_list[i]]['Acceleration'][
                            'Data'],int(filtersize),self.data_dict[self.test_list[i]]['Acceleration']['Sample Rate'])
                
          
            test_list = []
            accel_list = []
            disp_list = []
            time_list = []
            trun_accel = []
            trun_disp = []
            trun_time = []
            #Check to make sure sample rate are the same between all tests, if they are
            #Create a variable for the sample rate of the build sheet.
            for key in self.data_dict:
                test_list.append(key)
                accel_list.append(np.asarray(self.data_dict[key]['Acceleration']['Data']))
                disp_list.append(np.asarray(self.data_dict[key]['Displacement']['Data']))
                time_list.append(np.asarray(self.data_dict[key]['Acceleration']['Time']))
            idx1 = []
            for lst in time_list:
                idx = (np.abs(lst-0)).argmin()
                idx1.append(list(range(0,idx)))
            for i in range(len(accel_list)):
                trun_accel.append(np.delete(accel_list[i],idx1[i]))
            for i in range(len(disp_list)):
                trun_disp.append(np.delete(disp_list[i],idx1[i]))
            for i in range(len(time_list)):
                trun_time.append(np.delete(time_list[i],idx1[i]))
            
#            datatable = tableCalc(trun_accel,trun_disp,trun_time)
            
            p1 = figure(width = 1200, height = 450, title = plotTitle)
            p2 = figure(width = 1200, height = 450, title = plotTitle)
            legend_set1 = []
            legend_set2 = []
            for i in range(len(accel_list)):
                a = p1.line(trun_disp[i],trun_accel[i],line_color = group_color[i], alpha = 1, muted_color = group_color[i],muted_alpha=0)
                b = p2.line(trun_time[i],trun_accel[i],line_color = group_color[i], alpha = 1, muted_color = group_color[i],muted_alpha=0)
                legend_set1.append((self.test_name[i],[a]))
                legend_set2.append((self.test_name[i],[b]))
            
            output_file(plotTitle + '.html')
            
#            data = dict(titles = self.test_name,
#                        max_accel = datatable['Max Acceleration'],
#                        max_displacment = datatable['Max Displacement'],
#                        contact_time = datatable['Contact Time'])
#            source = ColumnDataSource(data)
#            
#            columns = [TableColumn(field=titles,title="Test Name"),
#                       TableColumn(field=max_accel,title="Maximum Acceleration"),
#                       TableColumn(field=max_displacment,title = "Maximum Dipslacement"),
#                       TableColumn(field = contact_time,title = "Contact Time @ 2g's")]
#            data_table = DataTable(source = source, columns = columns, width = 400, height = 300)
            
            legend1 = Legend(items = legend_set1, location=(0,0))
            legend1.click_policy = "mute"
            p1.add_layout(legend1,'below')   
            p1.legend.orientation = "horizontal"
            p1.legend.padding = 1
            p1.xaxis.axis_label = "Displacement (mm)"
            p1.yaxis.axis_label = "Acceleration (g)"
            p1.xaxis.axis_label = "Displacement (mm)"
            p1.yaxis.axis_label = "Acceleration (g)"
            tab1 = Panel(child=row(p1), title='Accel vs Disp')            
            
            legend2 = Legend(items = legend_set2, location=(0,0))
            legend2.click_policy = "mute"            
            p2.legend.orientation = "horizontal"
            p2.add_layout(legend2,'right')
            p2.xaxis.axis_label = "Time (msec)"
            p2.yaxis.axis_label = "Acceleration (g)"

            tab2 = Panel(child=row(p2), title='Accel vs Time')
            tabs = Tabs(tabs=[tab1,tab2])
            show(tabs)
            
        
                
             

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = LinearApp()
    form.show()
    app.exec_()
if __name__ == '__main__':
    main()