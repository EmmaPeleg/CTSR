# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 11:14:16 2021

@author: epeleg
"""
import csv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#READ ME: take trials A, B, C, D, E and GT, rename each test.stop.csv to A.csv, B.csv, etc.
#put in folder from which program is being run, that way the program can analyze all runs
#do for each sample set and save results
set_name=input("what is the sample set name?\n")
sampleset=set_name+'.png'
#for test A
dfA=pd.read_csv('A.csv') #read in the data in csv format from instron

dfA=dfA.drop(columns="Cycle Elapsed Time (s)")
dfA=dfA.drop(columns="Total Cycles")
dfA=dfA.drop(columns="Elapsed Cycles")
dfA=dfA.drop(columns="Step")
dfA=dfA.drop(columns="Total Cycle Count(8800 (0,1) Waveform)")

colA=dfA["Load(8800 (0,1):Load) (kN)"].to_numpy() #convert to array for python ease
colA=np.array(colA)

rangeA=np.argmax(colA>0.5)
dfA.iloc[rangeA]
count_rowA=dfA.shape[0]  # Gives number of rows

dfA=dfA[rangeA:count_rowA]

load_colA=dfA["Load(8800 (0,1):Load) (kN)"].to_numpy()

position_colA=dfA["Position(8800 (0,1):Position) (mm)"].to_numpy()
zeroA=position_colA[0]
zeroed_posA=position_colA-zeroA

maxloadA=max(colA)
adhesion_MPa_A=round(((maxloadA)/(3.1415*(25.4/2)**2)*1000),2)
dfA["Adhesion Strength"]=adhesion_MPa_A
dfA["max load"]=maxloadA

#for test B

dfB=pd.read_csv('B.csv') #read in the data in csv format from instron

dfB=dfB.drop(columns="Cycle Elapsed Time (s)")
dfB=dfB.drop(columns="Total Cycles")
dfB=dfB.drop(columns="Elapsed Cycles")
dfB=dfB.drop(columns="Step")
dfB=dfB.drop(columns="Total Cycle Count(8800 (0,1) Waveform)")

colB=dfB["Load(8800 (0,1):Load) (kN)"].to_numpy() #convert to array for python ease
colB=np.array(colB)

rangeB=np.argmax(colB>0.5)
dfB.iloc[rangeB]
count_rowB=dfB.shape[0]  # Gives number of rows

dfB=dfB[rangeB:count_rowB]

load_colB=dfB["Load(8800 (0,1):Load) (kN)"].to_numpy()
position_colB=dfB["Position(8800 (0,1):Position) (mm)"].to_numpy()
#position_col=np.array(position_col)

zeroB=position_colB[0]
zeroed_posB=position_colB-zeroB


maxloadB=max(colB)
adhesion_MPa_B=round(((maxloadB)/(3.1415*(25.4/2)**2)*1000),2)
dfB["Adhesion Strength"]=adhesion_MPa_B
dfB["max load"]=maxloadB



#fir test C

dfC=pd.read_csv('C.csv') #read in the data in csv format from instron

dfC=dfC.drop(columns="Cycle Elapsed Time (s)")
dfC=dfC.drop(columns="Total Cycles")
dfC=dfC.drop(columns="Elapsed Cycles")
dfC=dfC.drop(columns="Step")
dfC=dfC.drop(columns="Total Cycle Count(8800 (0,1) Waveform)")

colC=dfC["Load(8800 (0,1):Load) (kN)"].to_numpy() #convert to array for python ease
colC=np.array(colC)

rangeC=np.argmax(colC>0.5)
dfC.iloc[rangeC]
count_rowC=dfC.shape[0]  # Gives number of rows

dfC=dfC[rangeC:count_rowC]

load_colC=dfC["Load(8800 (0,1):Load) (kN)"].to_numpy()
position_colC=dfC["Position(8800 (0,1):Position) (mm)"].to_numpy()
zeroC=position_colC[0]
zeroed_posC=position_colC-zeroC

maxloadC=max(colC)
adhesion_MPa_C=round(((maxloadC)/(3.1415*(25.4/2)**2)*1000),2)
dfC["Adhesion Strength"]=adhesion_MPa_C
dfC["max load"]=maxloadC


# for test D
dfD=pd.read_csv('D.csv') #read in the data in csv format from instron

dfD=dfD.drop(columns="Cycle Elapsed Time (s)")
dfD=dfD.drop(columns="Total Cycles")
dfD=dfD.drop(columns="Elapsed Cycles")
dfD=dfD.drop(columns="Step")
dfD=dfD.drop(columns="Total Cycle Count(8800 (0,1) Waveform)")

colD=dfD["Load(8800 (0,1):Load) (kN)"].to_numpy() #convert to array for python ease
colD=np.array(colD)

rangeD=np.argmax(colD>0.5)
dfD.iloc[rangeD]
count_rowD=dfD.shape[0]  # Gives number of rows

dfD=dfD[rangeD:count_rowD]

load_colD=dfD["Load(8800 (0,1):Load) (kN)"].to_numpy()
position_colD=dfD["Position(8800 (0,1):Position) (mm)"].to_numpy()
zeroD=position_colD[0]
zeroed_posD=position_colD-zeroD

maxloadD=max(colD)
adhesion_MPa_D=round(((maxloadD)/(3.1415*(25.4/2)**2)*1000),2)
dfD["Adhesion Strength"]=adhesion_MPa_D
dfD["max load"]=maxloadD


#for test E

dfE=pd.read_csv('E.csv') #read in the data in csv format from instron

dfE=dfE.drop(columns="Cycle Elapsed Time (s)")
dfE=dfE.drop(columns="Total Cycles")
dfE=dfE.drop(columns="Elapsed Cycles")
dfE=dfE.drop(columns="Step")
dfE=dfE.drop(columns="Total Cycle Count(8800 (0,1) Waveform)")

colE=dfE["Load(8800 (0,1):Load) (kN)"].to_numpy() #convert to array for python ease
colE=np.array(colE)

rangeE=np.argmax(colE>0.5)
dfE.iloc[rangeE]
count_rowE=dfE.shape[0]  # Gives number of rows

dfE=dfE[rangeE:count_rowE]

load_colE=dfE["Load(8800 (0,1):Load) (kN)"].to_numpy()
position_colE=dfE["Position(8800 (0,1):Position) (mm)"].to_numpy()
zeroE=position_colE[0]
zeroed_posE=position_colE-zeroE

maxloadE=max(colE)
adhesion_MPa_E=round(((maxloadE)/(3.1415*(25.4/2)**2)*1000),2)

dfE["Adhesion Strength"]=adhesion_MPa_E
dfE["max load"]=maxloadE

#for glue test

dfGT=pd.read_csv('GT.csv') #read in the data in csv format from instron

dfGT=dfGT.drop(columns="Cycle Elapsed Time (s)")
dfGT=dfGT.drop(columns="Total Cycles")
dfGT=dfGT.drop(columns="Elapsed Cycles")
dfGT=dfGT.drop(columns="Step")
dfGT=dfGT.drop(columns="Total Cycle Count(8800 (0,1) Waveform)")

colGT=dfGT["Load(8800 (0,1):Load) (kN)"].to_numpy() #convert to array for python ease
colGT=np.array(colGT)

rangeGT=np.argmax(colGT>0.5)
dfGT.iloc[rangeGT]
count_rowGT=dfGT.shape[0]  # Gives number of rows

dfGT=dfGT[rangeGT:count_rowGT]

load_colGT=dfGT["Load(8800 (0,1):Load) (kN)"].to_numpy()
position_colGT=dfGT["Position(8800 (0,1):Position) (mm)"].to_numpy()
zeroGT=position_colGT[0]
zeroed_posGT=position_colGT-zeroGT

maxloadGT=max(colGT)
adhesion_MPa_GT=round(((maxloadGT)/(3.1415*(25.4/2)**2)*1000),2)

dfGT["Adhesion Strength"]=adhesion_MPa_GT
dfGT["max load"]=maxloadGT

#OUTPUT TIME!!

adhesion_array=[adhesion_MPa_A,adhesion_MPa_B,adhesion_MPa_C,adhesion_MPa_D,adhesion_MPa_E]
average_adhesion=sum(adhesion_array)/len(adhesion_array)

print('Adhesion Strength Test A:', adhesion_MPa_A,'MPa')
print('Adhesion Strength Test B:', adhesion_MPa_B,'MPa')
print('Adhesion Strength Test C:', adhesion_MPa_C,'MPa')
print('Adhesion Strength Test D:', adhesion_MPa_D,'MPa')
print('Adhesion Strength Test E:', adhesion_MPa_E,'MPa')
print('Adhesion Strength Glue Test:', adhesion_MPa_GT,'MPa')
print('Average adhesion of pull tests A-E:',average_adhesion)

load_array=[maxloadA,maxloadB,maxloadC,maxloadD,maxloadE,maxloadGT]
y_max=max(load_array)+10

plt.plot(zeroed_posA,load_colA,label=('A',adhesion_MPa_A,'MPa'))
plt.plot(zeroed_posB,load_colB,label=('B',adhesion_MPa_B,'MPa'))
plt.plot(zeroed_posC,load_colC,label=('C',adhesion_MPa_C,'MPa'))
plt.plot(zeroed_posD,load_colD,label=('D',adhesion_MPa_D,'MPa'))
plt.plot(zeroed_posE,load_colE,label=('E',adhesion_MPa_E,'MPa'))
plt.plot(zeroed_posGT,load_colGT,label=('GT',adhesion_MPa_GT,'MPa'))

plt.ylabel("Load (kN)")
plt.xlabel('Displacement (mm)')
plt.legend()
plt.ylim(0,y_max)
plt.title(set_name)

plt.savefig(sampleset)
A_csv=set_name+'A'+'.csv'
B_csv=set_name+'B'+'.csv'
C_csv=set_name+'C'+'.csv'
D_csv=set_name+'D'+'.csv'
E_csv=set_name+'E'+'.csv'
GT_csv=set_name+'GT'+'.csv'
output_name=set_name+'ALL'+'.csv'

dfA.to_csv(A_csv)
dfB.to_csv(B_csv)
dfC.to_csv(C_csv)
dfD.to_csv(D_csv)
dfE.to_csv(E_csv)
dfGT.to_csv(GT_csv)

output_data=[['A',adhesion_MPa_A,],['B',adhesion_MPa_B],['C',adhesion_MPa_C],['D',adhesion_MPa_D],['E',adhesion_MPa_E],['GT',adhesion_MPa_GT]]
output_df=pd.DataFrame(output_data,columns=['Sample #','Adhesion Strength (MPa)'])
output_df["Average Adhesion"]=average_adhesion
output_df.to_csv(output_name)
