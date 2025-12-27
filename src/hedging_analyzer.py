"""
FX Hedging Strategy Analyzer
Helps corporate clients analyze hedging options for FX exposure
Author: Jordan Ing
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta


class HedgingAnalyzer:
    """Analyzes hedging strategies for corporate FX exposure"""
    
    def __init__(self, forward_curve: pd.DataFrame):
        """
        Initialize with a forward curve for the relevant currency pair
        
        Args:
            forward_curve: DataFrame containing forward rates across tenors
        """
        self.forward_curve = forward_curve
        self.pair = forward_curve['Pair'].iloc[0]
    
    def calculate_hedge_cost(self, notional: float, tenor: str, 
                            hedge_ratio: float = 1.0) -> Dict:
        """
        Calculate the cost/benefit of hedging at current forward rates
        
        Args:
            notional: Exposure amount in base currency
            tenor: Hedging tenor (e.g., '3M', '6M', '1Y')
            hedge_ratio: Percentage of exposure to hedge (0.0 to 1.0)
            
        Returns:
            Dictionary with hedging analysis
        """
        # Get forward rate for specified tenor
        tenor_data = self.forward_curve[self.forward_curve['Tenor'] == tenor]
        
        if tenor_data.empty:
            raise ValueError(f"Tenor {tenor} not found in forward curve")
        
        forward_rate = tenor_data['Forward_Rate'].iloc[0]
        spot_rate = self.forward_curve[self.forward_curve['Tenor'] == 'Spot']['Forward_Rate'].iloc[0]
        forward_points = tenor_data['Forward_Points'].iloc[0]
        settlement_date = tenor_data['Settlement_Date'].iloc[0]
        
        hedged_amount = notional * hedge_ratio
        unhedged_amount = notional * (1 - hedge_ratio)
        
        # Calculate forward premium/discount
        premium_discount = ((forward_rate - spot_rate) / spot_rate) * 100
        
        return {
            'Pair': self.pair,
            'Notional': notional,
            'Hedge_Ratio': hedge_ratio,
            'Hedged_Amount': hedged_amount,
            'Unhedged_Amount': unhedged_amount,
            'Tenor': tenor,
            'Settlement_Date': settlement_date,
            'Spot_Rate': spot_rate,
            'Forward_Rate': forward_rate,
            'Forward_Points': forward_points,
            'Premium_Discount_pct': round(premium_discount, 4),
            'Locked_In_Rate': forward_rate
        }
    
    def scenario_analysis(self, notional: float, tenor: str, 
                         hedge_ratio: float = 1.0,
                         spot_scenarios: List[float] = None) -> pd.DataFrame:
        """
        Analyze P&L under different future spot rate scenarios
        
        Args:
            notional: Exposure amount
            tenor: Hedging tenor
            hedge_ratio: Percentage hedged
            spot_scenarios: List of potential future spot rates to analyze
            
        Returns:
            DataFrame with P&L analysis across scenarios
        """
        hedge_info = self.calculate_hedge_cost(notional, tenor, hedge_ratio)
        forward_rate = hedge_info['Forward_Rate']
        current_spot = hedge_info['Spot_Rate']
        
        # Default scenarios: +/- 10%, 5%, current, +5%, +10% from current spot
        if spot_scenarios is None:
            spot_scenarios = [
                current_spot * 0.90,
                current_spot * 0.95,
                current_spot,
                current_spot * 1.05,
                current_spot * 1.10
            ]
        
        results = []
        
        for future_spot in spot_scenarios:
            # P&L on hedged portion (locked in at forward rate)
            hedged_amount = hedge_info['Hedged_Amount']
            hedged_pnl = hedged_amount * (future_spot - forward_rate)
            
            # P&L on unhedged portion (exposed to spot movement)
            unhedged_amount = hedge_info['Unhedged_Amount']
            unhedged_pnl = unhedged_amount * (future_spot - current_spot)
            
            total_pnl = hedged_pnl + unhedged_pnl
            
            # Calculate effective rate achieved
            if notional > 0:
                effective_rate = forward_rate * hedge_ratio + future_spot * (1 - hedge_ratio)
            else:
                effective_rate = future_spot
            
            spot_change_pct = ((future_spot - current_spot) / current_spot) * 100
            
            results.append({
                'Future_Spot': round(future_spot, 4),
                'Spot_Change_pct': round(spot_change_pct, 2),
                'Hedged_PnL': round(hedged_pnl, 2),
                'Unhedged_PnL': round(unhedged_pnl, 2),
                'Total_PnL': round(total_pnl, 2),
                'Effective_Rate': round(effective_rate, 4)
            })
        
        return pd.DataFrame(results)
    
    def compare_hedge_ratios(self, notional: float, tenor: str,
                            future_spot: float) -> pd.DataFrame:
        """
        Compare P&L outcomes across different hedge ratios for a given future spot rate
        
        Args:
            notional: Exposure amount
            tenor: Hedging tenor
            future_spot: Expected/scenario future spot rate
            
        Returns:
            DataFrame comparing different hedging strategies
        """
        hedge_ratios = [0.0, 0.25, 0.50, 0.75, 1.0]
        results = []
        
        for ratio in hedge_ratios:
            scenario_df = self.scenario_analysis(
                notional, tenor, ratio, [future_spot]
            )
            
            results.append({
                'Hedge_Ratio': f"{int(ratio*100)}%",
                'Hedged_Amount': notional * ratio,
                'Unhedged_Amount': notional * (1 - ratio),
                'Total_PnL': scenario_df['Total_PnL'].iloc[0],
                'Effective_Rate': scenario_df['Effective_Rate'].iloc[0]
            })
        
        return pd.DataFrame(results)
    
    def generate_hedge_recommendation(self, notional: float, tenor: str,
                                     market_view: str = 'neutral') -> Dict:
        """
        Generate hedging recommendation based on market view and risk tolerance
        
        Args:
            notional: Exposure amount
            tenor: Hedging tenor
            market_view: 'bullish', 'neutral', or 'bearish' on base currency
            
        Returns:
            Dictionary with recommendation details
        """
        hedge_info = self.calculate_hedge_cost(notional, tenor)
        spot = hedge_info['Spot_Rate']
        forward = hedge_info['Forward_Rate']
        
        # Determine hedge ratio based on market view
        if market_view.lower() == 'bullish':
            # Bullish on base currency = expect it to strengthen
            # Lower hedge ratio to maintain exposure
            recommended_ratio = 0.50
            rationale = f"With a bullish view on {self.pair.split('/')[0]}, consider a 50% hedge to maintain some upside exposure while protecting against adverse moves."
        elif market_view.lower() == 'bearish':
            # Bearish on base currency = expect it to weaken
            # Higher hedge ratio to lock in current rates
            recommended_ratio = 1.00
            rationale = f"With a bearish view on {self.pair.split('/')[0]}, consider a 100% hedge to lock in current forward rate and eliminate downside risk."
        else:
            # Neutral view
            recommended_ratio = 0.75
            rationale = f"With a neutral market view, consider a 75% hedge to protect core exposure while maintaining some flexibility."
        
        hedge_details = self.calculate_hedge_cost(notional, tenor, recommended_ratio)
        
        return {
            'Recommendation': f"{int(recommended_ratio*100)}% Hedge Ratio",
            'Rationale': rationale,
            'Hedge_Details': hedge_details,
            'Forward_Premium_Discount': f"{hedge_details['Premium_Discount_pct']:.2f}%",
            'Action': f"Enter FX Forward to sell {hedge_details['Hedged_Amount']:,.0f} {self.pair.split('/')[0]} vs {self.pair.split('/')[1]} at {forward:.4f} for {tenor} settlement"
        }


if __name__ == "__main__":
    # Example usage with sample forward curve data
    sample_curve = pd.DataFrame({
        'Pair': ['USD/CAD'] * 8,
        'Tenor': ['Spot', '1W', '1M', '2M', '3M', '6M', '9M', '1Y'],
        'Days': [0, 7, 30, 60, 90, 180, 270, 365],
        'Forward_Rate': [1.3450, 1.3455, 1.3468, 1.3485, 1.3502, 1.3550, 1.3598, 1.3645],
        'Forward_Points': [0, 5, 18, 35, 52, 100, 148, 195],
        'Settlement_Date': [(datetime.now() + timedelta(days=d)).strftime('%Y-%m-%d') 
                           for d in [0, 7, 30, 60, 90, 180, 270, 365]]
    })
    
    analyzer = HedgingAnalyzer(sample_curve)
    
    # Scenario: Canadian importer expecting USD 5M payment in 6 months
    print("="*70)
    print("HEDGING ANALYSIS: Canadian Importer with USD 5M Receivable in 6M")
    print("="*70)
    
    hedge_cost = analyzer.calculate_hedge_cost(
        notional=5_000_000,
        tenor='6M',
        hedge_ratio=0.75
    )
    
    print("\nHedge Details:")
    for key, value in hedge_cost.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*70)
    print("SCENARIO ANALYSIS (75% Hedge)")
    print("="*70)
    scenarios = analyzer.scenario_analysis(
        notional=5_000_000,
        tenor='6M',
        hedge_ratio=0.75
    )
    print(scenarios.to_string(index=False))
    
    print("\n" + "="*70)
    print("HEDGE RATIO COMPARISON (Future Spot: 1.3200)")
    print("="*70)
    comparison = analyzer.compare_hedge_ratios(
        notional=5_000_000,
        tenor='6M',
        future_spot=1.3200
    )
    print(comparison.to_string(index=False))
    
    print("\n" + "="*70)
    print("RECOMMENDATION (Bearish View on USD)")
    print("="*70)
    recommendation = analyzer.generate_hedge_recommendation(
        notional=5_000_000,
        tenor='6M',
        market_view='bearish'
    )
    print(f"\n{recommendation['Recommendation']}")
    print(f"\nRationale: {recommendation['Rationale']}")
    print(f"\nAction: {recommendation['Action']}")
