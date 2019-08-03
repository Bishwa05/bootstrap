#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 22:52:47 2019

@author: i501895
"""

import pandas as pd

#load our data from CSV
tx_data = pd.read_csv('../data/hackathon_data.csv')

newdf = tx_data[['city_id','manufacturer_id','society_id','store_id']]

#To find with the provided city
newdf= newdf[newdf['city_id'] == 1120112]

newdf.groupby(['city_id', 'store_id'])


groupby_city_store_counts = newdf.groupby(['city_id', 'store_id']).count()
print(groupby_city_store_counts) #This to return to show the count. 

print(newdf) #This to be return when we query by cityid