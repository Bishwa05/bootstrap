#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 12:41:37 2019

@author: i501895
"""

# Import pandas and cars.csv
from datetime import datetime, timedelta
import pandas as pd
#import matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#from __future__ import division


#inititate Plotly
#pyoff.init_notebook_mode()

#load our data from CSV
tx_data = pd.read_csv('../data/sample_data.csv')

#convert the string date field to datetime
#tx_data['InvoiceDate'] = pd.to_datetime(tx_data['InvoiceDate'])

#we will be using only UK data
#tx_uk = tx_data.query("Country=='United Kingdom'").reset_index(drop=True)



#cust_data = pd.read_csv('../data/sample_data.csv', index_col = 0)

# Print out country column as Pandas Series
#print(cust_data)




#create a generic user dataframe to keep CustomerID and new segmentation scores
tx_user = pd.DataFrame(tx_data['customer_id'].unique())
tx_user.columns = ['customer_id']

print(tx_user)


#get the max purchase date for each customer and create a dataframe with it
