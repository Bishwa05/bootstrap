#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 12:41:37 2019

@author: i501895
"""

# Import pandas and cars.csv
from datetime import datetime, timedelta
import pandas as pd
#from matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#from __future__ import division

import chart_studio.plotly as py
import plotly.offline as pyoff
import plotly.graph_objs as go

#inititate Plotly
pyoff.init_notebook_mode()

#load our data from CSV
tx_data = pd.read_csv('../data/sample_data.csv')

#convert the string date field to datetime
#tx_data['InvoiceDate'] = pd.to_datetime(tx_data['InvoiceDate'])

#we will be using only UK data
#tx_uk = tx_data.query("Country=='United Kingdom'").reset_index(drop=True)



#cust_data = pd.read_csv('../data/sample_data.csv', index_col = 0)

# Print out country column as Pandas Series
#print(cust_data)


#convert the string date field to datetime
tx_data['InvoiceDate'] = pd.to_datetime(tx_data['product_addedtobasket_on'])

#create a generic user dataframe to keep CustomerID and new segmentation scores
tx_user = pd.DataFrame(tx_data['customer_id'].unique())
tx_user.columns = ['customer_id']

#print(tx_user)

#get the max purchase date for each customer and create a dataframe with it
tx_max_purchase = tx_data.groupby('customer_id').InvoiceDate.max().reset_index()
tx_max_purchase.columns = ['customer_id','InvoiceDate']
#print(tx_max_purchase)

#we take our observation point as the max invoice date in our dataset
#print(tx_max_purchase['InvoiceDate'].max())
#print('Bishwa')
#print(tx_max_purchase['InvoiceDate'])
tx_max_purchase['Recency'] = (tx_max_purchase['InvoiceDate'].max() - tx_max_purchase['InvoiceDate']).dt.days

#merge this dataframe to our new user dataframe
tx_user = pd.merge(tx_user, tx_max_purchase[['customer_id','Recency']], on='customer_id')

#print(tx_user)
tx_user.head()

#plot a recency histogram

plot_data = [
    go.Histogram(
        x=tx_user['Recency']
    )
]

plot_layout = go.Layout(
        title='Recency'
    )
fig = go.Figure(data=plot_data, layout=plot_layout)
pyoff.iplot(fig)

from sklearn.cluster import KMeans

sse={}
tx_recency = tx_user[['Recency']]
for k in range(1, 10):
    kmeans = KMeans(n_clusters=k, max_iter=1000).fit(tx_recency)
    tx_recency["clusters"] = kmeans.labels_
    sse[k] = kmeans.inertia_ 
plt.figure()
plt.plot(list(sse.keys()), list(sse.values()))
plt.xlabel("Number of cluster")
plt.show()

#get the max purchase date for each customer and create a dataframe with it
