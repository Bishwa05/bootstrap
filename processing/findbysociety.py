#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 01:14:43 2019

@author: i501895
"""

import pandas as pd

#load our data from CSV
tx_data = pd.read_csv('../data/sample_data.csv')

newdf = tx_data[['society_id','category_id','subcategory_id','product_id']]

#To find with the provided city
newdf= newdf[newdf['society_id'] == 1127168]

newdf.groupby(['category_id', 'subcategory_id'])


groupby_cond_counts = newdf.groupby(['category_id', 'subcategory_id']).count()
print(groupby_cond_counts) #This to return to show the count. 

print(newdf) #This to be return when we query by society_id