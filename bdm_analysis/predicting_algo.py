import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import os
import matplotlib.pyplot as plt

def currency_forecast_benefit(df, reference_code, currency):
    """
    For a given reference_code and currency:
      1. Filter the DataFrame for this reference_code and currency.
      2. Train a mini-model (LinearRegression) to predict price_eur based on date.
      3. Forecast the future price (30 days after the last known date).
      4. Calculate the difference (potential benefit) between the last known price and the forecast.
      5. Return the forecasted price in the selected currency and in euros, and the value of this benefit.

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
    currency : str
        The currency to analyze.

    Returns
    -------
    (forecast_price_currency, forecast_price_eur, benefit)
        forecast_price_currency : float
            The forecasted price in the selected currency.
        forecast_price_eur : float
            The forecasted price in euros.
        benefit : float
            The value of this potential benefit in euros.
        If no result, returns None.
    """
    # Filter by reference_code and currency
    df_filtered = df[(df['reference_code'] == reference_code) & (df['currency'] == currency)].copy()
    if df_filtered.empty:
        print(f"No data for reference_code: {reference_code} and currency: {currency}")
        return None
    
    # Convert life_span_date to datetime
    df_filtered['date_dt'] = pd.to_datetime(df_filtered['life_span_date'], dayfirst=True, errors='coerce')
    
    # Drop rows where date couldn't be parsed
    df_filtered.dropna(subset=['date_dt'], inplace=True)
    
    # Ensure price_eur is numeric
    df_filtered['price_eur'] = pd.to_numeric(df_filtered['price_eur'], errors='coerce')
    df_filtered.dropna(subset=['price_eur'], inplace=True)
    
    # Sort by date
    df_filtered = df_filtered.sort_values(by='date_dt')
    
    # Skip if only one data point
    if len(df_filtered) < 2:
        print(f"Not enough data points for reference_code: {reference_code} and currency: {currency}")
        return None
    
    # Prepare X and y for regression
    df_filtered['date_ordinal'] = df_filtered['date_dt'].apply(datetime.toordinal)
    X = df_filtered[['date_ordinal']]
    y = df_filtered['price_eur']
    
    # Train a simple linear regression
    model = LinearRegression()
    model.fit(X, y)
    
    # Forecast 30 days after the last known date
    last_date_ordinal = df_filtered['date_ordinal'].max()
    forecast_date_ordinal = last_date_ordinal + 30
    
    # Convert forecast date to DataFrame
    forecast_date_df = pd.DataFrame({'date_ordinal': [forecast_date_ordinal]})
    
    # Prediction
    forecast_price_eur = model.predict(forecast_date_df)[0]
    
    # Last known price
    last_price = df_filtered.iloc[-1]['price_eur']
    
    # Potential benefit
    benefit = forecast_price_eur - last_price
    
    # Display result
    print(f"Forecasted price in {currency}: {forecast_price_eur:.2f} EUR")
    print(f"Potential benefit (forecast): {benefit:.2f} EUR")
    print(f"Details: last known price = {last_price:.2f} EUR, predicted price = {forecast_price_eur:.2f} EUR")
    
    # Plot the data and the regression line
    plt.figure(figsize=(10, 6))
    plt.scatter(df_filtered['date_dt'], df_filtered['price_eur'], color='blue', label='Actual Prices')
    plt.plot(df_filtered['date_dt'], model.predict(df_filtered[['date_ordinal']]), color='red', label='Regression Line')
    plt.xlabel('Date')
    plt.ylabel('Price in EUR')
    plt.title(f'Price Prediction for {currency}')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return forecast_price_eur, benefit
