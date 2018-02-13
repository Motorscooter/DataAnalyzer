# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainwindow(object):
    def setupUi(self, mainwindow):
        mainwindow.setObjectName("mainwindow")
        mainwindow.resize(509, 378)
        self.centralwidget = QtWidgets.QWidget(mainwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.openFile = QtWidgets.QPushButton(self.centralwidget)
        self.openFile.setObjectName("openFile")
        self.verticalLayout.addWidget(self.openFile)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.titlebox = QtWidgets.QLineEdit(self.centralwidget)
        self.titlebox.setObjectName("titlebox")
        self.verticalLayout.addWidget(self.titlebox)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setAutoScroll(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.filterBox = QtWidgets.QComboBox(self.centralwidget)
        self.filterBox.setObjectName("filterBox")
        self.verticalLayout.addWidget(self.filterBox)
        self.graphbtn = QtWidgets.QPushButton(self.centralwidget)
        self.graphbtn.setObjectName("graphbtn")
        self.verticalLayout.addWidget(self.graphbtn)
        self.export_2 = QtWidgets.QPushButton(self.centralwidget)
        self.export_2.setObjectName("export_2")
        self.verticalLayout.addWidget(self.export_2)
        mainwindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainwindow)
        self.statusbar.setObjectName("statusbar")
        mainwindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainwindow)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        mainwindow.setWindowTitle(_translate("mainwindow", "Test Bay Analyzer"))
        self.openFile.setText(_translate("mainwindow", "Select Directory"))
        self.label_2.setText(_translate("mainwindow", "Title"))
        self.label.setText(_translate("mainwindow", "Filtering"))
        self.graphbtn.setText(_translate("mainwindow", "Graph"))
        self.export_2.setText(_translate("mainwindow", "Export to Excel"))

