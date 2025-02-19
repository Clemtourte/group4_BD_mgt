import pandas as pd

def verify_dataset_metrics(df):
    """
    Verify and display key dataset metrics.
    """
    print("\nVerifying dataset metrics:")
    
    # Unique references
    n_refs = df['reference_code'].nunique()
    print(f"\n1. Number of unique references: {n_refs}")
    print("\nReference examples:")
    print(df['reference_code'].unique()[:5])
    
    # Unique currencies
    n_currencies = df['currency'].nunique()
    print(f"\n2. Number of unique currencies: {n_currencies}")
    print("\nCurrencies present:")
    print(df['currency'].unique())
    
    # Unique dates
    n_dates = df['life_span_date'].nunique()
    print(f"\n3. Number of unique dates: {n_dates}")
    print("\nAvailable dates:")
    print(sorted(df['life_span_date'].unique()))
    
    return {
        'n_references': n_refs,
        'n_currencies': n_currencies,
        'n_dates': n_dates
    }

def analyze_collections(df):
    """
    Statistical analysis by collection.
    """
    stats = df.groupby('collection').agg({
        'reference_code': 'count',
        'price_eur': ['mean', 'min', 'max', 'std']
    }).round(2)
    
    stats.columns = [
        'model_count', 
        'avg_price_eur', 
        'min_price_eur', 
        'max_price_eur', 
        'price_std_eur'
    ]
    return stats.reset_index()

def analyze_price_ranges(df):
    """
    Price range segmentation.
    """
    price_bins = [0, 10000, 25000, 50000, float('inf')]
    labels = ['Entry Level', 'Mid Range', 'High End', 'Ultra Luxury']
    
    df['price_category'] = pd.cut(
        df['price_eur'],
        bins=price_bins,
        labels=labels
    )
    
    ranges = df.groupby('price_category', observed=True).agg({
        'reference_code': ['count', 'nunique'],
        'price_eur': 'mean',
        'collection': 'nunique'
    }).round(2)
    
    ranges.columns = [
        'model_count', 
        'unique_references', 
        'avg_price_eur', 
        'unique_collections'
    ]
    return ranges.reset_index()

def analyze_time_trends(df):
    """
    Temporal trend analysis.
    """
    df['year_quarter'] = pd.to_datetime(df['life_span_date']).dt.to_period('Q')
    
    trends = df.groupby('year_quarter').agg({
        'price_eur': ['mean', 'count'],
        'reference_code': 'nunique',
        'collection': 'nunique'
    }).round(2)
    
    trends.columns = [
        'avg_price_eur', 
        'model_count', 
        'unique_references', 
        'unique_collections'
    ]
    
    return trends.reset_index()

def create_price_reference_matrix(df):
    """
    Create a price reference matrix by currency.
    """
    matrix = df.pivot_table(
        index=['reference_code', 'life_span_date'],
        columns='currency',
        values='price',
        aggfunc='first'
    ).reset_index()
    
    return matrix

def analyze_currency_variations(df):
    """
    Analyze price variations between currencies.
    """
    latest_prices = df.sort_values('life_span_date').groupby('reference_code').last()
    
    summary = {
        'avg_eur_price': latest_prices['price_eur'].mean(),
        'min_eur_price': latest_prices['price_eur'].min(),
        'max_eur_price': latest_prices['price_eur'].max(),
        'price_std_eur': latest_prices['price_eur'].std(),
        'total_references': len(latest_prices),
        'currencies_count': df['currency'].nunique(),
        'date_range': f"{df['life_span_date'].min()} - {df['life_span_date'].max()}"
    }
    
    return summary

def generate_summary_stats(df):
    """
    Generate global dataset statistics.
    """
    summary = {
        'total_models': df['reference_code'].nunique(),
        'total_collections': df['collection'].nunique(),
        'avg_price_eur': df['price_eur'].mean().round(2),
        'price_range_eur': f"{df['price_eur'].min():.2f} - {df['price_eur'].max():.2f}",
        'most_common_collection': df['collection'].mode().iloc[0],
        'date_range': f"{df['life_span_date'].min()} - {df['life_span_date'].max()}"
    }
    
    return summary