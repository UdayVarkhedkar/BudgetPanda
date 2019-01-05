import pandas as pd

def get_date_filter(df, date_from, date_to):
    if isinstance(date_from, str):
        date_from = pd.Timestamp.strptime(date_from, '%Y-%m-%d')
    if isinstance(date_to, str):
        date_to = pd.Timestamp.strptime(date_to, '%Y-%m-%d')
    date_filter = ((df['Date'] >= date_from) & (df['Date'] < date_to))
    return date_filter

def get_credit_filter(df):
    return (df['Transaction Type'] == 'credit')

def get_debit_filter(df):
    return (df['Transaction Type'] == 'debit')

def get_category_filter(df, category, category_dict):
    return (df['Category'].isin(category_dict[category]))
    