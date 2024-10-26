import pandas as pd
from pathlib import Path

from typing import TypedDict, Literal


class SalesColumns:
    STOCK_CODE: Literal["Stock Code"] = "Stock Code"
    DESCRIPTION: Literal["Description"] = "Description"
    QUANTITY: Literal["Quantity"] = "Quantity"
    NET_AMOUNT: Literal["Net Amount"] = "Net Amount"
    TAX_AMOUNT: Literal["Tax Amount"] = "Tax Amount"
    GROSS_AMOUNT: Literal["Gross Amount"] = "Gross Amount"


class SalesRecord(TypedDict):
    stock_code: str
    description: str
    quantity: int
    net_amount: float
    tax_amount: float
    gross_amount: float


class SalesSummary(TypedDict):
    total_records: int
    machine_records: int
    parts_records: int
    gross_machine_sales: float
    gross_part_sales: float
    top_selling_machines: pd.DataFrame
    top_selling_parts: pd.DataFrame


class SalesProcessor:
    machine_threshold: int = 1000
    columns: pd.DataFrame = ['Stock Code', 'Description', 'Quanitity', 'Net Amount', 'Tax Amount', 'Gross Amount']
    input_path: Path = Path('./spreadsheets/farmec-sales.csv')
    output_path: Path = Path('./data/')

    def __init__(self):
        self.df: pd.DataFrame = pd.read_csv(self.input_path, dtype={
            SalesColumns.STOCK_CODE: str,
            SalesColumns.DESCRIPTION: str,
            SalesColumns.QUANTITY: int,
            SalesColumns.NET_AMOUNT: float,
            SalesColumns.TAX_AMOUNT: float,
            SalesColumns.GROSS_AMOUNT: float,
        })

        if missing_columns := set(self.columns) - set(self.df.columns):
            raise ValueError(f"Missing required columns: {missing_columns}")

    def get_sales(self, is_machinery: bool) -> pd.DataFrame:
        return (self.df[self.df[SalesColumns.GROSS_AMOUNT] >= self.machine_threshold].copy()
                if is_machinery else self.df[self.df[SalesColumns.GROSS_AMOUNT] <= self.machine_threshold].copy())

    def process(self) -> SalesSummary:
        machinery_sales: pd.DataFrame = self.df[self.df['Gross Amount'] >= self.machine_threshold].copy()
        parts_sales: pd.DataFrame = self.df[self.df['Gross Amount'] <= self.machine_threshold].copy()

        machinery_sales.to_csv(self.output_path / 'machinery_sales.csv', index=False)
        parts_sales.to_csv(self.output_path / 'parts_sales.csv', index=False)

        summary: SalesSummary = SalesSummary(
            total_records=len(self.df),
            machine_records=len(machinery_sales),
            parts_records=len(parts_sales),
            gross_machine_sales=machinery_sales.groupby('Gross Amount').sum(),
            gross_part_sales=parts_sales.groupby('Gross Amount').sum(),
            top_selling_machines=machinery_sales.groupby('Stock Code')['Quanitity'].sum().sort_values(ascending=False).head(),
            top_selling_parts=parts_sales.groupby('Gross Amount')['Quanitity'].sum().sort_values(ascending=False).head(),
        )
        return summary


if __name__ == '__main__':
    processer = SalesProcessor()
    summary = processer.process()

    print("Total sales records:", summary['total_records'])
    print("Total machinery sales records:", summary['machine_records'])
    print("Total parts sales records:", summary['parts_records'])
    print("Gross machinery sales amount:", summary['gross_machine_sales'])
    print("Gross parts sales amount:", summary['gross_part_sales'])
    print("Top selling machinery products by quantity:\n", summary['top_selling_machines'])
    print("Top selling parts products by quantity:\n", summary['top_selling_parts'])
