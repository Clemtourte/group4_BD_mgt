import pandas as pd
import os

def aggregate_to_csv(df):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'csv', 'summary.csv')
    df.to_csv(csv_path, index=False)