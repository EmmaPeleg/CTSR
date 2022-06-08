# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:23:44 2022

@author: Emma Peleg
"""
import numpy as np
import os
import pandas as pd
import hdbscan
from tkinter.filedialog import askopenfilename as ask
from tkinter.filedialog import asksaveasfilename as ssn
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats
from math import pi
import itertools 
import matplotlib.gridspec as gridspec


path_of_the_directory = r"C:\Users\EmmaPeleg\Desktop\Sandia\Mo-DPV"
os.chdir(path_of_the_directory)

for root, dirs, files in os.walk(path_of_the_directory):
    print(files)
    for title in files:
        if title.endswith(".prt"):
            sample_name = title[0:-4]
            print(sample_name)
            os.chdir(root)
    ## open the classes and clustered 
            file = title
            df = pd.read_table(file, header=0, delimiter='\s+')
            filename = file[0:-5]
            
            
            """ CLustering with HDBSCAN"""
            
            x = df['Diameter']
            y = df['Speed']
            z = df['Temperature']
            X = np.array(list(zip(x,y,z)))
            
            agg = hdbscan.HDBSCAN(min_cluster_size=20).fit(X)
            
            df['Class'] = agg.labels_
            
            no_outlier = df[df['Class']!=-1]
            
            """
            Solving for real Diameters
             """
            
            EnergyB = np.array(no_outlier["EnergyB"])
            Old_Diameters = np.array(no_outlier["Diameter"])
            PSA_Diameter_mode = 28 ## um input from known mode
            Full_Temp = np.array(no_outlier["Temperature"])
            DC = (Old_Diameters)/(np.sqrt(EnergyB/Full_Temp**4))
            DC_mode = stats.mode(DC)[0]
            Old_D_mode=stats.mode(Old_Diameters)[0]
            New_DC=DC_mode*(PSA_Diameter_mode/Old_D_mode)
            Real_Diameters = New_DC*(np.sqrt(EnergyB/Full_Temp**4))
            
            no_outlier["Diameter"]=Real_Diameters ## adding fixed diameters
            
            
            
            diameters = np.array(no_outlier["Diameter"])
            sorted_diameters = sorted(diameters)
            sorted_df = no_outlier.sort_values("Diameter")
            
            index_25 = int(len(sorted_diameters)*.25)
            index_50 = int(len(sorted_diameters)*.50)
            index_75 = int(len(sorted_diameters)*.75)
            index_100 = int(len(sorted_diameters)*1)
            
            
            """ Dividing the dataframe into quartiles based on particle size """
            q25 = sorted_df[0:index_25]
            q50 = sorted_df[index_25:index_50]
            q75 = sorted_df[index_50:index_75]
            q100 = sorted_df[index_75:index_100]
            
            quartiles = [q25,q50,q75,q100]
            names = ["q25","q50","q75","q100"]
            
            quartile_dict = {"Temperature":[],"Velocity":[],"Diameters":[],"MI":[],"KE":[],"Middle Bin MI":[],"MI %":[],"Middle Bin KE":[],"Max Count KE":[],"Mean Temperature":[],"Mean Velocity":[],"Mean KE":[],"Mean Diameter":[]}
            
            for i,j in zip(quartiles,names):
                clean_data_df = i
                setname = j + "_" + filename
                    ##  sturges rule: need to update to something better
                N = len(i)
                K = int(1 + 3.322*np.log(N))
                #clean_data_df.index(i)
                """ 
                Make the arrays for the different values without outliers
                """
                
                All_Temps = []      ##  list of all particle temperatures
                for i in clean_data_df["Temperature"]:
                    All_Temps.append(float(i))
                
                Temp_Array=np.array(All_Temps)+273.15 ## converting to Kelvin
                mean_T = np.mean(Temp_Array)
                quartile_dict["Mean Temperature"].append([mean_T])
            
                
                All_Vel = []        ##  list of all velocities of particles
                for i in clean_data_df["Speed"]:
                    All_Vel.append(float(i))
                Velocity_Array=np.array(All_Vel)
                mean_V = np.mean(All_Vel)
                quartile_dict["Mean Velocity"].append([mean_V])
            
                All_Diameters = []  ## list of all particle diameters
                for i in clean_data_df["Diameter"]:
                    All_Diameters.append(float(i))
                Diameter_Array=np.array(All_Diameters)*(10**-6) #in meters!
                #fix diameter scale coefficient bc particles r wrong!   
                Mean_D = np.mean(Diameter_Array*10**6)
                quartile_dict["Mean Diameter"].append([Mean_D])
                
                quartile_dict["Temperature"].append([All_Temps])
                quartile_dict["Diameters"].append([All_Diameters])
                quartile_dict["Velocity"].append([All_Vel])
                
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
                #low_Biot_MI = ((6*h)/(density*hf))*(1/(1+(4/biotNumber)))*(((Temp_Array-Tm)*(t_fly))/((Diameter_Array)**2))
                
                quartile_dict["MI"].append([MI])
            
                """ Kinetic Energy """ 
                
                Volume = (4/3)*pi*((.5*Diameter_Array)**3) ## cubic centimeters
                KE = 0.5*density*Volume*(Velocity_Array**2) ## Joules
                Average_KE = np.mean(KE)*10**6 ## micro Joules
                Average_KE_str = f"{Average_KE:.2f}" 
                
                quartile_dict["KE"].append([KE])
                
                """
                Plotting the velocities, temperatures, and particle diameters, and MI
                """
                ## Sturges Rule Calculations
                
                # fig, axs = plt.subplots(3,1,figsize=(6,6))
                
                           
                # """ Melting Index Figure """
                
                MI_counts,MI_bins = np.histogram(MI,20)
                max_count_MI = max(MI_counts)-75
                middle_bin = np.mean(MI)-5
                quartile_dict["Middle Bin MI"].append([middle_bin])
                
                # ## find molten % of particles
                melt_threshold = 0
                melted_particles = [element for element in MI if element > melt_threshold]
                melted_number = len(melted_particles)
                molten_percent = len(melted_particles)/len(MI)*100
                molten_percent_str = f"{molten_percent:.2f}" 
                quartile_dict["MI %"].append([molten_percent])
                
                # """ Kinetic Energy Figure """
                KE_counts,KE_bins = np.histogram(KE*10**6,20)
                max_count_KE = max(KE_counts)-10
                middle_bin_KE = np.mean(KE*10**6)+.5
                mean_KE = np.mean(KE*10**6)
                quartile_dict["Max Count KE"].append([max_count_KE])
                quartile_dict["Middle Bin KE"].append([middle_bin_KE])
                quartile_dict["Mean KE"].append([mean_KE])
            
            
                final_fig = plt.figure(constrained_layout=True,figsize=(8,8))
                
                gs0 = gridspec.GridSpec(1, 2, figure=final_fig)
                   
                    ## lefthand figure (TVD)
                gs1 = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs0[0])
                ax = final_fig.add_subplot(gs1[0])
                plt.hist(Temp_Array,K,facecolor='blue',edgecolor='black')
                ax.set_title('Temperature (K)')
                plt.xlabel("Average Temperature = "+ str(round(mean_T)) + " (K)")
                
                ax = final_fig.add_subplot(gs1[1])
                plt.hist(Velocity_Array,K,facecolor='red',edgecolor='black')
                ax.set_title('Velocity (m/s)')
                plt.xlabel("Average Velocity = "+ str(round(mean_V)) + " (m/s)")
            
                ax = final_fig.add_subplot(gs1[2])
                D_array_um = np.array(All_Diameters)
                plt.hist(D_array_um,10,facecolor='green',edgecolor='black')
                ax.set_title('Diameters (um)')
                plt.xlabel("Average Diameter = "+ str(round(Mean_D)) + " (um)")
            
                
                    ## righthand figure MI/KE
                gs2 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[1])
                
                ax = final_fig.add_subplot(gs2[0])
                plt.hist(MI,K,facecolor='grey',edgecolor='black')
                plt.ylabel("Count")
                plt.xlabel("Melting Index, Molten Content = " + molten_percent_str +"%")
                #plt.text(0,max_count_MI,'Molten Content '+ molten_percent_str +"%",rotation=90)
                plt.axvline(x=0,ymin=0,color='black',linestyle='dotted',linewidth=3)
                
                
                ax=final_fig.add_subplot(gs2[1])
                plt.hist(KE*10**6,K,facecolor='grey',edgecolor='black')
                plt.ylabel("Count")
                plt.xlabel("Kinetic Energy [uJ], Average KE = " + Average_KE_str + "uJ")
                x_max = 4.5*Average_KE
                #plt.text(middle_bin_KE,max_count_KE,'Average KE '+ Average_KE_str +"uJ",rotation=0)
                #plt.xlim(0,x_max)
                plt.suptitle(setname)
                plt.show()
                
                ##collecting final datas
            Mean_KE_list = quartile_dict["Mean KE"]
            Mean_MI_list = quartile_dict["MI %"]
            Mean_T_list = quartile_dict["Mean Temperature"]
            Mean_V_list = quartile_dict["Mean Velocity"]
            Mean_D_list = quartile_dict["Mean Diameter"]
            
            final_means_dict = {"Mean KE":Mean_KE_list,"Mean MI":Mean_MI_list,"Mean Temperature":Mean_T_list,"Mean Velocity":Mean_V_list,"Mean Diameter":Mean_D_list}
            
            final_quartile_means = pd.DataFrame(final_means_dict)
            final_quartile_means.to_csv("means.csv")

