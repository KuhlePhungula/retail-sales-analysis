# Functions for loading, cleaning, and reporting on the retail sales dataset

import pandas as pd
from datetime import datetime

# Load the raw CSV into a dataframe
def load_data(filepath):
    return pd.read_csv(filepath)

