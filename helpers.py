# Functions for loading, cleaning, and reporting on the retail sales dataset

import pandas as pd
from datetime import datetime

# Load the raw CSV into a dataframe
def load_data(filepath):
    return pd.read_csv(filepath)

# detect missing quantity - keep the ones with a valid quantity in a list via .append() and drop the rest
def drop_missing_quantity(df):

    clean_rows = []
    removed = 0

    for row in df.to_dict('records'):
        if pd.isna(row['quantity']):
            removed += 1
        else:
            clean_rows.append(row)

    return pd.DataFrame(clean_rows), removed

# loop over each row and try convert unit_price to a float. Keep rows where the conversion is successful and drop and count the ones that fail
def clean_price_column(df):

    clean_rows = []
    removed = 0

    for row in df.to_dict('records'):
        try:
            row['unit_price'] = float(row['unit_price'])
            clean_rows.append(row)
        except (ValueError, TypeError):
            removed += 1

    return pd.DataFrame(clean_rows), removed

# A sale can't be negative so we loop over each row and keep the ones with quantity >= 0. drop and count the negative quantities
def remove_negative_quantity(df):

    clean_rows = []
    removed = 0

    for row in df.to_dict('records'):
        if row['quantity'] < 0:
            removed += 1
        else:
            clean_rows.append(row)

    return pd.DataFrame(clean_rows), removed 

# Loop over each row, keeping track of rows already seen in a list. The first time a row appears, it's kept vis .append() and exact repeat is dropped and counted
def remove_duplicate_rows(df):

    clean_rows = []
    removed = 0

    for row in df.to_dict('records'):
        if row in clean_rows:
            removed += 1
        else:
            clean_rows.append(row)

    return pd.DataFrame(clean_rows), removed

# Try to parse a date value that might be in one of the known formats 
def parse_date_flexible(date_value):

    date_str = str(date_value).strip()
    known_formats = ['%Y-%m-%d', '%m/%d/%Y']

    for fmt in known_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    return None

# Apply parse_date_flexible. Rows that fial to pass are dropped
def parse_dates_column(df, column='date'):

    before = len(df)
    df[column] = df[column].apply(parse_date_flexible)
    df = df.dropna(subset=[column])
    removed = before - len(df)

    return df, removed

# Strip blank space and standardise
def standardise_text_columns(df, columns):

    for col in columns:
        df[col] = df[col].astype(str).str.strip().str.title()
    return df

# run full cleaning
def clean_dataset(df, text_columns=None, date_columns='date'):

    if text_columns is None:
        text_columns = ['store', 'category', 'payment_method', 'product_name']

    starting_rows = len(df)
    removal_log = {}

    df, removed = drop_missing_quantity(df)
    removal_log['missing quantity'] = removed

    df, removed = clean_price_column(df)
    removal_log['non-numeric price'] = removed

    df, removed = remove_negative_quantity(df)
    removal_log['negative quantity'] = removed

    df, removed = remove_duplicate_rows(df)
    removal_log['duplicate rows'] = removed

    df = standardise_text_columns(df, text_columns)

    df, removed = parse_dates_column(df)
    removal_log['unparseable dates'] = removed

    return df, removal_log, starting_rows

def print_quality_report(starting_rows, removal_log, clean_rows):

    print("DATA QUALITY REPORT")
    print("=" * 30)
    print(f"Starting rows: {starting_rows}")
    for reason, count in removal_log.items():
        print(f"Removed for {reason}: {count}")
    print(f"Total rows removed: {starting_rows - clean_rows}")
    print(f"Clean rows remaining: {clean_rows}")





# Descriptive Analysis

# add a revenue column
def calculate_revenue(df):
    df['revenue'] = df['quantity'] * df['unit_price']
    return df

# total revenue across all stores
def total_revenue(df):
    return df['revenue'].sum()

# revenue per category, ranked highest to lowest
def revenue_by_category(df):
    return df.groupby('category')['revenue'].sum().sort_values(ascending=False)

# revenue per store, ranked highest to lowest
def revenue_by_store(df):
    return df.groupby('store')['revenue'].sum().sort_values(ascending=False)

# best selling product with the highest total units sold
def best_selling_product_by_quantity(df):
    by_qty = df.groupby('product_name')['revenue'].sum().sort_values(ascending=False)
    return by_qty.index[0], by_qty.iloc[0]

# single product with the highest total revenue
def highest_earning_product_by_revenue(df):
    by_rev = df.grouby('product_name')['revenue'].sum().sort_values(ascending=False)
    return by_rev.index[0], by_rev.iloc[0]

# revenue summed by month
def revenue_by_month(df, date_columns='date'):
    month_period = df[date_columns].dt.to_period('M')
    return df.groupby(month_period)['revenue'].sum().sort_index()

# mean revenue per transaction
def average_transaction_value(df):
    return df['revenue'].mean()

# payment methods used in mosttransactions
def most_common_payment_method(df):
    counts = df['payment_method'].value_counts()
    return counts.index[0], counts.iloc[0]


