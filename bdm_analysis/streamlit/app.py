import streamlit as st
import pandas as pd
from bdm_analysis.load_data import load_data_from_bigquery
from bdm_analysis.clean_data import clean_data
from bdm_analysis.arbitrage_analysis import calculate_arbitrage_opportunities
from bdm_analysis.predicting_algo import best_currency_forecast_benefit
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Panerai Market Analysis",
    page_icon="⌚",
    layout="wide"
)

# Custom CSS styles with better contrast
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        font-size: 3rem !important;
        font-weight: 700 !important;
        color: #1E3D59 !important;
        margin-bottom: 2rem !important;
    }
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    div[data-testid="metric-container"] > div {
        color: #1E3D59 !important;
    }
    div[data-testid="metric-container"] label {
        color: #555 !important;
    }
    div[data-testid="stMetricValue"] > div {
        color: #1E3D59 !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Data loading function
@st.cache_data
def load_and_clean_data():
    raw_df = load_data_from_bigquery()
    if raw_df is not None and not raw_df.empty:
        return clean_data(raw_df)
    return None

def main():
    # Application title
    st.title("🎯 Panerai Market Analysis Dashboard")
    
    # Data loading with spinner
    with st.spinner('Loading data...'):
        df = load_and_clean_data()
    
    if df is None:
        st.error("❌ Error loading data.")
        return

    # Create tabs
    tab1, tab2 = st.tabs(["📊 Arbitrage Analysis", "📈 Price Predictions"])
    
    # Arbitrage Analysis Tab
    with tab1:
        st.header("Arbitrage Opportunities")
        
        # Calculate arbitrage opportunities
        with st.spinner('Calculating arbitrage opportunities...'):
            opportunities = calculate_arbitrage_opportunities(df)
        
        if not opportunities.empty:
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                min_profit = st.slider(
                    "Minimum Profit (%)", 
                    min_value=0.0, 
                    max_value=15.0, 
                    value=2.0,
                    step=0.5
                )
            with col2:
                selected_direction = st.selectbox(
                    "Arbitrage Direction",
                    ["All", "EUR->Foreign", "Foreign->EUR"]
                )
            with col3:
                selected_currency = st.selectbox(
                    "Currency",
                    ["All"] + list(opportunities['buy_currency'].unique())
                )
            
            # Filter data
            filtered_opps = opportunities[
                opportunities['profit_percentage'] >= min_profit
            ]
            if selected_direction != "All":
                filtered_opps = filtered_opps[
                    filtered_opps['arbitrage_direction'] == selected_direction
                ]
            if selected_currency != "All":
                filtered_opps = filtered_opps[
                    (filtered_opps['buy_currency'] == selected_currency) |
                    (filtered_opps['sell_currency'] == selected_currency)
                ]
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "Number of Opportunities", 
                    len(filtered_opps)
                )
            with col2:
                st.metric(
                    "Average Profit (EUR)", 
                    f"€{filtered_opps['potential_profit_eur'].mean():,.2f}"
                )
            with col3:
                st.metric(
                    "Average Profit (%)", 
                    f"{filtered_opps['profit_percentage'].mean():.1f}%"
                )
            with col4:
                st.metric(
                    "Maximum Profit (EUR)", 
                    f"€{filtered_opps['potential_profit_eur'].max():,.2f}"
                )
            
            # Opportunities by currency chart
            currency_profits = filtered_opps.groupby('sell_currency')[
                'potential_profit_eur'
            ].mean().reset_index()
            
            fig = px.bar(
                currency_profits,
                x='sell_currency',
                y='potential_profit_eur',
                title='Average Profit by Currency',
                labels={
                    'sell_currency': 'Currency',
                    'potential_profit_eur': 'Average Profit (EUR)'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Top opportunities table
            st.subheader("Top Arbitrage Opportunities")
            top_opps = filtered_opps.nlargest(10, 'potential_profit_eur')
            styled_opps = top_opps[[
                'reference_code', 
                'buy_currency', 
                'sell_currency', 
                'potential_profit_eur',
                'profit_percentage',
                'date'
            ]].copy()
            styled_opps.columns = [
                'Reference', 
                'Buy Currency', 
                'Sell Currency', 
                'Profit (EUR)',
                'Profit (%)',
                'Date'
            ]
            styled_opps['Profit (EUR)'] = styled_opps['Profit (EUR)'].round(2)
            styled_opps['Profit (%)'] = styled_opps['Profit (%)'].round(2)
            st.dataframe(
                styled_opps,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("No arbitrage opportunities found.")
    
    # Price Predictions Tab
    with tab2:
        st.header("Price Predictions by Reference")
        
        # Reference selection
        references = sorted(df['reference_code'].unique())
        selected_ref = st.selectbox(
            "Select a reference",
            references
        )
        
        if st.button("Analyze"):
            with st.spinner('Calculating predictions...'):
                try:
                    result = best_currency_forecast_benefit(df, selected_ref)
                    if result:
                        best_currency, best_benefit = result
                        
                        # Display results in metrics
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(
                                "Best Currency", 
                                best_currency
                            )
                        with col2:
                            st.metric(
                                "Potential Benefit", 
                                f"€{best_benefit:,.2f}"
                            )
                        
                        # The graph is already generated by the function
                        st.pyplot()
                    else:
                        st.warning("Not enough data for this reference.")
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")

if __name__ == "__main__":
    main()