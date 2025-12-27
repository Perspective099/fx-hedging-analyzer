"""
FX Forward Curve & Hedging Analyzer - Main Application
A comprehensive tool for FX forward curve construction and corporate hedging analysis
Author: Jordan Ing
Date: December 2024
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fx_data_fetcher import FXDataFetcher
from hedging_analyzer import HedgingAnalyzer
from visualizer import FXVisualizer
import pandas as pd


class FXHedgingTool:
    """Main application class for FX hedging analysis"""
    
    def __init__(self):
        """Initialize the FX hedging tool"""
        self.fetcher = FXDataFetcher()
        self.visualizer = FXVisualizer(output_dir='outputs')
        print("="*70)
        print("FX FORWARD CURVE & HEDGING ANALYZER")
        print("Developed by: Jordan Ing")
        print("="*70)
    
    def run_full_analysis(self, pair: str = 'USD/CAD', 
                         notional: float = 5_000_000,
                         tenor: str = '6M',
                         hedge_ratio: float = 0.75,
                         market_view: str = 'neutral'):
        """
        Run complete FX hedging analysis workflow
        
        Args:
            pair: Currency pair to analyze
            notional: Exposure amount
            tenor: Hedging tenor
            hedge_ratio: Percentage to hedge
            market_view: Market outlook ('bullish', 'neutral', 'bearish')
        """
        print(f"\n{'='*70}")
        print(f"ANALYSIS PARAMETERS")
        print(f"{'='*70}")
        print(f"Currency Pair: {pair}")
        print(f"Notional Exposure: {notional:,.0f}")
        print(f"Hedging Tenor: {tenor}")
        print(f"Hedge Ratio: {hedge_ratio:.0%}")
        print(f"Market View: {market_view.title()}")
        
        # Step 1: Fetch market data
        print(f"\n{'='*70}")
        print("STEP 1: Fetching Live FX Market Data")
        print(f"{'='*70}")
        
        spot_df = self.fetcher.get_spot_rates()
        print("\nCurrent Spot Rates:")
        print(spot_df[['Pair', 'Spot_Rate']].to_string(index=False))
        
        # Step 2: Build forward curves
        print(f"\n{'='*70}")
        print("STEP 2: Building Forward Curves")
        print(f"{'='*70}")
        
        forward_curves = self.fetcher.get_all_forward_curves()
        
        # Find the requested pair
        if pair not in forward_curves:
            print(f"\nWarning: {pair} not found. Available pairs:")
            for p in forward_curves.keys():
                print(f"  - {p}")
            pair = list(forward_curves.keys())[0]
            print(f"\nUsing {pair} instead.")
        
        selected_curve = forward_curves[pair]
        print(f"\nForward Curve for {pair}:")
        print(selected_curve[['Tenor', 'Forward_Rate', 'Forward_Points', 'Settlement_Date']].to_string(index=False))
        
        # Step 3: Hedging analysis
        print(f"\n{'='*70}")
        print("STEP 3: Hedging Strategy Analysis")
        print(f"{'='*70}")
        
        analyzer = HedgingAnalyzer(selected_curve)
        
        # Calculate hedge cost
        hedge_info = analyzer.calculate_hedge_cost(notional, tenor, hedge_ratio)
        print("\nHedge Details:")
        print(f"  Spot Rate: {hedge_info['Spot_Rate']:.4f}")
        print(f"  Forward Rate ({tenor}): {hedge_info['Forward_Rate']:.4f}")
        print(f"  Forward Points: {hedge_info['Forward_Points']:.2f} pips")
        print(f"  Premium/Discount: {hedge_info['Premium_Discount_pct']:.4f}%")
        print(f"  Hedged Amount: {hedge_info['Hedged_Amount']:,.0f}")
        print(f"  Unhedged Amount: {hedge_info['Unhedged_Amount']:,.0f}")
        
        # Scenario analysis
        print(f"\n{'='*70}")
        print("STEP 4: Scenario Analysis")
        print(f"{'='*70}")
        
        scenario_df = analyzer.scenario_analysis(notional, tenor, hedge_ratio)
        print("\nP&L Across Different Future Spot Scenarios:")
        print(scenario_df.to_string(index=False))
        
        # Hedge ratio comparison
        print(f"\n{'='*70}")
        print("STEP 5: Hedge Ratio Comparison")
        print(f"{'='*70}")
        
        # Use middle scenario for comparison
        middle_spot = scenario_df['Future_Spot'].iloc[len(scenario_df)//2]
        comparison_df = analyzer.compare_hedge_ratios(notional, tenor, middle_spot)
        print(f"\nComparison at Future Spot = {middle_spot:.4f}:")
        print(comparison_df.to_string(index=False))
        
        # Get recommendation
        print(f"\n{'='*70}")
        print("STEP 6: Hedging Recommendation")
        print(f"{'='*70}")
        
        recommendation = analyzer.generate_hedge_recommendation(notional, tenor, market_view)
        print(f"\nRecommended Strategy: {recommendation['Recommendation']}")
        print(f"\nRationale:\n{recommendation['Rationale']}")
        print(f"\nSuggested Action:\n{recommendation['Action']}")
        
        # Step 7: Generate visualizations
        print(f"\n{'='*70}")
        print("STEP 7: Generating Visualizations")
        print(f"{'='*70}")
        
        # Forward curve chart
        curve_path = self.visualizer.plot_forward_curve(selected_curve)
        print(f"\n✓ Forward curve chart saved: {curve_path}")
        
        # Scenario analysis chart
        scenario_path = self.visualizer.plot_scenario_analysis(scenario_df, hedge_info)
        print(f"✓ Scenario analysis chart saved: {scenario_path}")
        
        # Hedge ratio comparison chart
        comparison_path = self.visualizer.plot_hedge_ratio_comparison(
            comparison_df, pair, middle_spot
        )
        print(f"✓ Hedge ratio comparison chart saved: {comparison_path}")
        
        # Dashboard with all curves
        dashboard_path = self.visualizer.create_summary_dashboard(forward_curves)
        print(f"✓ FX dashboard saved: {dashboard_path}")
        
        # Step 8: Export data
        print(f"\n{'='*70}")
        print("STEP 8: Exporting Analysis Data")
        print(f"{'='*70}")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Export forward curve
        curve_export_path = f'outputs/forward_curve_{pair.replace("/", "")}_{timestamp}.csv'
        selected_curve.to_csv(curve_export_path, index=False)
        print(f"\n✓ Forward curve data: {curve_export_path}")
        
        # Export scenario analysis
        scenario_export_path = f'outputs/scenario_analysis_{timestamp}.csv'
        scenario_df.to_csv(scenario_export_path, index=False)
        print(f"✓ Scenario analysis data: {scenario_export_path}")
        
        # Export hedge comparison
        comparison_export_path = f'outputs/hedge_comparison_{timestamp}.csv'
        comparison_df.to_csv(comparison_export_path, index=False)
        print(f"✓ Hedge comparison data: {comparison_export_path}")
        
        print(f"\n{'='*70}")
        print("ANALYSIS COMPLETE")
        print(f"{'='*70}")
        print(f"\nAll outputs saved to 'outputs/' directory")
        print(f"Timestamp: {timestamp}")
        
        return {
            'forward_curve': selected_curve,
            'hedge_info': hedge_info,
            'scenario_analysis': scenario_df,
            'hedge_comparison': comparison_df,
            'recommendation': recommendation,
            'charts': {
                'forward_curve': curve_path,
                'scenario_analysis': scenario_path,
                'hedge_comparison': comparison_path,
                'dashboard': dashboard_path
            }
        }
    
    def interactive_mode(self):
        """Run tool in interactive mode with user inputs"""
        print("\n" + "="*70)
        print("INTERACTIVE MODE")
        print("="*70)
        
        # Get available pairs
        print("\nFetching available currency pairs...")
        spot_df = self.fetcher.get_spot_rates()
        pairs = spot_df['Pair'].tolist()
        
        print("\nAvailable Currency Pairs:")
        for i, pair in enumerate(pairs, 1):
            print(f"  {i}. {pair}")
        
        # User inputs
        try:
            pair_idx = int(input(f"\nSelect currency pair (1-{len(pairs)}): ")) - 1
            pair = pairs[pair_idx]
            
            notional = float(input("Enter exposure amount: "))
            
            print("\nAvailable tenors: 1W, 1M, 2M, 3M, 6M, 9M, 1Y")
            tenor = input("Select tenor: ").upper()
            
            hedge_ratio = float(input("Enter hedge ratio (0.0 to 1.0): "))
            
            print("\nMarket views: bullish, neutral, bearish")
            market_view = input("Enter market view: ").lower()
            
            # Run analysis
            self.run_full_analysis(pair, notional, tenor, hedge_ratio, market_view)
            
        except (ValueError, IndexError) as e:
            print(f"\nInvalid input: {e}")
            print("Running with default parameters...")
            self.run_full_analysis()


def main():
    """Main entry point"""
    tool = FXHedgingTool()
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        tool.interactive_mode()
    else:
        # Run with default example: Canadian importer hedging USD exposure
        print("\nRunning default analysis...")
        print("Example: Canadian importer with USD 5M receivable in 6 months\n")
        
        tool.run_full_analysis(
            pair='USD/CAD',
            notional=5_000_000,
            tenor='6M',
            hedge_ratio=0.75,
            market_view='neutral'
        )
        
        print("\n" + "="*70)
        print("To run in interactive mode, use: python main.py --interactive")
        print("="*70)


if __name__ == "__main__":
    main()
