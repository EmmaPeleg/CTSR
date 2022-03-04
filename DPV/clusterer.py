# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 10:49:00 2022

@author: Emma Peleg

does clustering for outlier removal
"""

import csv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from math import pi
import hdbscan

print("running the cluster buster")

w = pd.read_table('SA110_Center_60_CG3.5.prt', header=0, delimiter='\s+')
data_open = open("SA110_Center_60_CG3.5.prt","r")
data = w[["Speed","Temperature","Diameter"]].copy()
data=np.array(data) ## data for speed temp diameter as array for hdbscan

clusterer = hdbscan.HDBSCAN()

fit=clusterer.fit(data)

cluster_labels = clusterer.labels_
min_cluster = clusterer.labels_.min()
max_cluster = clusterer.labels_.max()
cluster_prob = clusterer.probabilities_
cluster_out = clusterer.outlier_scores_

sns.distplot(clusterer.outlier_scores_[np.isfinite(clusterer.outlier_scores_)], rug=True)

threshold = pd.Series(clusterer.outlier_scores_).quantile(0.9)
outliers = np.where(clusterer.outlier_scores_ > threshold)[0]

outlier_list = list(outliers)

outlier_index = []
for i in outliers:
    out = data[i]
    outlier_index.append(out)

data_index_list=list(range(0,len(data)))
    
for element in outlier_list:
    if element in data_index_list:
        data_index_list.remove(element)

clean_data=[]
        ## removing all of the outliers and saving in new array
        
for i in data_index_list:
    add_data=data[i]
    clean_data.append(add_data)








