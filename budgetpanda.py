import pandas as pd
import calendar

from filter_helpers import get_date_filter, get_category_filter, get_credit_filter, get_debit_filter


TRANSACTION_CSV_PATH = '~/Documents/Budgeting/transactions.csv'
COLUMN_ORDER = ['Account Name', 'Category', 'Date', 'Description', 'Amount', 'Transaction Type']
CATEGORY_MAP = {
    "Groceries": "Groceries",
    "Fast Food": "Restaurants",
    "Restaurants": "Restaurants",
    "Alcohol": "Restaurants",
    "Food & Dining": "Restaurants",
    "Coffee Shops": "Coffee",
    "Coffee": "Coffee",
    "Internet": "Utilities",
    "Home Insurance": "Utilities",
    "Utilities": "Utilities",
    "Gas & Fuel": "Transportation",
    "Parking": "Transportation",
    "Auto Insurance": "Transportation",
    "Transportation": "Transportation",
    "Air Travel": "Experiences",
    "Hotel": "Experiences",
    "Sports": "Experiences",
    "Entertainment": "Experiences",
    "Experiences": "Experiences",
    "Clothing": "Material Goods",
    "Books": "Material Goods",
    "Electronics & Software": "Material Goods",
    "Hobbies": "Material Goods",
    "Sporting Goods": "Material Goods",
    "Shopping": "Material Goods",
    "Material Goods": "Material Goods",
    "Dentist": "Health",
    "Doctor": "Health",
    "Eye care": "Health",
    "Pharmacy": "Health",
    "Health Insurance": "Health",
    "Health & Fitness": "Health",
    "Health": "Health",
    "Movies & DVDs": "Recurring",
    "Newspapers & Magazines": "Recurring",
    "Gym": "Recurring",
    "Television": "Recurring",
    "Mobile Phone": "Recurring",
    "Hair": "Recurring",
    "Mortgage & Rent": "Rent",
    "Interest Income": "Income",
    "Income": "Income",
    "Transfer": "Transfer",
    "Credit Card Payment": "Credit Card Payment"
}

class BudgetPanda():
    def __init__(self):
        self.transaction_df = pd.read_csv(TRANSACTION_CSV_PATH)
        self.transaction_df = self.initial_column_processing(self.transaction_df)

    def initial_column_processing(self, df):
        """Processes columns of Pandas Dataframe on Initialization"""
        df['Date'] = pd.to_datetime(df['Date'])
        df['Category'] = df['Category'].map(CATEGORY_MAP)
        df = df.drop(['Original Description', 'Labels', 'Notes'], axis=1)
        df = df.reindex(columns=COLUMN_ORDER)
        df = df.sort_values(by="Date")
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
        return df[get_category_filter(df, category)]

    def get_category_keys(self):
        return CATEGORY_MAP.keys()

    def get_current_month_df(self, df):
        today = pd.Timestamp.today()
        month_beginning = pd.Timestamp(today.year, today.month, 1)
        return self.get_range_df(df, month_beginning, today)

    def get_last_month_df(self, df):
        today = pd.Timestamp.today()
        if today.month == 1:
            month_beginning = pd.Timestamp(today.year-1, 12, 1)
            month_end = pd.Timestamp(today.year, today.month, 1)
        else:
            month_beginning = pd.Timestamp(today.year, today.month-1, 1)
            month_end = pd.Timestamp(today.year, today.month, 1)
        return self.get_range_df(df, month_beginning, month_end)
