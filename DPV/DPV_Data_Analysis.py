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
from scipy import stats

    ## this program can be used to analyze multiple files in multiple folders by inputting the path for the main containing folder
    ##i.e. put all of your DPV folders with data in one larger folder and run the program in the path of the larger folder
path_of_the_directory = input("Paste the path for the folder containing the desired DPV files :\n" )
ext = ".prt"

os.chdir(path_of_the_directory)

for root, dirs, files in os.walk(path_of_the_directory):
    for title in files:
        if title.endswith(".prt"):
            os.chdir(root) ##changes directory to working one each loop
            setname=title[0:-4]
            w = pd.read_table(title, header=0, delimiter='\s+')
            data_df = w[["Speed","Temperature"]].copy()
            
            ##diameter fixing using modal diameter from PSA
            EnergyB = np.array(w["EnergyB"])
            Old_Diameters = np.array(w["Diameter"])
            PSA_Diameter_mode = int(input("Enter modal diameter from PSA analysis: \n")) ## um
            Full_Temp = np.array(w["Temperature"])
            DC = (Old_Diameters)/(np.sqrt(EnergyB/Full_Temp**4))
            DC_mode = stats.mode(DC)[0]
            Old_D_mode=stats.mode(Old_Diameters)[0]
            New_DC=DC_mode*(PSA_Diameter_mode/Old_D_mode)
            Real_Diameters = New_DC*(np.sqrt(EnergyB/Full_Temp**4))
            
            data_df["Diameter"]=Real_Diameters ## adding fixed diameters
            data=np.array(data_df) ## data for speed temp diameter as array for hdbscan
            
            ## INPUT VARIABLES NEEDED
            
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
            
            """ 
            Do an outlier removal using hdbscan:
            """
            
            clusterer = hdbscan.HDBSCAN()
            
            fit=clusterer.fit(data_df)
            
            cluster_labels = clusterer.labels_
            min_cluster = clusterer.labels_.min()
            max_cluster = clusterer.labels_.max()
            cluster_prob = clusterer.probabilities_
            cluster_out = clusterer.outlier_scores_
            
            #sns.displot(clusterer.outlier_scores_[np.isfinite(clusterer.outlier_scores_)], rug=True)
            
            threshold = pd.Series(clusterer.outlier_scores_).quantile(0.9)
            outliers = np.where(clusterer.outlier_scores_ > threshold)[0]
            #cluster labels are outliers
            
            cluster_list = []
            for i in cluster_labels:
                cluster_list.append(i)
            
            outlier_list= []
            for index,i in enumerate(cluster_labels):
                if i == -1:
                    outlier_list.append(index)
                    #print(index,i)
         #plot xyz with color as label
            
            outlier_array = []
            for i in outlier_list:
                out = data[i]
                outlier_array.append(out)
            
            data_index_list=list(range(0,len(data)))
                
            for element in outlier_list:
                if element in data_index_list:
                    data_index_list.remove(element)
            
            clean_data=[]
                    ## removing all of the outliers and saving in new array        
            for i in data_index_list:
                add_data=data[i]
                clean_data.append(add_data)   
            clean_data_df = pd.DataFrame(clean_data,columns=["Velocity","Temperature","Diameter"])
            
            """ 
            Make the arrays for the different values without outliers
            """
            
            All_Temps = []      ##  list of all particle temperatures
            for i in clean_data_df["Temperature"]:
                All_Temps.append(float(i))
            
            Temp_Array=np.array(All_Temps)+273.15 ## converting to Kelvin
            
            All_Vel = []        ##  list of all velocities of particles
            for i in clean_data_df["Velocity"]:
                All_Vel.append(float(i))
            Velocity_Array=np.array(All_Vel)
            
            All_Diameters = []  ## list of all particle diameters
            for i in clean_data_df["Diameter"]:
                All_Diameters.append(float(i))
            Diameter_Array=np.array(All_Diameters)*(10**-6) #in meters!
            #fix diameter scale coefficient bc particles r wrong!   
            
            
            ##use df and pandas using hdbscan (doesnt work with dataframes) so use a np array
            #labels clusters based on their values (-1 = statistical noise etc)
            #sort by cluster that contained most points, sort high to low 
            #use velocity or T,V,D for outliers
            """ 
            
            Doing the melting index, kinetic energy, and oxidation index calculations
            
            """
            
            k = 138 ## thermal conductivity W/mK for Mo at 20C (>?????) change for different powders
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
            #low_Biot_MI = ((6*h)/(density*hf))*(1/(1+(4/biotNumber)))*(((Temp_Array-Tm)*(t_fly))/((Diameter_Array)**2))
            
            """ Kinetic Energy """ 
            
            Volume = (4/3)*pi*((.5*Diameter_Array)**3) ## cubic centimeters
            KE = 0.5*density*Volume*(Velocity_Array**2) ## Joules
            Average_KE = np.mean(KE)*10**6 ## micro Joules
            Average_KE_str = f"{Average_KE:.2f}" 
            
            """ Oxidation Index"""
            
            # need oxygen concentration in gas phase 
            
            """
            Plotting the velocities, temperatures, and particle diameters, and MI
            """
            ## Sturges Rule Calculations
            N = len(clean_data)
            K = int(1 + 3.322*np.log(N))
            
            fig, axs = plt.subplots(3,1,figsize=(6,6))
            
            axs[0].hist(Temp_Array,K,facecolor='blue',edgecolor='black')
            #axs[0].set_title('Temperature (C)')
            #axs[0].set_xlim(2500,5000)
            mean_temperature = np.mean(All_Temps)
            axs[0].set_xlabel('Temperature (C)' + " (Mean = " + str(round(mean_temperature,2)) + ")", fontsize=13)

            axs[1].hist(Velocity_Array,K,facecolor='red',edgecolor='black')
            mean_velocity = np.mean(All_Vel)
            axs[1].set_xlabel("Velocity (m/s)" + " (Mean = " + str(round(mean_velocity,2)) + ")", fontsize=13)
            #axs[1].set_title('Velocity (m/s)')
            #axs[1].set_xlim(30,300)
           
        
        #from DPV_Run_All import setname
            
                ##change diameter unit
            D_array_um = np.array(All_Diameters)
            
            axs[2].hist(D_array_um,K,facecolor='green',edgecolor='black')
            mean_diameters = np.mean(All_Diameters)
            axs[2].set_xlabel('Diameters (um)' + " (Mean = " + str(round(mean_diameters,2)) + ")", fontsize=13)
            #axs[2].set_title('Diameters (um)')
            #axs[2].set_xlim(0,60)
            plt.suptitle(setname)
            plt.tight_layout()
            
            plt.savefig("TVD_"+ setname[0] + ".png")
            for ax in axs.flat:
                ax.set(ylabel='Count')
                       
            """ Melting Index Figure """
            
            
            MI_counts,MI_bins = np.histogram(MI,20)
            max_count_MI = max(MI_counts)-75
            middle_bin = np.mean(MI)-5
            
            ## find molten % of particles
            melt_threshold = 0
            melted_particles = [element for element in MI if element > melt_threshold]
            melted_number = len(melted_particles)
            molten_percent = len(melted_particles)/len(MI)*100
            molten_percent_str = f"{molten_percent:.2f}" 
            
            fig2, ax1 = plt.subplots(1,1,figsize=(6,5))
            
            ax1=plt.hist(MI,K,facecolor='grey',edgecolor='black')
            #plt.title("Melting Index")
            plt.ylabel("Count")
            plt.xlabel("Melting Index" + ' (Molten Content '+ molten_percent_str +"%)")
            plt.axvline(x=0,ymin=0,color='black',linestyle='dotted',linewidth=3)
            plt.tight_layout()
            #plt.xlim(-5,5)
            plt.suptitle(setname)
            plt.tight_layout()
            plt.savefig("MI_"+ setname[0] + ".png")
            #plt.close()
            
            """ Kinetic Energy Figure """
            KE_counts,KE_bins = np.histogram(KE*10**6,20)
            max_count_KE = max(KE_counts)-10
            middle_bin_KE = np.mean(KE*10**6)+.5
            fig3, ax1 = plt.subplots(1,1,figsize=(6,5))
            
            ax1=plt.hist(KE*10**6,K,facecolor='grey',edgecolor='black')
            #plt.title("Melting Index")
            plt.ylabel("Count")
            plt.xlabel("Kinetic Energy [uJ]" + ' (Average KE '+ Average_KE_str +"uJ)")
            plt.tight_layout()
            x_max = 4.5*Average_KE
            #plt.text(middle_bin_KE,max_count_KE,'Average KE '+ Average_KE_str +"uJ",rotation=0)
            #plt.xlim(0,x_max)
            plt.suptitle(setname)
            plt.tight_layout()
            plt.savefig("KE_"+ setname[0] + ".png")
            
    
  
