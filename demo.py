"""
FX Hedging Analyzer - Demo Version (Offline Mode)
Runs with simulated data for demonstration purposes
Author: Jordan Ing
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from fx_data_fetcher import FXDataFetcher
    USE_LIVE_DATA = True
except:
    USE_LIVE_DATA = False

from fx_data_simulator import FXDataSimulator
from hedging_analyzer import HedgingAnalyzer
from visualizer import FXVisualizer
import pandas as pd


def run_demo_analysis():
    """Run demonstration analysis with simulated or live data"""
    
    print("="*70)
    print("FX FORWARD CURVE & HEDGING ANALYZER - DEMO")
    print("Developed by: Jordan Ing")
    print("="*70)
    
    # Initialize components
    if USE_LIVE_DATA:
        print("\n[Using LIVE market data from yfinance]")
        fetcher = FXDataFetcher()
    else:
        print("\n[Using SIMULATED market data - network unavailable]")
        fetcher = FXDataSimulator()
    
    visualizer = FXVisualizer(output_dir='outputs')
    
    # Demo parameters
    pair = 'USD/CAD'
    notional = 5_000_000
    tenor = '6M'
    hedge_ratio = 0.75
    market_view = 'neutral'
    
    print(f"\n{'='*70}")
    print("DEMO SCENARIO: Canadian Importer Hedging USD Exposure")
    print(f"{'='*70}")
    print(f"Currency Pair: {pair}")
    print(f"Notional Exposure: USD {notional:,.0f}")
    print(f"Hedging Tenor: {tenor}")
    print(f"Hedge Ratio: {hedge_ratio:.0%}")
    print(f"Market View: {market_view.title()}")
    
    # Fetch data
    print(f"\n{'='*70}")
    print("STEP 1: Market Data")
    print(f"{'='*70}")
    
    spot_df = fetcher.get_spot_rates()
    print("\nCurrent Spot Rates:")
    print(spot_df[['Pair', 'Spot_Rate']].to_string(index=False))
    
    # Build forward curves
    print(f"\n{'='*70}")
    print("STEP 2: Forward Curve Construction")
    print(f"{'='*70}")
    
    forward_curves = fetcher.get_all_forward_curves()
    selected_curve = forward_curves[pair]
    
    print(f"\nForward Curve for {pair}:")
    print(selected_curve[['Tenor', 'Forward_Rate', 'Forward_Points']].to_string(index=False))
    
    # Hedging analysis
    print(f"\n{'='*70}")
    print("STEP 3: Hedging Analysis")
    print(f"{'='*70}")
    
    analyzer = HedgingAnalyzer(selected_curve)
    hedge_info = analyzer.calculate_hedge_cost(notional, tenor, hedge_ratio)
    
    print(f"\nHedge Details:")
    print(f"  Spot Rate: {hedge_info['Spot_Rate']:.4f}")
    print(f"  Forward Rate ({tenor}): {hedge_info['Forward_Rate']:.4f}")
    print(f"  Forward Points: {hedge_info['Forward_Points']:.2f} pips")
    print(f"  Premium/Discount: {hedge_info['Premium_Discount_pct']:.4f}%")
    print(f"  Hedged Amount: USD {hedge_info['Hedged_Amount']:,.0f}")
    print(f"  Unhedged Amount: USD {hedge_info['Unhedged_Amount']:,.0f}")
    
    # Scenario analysis
    print(f"\n{'='*70}")
    print("STEP 4: P&L Scenario Analysis")
    print(f"{'='*70}")
    
    scenario_df = analyzer.scenario_analysis(notional, tenor, hedge_ratio)
    print("\nP&L Under Different Future Spot Scenarios:")
    print(scenario_df.to_string(index=False))
    
    # Hedge ratio comparison
    print(f"\n{'='*70}")
    print("STEP 5: Hedge Ratio Comparison")
    print(f"{'='*70}")
    
    middle_spot = scenario_df['Future_Spot'].iloc[2]
    comparison_df = analyzer.compare_hedge_ratios(notional, tenor, middle_spot)
    
    print(f"\nP&L Comparison at Future Spot = {middle_spot:.4f}:")
    print(comparison_df.to_string(index=False))
    
    # Recommendation
    print(f"\n{'='*70}")
    print("STEP 6: Hedging Recommendation")
    print(f"{'='*70}")
    
    recommendation = analyzer.generate_hedge_recommendation(notional, tenor, market_view)
    print(f"\nRecommended Strategy: {recommendation['Recommendation']}")
    print(f"\nRationale:\n{recommendation['Rationale']}")
    print(f"\nSuggested Action:\n{recommendation['Action']}")
    
    # Generate visualizations
    print(f"\n{'='*70}")
    print("STEP 7: Generating Visualizations")
    print(f"{'='*70}")
    
    try:
        curve_path = visualizer.plot_forward_curve(selected_curve)
        print(f"\n✓ Forward curve chart: {curve_path}")
        
        scenario_path = visualizer.plot_scenario_analysis(scenario_df, hedge_info)
        print(f"✓ Scenario analysis chart: {scenario_path}")
        
        comparison_path = visualizer.plot_hedge_ratio_comparison(
            comparison_df, pair, middle_spot
        )
        print(f"✓ Hedge ratio comparison: {comparison_path}")
        
        dashboard_path = visualizer.create_summary_dashboard(forward_curves)
        print(f"✓ FX dashboard: {dashboard_path}")
        
    except Exception as e:
        print(f"\n⚠ Visualization error: {e}")
        print("Charts may not be generated properly")
    
    # Export data
    print(f"\n{'='*70}")
    print("STEP 8: Exporting Data")
    print(f"{'='*70}")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    curve_file = f'outputs/forward_curve_{pair.replace("/", "")}_{timestamp}.csv'
    selected_curve.to_csv(curve_file, index=False)
    print(f"\n✓ Forward curve: {curve_file}")
    
    scenario_file = f'outputs/scenario_analysis_{timestamp}.csv'
    scenario_df.to_csv(scenario_file, index=False)
    print(f"✓ Scenario analysis: {scenario_file}")
    
    comparison_file = f'outputs/hedge_comparison_{timestamp}.csv'
    comparison_df.to_csv(comparison_file, index=False)
    print(f"✓ Hedge comparison: {comparison_file}")
    
    print(f"\n{'='*70}")
    print("DEMO COMPLETE")
    print(f"{'='*70}")
    print(f"\n✓ All outputs saved to 'outputs/' directory")
    print(f"✓ Review charts and CSV files for detailed analysis")
    print(f"\n💡 This demonstrates the complete workflow for FX hedging analysis")
    print(f"💡 Ready for portfolio inclusion and technical interviews!")
    print(f"\n{'='*70}")


if __name__ == "__main__":
    run_demo_analysis()
