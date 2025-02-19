import pandas as pd
import datetime
from currency_converter import CurrencyConverter

def get_fallback_rates():
    """
    Taux de conversion moyens pour 2022.
    Les taux représentent la valeur en EUR d'une unité de devise étrangère.
    """
    return {
        'USD': 0.95,      # Taux moyen 2022
        'JPY': 0.0073,
        'GBP': 1.17,
        'CHF': 0.99,
        'SGD': 0.69,
        'HKD': 0.12,
        'CNY': 0.14,
        'KRW': 0.00074,
        'TWD': 0.032,
        'AED': 0.26
    }

def convert_prices_to_eur(df):
    """
    Convertit les prix en euros en utilisant CurrencyConverter quand possible,
    sinon utilise les taux moyens de 2022.
    """
    c = CurrencyConverter()
    fallback_rates = get_fallback_rates()
    
    def convert_row(row):
        try:
            if pd.isna(row['price']) or row['price'] <= 0:
                return None
                
            price = float(row['price'])
            currency = row['currency']
            
            # Si déjà en EUR, pas besoin de conversion
            if currency == 'EUR':
                return price
            
            # Date de conversion
            conversion_date = pd.to_datetime(row['life_span_date']).date()
            
            try:
                # Essai avec CurrencyConverter d'abord
                return c.convert(price, currency, 'EUR', date=conversion_date)
            except:
                # Si échec, utilisation des taux moyens
                if currency in fallback_rates:
                    return price * fallback_rates[currency]
                return None
                
        except Exception as e:
            return None

    df['price_eur'] = df.apply(convert_row, axis=1)
    
    # Statistiques de conversion
    conversions = {
        'Total rows': len(df),
        'Successful conversions': df['price_eur'].notna().sum(),
        'Failed conversions': df['price_eur'].isna().sum(),
    }
    
    print("\nConversion statistics:")
    for key, value in conversions.items():
        print(f"{key}: {value}")
    
    success_rate = (conversions['Successful conversions'] / conversions['Total rows']) * 100
    print(f"Success rate: {success_rate:.1f}%")
    
    return df

def clean_data(df):
    """
    Nettoie le dataset en appliquant des filtres de base et
    en standardisant les formats.
    """
    print("🧹 Starting data cleaning process...")
    
    df_clean = df.copy()
    initial_rows = len(df_clean)
    
    # 1. Nettoyage des collections
    print("1️⃣ Cleaning collections...")
    df_clean = df_clean[~df_clean['collection'].str.contains('HTTPS:', na=False)]
    
    # 2. Standardisation des champs
    print("2️⃣ Standardizing fields...")
    df_clean['currency'] = df_clean['currency'].str.strip().str.upper()
    df_clean['collection'] = df_clean['collection'].str.strip()
    df_clean['reference_code'] = df_clean['reference_code'].str.strip()
    
    # 3. Conversion des dates
    print("3️⃣ Converting dates...")
    df_clean['life_span_date'] = pd.to_datetime(df_clean['life_span_date'], errors='coerce')
    
    # 4. Suppression des valeurs manquantes critiques
    print("4️⃣ Handling missing values...")
    df_clean = df_clean.dropna(subset=['price', 'collection', 'reference_code', 'life_span_date'])
    
    # 5. Nettoyage des prix
    print("5️⃣ Cleaning prices...")
    df_clean = df_clean[df_clean['price'] > 0]
    df_clean = convert_prices_to_eur(df_clean)
    df_clean = df_clean.dropna(subset=['price_eur'])
    
    # 6. Colonnes temporelles
    print("6️⃣ Adding time columns...")
    df_clean['year'] = df_clean['life_span_date'].dt.year
    df_clean['quarter'] = df_clean['life_span_date'].dt.quarter
    
    # 7. Suppression des colonnes inutiles
    print("7️⃣ Removing unnecessary columns...")
    cols_to_drop = [
        'is_new', 'country', 'price_before',
        'price_changed', 'price_percent_change', 'price_difference'
    ]
    df_clean = df_clean.drop(columns=cols_to_drop, errors='ignore')
    
    # Résumé
    final_rows = len(df_clean)
    rows_removed = initial_rows - final_rows
    print(f"\n✅ Cleaning completed!")
    print(f"📊 Rows removed: {rows_removed} ({rows_removed/initial_rows*100:.1f}%)")
    print(f"📊 Final dataset: {final_rows} rows")
    
    return df_clean