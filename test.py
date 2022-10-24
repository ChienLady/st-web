import pandas as pd
import os

THIS_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(THIS_PATH)
DDIR_PATH = os.path.dirname(DIR_PATH)
ASSET_PATH = os.path.join(DDIR_PATH, 'Assets')

def read_money_csv(path = os.path.join(ASSET_PATH, 'money.csv')):
    money_df = pd.read_csv(path, sep = ',', encoding = 'utf-8')
    money_df.index = range(1, money_df.shape[0] + 1)
    money_df = money_df.sort_index()
    return money_df

df = read_money_csv('E:\st-web\Assets\money.csv')
df_only = df[['Trần Minh Chiến', 'tiền Chiến']]

df_only.loc[len(df_only.index) + 1] = [1, 1]
df[['Trần Minh Chiến', 'tiền Chiến']] = df_only

print(df_only.head())
print(df.head())
