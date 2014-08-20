from datetime import date
import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal
from django.test import TestCase
from ..pandas_utils import (create_pandas_dataframe, round_series_values, col_difference, sum_two_columns, 
                            create_dygraphs_error_str, check_for_nans_and_none)


class TestCreatePandasDataFrame(TestCase):
    
    def setUp(self):
        
        self.fake_data = [(date(2014, 1, 1), 23, None), (date(2014, 1, 2), 14, 15)]
        self.columns = ('date', 'A', 'B')
        self.fake_no_data = []
        
    def test_create_df(self):
        
        df = create_pandas_dataframe(self.fake_data, self.columns)
        df_shape = df.shape
        expected_shape = (2, 3)
        self.assertEqual(df_shape, expected_shape)
        df_columns = df.columns.values
        self.assertEqual(len(df_columns), 3)
        
    def test_fake_data(self):
        
        df = create_pandas_dataframe(self.fake_no_data, self.columns, True)
        df_shape = df.shape
        expected_shape = (1, 3)
        self.assertEqual(df_shape, expected_shape)
        
        
class TestRoundSeriesValues(TestCase):
    
    def setUp(self):
        
        self.fake_data = [(date(2013, 12, 14), 12.2012, None), (date(2013, 12, 15), 16.84928, 20.11111)]
        self.columns = ('date', 'A', 'B')
        
    def test_rounding(self):
        
        df = create_pandas_dataframe(self.fake_data, self.columns)
        df_rounded = df.applymap(round_series_values)
        expected_data = [(date(2013, 12, 14), 12.20, None), (date(2013, 12, 15), 16.85, 20.11)]
        df_expected = create_pandas_dataframe(expected_data, self.columns)
        df_equals = df_expected.equals(df_rounded)
        self.assertTrue(df_equals)
        

class TestColDifference(TestCase):
    
    def setUp(self):
        
        self.fake_data = [(date(2013, 3, 14), 29.58, None), (date(2013, 4, 15), 35.89, 21.32)]
        self.columns = ('date', 'A', 'B')
        
    def test_col_diff(self):
        
        df = create_pandas_dataframe(self.fake_data, self.columns)
        df['C'] = df.apply(col_difference, axis=1, col_x='A', col_y='B')
        expected_data = [(date(2013, 3, 14), 29.58, None, 29.58), (date(2013, 4, 15), 35.89, 21.32, 14.57)]
        df_expected = create_pandas_dataframe(expected_data, columns=('date', 'A', 'B', 'C'))
        # returns None if dataframes are equal
        df_equals = assert_frame_equal(df, df_expected)
        self.assertIsNone(df_equals)
        

class TestSumColumns(TestCase):
    
    def setUp(self):
        
        self.fake_data = [(date(2013, 4, 5), 16.91, 10.78), (date(2013, 5, 17), 11.34, None)]
        self.columns = ('date', 'A', 'B')
        
    def test_sum_two_columns(self):
        
        df = create_pandas_dataframe(self.fake_data, self.columns)
        df['C'] = df.apply(sum_two_columns, axis=1, col_x='A', col_y='B')
        expected_data = [(date(2013, 4, 5), 16.91, 10.78, 27.69), (date(2013, 5, 17), 11.34, None, 11.34)]
        df_expected = create_pandas_dataframe(expected_data, columns=('date', 'A', 'B', 'C'))
        # returns None if dataframes are equal
        df_equals = assert_frame_equal(df, df_expected)
        self.assertIsNone(df_equals)
        

class TestDygraphsErrorString(TestCase):
    
    def setUp(self):
        
        self.fake_data = [
                          (date(2013, 2, 1), 10.12, 12.56, 15.67),
                          (date(2013, 2, 2), 21.22, 24.56, 27.99),
                          (date(2013, 2, 3), None, 31.46, 34.01),
                          (date(2013, 2, 4), None, None, None)
                          ]
        self.columns = ('date', 'A', 'B', 'C')
        
    def test_dygraphs_err_str(self):
        
        df = create_pandas_dataframe(self.fake_data, self.columns)
        df['D'] = df.apply(create_dygraphs_error_str, axis=1, low='A', med='B', high='C')
        expected_data = [
                          (date(2013, 2, 1), 10.12, 12.56, 15.67, '10.12;12.56;15.67'),
                          (date(2013, 2, 2), 21.22, 24.56, 27.99, '21.22;24.56;27.99'),
                          (date(2013, 2, 3), None, 31.46, 34.01, None),
                          (date(2013, 2, 4), None, None, None, None)
                          ]
        df_expected = create_pandas_dataframe(expected_data, ('date', 'A', 'B', 'C', 'D'))
        df_equals = assert_frame_equal(df, df_expected)
        self.assertIsNone(df_equals)
        

class TestCheckForNaNs(TestCase):
    
    def setUp(self):
        
        self.no_nans = [23.91, 23.12, 82.33]
        self.single_nan = [np.nan, 17.84, 99.12]
        self.single_nat = [pd.NaT, 90.21, 0.391]
        self.single_none = [None, 390.231, 1.23]
        
    def test_no_nan(self):
        
        result = check_for_nans_and_none(self.no_nans)
        self.assertFalse(result)
        
    def test_nan(self):
        
        result = check_for_nans_and_none(self.single_nan)
        self.assertTrue(result)
        
    def test_nat(self):
        
        result = check_for_nans_and_none(self.single_nat)
        self.assertTrue(result)
        
    def test_none(self):
        
        result = check_for_nans_and_none(self.single_none)
        self.assertTrue(result)