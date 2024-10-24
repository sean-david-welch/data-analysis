import pandas as pd
from pathlib import Path

file_path = Path('../spreadsheets/farmec-sales.csv')
df = pd.read_csv(file_path)

top_selling = df.groupby('Stock Code')('Quanitity').sum().sort_values(ascending=format(ascending=False))
print('Top selling products by quantity')
print(top_selling.head())
