from bdm_analysis.load_data import load_data_from_bigquery
from bdm_analysis.clean_data import clean_data
import pandas as pd

def main():
    """
    Executes the preprocessing pipeline:
    1. Loads data
    2. Cleans data
    3. Displays the first few rows
    """
    print("🚀 Starting the preprocessing pipeline...")
    df = load_data_from_bigquery()
    
    if df is not None:
        df = clean_data(df)
        print("📊 Data preview:")
        print(df.head())
    else:
        print("❌ Unable to proceed, data was not loaded.")

if __name__ == "__main__":
    main()
