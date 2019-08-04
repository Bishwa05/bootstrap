#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 09:02:26 2019

@author: i501895
"""

import pandas as pd

tx_data = pd.read_csv('../data/sample_data.csv')
newdf = tx_data[['subcategory_id','total_cost']]
newdf.columns =['subcatid','totrev']
newdf['totrev'] = tx_data['total_cost']
getsum = newdf.groupby(['subcatid']).sum()
getsum = newdf.groupby('subcatid').totrev.sum().reset_index()
getsum.columns = ['subcategory_id','Sum']
print(getsum.to_json(orient='records'))
#orderdf = newdf.groupby(['subcategory_id']).count()
#print(orderdf)#Total no of orders per sub category

#final = pd.merge(getsum, orderdf, on='subcategory_id')
#final.columns= ["Total_Revenue", "Total_Orders"]
#print(final) # Count of Orders per sub category
#final['Total_Orders'].loc[final['Total_Orders']>=1] = final['Total_Revenue']/final['Total_Orders']
#print(final) # AOV per sub category