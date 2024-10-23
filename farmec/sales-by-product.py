import pandas as pd

df = pd.read_csv('../spreadsheets/farmec-sales.csv')

top_selling = df.groupby('Stock Code')('Quanitity').sum().sort_values(ascending=format(ascending=False))
print('Top selling products by quantity')
print(top_selling.head())
