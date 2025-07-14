# src/utils.py

import pandas as pd

def load_sample_portfolio(filename):
    return pd.read_csv(filename)

def save_to_csv(df, filename):
    df.to_csv(filename, index=False)
