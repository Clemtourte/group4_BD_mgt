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

def main():
    """
    Executes the complete analysis pipeline:
    1. Loads raw data
    2. Cleans data
    3. Runs all analyses
    """
    print("🚀 Starting the analysis pipeline...")
    
    # 1. Load raw data
    print("\n1️⃣ Loading data from BigQuery...")
    raw_df = load_data_from_bigquery()
    if raw_df is None:
        return
    
    # 2. Clean data
    print("\n2️⃣ Cleaning data...")
    clean_df = clean_data(raw_df)
    
    # 3. Run analyses
    print("\n3️⃣ Running analyses...")
    try:
        # First verify the dataset metrics
        metrics = verify_dataset_metrics(clean_df)
        
        # Generate summary statistics
        summary = generate_summary_stats(clean_df)
        print("\n📊 Overall Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        # Run specific analyses
        collection_stats = analyze_collections(clean_df)
        print("\n📈 Collection Statistics:")
        print(collection_stats)
        
        price_ranges = analyze_price_ranges(clean_df)
        print("\n💰 Price Range Analysis:")
        print(price_ranges)
        
        time_trends = analyze_time_trends(clean_df)
        print("\n⏰ Time Trends:")
        print(time_trends.head())
        
        # Analyze currency variations
        currency_stats = analyze_currency_variations(clean_df)
        print("\n💱 Currency Analysis:")
        for key, value in currency_stats.items():
            print(f"{key}: {value}")
        
        # Create price reference matrix
        price_matrix = create_price_reference_matrix(clean_df)
        print("\n🔄 Price Reference Matrix (sample):")
        print(price_matrix.head())
        
        print("\n✅ Analysis pipeline completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return

if __name__ == "__main__":
    main()