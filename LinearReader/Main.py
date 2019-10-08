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
        self.tableWidget.setColumnCount(4)        
        self.filterBox.addItems(filterlist)
        self.openFile.clicked.connect(self.browse_folder)
        self.graphbtn.clicked.connect(self.report)
#        self.export_2.clicked.connect(self.exportexcel)
        self.tableWidget.cellChanged.connect(self.titleUpdate)
        self.data_dict = {}

    def browse_folder(self):
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self,"Pick a Folder")        
        if self.directory:
            self.tableWidget.clear()
            self.test_list = []
            tempdict = {}
            group_list = []

            tempdict = fileRead(self.directory)
            # for key in tempdict:
            #     if key in self.data_dict.keys():
            #         self.data_dict[key] = tempdict[key]
            #         tempdict.pop(key,None)
            # self.data_dict.update(tempdict)
            self.data_dict.update(tempdict)
            for key in self.data_dict:
                if 'Title' not in self.data_dict[key].keys():
                    self.data_dict[key]['Title'] = key
                    self.test_list.append(self.data_dict[key]['Title'])
                else:
                    self.test_list.append(self.data_dict[key]['Title'])
            self.colorList = ['#000000' for x in range(len(self.test_list))]
            for i in range(len(self.test_list)):
                group_list.append(str(i+1))
            self.tableWidget.setRowCount(len(self.test_list))
            self.tableWidget.setHorizontalHeaderLabels(['Test Name','Group #','Line Color','Delete'])
            self.tableWidget.setVerticalHeaderLabels(self.data_dict.keys())
            i = 0
            for k in self.test_list:
                self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(k)))
                header = self.tableWidget.horizontalHeader()
                header.setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
                comboBox = QtWidgets.QComboBox()                                   
                comboBox.addItems(group_list)
                comboBox.setCurrentIndex(i)
                self.tableWidget.setCellWidget(i,1,comboBox) 
                self.btncolor = QtWidgets.QPushButton()
                self.btncolor.clicked.connect(self.clickedColor)
                self.btncolor.setStyleSheet("background-color: black")
                self.tableWidget.setCellWidget(i,2,self.btncolor)
                self.btnDel = QtWidgets.QPushButton()
                self.btnDel.clicked.connect(self.deleteData)
                self.btnDel.setText("Remove")
                self.tableWidget.setCellWidget(i,3,self.btnDel)
                i +=1
#Button function for selection color with color picker. 
    def clickedColor(self):
        button = QtWidgets.qApp.focusWidget()
        color = QtWidgets.QColorDialog.getColor()
        button.setStyleSheet("QWidget { background-color: %s}" % color.name())
        index = self.tableWidget.indexAt(button.pos())
        self.data_dict[self.tableWidget.item(index.row(),0).text()]['Color'] = color.name()
#Delete unwanted files from dictionary. (Not from folder)        
    def deleteData(self):
        button = QtWidgets.qApp.focusWidget()
        index = self.tableWidget.indexAt(button.pos())
        namedel = self.tableWidget.item(index.row(),0).text()
        self.data_dict.pop(namedel,None)
        self.tableWidget.removeRow(index.row())
    def titleUpdate(self,row):
        self.data_dict[self.tableWidget.verticalHeaderItem(row).text()]['Title'] = self.tableWidget.item(row, 0).text()

        
##Function for exporting data to Excel        
#    def exportexcel(self):
#        i = 0
#        savedirectory = QtWidgets.QFileDialog.getExistingDirectory(self,"Save Excel File")
#
#        for keys in self.data_dict:
#            self.data_dict[keys]['Acceleration']['Title'] = self.test_name[i]
#            i += 1
#        exportToexcel(self.data_dict,self.data,savedirectory,self.titlebox.text())
        
