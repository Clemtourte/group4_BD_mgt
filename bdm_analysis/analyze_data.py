import pandas as pd
import numpy as np

def verify_dataset_metrics(df):
    """
    Verifies key metrics of the dataset and prints the results.
    """
    print("\n🔍 Verifying Dataset Metrics:")
    
    # Count unique references
    n_refs = df['reference_code'].nunique()
    print(f"\n1️⃣ Number of unique references: {n_refs}")
    print("\nSample references:")
    print(df['reference_code'].unique()[:5])
    
    # Count unique currencies
    n_currencies = df['currency'].nunique()
    print(f"\n2️⃣ Number of unique currencies: {n_currencies}")
    print("\nAll currencies:")
    print(df['currency'].unique())
    
    # Count unique dates
    n_dates = df['life_span_date'].nunique()
    print(f"\n3️⃣ Number of unique dates: {n_dates}")
    print("\nAll dates:")
    print(sorted(df['life_span_date'].unique()))
    
    return {
        'n_references': n_refs,
        'n_currencies': n_currencies,
        'n_dates': n_dates
    }

def analyze_collections(df):
    """
    Analyzes collections statistics.
    """
    stats = df.groupby('collection').agg({
        'reference_code': 'count',
        'price': ['mean', 'min', 'max', 'std']
    }).round(2)
    
    stats.columns = ['model_count', 'avg_price', 'min_price', 'max_price', 'price_std']
    return stats.reset_index()

def analyze_price_ranges(df):
    """
    Segments watches into price categories and analyzes each segment.
    """
    df['price_category'] = pd.cut(
        df['price'],
        bins=[0, 10000, 25000, 50000, float('inf')],
        labels=['Entry Level', 'Mid Range', 'High End', 'Ultra Luxury']
    )
    
    ranges = df.groupby('price_category').agg({
        'reference_code': ['count', 'nunique'],
        'price': 'mean',
        'collection': 'nunique'
    }).round(2)
    
    ranges.columns = ['model_count', 'unique_references', 'avg_price', 'unique_collections']
    return ranges.reset_index()

def analyze_time_trends(df):
    """
    Analyzes trends over time.
    """
    df['year_quarter'] = pd.to_datetime(df['life_span_date']).dt.to_period('Q')
    
    trends = df.groupby('year_quarter').agg({
        'price': ['mean', 'count'],
        'reference_code': 'nunique',
        'collection': 'nunique'
    }).round(2)
    
    trends.columns = ['avg_price', 'model_count', 'unique_references', 'unique_collections']
    return trends.reset_index()

def analyze_price_changes(df):
    """
    Analyzes price changes patterns.
    """
    price_changes = df[df['price_difference'] != 0].copy()
    
    changes = price_changes.groupby('collection').agg({
        'price_difference': ['count', 'mean', 'min', 'max'],
        'reference_code': 'nunique'
    }).round(2)
    
    changes.columns = ['change_count', 'avg_change', 'min_change', 'max_change', 'models_affected']
    return changes.reset_index()

def create_price_reference_matrix(df):
    """
    Creates a matrix of prices by reference and currency.
    Uses EUR as base currency.
    """
    price_matrix = df.pivot_table(
        index=['reference_code', 'life_span_date'],
        columns='currency',
        values='price',
        aggfunc='first'
    ).reset_index()
    
    # Sort by date and reference
    price_matrix = price_matrix.sort_values(['reference_code', 'life_span_date'])
    
    return price_matrix

def generate_summary_stats(df):
    """
    Generates overall summary statistics.
    """
    summary = {
        'total_models': df['reference_code'].nunique(),
        'total_collections': df['collection'].nunique(),
        'avg_price': df['price'].mean().round(2),
        'price_range': f"{df['price'].min()} - {df['price'].max()}",
        'most_common_collection': df['collection'].mode().iloc[0],
        'date_range': f"{df['life_span_date'].min().date()} - {df['life_span_date'].max().date()}"
    }
    
    return summary