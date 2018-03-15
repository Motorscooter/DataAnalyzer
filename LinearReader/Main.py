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
from bokeh.models import Legend, ColumnDataSource
from bokeh.models.widgets import Panel, Tabs, DataTable, TableColumn
import bokeh.io as bk
import bokeh.plotting
#Object that runs GUI.
class LinearApp(QtWidgets.QMainWindow, Mainwindow.Ui_mainwindow):

#Initialize widgets.    
    def __init__(self,parent=None):
        filterlist = ['Raw','60','180']
        super(LinearApp, self).__init__(parent)
        self.setupUi(self)
        self.tableWidget.setColumnCount(3)        
        self.filterBox.addItems(filterlist)
        self.openFile.clicked.connect(self.browse_folder)
        self.graphbtn.clicked.connect(self.graph)
        self.export_2.clicked.connect(self.exportexcel)
        self.data_dict = {}        
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
            self.colorList = ['#000000' for x in range(len(self.test_list))]
            for i in range(len(self.test_list)):
                group_list.append(str(i+1))
            self.tableWidget.setRowCount(len(self.test_list))
            self.tableWidget.setHorizontalHeaderLabels(['Test Name','Group #','Line Color'])
            i = 0         
            for k in self.test_list:
                self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem("Test_"+str(k))) 
                comboBox = QtWidgets.QComboBox()                                   
                comboBox.addItems(group_list)
                comboBox.setCurrentIndex(i)
                self.tableWidget.setCellWidget(i,1,comboBox) 
                self.btncolor = QtWidgets.QPushButton()
                self.btncolor.clicked.connect(self.clickedColor)
                self.btncolor.setStyleSheet("background-color: black")
                self.tableWidget.setCellWidget(i,2,self.btncolor)
                i +=1
#Button function for selection color with color picker. 
    def clickedColor(self):
        button = QtWidgets.qApp.focusWidget()
        color = QtWidgets.QColorDialog.getColor()
        button.setStyleSheet("QWidget { background-color: %s}" % color.name())
        index = self.tableWidget.indexAt(button.pos())
        self.colorList[index.row()] = color.name()

#Function for exporting data to Excel        
    def exportexcel(self):
        i = 0
        savedirectory = QtWidgets.QFileDialog.getExistingDirectory(self,"Save Excel File")
        for keys in self.data_dict:
            self.data_dict[keys]['Acceleration']['Title'] = self.test_name[i]
            i += 1
        exportToexcel(self.data_dict,self.data,savedirectory,self.titlebox.text())
        
#Fucntion for graphing data        
    def graph(self):
        if self.directory:
            
            group_list = []
            self.test_name = []
            filtersize = self.filterBox.currentText()
            plotTitle = self.titlebox.text()
            
            for i in range(len(self.test_list)):
                self.test_name.append(self.tableWidget.item(i,0).text())
                group_list.append(self.tableWidget.cellWidget(i,1).currentText())
            self.final_data = {i:group_list.count(i) for i in group_list}
            for key in self.final_data:
                self.final_data[key] = {}

            for i in range(len(self.test_list)):
                if filtersize == 'Raw':
                    continue
                else:
                    self.data_dict[self.test_list[i]]['Acceleration']['Data'] =     filterProcessing(self.data_dict[self.test_list[i]]['Acceleration'][
                            'Data'],int(filtersize),self.data_dict[self.test_list[i]]['Acceleration']['Sample Rate'])
                          
            test_list = []
            accel_list = []
            disp_list = []
            time_list = []

            #Check to make sure sample rate are the same between all tests, if they are
            #Create a variable for the sample rate of the build sheet.
            for key in self.data_dict:
                test_list.append(key)
                accel_list.append((self.data_dict[key]['Acceleration']['Data']))
                disp_list.append((self.data_dict[key]['Displacement']['Data']))
                time_list.append((self.data_dict[key]['Acceleration']['Time']))
           
            maxAccel, maxDisp, contTime = tableCalc(accel_list,disp_list,time_list)
            output_file(plotTitle + '.html')
            p1 = figure(width = 1200, height = 600, title = plotTitle)
            p2 = figure(width = 1200, height = 600, title = plotTitle)
            legend_set1 = []
            legend_set2 = []
            
            for i in range(len(accel_list)):
                a = p1.line(disp_list[i],accel_list[i],line_color = self.colorList[i], line_width = 4, alpha = 1, muted_color = self.colorList[i],muted_alpha=0)
                b = p2.line(time_list[i],accel_list[i],line_color = self.colorList[i], line_width = 5, alpha = 1, muted_color = self.colorList[i],muted_alpha=0)
                legend_set1.append((self.test_name[i],[a]))
                legend_set2.append((self.test_name[i],[b]))
                
            legend1 = Legend(items = legend_set1, location=(0,0))
            legend1.click_policy = "mute"
            p1.add_layout(legend1,'right')   
            p1.legend.orientation = "vertical"
            p1.legend.padding = 1
            p1.xaxis.axis_label = "Displacement (mm)"
            p1.yaxis.axis_label = "Acceleration (g)"
            p1.xaxis.axis_label = "Displacement (mm)"
            p1.yaxis.axis_label = "Acceleration (g)"

            tab1 = Panel(child=p1, title='Accel vs Disp')            
            
            legend2 = Legend(items = legend_set2, location=(0,0))
            legend2.click_policy = "mute"            
            p2.legend.orientation = "vertical"
            p2.add_layout(legend2,'right')
            p2.legend.padding = 1
            p2.xaxis.axis_label = "Time (msec)"
            p2.yaxis.axis_label = "Acceleration (g)"    
            tab2 = Panel(child=p2, title='Accel vs Time')  


            self.data = dict(testnum = self.test_name,
                        max_accel = maxAccel,
                        max_displacment = maxDisp,
                        contact_time = contTime)
            source = ColumnDataSource(self.data)
            
            columns = [TableColumn(field= "testnum", title="Test Name"),
                       TableColumn(field= "max_accel" ,title="Maximum Acceleration"),
                       TableColumn(field= "max_displacment",title = "Maximum Dipslacement"),
                       TableColumn(field = "contact_time" ,title = "Contact Time @ 2g's")]
            data_table = DataTable(source = source, columns = columns, width = 700, height = 300) 
            tab3 = Panel(child=data_table, title= plotTitle + ' Data Table')                   
            tabs = Tabs(tabs=[tab1,tab2,tab3])
            show(tabs)
                                                
def main():
    app = QtWidgets.QApplication(sys.argv)
    form = LinearApp()
    form.show()
    app.exec_()
if __name__ == '__main__':
    main()