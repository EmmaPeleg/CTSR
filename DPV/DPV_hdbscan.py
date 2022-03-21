import numpy as np
import os
import pandas as pd
import hdbscan
from tkinter.filedialog import askopenfilename as ask
from tkinter.filedialog import asksaveasfilename as ssn
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats

file = ask()

df = pd.read_table(file, header=0, delimiter='\s+')

x = df['Diameter']
y = df['Speed']
z = df['Temperature']

##diameter fixing
EnergyB = np.array(df["EnergyB"])
Old_Diameters = np.array(df["Diameter"])
PSA_Diameter_mode = 37.97 ## um
Full_Temp = np.array(df["Temperature"])
DC = (Old_Diameters)/(np.sqrt(EnergyB/Full_Temp**4))
DC_mode = stats.mode(DC)[0]
Old_D_mode=stats.mode(Old_Diameters)[0]
New_DC=DC_mode*(PSA_Diameter_mode/Old_D_mode)
Real_Diameters = New_DC*(np.sqrt(EnergyB/Full_Temp**4))

df["Diameter"]=Real_Diameters ## adding fixed diameters
#data=np.array(data_df) ## data for speed temp diameter as array for hdbscan

X = np.array(list(zip(x,y,z)))

agg = hdbscan.HDBSCAN(min_cluster_size=20).fit(X)

df['Class'] = agg.labels_

no_outlier = df[df['Class']!=-1]

##########################
#### FIND BIG CLUSTER ####
##########################

n = no_outlier['Class'].unique()

cluster_sizes = []

for i in n:
	cluster_sizes.append(df[df['Class']==i].count()[1])

res = dict(zip(cluster_sizes, n))

largest_cluster = res[max(cluster_sizes)]

print("Filtered Temp:   ", df[df['Class']==largest_cluster]['Temperature'].mean())
print("Unfiltered Temp: ", df['Temperature'].mean())
print("dT:              ", df['Temperature'].mean() - df[df['Class']==largest_cluster]['Temperature'].mean())
print()
print("Filtered Speed:   ", df[df['Class']==largest_cluster]['Speed'].mean())
print("Unfiltered Speed: ", df['Speed'].mean())
print("dv:               ", df['Speed'].mean() - df[df['Class']==largest_cluster]['Speed'].mean())



##########################
##### PLOTTING STUFF #####
##########################

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(df['Speed'], df['Temperature'], df['Diameter'], c= df['Class'], alpha=1)
ax.set_xlabel('Velocity (m/s)')
ax.set_ylabel('Temperature (C)')
ax.set_zlabel('Diameter (um)', rotation=90)
ax.set_title('Initial Clustering Groups')

plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(no_outlier['Speed'], no_outlier['Temperature'], no_outlier['Diameter'], c= no_outlier['Class'], alpha=1)
ax.set_xlabel('Velocity (m/s)')
ax.set_ylabel('Temperature (C)')
ax.set_zlabel('Diameter (um)', rotation=90)
ax.set_title('After Outlier Clustering')
plt.show()

##########################
####### SAVE DATA ########
##########################

sname = ssn()

writer=pd.ExcelWriter(sname+'.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='data')
writer.save()
writer.close()

##########################
##### SAVING PLOTS #######
##########################
'''
fname = ssn()
plt.savefig(fname, dpi=1200, format = 'tiff')
'''