#Fucntion for graphing data                   
    def report(self):
        directory = QtWidgets.QFileDialog.getSaveFileName(self,"Select Where to Save")
        if directory:
            if self.data_dict:
                group_list = []
                bokehTabs = []
                avgDict = {}
                testName =[]
                testLen = len(self.data_dict.keys())
                for i in range(0,testLen):
                    self.data_dict[self.tableWidget.verticalHeaderItem(i).text()]['Title'] = self.tableWidget.item(i,0).text()
                    self.data_dict[self.tableWidget.verticalHeaderItem(i).text()]['Group'] = int(self.tableWidget.cellWidget(i,1).currentText())
                filtersize = self.filterBox.currentText()
                plotTitle = self.titlebox.text()
                for key in self.data_dict:
                    testName.append(key)
                for i in range(len(self.test_list)):
                    group_list.append(self.tableWidget.cellWidget(i,1).currentText())

                if filtersize != 'Raw':
                    for key in self.data_dict:
                        self.data_dict[key]['Acceleration']['RawYData'] = filterProcessing(self.data_dict[key]['Acceleration']['RawYData'],int(filtersize),self.data_dict[key]['Acceleration']['Sample Rate'])
#                else:
#                    for key in self.data_dict:
#                        self.data_dict[key]['Acceleration']['YData'] = self.data_dict[key]['Acceleration']['RawYData']
                output_file(directory[0]+'.html')
# =============================================================================
# If user checks acceleration vs displacement
                if self.accelvdisp.isChecked():
                    avd = figure(width = 1200, height = 600, title = plotTitle)
                    avdLegend = []
                    for key in self.data_dict:
                        accelvdisp = avd.line(self.data_dict[key]['Displacement']['RawYData'],self.data_dict[key]['Acceleration']['RawYData'],line_color = self.data_dict[key]['Color'],line_width = 4, alpha = 1, muted_color = self.data_dict[key]['Color'],muted_alpha = 0)
                        avdLegend.append((self.data_dict[key]['Title'],[accelvdisp]))
                    avdLegend = Legend(items = avdLegend, location=(0,0))
                    avdLegend.click_policy = "mute"
                    avd.add_layout(avdLegend,'right')
                    avd.legend.orientation = "vertical"
                    avd.legend.padding = 1
                    avd.xaxis.axis_label = "Displacement (mm)"
                    avd.yaxis.axis_label = "Acceleration (g's)"
                    avdTab = Panel(child=avd, title="Acceleration vs. Displacement")
                    bokehTabs.append(avdTab)
# =============================================================================                    
# =============================================================================
# If user has checked Acceleration vs. Time Box
                if self.accelvtime.isChecked():
                    avt = figure(width = 1200, height = 600, title = plotTitle)
                    avtLegend = []
                    for key in self.data_dict:
                        accelvtime = avt.line(self.data_dict[key]['Acceleration']['XData'],self.data_dict[key]['Acceleration']['RawYData'],line_color = self.data_dict[key]['Color'],line_width = 4, alpha = 1, muted_color = self.data_dict[key]['Color'],muted_alpha = 0)
                        avtLegend.append((self.data_dict[key]['Title'],[accelvtime]))
                    avtLegend = Legend(items = avtLegend, location=(0,0))
                    avtLegend.click_policy = "mute"
                    avt.add_layout(avtLegend,'right')
                    avt.legend.orientation = "vertical"
                    avt.legend.padding = 1
                    avt.xaxis.axis_label = "Time (mSec)"
                    avt.yaxis.axis_label = "Acceleration (g's)"
                    avtTab = Panel(child=avt, title="Acceleration vs. Time")
                    bokehTabs.append(avtTab)                    
# =============================================================================
# =============================================================================
# If User had checked Average box

# =============================================================================
# =============================================================================
# If User has checked Current Box
                if self.current.isChecked():
                    cur = figure(width = 1200, height = 600, title = plotTitle)
                    curLegend = []
                    for key in self.data_dict:
                        current = cur.line(self.data_dict[key]['Current']['XData'],self.data_dict[key]['Current']['RawYData'],line_color = self.data_dict[key]['Color'],line_width = 4, alpha = 1, muted_color = self.data_dict[key]['Color'],muted_alpha = 0)
                        curLegend.append((self.data_dict[key]['Title'],[current]))
                    curLegend = Legend(items = curLegend, location=(0,0))
                    curLegend.click_policy = "mute"
                    cur.add_layout(curLegend,'right')
                    cur.legend.orientation = "vertical"
                    cur.legend.padding = 1
                    cur.xaxis.axis_label = "Time (mSec)"
                    cur.yaxis.axis_label = "Current (A)"
                    curTab = Panel(child=cur, title="Current vs. Time")
                    bokehTabs.append(curTab)                      
