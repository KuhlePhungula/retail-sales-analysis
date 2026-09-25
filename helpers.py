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


