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

