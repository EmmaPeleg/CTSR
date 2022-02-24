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

## Creates empty array for rows to be parsed from DPV data
data_rows_array = np.array(['X','Y','Speed','Temperature','Diameter','EnergyA','EnergyB'])
## empty array for dates in data
dates=[]
## empty array for timestamps in data
time=[]

## iterates through data, saving dates and timestamps
for row in data:
    new_row = row.split()
    dates.append(new_row[0])
    time.append(new_row[1])
        
#new_row_floats=np.array([])

#iterate over the data once again, removing the time and date, and then converting
    ## the data into floats to be added to an array
for row in data:
    new_row_floats=[]  ## empty array for new row of floats
    new_row = row.split() ## splits array by spaces
    new_row.pop(0) ## removes date
    new_row.pop(0) ## removes time
    for i in new_row:
       floater=float(i) ## takes each element in the row and converts to a float
       new_row_floats.append(floater) ## apends new row of floats to a data array
       
    new_row_floats_arr=np.array(new_row_floats)
    data_rows_array = np.vstack((data_rows_array,new_row_floats_arr))

data_rows_array = np.delete(data_rows_array, (0), axis=0)
 
df_data = pd.DataFrame(data_rows_array) 

df=df_data.rename(columns={0: "X", 1: "Y", 2: "Velocity", 3: "Temperature", 4: "Diameter", 5: "Energy A", 6: "Energy B"})
df.insert(0,"Time",time)
df.insert(0,"Date",dates)

## INPUT VARIABELS NEEDED

k = 138 ## for Mo at 20C (>?????)
hf = hf = 36/95.95*1000*1000 ## heat fusion for Mo in J/kg
density = 10.22 ## density for Mo
Tm = 2623 ## melting temperature for Mo
#biotNumber = 30000*(0.5*All_Diameters*(10^-6))/k



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

All_Temps = []
for i in df["Temperature"]:
    All_Temps.append(float(i))

Temp_Array=np.array(All_Temps)

All_Vel = []
for i in df["Velocity"]:
    All_Vel.append(float(i))
Velocity_Array=np.array(All_Vel)


All_Diameters = []
for i in df["Diameter"]:
    All_Diameters.append(float(i))
Diameter_Array=np.array(All_Diameters)
   
    

fig, axs = plt.subplots(3,1,figsize=(3,6))


axs[0].hist(Temp_Array,20)
axs[0].set_title('Temperature (C)')

axs[1].hist(Velocity_Array,20)
axs[1].set_title('Velocity (m/s)')
axs[2].hist(Diameter_Array,20)
axs[2].set_title('Diameters (um)')
plt.tight_layout()

for ax in axs.flat:
    ax.set(ylabel='Count')

## might be nice to add x labels too but they're the same as titles so>>>?

    

""" 

make histograms for each important variable, then make histograms for MI and OI?

not really sure but then using the data we get we can say anything above MI=1 (?) is someting?


"""

# for files in os.listdir(path_of_the_directory):
#     if files.endswith(ext):
#         print(files)
#     else:
#         continue
          


