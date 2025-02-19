import pandas as pd
import datetime
from currency_converter import CurrencyConverter

def convert_prices_to_eur(df):
    """
    convert prices to euros
    """
    c = CurrencyConverter()
    
    def convert_row(row):
        try:
            price = float(row['price'])
            base_currency = row['currency']
            
            
            if isinstance(row['life_span_date'], pd.Timestamp):
                conversion_date = row['life_span_date'].date()
            elif isinstance(row['life_span_date'], str):
                conversion_date = datetime.strptime(row['life_span_date'].strip(), '%Y-%m-%d').date()
            else:
                # Convert by default
                conversion_date = datetime.strptime(str(row['life_span_date']).strip(), '%Y-%m-%d').date()
            
            converted_price = c.convert(price, base_currency, 'EUR', date=conversion_date)
            return converted_price
        except Exception as e:
            print(f"Erreur pour l'uid {row.get('uid', 'Inconnu')} avec price={row['price']}, "
                  f"currency={row['currency']}, date={row['life_span_date']}: {e}")
            return None

    df['currency_converted'] = df.apply(convert_row, axis=1)
    return df

def clean_data(df):
    """
    Cleans the dataset by removing null values and outlier prices.
    """
    df = df.dropna(subset=['price'])  # Remove rows without prices
    df.loc[:, 'currency'] = df['currency'].str.strip().str.upper()  # Standardize currency encoding
    df = df[df['price'] > 0]  # Remove zero price values
    df = convert_prices_to_eur(df)
    print(df['currency_converted'])
    df = df[df['price'] <= 150000]  # Remove abnormally high prices
    # Remove useless columns
    columns_to_drop = ['price_before', 'price_difference', 'price_percent_change', 'price_changed', 'is_new']
    df = df.drop(columns=columns_to_drop, errors="ignore")  # Ignore si la colonne n'existe pas

    print("✅ Data cleaning completed.")
    return df
