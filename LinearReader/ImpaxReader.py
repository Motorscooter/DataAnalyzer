# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 12:13:16 2018

@author: scott.downard
"""
from LinearReader import *

from tkinter import *
#from tkinter import tkk
import tkinter.filedialog as tk

import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, show
import pyqtgraph as pg
root = Tk()
root.withdraw()
directory = tk.askdirectory()

filterlist = ['Raw','60','180']
color_list = ['black','red','blue','green','purple','grey','orange',
              'yellow','dark green','magenta']

                    

final_data = fileRead(directory)
test_list = []
accel_list = []
disp_list = []
time_list = []
#Check to make sure sample rate are the same between all tests, if they are
#Create a variable for the sample rate of the build sheet.
for key in final_data:
    test_list.append(key)
    accel_list.append(final_data[key]['Acceleration']['Data'])
    disp_list.append(final_data[key]['Displacement']['Data'])
    time_list.append(final_data[key]['Acceleration']['Time'])
    
sampleRate = final_data[test_list[0]]['Acceleration']['Sample Rate']
for key in final_data:
    newsampleRate = final_data[key]['Acceleration']['Sample Rate']
    if sampleRate is not newsampleRate:
        break

######Create a data frame to better analyze and visualize data points
accel_df = pd.DataFrame(accel_list,index = [test_list])
disp_df = pd.DataFrame(disp_list,index = [test_list])
time_df = pd.DataFrame(time_list,index = [test_list])
#filtered_df = pd.DataFrame(filterProcessing(accel_df,180,))

    