# =============================================================================                
# =============================================================================
# If User has checked Voltage Box
                if self.voltage.isChecked():
                    vol = figure(width = 1200, height = 600, title = plotTitle)
                    volLegend = []
                    for key in self.data_dict:
                        voltage = vol.line(self.data_dict[key]['Voltage']['XData'],self.data_dict[key]['Voltage']['RawYData'],line_color = self.data_dict[key]['Color'],line_width = 4, alpha = 1, muted_color = self.data_dict[key]['Color'],muted_alpha = 0)
                        volLegend.append((self.data_dict[key]['Title'],[voltage]))
                    volLegend = Legend(items = volLegend, location=(0,0))
                    volLegend.click_policy = "mute"
                    vol.add_layout(volLegend,'right')
                    vol.legend.orientation = "vertical"
                    vol.legend.padding = 1
                    vol.xaxis.axis_label = "Time (mSec)"
                    vol.yaxis.axis_label = "Voltage (V)"
                    volTab = Panel(child=vol, title="Voltage vs. Time")
                    bokehTabs.append(volTab)
# =============================================================================
                if self.average.isChecked():
                    avgDict = {}
                    for key in self.data_dict:
                        if self.data_dict[key]['Group'] in avgDict:
                          avgDict[self.data_dict[key]['Group']]['AverageDisp'].append(self.data_dict[key]['Displacement']['RawYData'])
                          avgDict[self.data_dict[key]['Group']]['AverageAccel'].append(self.data_dict[key]['Acceleration']['RawYData'])
                          avgDict[self.data_dict[key]['Group']]['AverageTime'].append(self.data_dict[key]['Acceleration']['XData'])
                        else:
                          avgDict[self.data_dict[key]['Group']] = {}
                          avgDict[self.data_dict[key]['Group']]['AverageDisp'] = []
                          avgDict[self.data_dict[key]['Group']]['AverageAccel'] = []
                          avgDict[self.data_dict[key]['Group']]['AverageTime'] = []
                          avgDict[self.data_dict[key]['Group']]['Title'] = self.data_dict[key]['Title']
                          avgDict[self.data_dict[key]['Group']]['Color'] = self.data_dict[key]['Color']
                          avgDict[self.data_dict[key]['Group']]['AverageDisp'].append(self.data_dict[key]['Displacement']['XData'])
                          avgDict[self.data_dict[key]['Group']]['AverageAccel'].append(self.data_dict[key]['Acceleration']['RawYData'])
                          avgDict[self.data_dict[key]['Group']]['AverageTime'].append(self.data_dict[key]['Acceleration']['XData'])
                          avgDict[self.data_dict[key]['Group']]['Points'] = self.data_dict[key]['Acceleration']['NumofPoints']
                    avgsumd = 0
                    avgsuma = 0
                    avgsumt = 0
                    for key in avgDict:
                        avgDict[key]['avgDisp'] = []
                        avgDict[key]['avgAccel'] = []
                        avgDict[key]['avgTime'] = []
                        for i in range(avgDict[key]['Points']):
                            for avdispist in avgDict[key]['AverageDisp']:
                                avgsumd += avdispist[i]
                            for avaccist in avgDict[key]['AverageAccel']:
                                avgsuma += avaccist[i]
                            for avtimist in avgDict[key]['AverageTime']:
                                avgsumt += avtimist[i]
                            avgd = avgsumd/len(avgDict[key]['AverageDisp'])
                            avga = avgsuma/len(avgDict[key]['AverageAccel'])
                            avgt = avgsumt/len(avgDict[key]['AverageTime'])
                            avgDict[key]['avgDisp'].append(avgd)
                            avgDict[key]['avgAccel'].append(avga)
                            avgDict[key]['avgTime'].append(avgt)
                            avgsumd = 0
                            avgsuma = 0
                            avgsumt = 0

                    avgavd = figure(width = 1200, height = 600, title = 'Average Acceleration vs. Displacement')
                    avgavt = figure(width = 1200, height = 600, title = 'Average Acceleration vs. Time')
                    legendAVT = []
                    legendAVD = []
                    for key in avgDict:
                         a = avgavt.line(avgDict[key]['avgTime'],avgDict[key]['avgAccel'],line_color = avgDict[key]['Color'], line_width = 4, alpha = 1, muted_color = avgDict[key]['Color'],muted_alpha=0)
                         b = avgavd.line(avgDict[key]['avgDisp'],avgDict[key]['avgAccel'],line_color = avgDict[key]['Color'], line_width = 4, alpha = 1, muted_color = avgDict[key]['Color'],muted_alpha=0)
                         legendAVT.append((avgDict[key]['Title'],[a]))
                         legendAVD.append((avgDict[key]['Title'],[b]))
                    Tlegend = Legend(items = legendAVT, location=(0,0))
                    Tlegend.click_policy = "mute"
                    avgavt.add_layout(Tlegend,'right')   
                    avgavt.legend.orientation = "vertical"
                    avgavt.legend.padding = 1
                    avgavt.xaxis.axis_label = "Time (mSec)"
                    avgavt.yaxis.axis_label = "Acceleration (g's)"
                    avgTTab =  Panel(child=avgavt, title='Average Acceleration vs. Time')
                    bokehTabs.append(avgTTab)
                    
                    Dlegend = Legend(items = legendAVD, location=(0,0))
                    Dlegend.click_policy = "mute"
                    avgavd.add_layout(Dlegend,'right')   
                    avgavd.legend.orientation = "vertical"
                    avgavd.legend.padding = 1
                    avgavd.xaxis.axis_label = "Displacement (mm)"
                    avgavd.yaxis.axis_label = "Acceleration (g's)"
                    avgDTab =  Panel(child=avgavd, title='Average Acceleration vs. Displacement')
                    bokehTabs.append(avgDTab)
                    
