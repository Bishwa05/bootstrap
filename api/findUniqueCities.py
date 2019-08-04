import pandas as pd

def findUniqueCities():
    tx_data = pd.read_csv('../data/sample_data.csv')
    return tx_data['city_id'].unique().tolist()
