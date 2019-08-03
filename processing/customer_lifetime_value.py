#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 19:58:43 2019

@author: i501895

LifeTime value = Revenue - cost
"""


#import libraries
from datetime import datetime, timedelta,date
import pandas as pd
#%matplotlib inline
from sklearn.metrics import classification_report,confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

#import XGBoost as xgb
#import chart_studio.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go

from sklearn.model_selection import KFold, cross_val_score, train_test_split


#read data from csv and redo the data work we done before
tx_data = pd.read_csv('../data/sample_data.csv')
tx_data['InvoiceDate'] = pd.to_datetime(tx_data['product_addedtobasket_on'])

print(tx_data)

#create 1m and 2m dataframes
tx_1m = tx_data[(tx_data.InvoiceDate < date(2018,4,30)) & (tx_data.InvoiceDate >= date(2018,4,1))].reset_index(drop=True)
tx_2m = tx_data[(tx_data.InvoiceDate >= date(2018,5,1)) & (tx_data.InvoiceDate < date(2018,5,30))].reset_index(drop=True)

print('Bishwa',tx_1m)


#create tx_user for assigning clustering
tx_user = pd.DataFrame(tx_1m['customer_id'].unique())
tx_user.columns = ['customer_id']

#order cluster method
def order_cluster(cluster_field_name, target_field_name,df,ascending):
    new_cluster_field_name = 'new_' + cluster_field_name
    df_new = df.groupby(cluster_field_name)[target_field_name].mean().reset_index()
    df_new = df_new.sort_values(by=target_field_name,ascending=ascending).reset_index(drop=True)
    df_new['index'] = df_new.index
    df_final = pd.merge(df,df_new[[cluster_field_name,'index']], on=cluster_field_name)
    df_final = df_final.drop([cluster_field_name],axis=1)
    df_final = df_final.rename(columns={"index":cluster_field_name})
    return df_final


#calculate recency score
tx_max_purchase = tx_1m.groupby('customer_id').InvoiceDate.max().reset_index()
tx_max_purchase.columns = ['customer_id','MaxPurchaseDate']
tx_max_purchase['Recency'] = (tx_max_purchase['MaxPurchaseDate'].max() - tx_max_purchase['MaxPurchaseDate']).dt.days
tx_user = pd.merge(tx_user, tx_max_purchase[['customer_id','Recency']], on='customer_id')

print('Bishwa2',tx_user)

kmeans = KMeans(n_clusters=4)
kmeans.fit(tx_user[['Recency']])
tx_user['RecencyCluster'] = kmeans.predict(tx_user[['Recency']])
tx_user = order_cluster('RecencyCluster', 'Recency',tx_user,False)

#calcuate frequency score

tx_frequency = tx_1m.groupby('customer_id').InvoiceDate.count().reset_index()
tx_frequency.columns = ['customer_id','Frequency']
tx_user = pd.merge(tx_user, tx_frequency, on='customer_id')

kmeans = KMeans(n_clusters=4)
kmeans.fit(tx_user[['Frequency']])
tx_user['FrequencyCluster'] = kmeans.predict(tx_user[['Frequency']])

tx_user = order_cluster('FrequencyCluster', 'Frequency',tx_user,True)

#calcuate revenue score
tx_1m['Revenue'] = tx_1m['selling_price_per_unit'] * tx_1m['product_quantity']
tx_revenue = tx_1m.groupby('customer_id').Revenue.sum().reset_index()
tx_user = pd.merge(tx_user, tx_revenue, on='customer_id')

kmeans = KMeans(n_clusters=4)
kmeans.fit(tx_user[['Revenue']])
tx_user['RevenueCluster'] = kmeans.predict(tx_user[['Revenue']])
tx_user = order_cluster('RevenueCluster', 'Revenue',tx_user,True)


#overall scoring
tx_user['OverallScore'] = tx_user['RecencyCluster'] + tx_user['FrequencyCluster'] + tx_user['RevenueCluster']
tx_user['Segment'] = 'Low-Value'
tx_user.loc[tx_user['OverallScore']>2,'Segment'] = 'Mid-Value' 
tx_user.loc[tx_user['OverallScore']>4,'Segment'] = 'High-Value' 


tx_2m['Revenue'] = tx_2m['selling_price_per_unit'] * tx_2m['product_quantity']
tx_user_2m = tx_2m.groupby('customer_id')['Revenue'].sum().reset_index()
tx_user_2m.columns = ['customer_id','m2_Revenue']


#plot LTV histogram
plot_data = [
    go.Histogram(
        x=tx_user_2m.query('m2_Revenue < 10000')['m2_Revenue']
    )
]

plot_layout = go.Layout(
        title='2m Revenue'
    )
fig = go.Figure(data=plot_data, layout=plot_layout)
plot(fig)

tx_graph = tx_merge.query("m2_Revenue < 30000")

plot_data = [
    go.Scatter(
        x=tx_graph.query("Segment == 'Low-Value'")['OverallScore'],
        y=tx_graph.query("Segment == 'Low-Value'")['m6_Revenue'],
        mode='markers',
        name='Low',
        marker= dict(size= 7,
            line= dict(width=1),
            color= 'blue',
            opacity= 0.8
           )
    ),
        go.Scatter(
        x=tx_graph.query("Segment == 'Mid-Value'")['OverallScore'],
        y=tx_graph.query("Segment == 'Mid-Value'")['m6_Revenue'],
        mode='markers',
        name='Mid',
        marker= dict(size= 9,
            line= dict(width=1),
            color= 'green',
            opacity= 0.5
           )
    ),
        go.Scatter(
        x=tx_graph.query("Segment == 'High-Value'")['OverallScore'],
        y=tx_graph.query("Segment == 'High-Value'")['m6_Revenue'],
        mode='markers',
        name='High',
        marker= dict(size= 11,
            line= dict(width=1),
            color= 'red',
            opacity= 0.9
           )
    ),
]

plot_layout = go.Layout(
        yaxis= {'title': "2m LTV"},
        xaxis= {'title': "RFM Score"},
        title='LTV'
    )
fig = go.Figure(data=plot_data, layout=plot_layout)
plot(fig)

#remove outliers
tx_merge = tx_merge[tx_merge['m2_Revenue']<tx_merge['m2_Revenue'].quantile(0.99)]


#creating 3 clusters
kmeans = KMeans(n_clusters=3)
kmeans.fit(tx_merge[['m2_Revenue']])
tx_merge['LTVCluster'] = kmeans.predict(tx_merge[['m2_Revenue']])

#order cluster number based on LTV
tx_merge = order_cluster('LTVCluster', 'm2_Revenue',tx_merge,True)

#creatinga new cluster dataframe
tx_cluster = tx_merge.copy()

#see details of the clusters
tx_cluster.groupby('LTVCluster')['m6_Revenue'].describe()

#convert categorical columns to numerical
tx_class = pd.get_dummies(tx_cluster)

#calculate and show correlations
corr_matrix = tx_class.corr()
corr_matrix['LTVCluster'].sort_values(ascending=False)

#create X and y, X will be feature set and y is the label - LTV
X = tx_class.drop(['LTVCluster','m2_Revenue'],axis=1)
y = tx_class['LTVCluster']

#split training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=56)

#XGBoost Multiclassification Model
ltv_xgb_model = xgb.XGBClassifier(max_depth=5, learning_rate=0.1,objective= 'multi:softprob',n_jobs=-1).fit(X_train, y_train)

print('Accuracy of XGB classifier on training set: {:.2f}'
       .format(ltv_xgb_model.score(X_train, y_train)))
print('Accuracy of XGB classifier on test set: {:.2f}'
       .format(ltv_xgb_model.score(X_test[X_train.columns], y_test)))

y_pred = ltv_xgb_model.predict(X_test)
print(classification_report(y_test, y_pred))
