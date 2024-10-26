import pandas as pd
from pathlib import Path


def process_sales_data():
    file_path = Path('./spreadsheets/farmec-sales.csv')
    df = pd.read_csv(file_path)

    machinery_sales = df[df['Gross Amount'] >= 1000].copy()
    parts_sales = df[df['Gross Amount'] <= 1000].copy()

    machinery_sales.to_csv('./data/machinery_sales.csv', index=False)
    parts_sales.to_csv('./data/parts_sales.csv', index=False)

    total_sales = len(df)
    total_machine_sales = len(machinery_sales)
    total_parts_sales = len(parts_sales)

    gross_machine_sales = machinery_sales['Gross Amount'].sum()
    gross_parts_sales = parts_sales['Gross Amount'].sum()

    top_selling_machine = machinery_sales.groupby('Stock Code')['Quantity'].sum().sort_values(ascending=False).head()
    top_selling_parts = parts_sales.groupby('Stock Code')['Quantity'].sum().sort_values(ascending=False).head()

    print("Total sales records:", total_sales)
    print("Total machinery sales records:", total_machine_sales)
    print("Total parts sales records:", total_parts_sales)
    print("Gross machinery sales amount:", gross_machine_sales)
    print("Gross parts sales amount:", gross_parts_sales)
    print("Top selling machinery products by quantity:\n", top_selling_machine)
    print("Top selling parts products by quantity:\n", top_selling_parts)


if __name__ == '__main__':
    process_sales_data()
