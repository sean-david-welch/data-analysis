import os
import pandas as pd

from unittest import TestCase
from pandas.testing import assert_frame_equal

from sales_processor import SalesProcessor, SalesColumns


class TestSalesProcessor(TestCase):
    def setUp(self):
        os.makedirs('./data', exist_ok=True)
        self.test_data: pd.DataFrame = pd.DataFrame({
            SalesColumns.STOCK_CODE: ['M001', 'M002', 'P001', 'P002', 'P003'],
            SalesColumns.DESCRIPTION: ['Machine 1', 'Machine 2', 'Part 1', 'Part 2', 'Part 3'],
            SalesColumns.QUANTITY: [1, 2, 10, 20, 30],
            SalesColumns.NET_AMOUNT: [1000, 2000, 100, 200, 300],
            SalesColumns.TAX_AMOUNT: [200, 400, 20, 40, 60],
            SalesColumns.GROSS_AMOUNT: [1200, 2400, 120, 240, 360]
        })

        self.test_data.to_csv('./data/test_data.csv', index=False)
        self.processor: SalesProcessor = SalesProcessor()

    def test_initialization(self):
        assert_frame_equal(self.processor.df, self.test_data)
        assert self.processor.output_path.exists()

    def test_initialization_missing_columns(self):
        invalid_data = pd.DataFrame({
            'Invalid Column': [1, 2, 3]
        })
        invalid_path = self.tmp_path / 'invalid-sales.csv'
        invalid_data.to_csv(invalid_path, index=False)

        with self.assertRaises(ValueError) as context:
            processor = SalesProcessor()
            processor.input_path = invalid_path
        self.assertIn("Missing required columns", str(context.exception))

    def test_get_sales_machinery(self):
        machinery = self.processor.get_sales(is_machinery=True)

        self.assertEqual(len(machinery), 2)
        self.assertTrue(all(machinery[SalesColumns.STOCK_CODE].isin(['M001', 'M002'])))
        unit_prices = machinery[SalesColumns.GROSS_AMOUNT] / machinery[SalesColumns.QUANTITY]
        self.assertTrue(all(unit_prices >= self.processor.machine_threshold))

    def test_get_sales_parts(self):
        parts = self.processor.get_sales(is_machinery=False)

        self.assertEqual(len(parts), 3)
        self.assertTrue(all(parts[SalesColumns.STOCK_CODE].isin(['P001', 'P002', 'P003'])))
        unit_prices = parts[SalesColumns.GROSS_AMOUNT] / parts[SalesColumns.QUANTITY]
        self.assertTrue(all(unit_prices < self.processor.machine_threshold))

    def test_get_top_selling(self):
        parts = self.processor.get_sales(is_machinery=False)
        top_parts = self.processor.get_top_selling(parts)

        self.assertEqual(len(top_parts), 3)
        self.assertEqual(list(top_parts[SalesColumns.QUANTITY]), [30, 20, 10])
        self.assertEqual(list(top_parts[SalesColumns.STOCK_CODE]), ['P003', 'P002', 'P001'])

    def test_add_totals(self):
        parts = self.processor.get_sales(is_machinery=False)
        result = self.processor.add_totals(parts)

        self.assertEqual(len(result), len(parts) + 1)
        totals_row = result.iloc[-1]
        self.assertEqual(totals_row[SalesColumns.STOCK_CODE], 'TOTAL')
        self.assertEqual(totals_row[SalesColumns.QUANTITY], parts[SalesColumns.QUANTITY].sum())
        self.assertEqual(totals_row[SalesColumns.GROSS_AMOUNT], parts[SalesColumns.GROSS_AMOUNT].sum())

    def test_save_to_csv(self):
        parts = self.processor.get_sales(is_machinery=False)
        self.processor.save_to_csv(parts, 'test-output.csv')

        output_file = self.processor.output_path / 'test-output.csv'
        self.assertTrue(output_file.exists())

        saved_data = pd.read_csv(output_file)
        self.assertEqual(len(saved_data), len(parts) + 1)
        self.assertEqual(list(saved_data[SalesColumns.QUANTITY][:-1]), [30, 20, 10])

    def test_process_summary(self):
        summary = self.processor.process()

        self.assertEqual(summary['total_records'], 5)
        self.assertEqual(summary['machine_records'], 2)
        self.assertEqual(summary['parts_records'], 3)
        self.assertEqual(summary['gross_machine_sales'], 3600)
        self.assertEqual(summary['gross_part_sales'], 720)

        self.assertEqual(len(summary['top_selling_machines']), 2)
        self.assertEqual(len(summary['top_selling_parts']), 3)

        self.assertTrue((self.processor.output_path / 'machinery_sales.csv').exists())
        self.assertTrue((self.processor.output_path / 'parts_sales.csv').exists())

    def test_edge_case_zero_quantity(self):
        edge_data = pd.DataFrame({
            SalesColumns.STOCK_CODE: ['E001', 'E002', 'E003'],
            SalesColumns.DESCRIPTION: ['Edge 1', 'Edge 2', 'Edge 3'],
            SalesColumns.QUANTITY: [0, 1, 1],
            SalesColumns.NET_AMOUNT: [1000, 2000, 100],
            SalesColumns.TAX_AMOUNT: [200, 400, 20],
            SalesColumns.GROSS_AMOUNT: [1200, 2400, 120]
        })

        edge_path = self.tmp_path / 'edge-sales.csv'
        edge_data.to_csv(edge_path, index=False)

        processor = SalesProcessor()
        processor.input_path = edge_path
        processor.output_path = self.tmp_path / 'edge-output'

        machinery = processor.get_sales(is_machinery=True)
        self.assertEqual(len(machinery), 1)
        self.assertEqual(machinery[SalesColumns.STOCK_CODE].iloc[0], 'E002')
