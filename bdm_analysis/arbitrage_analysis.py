import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Tuple, List, Optional

def calculate_arbitrage_opportunities(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les opportunités d'arbitrage dans les deux sens (EUR -> autre devise et autre devise -> EUR).
    """
    main_currencies = ['EUR', 'USD', 'GBP', 'CHF', 'JPY', 'SGD', 'CNY', 'AED']
    df = df[df['currency'].isin(main_currencies)].copy()
    
    results = []
    for reference in df['reference_code'].unique():
        ref_data = df[df['reference_code'] == reference].copy()
        
        for date in ref_data['life_span_date'].unique():
            date_data = ref_data[ref_data['life_span_date'] == date]
            
            # Vérifier si EUR est présent
            eur_data = date_data[date_data['currency'] == 'EUR']
            if len(eur_data) == 0:
                continue
                
            eur_price = eur_data.iloc[0]['price']
            
            # Vérifier que le prix EUR est réaliste
            if eur_price < 1000 or eur_price > 100000:
                continue
            
            # Comparer avec chaque autre devise
            for curr in main_currencies:
                if curr == 'EUR':
                    continue
                    
                curr_data = date_data[date_data['currency'] == curr]
                if len(curr_data) == 0:
                    continue
                    
                curr_price = curr_data.iloc[0]['price']  # Prix dans la devise locale
                curr_price_eur = curr_data.iloc[0]['price_eur']  # Prix converti en EUR
                
                # Vérifier que le prix converti est réaliste
                if curr_price_eur < 1000 or curr_price_eur > 100000:
                    continue
                
                # Calculer le taux de change effectif
                exchange_rate = curr_price_eur / curr_price
                
                # 1. Arbitrage EUR -> Autre devise
                if curr_price_eur > eur_price:
                    profit = curr_price_eur - eur_price
                    profit_percentage = (profit / eur_price) * 100
                    
                    if 1 <= profit_percentage <= 15:
                        results.append({
                            'reference_code': reference,
                            'buy_currency': 'EUR',
                            'buy_price': eur_price,
                            'sell_currency': curr,
                            'sell_price_local': curr_price,
                            'sell_price_eur': curr_price_eur,
                            'exchange_rate': exchange_rate,
                            'potential_profit_eur': profit,
                            'profit_percentage': profit_percentage,
                            'date': date,
                            'arbitrage_direction': 'EUR->Foreign'
                        })
                
                # 2. Arbitrage Autre devise -> EUR
                if eur_price > curr_price_eur:
                    profit = eur_price - curr_price_eur
                    profit_percentage = (profit / curr_price_eur) * 100
                    
                    if 1 <= profit_percentage <= 15:
                        results.append({
                            'reference_code': reference,
                            'buy_currency': curr,
                            'buy_price': curr_price,
                            'sell_currency': 'EUR',
                            'sell_price_local': eur_price,
                            'sell_price_eur': eur_price,
                            'exchange_rate': exchange_rate,
                            'potential_profit_eur': profit,
                            'profit_percentage': profit_percentage,
                            'date': date,
                            'arbitrage_direction': 'Foreign->EUR'
                        })
    
    return pd.DataFrame(results)


def analyze_historical_arbitrage(df: pd.DataFrame, min_profit_threshold: float = 2.0) -> Dict:
    """
    Analyse historique des opportunités d'arbitrage.
    """
    opportunities = calculate_arbitrage_opportunities(df)
    
    if opportunities.empty:
        return {
            "status": "No arbitrage opportunities found",
            "opportunities_count": 0
        }
    
    valid_opps = opportunities[opportunities['profit_percentage'] >= min_profit_threshold]
    
    stats = {
        "total_opportunities": len(valid_opps),
        "average_profit_eur": valid_opps['potential_profit_eur'].mean(),
        "average_profit_percentage": valid_opps['profit_percentage'].mean(),
        "max_profit_opportunity": {
            "reference": valid_opps.loc[valid_opps['potential_profit_eur'].idxmax()]['reference_code'],
            "profit_eur": valid_opps['potential_profit_eur'].max(),
            "profit_percentage": valid_opps.loc[valid_opps['potential_profit_eur'].idxmax()]['profit_percentage'],
            "currency": valid_opps.loc[valid_opps['potential_profit_eur'].idxmax()]['other_currency']
        },
        "best_currencies": valid_opps['other_currency'].value_counts().to_dict(),
        "most_profitable_references": valid_opps.groupby('reference_code')['potential_profit_eur'].mean().nlargest(5).to_dict()
    }
    
    return stats

def find_stable_arbitrage_pairs(df: pd.DataFrame, 
                              min_occurrence: int = 3,
                              min_profit: float = 2.0) -> List[Dict]:
    """
    Identifie les devises qui offrent des opportunités d'arbitrage stables par rapport à l'EUR.
    """
    opportunities = calculate_arbitrage_opportunities(df)
    
    if opportunities.empty:
        return []
    
    # Analyser chaque devise
    currency_stats = []
    for currency in opportunities['other_currency'].unique():
        curr_data = opportunities[opportunities['other_currency'] == currency]
        
        if len(curr_data) >= min_occurrence:
            avg_profit = curr_data['profit_percentage'].mean()
            if avg_profit >= min_profit:
                stats = {
                    'currency': currency,
                    'occurrences': len(curr_data),
                    'avg_profit_percentage': avg_profit,
                    'avg_profit_eur': curr_data['potential_profit_eur'].mean(),
                    'success_rate': len(curr_data[curr_data['profit_percentage'] >= min_profit]) / len(curr_data) * 100,
                    'best_references': curr_data.groupby('reference_code')['profit_percentage'].mean().nlargest(3).to_dict()
                }
                currency_stats.append(stats)
    
    return sorted(currency_stats, key=lambda x: x['avg_profit_percentage'], reverse=True)

def generate_arbitrage_report(df: pd.DataFrame) -> str:
    """
    Génère un rapport détaillé des opportunités d'arbitrage dans les deux sens.
    """
    opportunities = calculate_arbitrage_opportunities(df)
    if opportunities.empty:
        return "Aucune opportunité d'arbitrage trouvée."
        
    report = ["📊 RAPPORT D'ARBITRAGE PANERAI (Bidirectionnel) 📊\n"]
    
    # Statistiques globales
    report.append("1. APERÇU GÉNÉRAL")
    report.append(f"Nombre total d'opportunités: {len(opportunities)}")
    report.append(f"Profit moyen: {opportunities['potential_profit_eur'].mean():.2f} EUR")
    report.append(f"Profit moyen (%): {opportunities['profit_percentage'].mean():.1f}%")
    
    # Statistiques par direction
    report.append("\n2. ANALYSE PAR DIRECTION")
    for direction in ['EUR->Foreign', 'Foreign->EUR']:
        dir_opps = opportunities[opportunities['arbitrage_direction'] == direction]
        report.append(f"\n{direction}:")
        report.append(f"- Nombre d'opportunités: {len(dir_opps)}")
        if not dir_opps.empty:
            report.append(f"- Profit moyen: {dir_opps['potential_profit_eur'].mean():.2f} EUR")
            report.append(f"- Profit moyen (%): {dir_opps['profit_percentage'].mean():.1f}%")
            
            # Meilleure opportunité pour cette direction
            best_opp = dir_opps.loc[dir_opps['potential_profit_eur'].idxmax()]
            report.append(f"\nMeilleure opportunité {direction}:")
            report.append(f"- Référence: {best_opp['reference_code']}")
            report.append(f"- Achat: {best_opp['buy_price']:.2f} {best_opp['buy_currency']}")
            report.append(f"- Vente: {best_opp['sell_price_local']:.2f} {best_opp['sell_currency']}")
            report.append(f"- Profit: {best_opp['potential_profit_eur']:.2f} EUR ({best_opp['profit_percentage']:.1f}%)")
            report.append(f"- Taux de change: 1 EUR = {1/best_opp['exchange_rate']:.4f} {best_opp['sell_currency']}" 
                        if direction == 'EUR->Foreign' else 
                        f"- Taux de change: 1 {best_opp['buy_currency']} = {best_opp['exchange_rate']:.4f} EUR")
    
    # Opportunités actuelles (dernière date)
    latest_date = opportunities['date'].max()
    latest_opps = opportunities[opportunities['date'] == latest_date].nlargest(5, 'profit_percentage')
    
    if not latest_opps.empty:
        report.append("\n3. OPPORTUNITÉS ACTUELLES (Top 5)")
        report.append(f"\nDate: {latest_date}")
        for _, opp in latest_opps.iterrows():
            report.append(f"\nRéférence: {opp['reference_code']}")
            report.append(f"Direction: {opp['arbitrage_direction']}")
            report.append(f"Achat: {opp['buy_price']:.2f} {opp['buy_currency']}")
            report.append(f"Vente: {opp['sell_price_local']:.2f} {opp['sell_currency']}")
            report.append(f"Taux: 1 {opp['buy_currency']} = {opp['exchange_rate']:.4f} EUR")
            report.append(f"Profit: {opp['potential_profit_eur']:.2f} EUR ({opp['profit_percentage']:.1f}%)")
    
    return "\n".join(report)