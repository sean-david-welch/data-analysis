from pytest import TestCase

import pandas as pd
from pathlib import Path
from sales_processor import SalesProcessor, SalesColumns


class TestSalesProcessor(TestCase):
    def setUp(self):
        self.test_data: pd.DataFrame = pd.DataFrame({
            SalesColumns.STOCK_CODE: ['M001', 'M002', 'P001', 'P002', 'P003'],
            SalesColumns.DESCRIPTION: ['Machine 1', 'Machine 2', 'Part 1', 'Part 2', 'Part 3'],
            SalesColumns.QUANTITY: [1, 2, 10, 20, 30],
            SalesColumns.NET_AMOUNT: [1000, 2000, 100, 200, 300],
            SalesColumns.TAX_AMOUNT: [200, 400, 20, 40, 60],
            SalesColumns.GROSS_AMOUNT: [1200, 2400, 120, 240, 360]
        })

        self.temp_path = Path
