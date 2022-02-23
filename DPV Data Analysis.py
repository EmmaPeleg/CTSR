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
    data_rows_array = np.vstack((data_rows_array,new_row_floats_arr))

data_rows_array = np.delete(data_rows_array, (0), axis=0)
 
df_data = pd.DataFrame(data_rows_array) 

df=df_data.rename(columns={0: "X", 1: "Y", 2: "Speed", 3: "Temperature", 4: "Diameter", 5: "Energy A", 6: "Energy B"})
df.insert(0,"Time",time)
df.insert(0,"Date",dates)

"""the official dataframe of the data from the DPV *.prt file is saved as df

Proceed to do more stuff
temp = temperature [C]
vel = velocity [m/s]
diam = diameter [um]
tMelt = melting temperature [C]
den = density [kg/m^3]  (1 g/cc = 1000 kg/m^3)
k = thermal conductivity [W/mK]
hf = heat of fusion [J/kg]
h = heat transfer coefficient [W/m^2K]
D = particle size [m]
rp = radius of particle [m] ??

            k = obj.thermalConductivity;
            hf = obj.heatOfFusion;
            
            biotNumber = 30000*(0.5*diam*(10^-6))/k;
            
            MI = 3.3*(12*k*(temp-tMelt)*(sprayDist*(10^-3)))./(den*hf*(1+2./biotNumber).*((.5*diam*(10^-6)).^2).*vel);
            
            %CALCULATE KE
            volume = (4/3)*pi*((0.5*diam).^3)*(10^(-18));
            KE = 0.5*den*volume.*(vel.^2) * 10^6;
            
"""



# for files in os.listdir(path_of_the_directory):
#     if files.endswith(ext):
#         print(files)
#     else:
#         continue
          


