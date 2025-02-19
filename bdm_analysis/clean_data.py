import pandas as pd

def clean_data(df):
    """
    Cleans the dataset by handling missing values, standardizing formats,
    and removing invalid entries.
    
    Args:
        df (pd.DataFrame): Raw dataframe from BigQuery
    
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    print("🧹 Starting data cleaning process...")
    
    # Create a copy to avoid modifying the original
    df_clean = df.copy()
    
    # Basic cleaning steps
    print("1️⃣ Cleaning basic fields...")
    df_clean['currency'] = df_clean['currency'].str.strip().str.upper()
    df_clean['collection'] = df_clean['collection'].str.strip()
    df_clean['reference_code'] = df_clean['reference_code'].str.strip()
    
    # Handle missing values
    print("2️⃣ Handling missing values...")
    # Remove rows without essential data
    df_clean = df_clean.dropna(subset=['price', 'collection', 'reference_code'])
    
    # Price related cleaning
    print("3️⃣ Cleaning price data...")
    # Remove invalid prices
    df_clean = df_clean[df_clean['price'] > 0]
    df_clean = df_clean[df_clean['price'] <= 150000]  # Remove abnormally high prices
    
    # Convert price_difference to numeric if not already
    if df_clean['price_difference'].dtype == 'object':
        df_clean['price_difference'] = pd.to_numeric(df_clean['price_difference'], errors='coerce')
    
    # Clean and standardize dates
    print("4️⃣ Standardizing dates...")
    df_clean['life_span_date'] = pd.to_datetime(df_clean['life_span_date'], errors='coerce')
    
    # Add derived columns
    print("5️⃣ Adding derived columns...")
    # Extract year and quarter from life_span_date
    df_clean['year'] = df_clean['life_span_date'].dt.year
    df_clean['quarter'] = df_clean['life_span_date'].dt.quarter
    
    # Calculate price changes where possible
    df_clean['has_price_change'] = df_clean['price_difference'].notna() & (df_clean['price_difference'] != 0)
    
    # Drop unnecessary columns
    print("6️⃣ Removing unnecessary columns...")
    columns_to_drop = [
        'is_new',  # All null
        'country',  # All null
        'price_before',  # Partially null, can be derived if needed
        'price_changed', # Redundant with has_price_change
        'price_percent_change'  # Can be recalculated if needed
    ]
    df_clean = df_clean.drop(columns=columns_to_drop, errors='ignore')
    
    # Final validation
    print("7️⃣ Performing final validation...")
    # Ensure no null values in critical columns
    critical_columns = ['price', 'collection', 'reference_code', 'life_span_date']
    if df_clean[critical_columns].isnull().any().any():
        print("⚠️ Warning: Still have null values in critical columns!")
    
    print("✅ Data cleaning completed!")
    print(f"📊 Rows remaining: {len(df_clean)} out of {len(df)} original rows")
    
    return df_clean