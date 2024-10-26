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
    columns: list = ['Stock Code', 'Description', 'Quantity', 'Net Amount', 'Tax Amount', 'Gross Amount']
    input_path: Path = Path('./spreadsheets/farmec-sales.csv')
    output_path: Path = Path('./data/')

    def __init__(self):
        self.df: pd.DataFrame = pd.read_csv(self.input_path, dtype={
            SalesColumns.STOCK_CODE: str,
            SalesColumns.DESCRIPTION: str,
            SalesColumns.QUANTITY: 'float64',
            SalesColumns.NET_AMOUNT: float,
            SalesColumns.TAX_AMOUNT: float,
            SalesColumns.GROSS_AMOUNT: float,
        })

        if missing_columns := set(self.columns) - set(self.df.columns):
            raise ValueError(f"Missing required columns: {missing_columns}")

    def get_sales(self, is_machinery: bool) -> pd.DataFrame:
        return (self.df[self.df[SalesColumns.GROSS_AMOUNT] >= self.machine_threshold].copy()
                if is_machinery else self.df[self.df[SalesColumns.GROSS_AMOUNT] < self.machine_threshold].copy())

    def get_top_selling(self, df: pd.DataFrame):
        return df.groupby(SalesColumns.STOCK_CODE)[SalesColumns.QUANTITY].sum().sort_values(ascending=False).head()

    def process(self) -> SalesSummary:
        machinery_sales: pd.DataFrame = self.get_sales(is_machinery=True)
        parts_sales: pd.DataFrame = self.get_sales(is_machinery=False)

        machinery_sales.to_csv(self.output_path / 'machinery_sales.csv', index=False)
        parts_sales.to_csv(self.output_path / 'parts_sales.csv', index=False)

        summary: SalesSummary = SalesSummary(
            total_records=len(self.df),
            machine_records=len(machinery_sales),
            parts_records=len(parts_sales),
            gross_machine_sales=machinery_sales['Gross Amount'].sum(),
            gross_part_sales=parts_sales['Gross Amount'].sum(),
            top_selling_machines=self.get_top_selling(machinery_sales),
            top_selling_parts=self.get_top_selling(parts_sales),
        )
        return summary


def main():
    processor = SalesProcessor()
    summary = processor.process()

    print(f"Total sales records: {summary['total_records']:,}")
    print(f"Total machinery sales records: {summary['machine_records']:,}")
    print(f"Total parts sales records: {summary['parts_records']:,}")
    print(f"Gross machinery sales amount: €{summary['gross_machine_sales']:,.2f}")
    print(f"Gross parts sales amount: €{summary['gross_part_sales']:,.2f}")
    print("\nTop selling machinery products by quantity:")
    print(summary['top_selling_machines'])
    print("\nTop selling parts products by quantity:")
    print(summary['top_selling_parts'])


if __name__ == '__main__':
    main()
