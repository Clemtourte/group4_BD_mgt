import pandas as pd
import numpy as np

def analyze_collections(df):
    """
    Analyzes collections statistics.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe
        
    Returns:
        pd.DataFrame: Collection-level statistics
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
    
    Args:
        df (pd.DataFrame): Cleaned dataframe
        
    Returns:
        pd.DataFrame: Price segment analysis
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
    
    Args:
        df (pd.DataFrame): Cleaned dataframe
        
    Returns:
        pd.DataFrame: Time-based trends
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
    
    Args:
        df (pd.DataFrame): Cleaned dataframe
        
    Returns:
        pd.DataFrame: Price change analysis
    """
    # Only consider rows with price differences
    price_changes = df[df['price_difference'] != 0].copy()
    
    changes = price_changes.groupby('collection').agg({
        'price_difference': ['count', 'mean', 'min', 'max'],
        'reference_code': 'nunique'
    }).round(2)
    
    changes.columns = ['change_count', 'avg_change', 'min_change', 'max_change', 'models_affected']
    return changes.reset_index()

def generate_summary_stats(df):
    """
    Generates overall summary statistics.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe
        
    Returns:
        dict: Summary statistics
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