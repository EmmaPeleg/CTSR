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
from math import pi
import hdbscan

#path_of_the_directory = input("Paste the path for the folder containing the desired Accuraspray files:\n" )
path_of_the_directory = r"C:\Users\Emma Peleg\Desktop\CTSR\Mo-Study\DPV-Mo Powders\DPV Files for DAQ"
ext = ".prt"

# for files in os.listdir(path_of_the_directory):
#     if files.endswith(ext):
#         print(files)
#     else:
#         continue

w = pd.read_table('SA110_Center_60_CG3.5.prt', header=0, delimiter='\s+')
data_open = open("SA110_Center_60_CG3.5.prt","r")
data = data_open.readlines()[1:]
data=np.array(data)
## INPUT VARIABELS NEEDED

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

All_Temps = []      ##  list of all particle temperatures
for i in w["Temperature"]:
    All_Temps.append(float(i))

Temp_Array=np.array(All_Temps)+273.15 ## converting to Kelvin

All_Vel = []        ##  list of all velocities of particles
for i in w["Speed"]:
    All_Vel.append(float(i))
Velocity_Array=np.array(All_Vel)


All_Diameters = []  ## list of all particle diameters
for i in w["Diameter"]:
    All_Diameters.append(float(i))
Diameter_Array=np.array(All_Diameters)*(10**-6) #in meters!
   
##use df and pandas using hdbscan (doesnt work with dataframes) so use a np array
#labels clusters based on their values (-1 = statistical noise etc)
#sort by cluster that contained most points, sort high to low 
#use velocity or T,V,D for outliers

""" 

Doing the melting index, kinetic energy, and oxidation index calculations

"""

k = 138 ## thermal conductivity W/mK for Mo at 20C (>?????)
hf = 36/95.95*1000*1000 ## heat fusion for Mo in J/kg
density_cc = 9 ## g/cc
density = 9*(1000) ## density for Mo kg/m3
Tm = 2623 ## melting temperature for Mo
sprayDist = .15

h = [] ## convective coefficient
for i in Velocity_Array:
    h_app=0.0167*i**3 - 7.3956*i**2 + 1109.3*i - 43732
    h.append(h_app)
h = np.array(h)

biotNumber = h*(Diameter_Array)/k

t_fly = []
for i in Velocity_Array:
    t = (2*sprayDist)/i
    t_fly.append(t)

""" Melting Index formulas""" 
simpMI = Temp_Array*t_fly/Diameter_Array

MI = (24*k/(density*hf))*(1/(1+(4/biotNumber)))*(((Temp_Array-Tm)*(t_fly))/((Diameter_Array)**2))
low_Biot_MI = ((6*h)/(density*hf))*(1/(1+(4/biotNumber)))*(((Temp_Array-Tm)*(t_fly))/((Diameter_Array)**2))
""" Kinetic Energy """ 

Volume = (4/3)*pi*((.5*Diameter_Array)**3) ## cubic centim
Mass = Volume*density_cc
KE = 0.5*density*Volume*(Velocity_Array**2)*(10**6)
 

"""
Plotting the velocities, temperatures, and particle diameters
"""
   
fig, axs = plt.subplots(3,1,figsize=(6,6))

axs[0].hist(Temp_Array,20)
axs[0].set_title('Temperature (C)')

axs[1].hist(Velocity_Array,20)
axs[1].set_title('Velocity (m/s)')
axs[2].hist(Diameter_Array,20)
axs[2].set_title('Diameters (um)')
plt.tight_layout()


for ax in axs.flat:
    ax.set(ylabel='Count')
  
""" 

Previous program code, saved for later use maybe?

"""
# data_open = open("SA110_Center_60_CG3.5.prt","r")
# data = data_open.readlines()[1:]

# ## Creates empty array for rows to be parsed from DPV data
# data_rows_array = np.array(['X','Y','Speed','Temperature','Diameter','EnergyA','EnergyB'])
# ## empty array for dates in data
# dates=[]
# ## empty array for timestamps in data
# time=[]
       
# ## iterates through data, saving dates and timestamps
# for row in data:
#     new_row = row.split()
#     dates.append(new_row[0])
#     time.append(new_row[1])
        
# #new_row_floats=np.array([])

# #iterate over the data once again, removing the time and date, and then converting
#     ## the data into floats to be added to an array
# for row in data:
#     new_row_floats=[]  ## empty array for new row of floats
#     new_row = row.split() ## splits array by spaces
#     new_row.pop(0) ## removes date
#     new_row.pop(0) ## removes time
#     for i in new_row:
#        floater=float(i) ## takes each element in the row and converts to a float
#        new_row_floats.append(floater) ## apends new row of floats to a data array
       
#     new_row_floats_arr=np.array(new_row_floats)
#     data_rows_array = np.vstack((data_rows_array,new_row_floats_arr))

# data_rows_array = np.delete(data_rows_array, (0), axis=0)
 
# df_data = pd.DataFrame(data_rows_array) 

# df=df_data.rename(columns={0: "X", 1: "Y", 2: "Velocity", 3: "Temperature", 4: "Diameter", 5: "Energy A", 6: "Energy B"})
# df.insert(0,"Time",time)
# df.insert(0,"Date",dates)