# =============================================================================
# If user selects data table
                if self.dataTable.isChecked():                    
                    test_list = []
                    accel_list = []
                    disp_list = []
                    time_list = []
        
                    #Check to make sure sample rate are the same between all tests, if they are
                    #Create a variable for the sample rate of the build sheet.
                    for key in self.data_dict:
                        test_list.append(key)
                        accel_list.append((self.data_dict[key]['Acceleration']['RawYData']))
                        disp_list.append((self.data_dict[key]['Displacement']['RawYData']))
                        time_list.append((self.data_dict[key]['Acceleration']['XData']))
                    maxAccel, maxDisp, contTime = tableCalc(accel_list,disp_list,time_list)           
                    self.data = dict(testnum = testName,                                               
                        max_accel = maxAccel,
                        max_displacment = maxDisp,
                        contact_time = contTime)
                    source = ColumnDataSource(self.data)
                    
                    columns = [TableColumn(field= "testnum", title="Test Name"),
                               TableColumn(field= "max_accel" ,title="Maximum Acceleration"),
                               TableColumn(field= "max_displacment",title = "Maximum Dipslacement"),
                               TableColumn(field = "contact_time" ,title = "Contact Time @ 2g's")]
                    data_table = DataTable(source = source, columns = columns, width = 700, height = 300) 
                    datatab = Panel(child=data_table, title= plotTitle + ' Data Table')  
                    bokehTabs.append(datatab)
# =============================================================================
                tabs = Tabs(tabs = bokehTabs)
                show(tabs)
                
                
def main():
    app = QtWidgets.QApplication(sys.argv)
    form = LinearApp()
    form.show()
    app.exec_()
if __name__ == '__main__':
    main()