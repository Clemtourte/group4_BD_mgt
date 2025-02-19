import pandas as pd
import datetime
from currency_converter import CurrencyConverter

def convert_prices_to_eur(df):
    """
    Convert prices to euros using historical rates.
    
    Args:
        df (pd.DataFrame): DataFrame with price, currency and life_span_date columns
        
    Returns:
        pd.DataFrame: DataFrame with additional price_eur column
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
                conversion_date = datetime.strptime(str(row['life_span_date']).strip(), '%Y-%m-%d').date()
            
            converted_price = c.convert(price, base_currency, 'EUR', date=conversion_date)
            return converted_price
        except Exception as e:
            print(f"Error for uid {row.get('uid', 'Unknown')} with price={row['price']}, "
                  f"currency={row['currency']}, date={row['life_span_date']}: {e}")
            return None

    df['price_eur'] = df.apply(convert_row, axis=1)
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