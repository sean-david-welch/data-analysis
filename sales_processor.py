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
    top_selling_machines: pd.Series
    top_selling_parts: pd.Series


class SalesProcessor:
    machine_threshold: int = 1000
    numerical_cols: list[str] = [SalesColumns.QUANTITY, SalesColumns.NET_AMOUNT, SalesColumns.TAX_AMOUNT, SalesColumns.GROSS_AMOUNT]
    input_path: Path = Path('./spreadsheets/farmec-sales.csv')
    output_path: Path = Path('./data/')

    def __init__(self):
        self.output_path.mkdir(parents=True, exist_ok=True)

        self.df: pd.DataFrame = pd.read_csv(self.input_path, dtype={
            SalesColumns.STOCK_CODE: str,
            SalesColumns.DESCRIPTION: str,
            SalesColumns.QUANTITY: 'float64',
            SalesColumns.NET_AMOUNT: float,
            SalesColumns.TAX_AMOUNT: float,
            SalesColumns.GROSS_AMOUNT: float,
        })

        required_columns = [
            SalesColumns.STOCK_CODE,
            SalesColumns.DESCRIPTION,
            SalesColumns.QUANTITY,
            SalesColumns.NET_AMOUNT,
            SalesColumns.TAX_AMOUNT,
            SalesColumns.GROSS_AMOUNT
        ]

        if missing_columns := set(required_columns) - set(self.df.columns):
            raise ValueError(f"Missing required columns: {missing_columns}")

    def get_sales(self, is_machinery: bool) -> pd.DataFrame:
        unit_prices = (
            self.df[SalesColumns.GROSS_AMOUNT].div(self.df[SalesColumns.QUANTITY])
            .replace([float('inf'), float('-inf')], float('nan'))
            .fillna(0)
        )
        return (self.df[unit_prices >= self.machine_threshold].copy()
                if is_machinery else self.df[unit_prices <= self.machine_threshold].copy())

    def get_top_selling(self, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby([SalesColumns.STOCK_CODE, SalesColumns.DESCRIPTION])[SalesColumns.QUANTITY]
            .sum()
            .reset_index()
            .sort_values(by=SalesColumns.QUANTITY, ascending=False)
            .head()
        )

    def add_totals(self, df: pd.DataFrame) -> pd.DataFrame:
        totals: pd.Series = pd.Series({
            SalesColumns.STOCK_CODE: 'TOTAL',
            SalesColumns.DESCRIPTION: '',
            **{col: df[col].sum() for col in self.numerical_cols}
        })
        return pd.concat([df, pd.DataFrame([totals])], ignore_index=True)

    def save_to_csv(self, df: pd.DataFrame, filename: str) -> pd.Series:
        df_sorted = df.sort_values(by=SalesColumns.QUANTITY, ascending=False)
        df_with_totals = self.add_totals(df_sorted)
        df_with_totals.to_csv(self.output_path / filename, index=False, float_format='%.2f')

    def process(self) -> SalesSummary:
        machinery_sales: pd.DataFrame = self.get_sales(is_machinery=True)
        parts_sales: pd.DataFrame = self.get_sales(is_machinery=False)

        self.save_to_csv(machinery_sales, 'machinery_sales.csv')
        self.save_to_csv(parts_sales, 'parts_sales.csv')

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
