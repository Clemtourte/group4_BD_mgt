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
from bdm_analysis.predicting_algo import best_currency_forecast_benefit
from bdm_analysis.arbitrage_analysis import (
    calculate_arbitrage_opportunities,
    analyze_historical_arbitrage,
    find_stable_arbitrage_pairs,
    generate_arbitrage_report
)

def main():
    """
    Exécute le pipeline d'analyse complet :
    1. Chargement des données
    2. Nettoyage des données
    3. Analyses et prédictions
    """
    print("🚀 Starting the analysis pipeline...")

    # 1️⃣ Chargement des données
    print("\n1️⃣ Loading data from BigQuery...")
    raw_df = load_data_from_bigquery()
    if raw_df is None or raw_df.empty:
        print("❌ No data retrieved, exiting.")
        return

    # 2️⃣ Nettoyage des données
    print("\n2️⃣ Cleaning data...")
    clean_df = clean_data(raw_df)

    # 3️⃣ Analyses
    print("\n3️⃣ Running analyses...")
    try:
        # ✅ Vérification des métriques de base
        metrics = verify_dataset_metrics(clean_df)

        # ✅ Statistiques globales
        summary = generate_summary_stats(clean_df)
        print("\n📊 Overall Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")

        # ✅ Analyse des collections
        collection_stats = analyze_collections(clean_df)
        print("\n📈 Collection Statistics:")
        print(collection_stats)

        # ✅ Analyse des gammes de prix
        price_ranges = analyze_price_ranges(clean_df)
        print("\n💰 Price Range Analysis:")
        print(price_ranges)

        # ✅ Tendances temporelles
        time_trends = analyze_time_trends(clean_df)
        print("\n⏰ Time Trends:")
        print(time_trends.head())

        # ✅ Analyse des devises
        currency_stats = analyze_currency_variations(clean_df)
        print("\n💱 Currency Analysis:")
        for key, value in currency_stats.items():
            print(f"{key}: {value}")

        # ✅ Matrice des prix de référence
        price_matrix = create_price_reference_matrix(clean_df)
        print("\n🔄 Price Reference Matrix (sample):")
        print(price_matrix.head())

        # ✅ Sauvegarde des données
        print("\n💾 Saving aggregated data...")
        if aggregate_to_csv(clean_df):
            print("✅ Data saved successfully!")
        else:
            print("⚠️ Warning: Data may not have been saved properly")

        # 💹 Analyse d'arbitrage
        print("\n💹 Running arbitrage analysis...")
        try:
            # Générer et afficher le rapport d'arbitrage
            arbitrage_report = generate_arbitrage_report(clean_df)
            print("\nRapport d'Arbitrage:")
            print(arbitrage_report)
            
            # Trouver les opportunités actuelles
            current_opportunities = calculate_arbitrage_opportunities(clean_df)
            if not current_opportunities.empty:
                print("\nOpportunités d'arbitrage actuelles:")
                print(current_opportunities.sort_values('profit_percentage', ascending=False).head())
        except Exception as e:
            print(f"⚠️ Warning: Arbitrage analysis failed: {e}")

        # 🔮 Prédiction des meilleures devises
        print("\n🔮 Running currency predictions...")
        try:
            # Exemple avec une référence spécifique
            reference_to_predict = 'PNPAM00317'  # Vous pouvez modifier cette référence
            print(f"\nPredicting best currencies for reference: {reference_to_predict}")
            best_currency_forecast_benefit(clean_df, reference_to_predict)
        except Exception as e:
            print(f"⚠️ Warning: Prediction failed: {e}")

        print("\n✅ Analysis pipeline completed successfully!")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return

if __name__ == "__main__":
    main()
    #test