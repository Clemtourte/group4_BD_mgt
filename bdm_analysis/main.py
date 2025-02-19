from bdm_analysis.load_data import load_data_from_bigquery
from bdm_analysis.clean_data import clean_data
from bdm_analysis.analyze_data import (
    analyze_collections,
    analyze_price_ranges,
    analyze_time_trends,
    analyze_price_changes,
    generate_summary_stats
)

def main():
    """
    Executes the complete analysis pipeline:
    1. Loads raw data
    2. Cleans the data
    3. Runs various analyses
    """
    print("🚀 Starting the analysis pipeline...")
    
    # 1. Load raw data
    print("\n1️⃣ Loading data from BigQuery...")
    raw_df = load_data_from_bigquery()
    
    if raw_df is None:
        print("❌ Unable to proceed, data was not loaded.")
        return
        
    # 2. Clean data
    print("\n2️⃣ Cleaning data...")
    clean_df = clean_data(raw_df)
    
    # 3. Run analyses
    print("\n3️⃣ Running analyses...")
    try:
        # Generate overall summary
        summary = generate_summary_stats(clean_df)
        print("\n📊 Overall Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        # Run specific analyses
        collection_stats = analyze_collections(clean_df)
        price_ranges = analyze_price_ranges(clean_df)
        time_trends = analyze_time_trends(clean_df)
        price_changes = analyze_price_changes(clean_df)
        
        print("\n✅ Analysis pipeline completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return

if __name__ == "__main__":
    main()