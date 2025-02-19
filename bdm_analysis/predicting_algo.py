import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import os

def best_currency_forecast_benefit(df, reference_code):
    """
    For a given reference_code:
      1. Filter the DataFrame for this reference_code.
      2. Group by 'currency'.
      3. Train a mini-model (LinearRegression) to predict price_eur based on date.
      4. Forecast the future price (30 days after the last known date).
      5. Calculate the difference (potential benefit) between the last known price and the forecast.
      6. Return the currency with the highest benefit and the value of this benefit.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing at least the following columns:
          - 'reference_code'
          - 'price_eur'
          - 'currency'
          - 'life_span_date' (format DD/MM/YYYY or YYYY-MM-DD, etc.)
    reference_code : str
        The reference code to analyze.

    Returns
    -------
    (best_currency, best_benefit)
        best_currency : str
            The currency with the highest forecasted benefit.
        best_benefit : float
            The value of this potential benefit in euros.
        If no result, returns None.
    """
    # Filter by reference_code
    df_filtered = df[df['reference_code'] == reference_code].copy()
    if df_filtered.empty:
        print(f"No data for reference_code: {reference_code}")
        return None
    
    # Convert life_span_date to datetime
    df_filtered['date_dt'] = pd.to_datetime(df_filtered['life_span_date'], dayfirst=True, errors='coerce')
    
    # Drop rows where date couldn't be parsed
    df_filtered.dropna(subset=['date_dt'], inplace=True)
    
    # Ensure price_eur is numeric
    df_filtered['price_eur'] = pd.to_numeric(df_filtered['price_eur'], errors='coerce')
    df_filtered.dropna(subset=['price_eur'], inplace=True)
    
    # Store the best result
    best_currency = None
    best_benefit = -np.inf  # To compare benefits
    best_forecast_price = None
    
    # Iterate through each currency
    for currency, group in df_filtered.groupby('currency'):
        # Sort by date
        group = group.sort_values(by='date_dt')
        
        # Skip if only one data point
        if len(group) < 2:
            continue
        
        # Prepare X and y for regression
        group['date_ordinal'] = group['date_dt'].apply(datetime.toordinal)
        X = group[['date_ordinal']]
        y = group['price_eur']
        
        # Train a simple linear regression
        model = LinearRegression()
        model.fit(X, y)
        
        # Forecast 30 days after the last known date
        last_date_ordinal = group['date_ordinal'].max()
        forecast_date_ordinal = last_date_ordinal + 30
        
        # Prediction
        y_pred = model.predict([[forecast_date_ordinal]])[0]
        
        # Last known price
        last_price = group.iloc[-1]['price_eur']
        
        # Potential benefit
        benefit = y_pred - last_price
        
        # Check if it's the best currency
        if benefit > best_benefit:
            best_benefit = benefit
            best_currency = currency
            best_forecast_price = y_pred
    
    # Display result
    if best_currency is None:
        print(f"Cannot calculate benefit for reference_code {reference_code} (not enough data).")
        return None
    
    print(f"Best currency to buy: {best_currency}")
    print(f"Potential benefit (forecast): {best_benefit:.2f} EUR")
    print(f"Details: last known price = {last_price:.2f} EUR, predicted price = {best_forecast_price:.2f} EUR")
    
    return best_currency, best_benefit
