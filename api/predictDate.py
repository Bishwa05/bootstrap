import pandas as pd
import datetime
#from matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#from __future__ import division
#
# import chart_studio.plotly as py
import plotly.offline as pyoff
import plotly.graph_objs as go

def predict_next_purchase_date(socId):
    tx_data = pd.read_csv('../data/sample_data.csv')
    tx_data['InvoidataceDate'] = pd.to_datetime(tx_data['product_addedtobasket_on'])

    tx_data['InvoiceDate'] = pd.to_datetime(tx_data['product_addedtobasket_on'])
    tx_max_purchase = tx_data.groupby('product_id').InvoiceDate.max().reset_index()
    tx_max_purchase.columns = ['product_id', 'InvoiceDate']
    # print(tx_max_purchase)
    tx_user = pd.DataFrame(tx_data['product_id'].unique())
    tx_user.columns = ['product_id']
    tx_data = tx_data[
        (tx_data['customer_id'] == 1121904) & (tx_data['subscription'] == 0) & (tx_data['society_id'] == socId)]
    tx_data.sort_values(['InvoidataceDate'], ascending=[True], inplace=True)
    tx_user = pd.merge(tx_user, tx_data[['customer_id', 'city_id', 'product_id', 'InvoidataceDate']], on=['product_id'])

    tx_user['difference'] = tx_user.groupby('product_id')['InvoidataceDate'].diff().apply(lambda x: x.days)

    tx_final = tx_user.dropna()
    tx_final = tx_final.groupby('product_id', as_index=False)['difference'].mean()

    df3 = tx_final.merge(tx_max_purchase, on='product_id',
                           how='outer')
    tx_final = df3.dropna()
    print(tx_final)
    curr_time = pd.to_datetime("now")
    tx_final['repetation'] = (curr_time - tx_final['InvoiceDate']).apply(lambda x: x.days)
    tx_final.columns = ['product_id', 'difference', 'InvoiceDate', 'repetation']
    tx_finalDate = tx_final
    finalList = []
    print (tx_final)
    for index, row in tx_final.iterrows():
        print (row['repetation'])
        if (row['repetation'] > 1 and row['repetation'] < 3):
            finalList.append((1121904, row['product_id'], "Daily"))
        elif (row['repetation'] > 5 and row['repetation'] < 9):
            finalList.append((1121904, row['product_id'], "Weekly"))
        elif (row['repetation'] > 25 and row['repetation'] < 40):
            finalList.append((1121904, row['product_id'], "Monthly"))
        else:
            finalList.append((1121904, row['product_id'], "Yearly"))
    print(finalList)
    return finalList
    # cust_list=['1121904']
    # print (cust_list)
    # for customerId in cust_list:
    #     tx_data = pd.DataFrame()
    #     tx_data = tx_data.fillna(0)
    #     tx_data = pd.read_csv('../data/sample_data.csv')
    #       # with 0s rather than NaNs
    #     tx_data['InvoidataceDate'] = pd.to_datetime(tx_data['product_addedtobasket_on'])
    #
    #     tx_data['InvoiceDate'] = pd.to_datetime(tx_data['product_addedtobasket_on'])
    #     tx_max_purchase = tx_data.groupby('product_id').InvoiceDate.max().reset_index()
    #     tx_max_purchase.columns = ['product_id', 'InvoiceDate']
    #     # print(tx_max_purchase)
    #     tx_user = pd.DataFrame(tx_data['product_id'].unique())
    #     tx_user.columns = ['product_id']
    #     tx_data = tx_data[
    #         (tx_data['customer_id'] == customerId) & (tx_data['subscription'] == 0)
    #         & (tx_data['society_id'] == socId)]
    #     tx_data.sort_values(['InvoidataceDate'], ascending=[True], inplace=True)
    #     tx_user = pd.merge(tx_user, tx_data[['customer_id', 'city_id', 'product_id', 'InvoidataceDate']],
    #                        on=['product_id'])
    #     # tx_user.pct_change()
    #     tx_user['difference'] = tx_user.groupby('product_id')['InvoidataceDate'].diff().apply(lambda x: x.days)
    #
    #     tx_final = tx_user.dropna()
    #     tx_final = tx_final.groupby(['product_id'], as_index=False)['difference'].mean()
    #     tx_final.columns = ['product_id', 'difference']
    #
    #     df3 = tx_final.merge(tx_max_purchase, on='product_id',
    #                          how='outer')
    #     tx_final = df3.dropna()
    #     #print(tx_final)
    #     curr_time = pd.to_datetime("now")
    #     tx_final['repetation'] = (curr_time - tx_final['InvoiceDate']).apply(lambda x: x.days)
    #     tx_final.columns = ['product_id', 'difference', 'InvoiceDate', 'repetation']
    #     tx_finalDate = tx_final
    #     finalList = []
    #     #print (tx_final)
    #     for index, row in tx_final.iterrows():
    #         #print (row['repetation'])
    #         if (row['repetation'] > 1 and row['repetation'] < 3):
    #             finalList.append((customerId, row['product_id'], "Daily"))
    #         elif (row['repetation'] > 5 and row['repetation'] < 9):
    #             finalList.append((customerId, row['product_id'], "Weekly"))
    #         elif (row['repetation'] > 25 and row['repetation'] < 40):
    #             finalList.append((customerId, row['product_id'], "Monthly"))
    #         else:
    #             finalList.append((customerId, row['product_id'], "Never"))
    #     #print(finalList)
    #     return finalList



