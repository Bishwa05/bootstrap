#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 12:41:37 2019

@author: i501895
"""

# Import pandas and csv file
from datetime import datetime, timedelta
import pandas as pd
#from matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns
#from __future__ import division

#import chart_studio.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go


#load our data from CSV
tx_data = pd.read_csv('../data/hackathon_data.csv')

#convert the string date field to datetime
#tx_data['InvoiceDate'] = pd.to_datetime(tx_data['InvoiceDate'])

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
tx_max_purchase['Recency'] = (tx_max_purchase['InvoiceDate'].max() - tx_max_purchase['InvoiceDate']).dt.days

#merge this dataframe to our new user dataframe
tx_user = pd.merge(tx_user, tx_max_purchase[['customer_id','Recency']], on='customer_id')

#print("Bishwa", tx_user)

#print(tx_user.head())

print(tx_user.Recency.describe())

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
#plot(fig)

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

#build 4 clusters for recency and add it to dataframe
kmeans = KMeans(n_clusters=4)
kmeans.fit(tx_user[['Recency']])
tx_user['RecencyCluster'] = kmeans.predict(tx_user[['Recency']])

#function for ordering cluster numbers
def order_cluster(cluster_field_name, target_field_name,df,ascending):
    new_cluster_field_name = 'new_' + cluster_field_name
    df_new = df.groupby(cluster_field_name)[target_field_name].mean().reset_index()
    df_new = df_new.sort_values(by=target_field_name,ascending=ascending).reset_index(drop=True)
    df_new['index'] = df_new.index
    df_final = pd.merge(df,df_new[[cluster_field_name,'index']], on=cluster_field_name)
    df_final = df_final.drop([cluster_field_name],axis=1)
    df_final = df_final.rename(columns={"index":cluster_field_name})
    return df_final

tx_user = order_cluster('RecencyCluster', 'Recency',tx_user,False)
#print(tx_user['RecencyCluster'])


#get order counts for each user and create a dataframe with it
tx_frequency = tx_data.groupby('customer_id').InvoiceDate.count().reset_index()
tx_frequency.columns = ['customer_id','Frequency']

#add this data to our main dataframe
tx_user = pd.merge(tx_user, tx_frequency, on='customer_id')

#print(tx_frequency)

#plot the histogram
plot_data = [
    go.Histogram(
        x=tx_user.query('Frequency < 1000')['Frequency']
    )
]

plot_layout = go.Layout(
        title='Frequency'
    )
fig = go.Figure(data=plot_data, layout=plot_layout)
plot(fig)


#k-means
kmeans = KMeans(n_clusters=4)
kmeans.fit(tx_user[['Frequency']])
tx_user['FrequencyCluster'] = kmeans.predict(tx_user[['Frequency']])

#order the frequency cluster
tx_user = order_cluster('FrequencyCluster', 'Frequency',tx_user,True)

#see details of each cluster
#print(tx_user.groupby('FrequencyCluster')['Frequency'].describe())


#calculate revenue for each customer
tx_data['Revenue'] = tx_data['total_cost']
tx_revenue = tx_data.groupby('customer_id').Revenue.sum().reset_index()

#merge it with our main dataframe
tx_user = pd.merge(tx_user, tx_revenue, on='customer_id')

#plot the histogram
plot_data = [
    go.Histogram(
        x=tx_user.query('Revenue < 10000')['Revenue']
    )
]

plot_layout = go.Layout(
        title='Monetary Value'
    )
fig = go.Figure(data=plot_data, layout=plot_layout)
plot(fig)

#apply clustering
kmeans = KMeans(n_clusters=4)
kmeans.fit(tx_user[['Revenue']])
tx_user['RevenueCluster'] = kmeans.predict(tx_user[['Revenue']])


#order the cluster numbers
tx_user = order_cluster('RevenueCluster', 'Revenue',tx_user,True)

#show details of the dataframe
#print(tx_user.groupby('RevenueCluster')['Revenue'].describe())

#calculate overall score and use mean() to see details
tx_user['OverallScore'] = tx_user['RecencyCluster'] + tx_user['FrequencyCluster'] + tx_user['RevenueCluster']
tx_user.groupby('OverallScore')['Recency','Frequency','Revenue'].mean()

tx_user['Segment'] = 'Low-Value'
tx_user.loc[tx_user['OverallScore']>2,'Segment'] = 'Mid-Value' 
tx_user.loc[tx_user['OverallScore']>4,'Segment'] = 'High-Value'

#print(tx_user)

#Revenue vs Frequency
plotRevenueFrequency(tx_user)

#Revenue Recency
plotRecencyRecency(tx_user)

# Revenue vs Frequency
plotRevenueFrequency(tx_user)

