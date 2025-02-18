import pandas as pd

def clean_data(df):
    """
    Cleans the dataset by removing null values and outlier prices.
    """
    df = df.dropna(subset=['price'])  # Remove rows without prices
    df.loc[:, 'currency'] = df['currency'].str.strip().str.upper()  # Standardize currency encoding
    df = df[df['price'] > 0]  # Remove zero price values
    df = df[df['price'] <= 150000]  # Remove abnormally high prices

    # Remove useless columns
    columns_to_drop = ['price_before', 'price_difference', 'price_percent_change', 'price_changed', 'is_new']
    df = df.drop(columns=columns_to_drop, errors="ignore")  # Ignore si la colonne n'existe pas

    print("✅ Data cleaning completed.")
    return df
