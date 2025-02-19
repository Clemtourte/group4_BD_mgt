from bdm_analysis.load_data import load_data_from_bigquery
from bdm_analysis.clean_data import clean_data
from bdm_analysis.analyze_data import (
    verify_dataset_metrics,
    analyze_collections,
    analyze_price_ranges,
    analyze_time_trends,
    create_price_reference_matrix,
    analyze_currency_variations,
    generate_summary_stats
)
from bdm_analysis.aggregate_to_csv import aggregate_to_csv
from bdm_analysis.predicting_algo import currency_forecast_benefit
from bdm_analysis.arbitrage_analysis import (
    calculate_arbitrage_opportunities,
    analyze_historical_arbitrage,
    find_stable_arbitrage_pairs,
    generate_arbitrage_report
)

def main():
    """
    Executes the complete analysis pipeline:
    1. Data loading
    2. Data cleaning
    3. Analyses and predictions
    """
    print("Starting the analysis pipeline...")

    #Data loading
    print("\nLoading data from BigQuery...")
    raw_df = load_data_from_bigquery()
    if raw_df is None or raw_df.empty:
        print("No data retrieved, exiting.")
        return

    #Data cleaning
    print("\nCleaning data...")
    clean_df = clean_data(raw_df)

    # Analyses
    print("\nRunning analyses...")
    try:
        # Basic metrics verification
        metrics = verify_dataset_metrics(clean_df)

        # Overall statistics
        summary = generate_summary_stats(clean_df)
        print("\nOverall Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")

        # Collection analysis
        collection_stats = analyze_collections(clean_df)
        print("\nCollection Statistics:")
        print(collection_stats)

        # Price range analysis
        price_ranges = analyze_price_ranges(clean_df)
        print("\n Price Range Analysis:")
        print(price_ranges)

        # Time trends
        time_trends = analyze_time_trends(clean_df)
        print("\nTime Trends:")
        print(time_trends.head())

        # Currency analysis
        currency_stats = analyze_currency_variations(clean_df)
        print("\n Currency Analysis:")
        for key, value in currency_stats.items():
            print(f"{key}: {value}")

        # Price reference matrix
        price_matrix = create_price_reference_matrix(clean_df)
        print("\n Price Reference Matrix (sample):")
        print(price_matrix.head())

        # Saving data
        print("\n Saving aggregated data...")
        if aggregate_to_csv(clean_df):
            print("Data saved successfully!")
        else:
            print(" Warning: Data may not have been saved properly")

        # Arbitrage analysis
        print("\n Running arbitrage analysis...")
        try:
            # Generate and display arbitrage report
            arbitrage_report = generate_arbitrage_report(clean_df)
            print("\nArbitrage Report:")
            print(arbitrage_report)
            
            # Find current opportunities
            current_opportunities = calculate_arbitrage_opportunities(clean_df)
            if not current_opportunities.empty:
                print("\nCurrent arbitrage opportunities:")
                print(current_opportunities.sort_values('profit_percentage', ascending=False).head())
        except Exception as e:
            print(f" Warning: Arbitrage analysis failed: {e}")

        # 🔮 Currency predictions
        print("\nRunning currency predictions...")
        try:
            # Example with a specific reference
            reference_to_predict = 'PNPAM00715'  # You can change this reference
            print(f"\nPredicting best currencies for reference: {reference_to_predict}")
            currency_forecast_benefit(clean_df, reference_to_predict,currency='EUR')
        except Exception as e:
            print(f" Warning: Prediction failed: {e}")

        print("\nAnalysis pipeline completed successfully!")

    except Exception as e:
        print(f" Error during analysis: {e}")
        return

if __name__ == "__main__":
    main()