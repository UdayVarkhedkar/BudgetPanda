import pandas as pd
from pandas import Timestamp as panda_time
import calendar

from filter_helpers import get_date_filter, get_category_filter, get_credit_filter, get_debit_filter


TRANSACTION_CSV_PATH = '~/Documents/Budgeting/transactions.csv'
DATE_RANGE_FROM = '2018-10-01'
DATE_RANGE_TO = '2018-11-01'
COLUMN_ORDER = ['Account Name', 'Category', 'Date', 'Description', 'Amount', 'Transaction Type']
CATEGORY_DICT = {
    "Groceries": ["Groceries"],
    "Restaurants": ["Fast Food", "Restaurants", "Alcohol"],
    "Coffee": ["Coffee shops"],
    "Utilities": ["Internet", "Utilities", "Mobile Phone"],
    "Transportation": ["Gas & Fuel", "Parking", "Auto Insurance"],
    "Experiences": ["Air Travel", "Hotel", "Sports", "Entertainment"],
    "Material Goods": ["Clothing", "Books", "Electronics and Software", "Hobbies", "Sporting Goods"],
    "Health": ["Dentist", "Doctor", "Eye care", "Pharmacy", "Health Insurance"]
}

class BudgetPanda():
    def __init__(self):
        self.transaction_df = pd.read_csv(TRANSACTION_CSV_PATH)
        self.transaction_df = self.initial_column_processing(self.transaction_df)

    def initial_column_processing(self, df):
        """Processes columns of Pandas Dataframe on Initialization"""
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.drop(['Original Description', 'Labels', 'Notes'], axis=1)
        df = df.reindex(columns=COLUMN_ORDER)
        return df

    def get_range_df(self, df, date_from, date_to):
        return df[get_date_filter(df, date_from, date_to)]

    def get_credit_df(self, df):
        df = df[get_credit_filter(df)]
        return df.drop('Transaction Type', axis=1)

    def get_debit_df(self, df):
        df = df[get_debit_filter(df)]
        return df.drop('Transaction Type', axis=1)

    def get_category_df(self, df, category):
        return df[get_category_filter(df, category, CATEGORY_DICT)]

    def get_category_keys(self):
        return CATEGORY_DICT.keys()

    def get_current_month_df(self, df):
        today = pd.Timestamp.today()
        month_beginning = pd.Timestamp(today.year, today.month, 1)
        return self.get_range_df(df, month_beginning, today)

    def get_last_month_df(self, df):
        today = pd.Timestamp.today()
        month_beginning = pd.Timestamp(today.year, today.month-1, 1)
        month_end = pd.Timestamp(today.year, today.month, 1)
        return self.get_range_df(df, month_beginning, month_end)
        