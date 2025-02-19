import pandas as pd
import datetime
from currency_converter import CurrencyConverter

def get_fallback_rates():
    """
    Returns fallback exchange rates to EUR from European Central Bank (2022 averages).
    Each rate represents how many EUR one unit of foreign currency is worth.
    Source: https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/
    """
    return {
        'USD': 0.9497,    # 1 USD = 0.9497 EUR
        'JPY': 0.00725,   # 1 JPY = 0.00725 EUR
        'GBP': 1.1726,    # 1 GBP = 1.1726 EUR
        'CNY': 0.1413,    # 1 CNY = 0.1413 EUR
        'HKD': 0.1216,    # 1 HKD = 0.1216 EUR
        'SGD': 0.6891,    # 1 SGD = 0.6891 EUR
        'KRW': 0.000736,  # 1 KRW = 0.000736 EUR
        'TWD': 0.0320,    # 1 TWD = 0.0320 EUR
        'AED': 0.2585,    # 1 AED = 0.2585 EUR
        'CHF': 0.9955     # 1 CHF = 0.9955 EUR
    }

def convert_price_with_rate(price, currency, fallback_rates):
    """
    Converts price to EUR using fallback rates.
    Multiplies by the rate as the rates are expressed in EUR per unit of foreign currency.
    """
    if currency == 'EUR':
        return price
        
    if currency not in fallback_rates:
        return None
        
    return price * fallback_rates[currency]

def convert_prices_to_eur(df):
    """
    Convert prices to euros using historical rates when available,
    falling back to ECB rates when necessary.
    
    Args:
        df (pd.DataFrame): DataFrame with price, currency and life_span_date columns
        
    Returns:
        pd.DataFrame: DataFrame with additional price_eur column
    """
    c = CurrencyConverter()
    fallback_rates = get_fallback_rates()
    
    def convert_row(row):
        try:
            price = float(row['price'])
            base_currency = row['currency']
            
            # Get the date
            if isinstance(row['life_span_date'], pd.Timestamp):
                conversion_date = row['life_span_date'].date()
            else:
                conversion_date = pd.to_datetime(row['life_span_date']).date()
            
            try:
                # Try with CurrencyConverter first
                converted_price = c.convert(price, base_currency, 'EUR', date=conversion_date)
                return converted_price
            except:
                # If that fails, use ECB rates
                converted_price = convert_price_with_rate(price, base_currency, fallback_rates)
                if converted_price is not None:
                    return converted_price
                else:
                    print(f"No conversion rate available for {base_currency}")
                    return None
                
        except Exception as e:
            print(f"Error converting price for uid {row.get('uid', 'Unknown')}: {str(e)}")
            return None

    df['price_eur'] = df.apply(convert_row, axis=1)
    
    # Log conversion statistics
    conversions_by_method = {
        'Currency Converter': sum((df['price_eur'].notna()) & (df['currency'] != 'EUR')),
        'ECB Rates': sum(df['currency'].isin(fallback_rates.keys()) & df['price_eur'].notna()),
        'Already EUR': sum(df['currency'] == 'EUR'),
        'Failed': sum(df['price_eur'].isna())
    }
    
    print("\nConversion statistics:")
    for method, count in conversions_by_method.items():
        print(f"{method}: {count} rows")
    
    success_rate = (df['price_eur'].notna().sum() / len(df)) * 100
    print(f"Overall success rate: {success_rate:.1f}%")
    
    return df

def clean_data(df):
    """
    Cleans the dataset by removing invalid entries and standardizing formats.
    
    Args:
        df (pd.DataFrame): Raw dataframe from BigQuery
        
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    print("🧹 Starting data cleaning process...")
    
    # Create a copy
    df_clean = df.copy()
    initial_rows = len(df_clean)
    
    # 1. Remove HTTPS collection
    print("1️⃣ Removing HTTPS collection...")
    rows_before = len(df_clean)
    df_clean = df_clean[~df_clean['collection'].str.contains('HTTPS:', na=False)]
    rows_removed = rows_before - len(df_clean)
    print(f"   Removed {rows_removed} rows with HTTPS collection")
    
    # 2. Clean basic fields
    print("2️⃣ Cleaning basic fields...")
    df_clean['currency'] = df_clean['currency'].str.strip().str.upper()
    df_clean['collection'] = df_clean['collection'].str.strip()
    df_clean['reference_code'] = df_clean['reference_code'].str.strip()
    
    # 3. Standardize dates
    print("3️⃣ Standardizing dates...")
    df_clean['life_span_date'] = pd.to_datetime(df_clean['life_span_date'], errors='coerce')
    
    # 4. Handle missing values
    print("4️⃣ Handling missing values...")
    rows_before = len(df_clean)
    df_clean = df_clean.dropna(subset=['price', 'collection', 'reference_code', 'life_span_date'])
    rows_removed = rows_before - len(df_clean)
    print(f"   Removed {rows_removed} rows with missing critical values")
    
    # 5. Convert and clean prices
    print("5️⃣ Converting and cleaning prices...")
    rows_before = len(df_clean)
    
    # Remove zero or negative prices
    df_clean = df_clean[df_clean['price'] > 0]
    
    # Convert to EUR
    df_clean = convert_prices_to_eur(df_clean)
    
    # Keep only rows where conversion succeeded
    df_clean = df_clean.dropna(subset=['price_eur'])
    
    # Log unsuccessful conversions
    rows_removed = rows_before - len(df_clean)
    print(f"   Could not convert {rows_removed} prices to EUR")
    
    # 6. Add derived columns
    print("6️⃣ Adding derived columns...")
    df_clean['year'] = df_clean['life_span_date'].dt.year
    df_clean['quarter'] = df_clean['life_span_date'].dt.quarter
    
    # 7. Drop unnecessary columns
    print("7️⃣ Removing unnecessary columns...")
    columns_to_drop = [
        'is_new',  # All null
        'country',  # All null
        'price_before',  # Partially null
        'price_changed',
        'price_percent_change',
        'price_difference'  # We'll focus on actual prices and their EUR conversion
    ]
    df_clean = df_clean.drop(columns=columns_to_drop, errors='ignore')
    
    total_rows_removed = initial_rows - len(df_clean)
    print("\n✅ Cleaning completed!")
    print(f"📊 Total rows removed: {total_rows_removed} ({(total_rows_removed/initial_rows*100):.1f}%)")
    print(f"📊 Final dataset: {len(df_clean)} rows")
    
    return df_clean