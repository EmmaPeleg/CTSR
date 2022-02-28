# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 15:44:38 2022

@author: Emma Peleg
"""
#accuraspray data, fast!

""" 
***seeing if this works with git

This super cool program will ask you for the path (file location) of the folder containing your 
accuraspray files

It is intended to take in raw - unedited data directly from accuraspray, make sure to use raw data only

It will prompt the user to input a standoff distance (in) for each run/measurement, this is simply a float
i.e. the number 16 (nothing else, not parenthesis, quotes, or units)

Any questions ask emma.peleg@stonybrook.edu
"""

import csv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#path_of_the_directory = r'C:\Users\Emma Peleg\Desktop\CTSR\programming'

path_of_the_directory = input("Paste the path for the folder containing the desired Accuraspray files:\n" )
ext = ".csv"

for files in os.listdir(path_of_the_directory):
    if files.endswith(ext):
        
        csv_name = files
    
        run_number = "Final Data_" + files 
#csv_name = "checking.csv" ###you can use this to input the file name manually
        standoff = float(input("what is the standoff distance? for run #:" + files + "\n"))

        old_df=pd.read_csv(csv_name ,skiprows=70) #read in the data in csv to dataframe

#new = old[['A','C','D']] is the convention here

        df=old_df[["Temperature (C)","Velocity (m/s)","Intensity (a.u.)","Plume Density (a.u.)","Plume Width (mm)","Plume Deviation (mm)","Plume Angle (deg)"]]

#Temp
        temp_col=df["Temperature (C)"].to_numpy() #convert to array for python ease
        mean_temp = temp_col.mean()

#velocity
        vel_col=df["Velocity (m/s)"].to_numpy() #convert to array for python ease
        mean_velocity = vel_col.mean()

#plume intensity
        intensity_col=df["Intensity (a.u.)"].to_numpy() #convert to array for python ease
        mean_intensity = intensity_col.mean()

#plume density
        density_col=df["Plume Density (a.u.)"].to_numpy() #convert to array for python ease
        mean_density = density_col.mean()

#plume width
        width_col=df["Plume Width (mm)"].to_numpy() #convert to array for python ease
        mean_width = width_col.mean()

#plume deviation
        dev_col=df["Plume Deviation (mm)"].to_numpy() #convert to array for python ease
        mean_dev = dev_col.mean()

#plume angle
        angle_col=df["Plume Angle (deg)"].to_numpy() #convert to array for python ease
        mean_angle = angle_col.mean()

        df_final = pd.DataFrame()
        titles = ["Temperature","Velocity (m/s)","Plume Intensity","Plume Density","Plume Width","Plume Deviation","Plume Angle","Standoff"]
        add_values = [mean_temp, mean_velocity, mean_intensity, mean_density, mean_width, mean_dev, mean_angle, standoff]

        df_last_row=df.iloc[-1]
        last_row=df_last_row.to_numpy()
        last_row=np.append(last_row,standoff)

        df_final["Measurement"]=titles
        df_final["Average Value"]=add_values
        df_final["Final Values"]=last_row #the last row of all of the values

        df_final.to_csv(run_number + ".csv")





