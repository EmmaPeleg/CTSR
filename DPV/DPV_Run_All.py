# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 13:43:29 2022

@author: Emma Peleg
"""
import os
import pandas as pd
import DPV_Data_Analysis as dpv
import numpy as np

path_of_the_directory = r"C:\Users\Emma Peleg\Desktop\CTSR\Mo-Study\DPV-Mo Powders\DPV Files for DAQ\SA 101 CG 3.0"
ext = ".prt"

for files in os.listdir(path_of_the_directory):
    os.chdir(path_of_the_directory)
    if files.endswith(ext):
        print(files)
        rename = files.replace(" ","_")
        os.rename(files,rename)
        setname=files[0:-4]
        w = pd.read_table(files, header=0, delimiter='\s+')
     
        
# data_open = open(files,"r")
# data = w[["Speed","Temperature","Diameter"]].copy()
# data=np.array(data) ##