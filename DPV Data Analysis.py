# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 14:03:36 2022

@author: Emma Peleg

This program runs DPV histogram data and procecess it

Maybe it will look at the melting Index? Maybe not
"""
import csv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#path_of_the_directory = input("Paste the path for the folder containing the desired Accuraspray files:\n" )
path_of_the_directory = r"C:\Users\Emma Peleg\Desktop\CTSR\Mo-Study\DPV-Mo Powders\DPV Files for DAQ"
ext = ".prt"

data_open = open("SA110_Center_60_CG3.5.prt","r")
data = data_open.readlines()[1:]


data_rows_array = np.array(['X','Y','Speed','Temperature','Diameter','EnergyA','EnergyB'])
dates=[]
time=[]
for row in data:
    new_row = row.split()
    dates.append(new_row[0])
    time.append(new_row[1])
        
#new_row_floats=np.array([])

for row in data:
    new_row_floats=[]
    new_row = row.split()
    new_row.pop(0)
    new_row.pop(0)
    for i in new_row:
       floater=float(i)
       new_row_floats.append(floater)
       
    new_row_floats_arr=np.array(new_row_floats)
    #print(new_row_floats_arr)
    data_rows_array = np.vstack((data_rows_array,new_row_floats_arr))
    
        
        
# for row in data:
#     new_row = row.split()
#     new_row_arr = np.array(new_row)
#     data_rows_array = np.vstack((data_rows_array,new_row_arr))
    

# for row in data_arr:
#     #print(row)
#     new_row=np.char.split(row)
#     data_rows_array = np.hstack((data_rows_array,new_row))
#     #data_rows_array=np.append(data_rows_array,new_row,axis=0)


#df=pd.DataFrame(data_rows_array,columns=['Date','Time','X','Y','Speed','Temperature','Diameter','EnergyA','EnergyB'])                

#split_df = pd.read_excel("data_convert.xlsx")


# for files in os.listdir(path_of_the_directory):
#     if files.endswith(ext):
#         print(files)
#     else:
#         continue
          
""" extra shit """
# for index, row in df_data.iterrows():
#     print(row)


