"""
FX Data Simulator (for demonstration/offline use)
Generates realistic FX data when live market data is unavailable
Author: Jordan Ing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict


class FXDataSimulator:
    """Simulates FX market data for demonstration purposes"""
    
    def __init__(self):
        # Realistic spot rates as of December 2024
        self.spot_rates = {
            'EUR/USD': 1.0545,
            'GBP/USD': 1.2675,
            'USD/JPY': 149.85,
            'USD/CAD': 1.4320,
            'AUD/USD': 0.6315,
            'USD/CHF': 0.8895
        }
        
        # Interest rates (annualized)
        self.interest_rates = {
            'USD': 0.0450,
            'EUR': 0.0300,
            'GBP': 0.0475,
            'JPY': 0.0010,
            'CAD': 0.0375,
            'AUD': 0.0400,
            'CHF': 0.0125
        }
    
    def get_spot_rates(self) -> pd.DataFrame:
        """Generate simulated spot rates"""
        spot_data = []
        
        for pair, rate in self.spot_rates.items():
            # Add small random variation (+/- 0.5%)
            variation = np.random.uniform(-0.005, 0.005)
            simulated_rate = rate * (1 + variation)
            
            spot_data.append({
                'Pair': pair,
                'Spot_Rate': round(simulated_rate, 4),
                'Timestamp': datetime.now()
            })
        
        return pd.DataFrame(spot_data)
    
    def calculate_forward_rate(self, spot_rate: float, domestic_rate: float,
                              foreign_rate: float, days: int) -> float:
        """Calculate forward rate using IRP"""
        t = days / 365.0
        forward_rate = spot_rate * ((1 + domestic_rate * t) / (1 + foreign_rate * t))
        return round(forward_rate, 4)
    
    def build_forward_curve(self, pair: str, spot_rate: float) -> pd.DataFrame:
        """Build forward curve for a currency pair"""
        base_ccy = pair.split('/')[0]
        quote_ccy = pair.split('/')[1]
        
        tenors = {
            'Spot': 0,
            '1W': 7,
            '1M': 30,
            '2M': 60,
            '3M': 90,
            '6M': 180,
            '9M': 270,
            '1Y': 365
        }
        
        forward_data = []
        
        for tenor_name, days in tenors.items():
            if days == 0:
                forward_rate = spot_rate
                forward_points = 0
            else:
                if quote_ccy == 'USD':
                    domestic_rate = self.interest_rates['USD']
                    foreign_rate = self.interest_rates[base_ccy]
                else:
                    domestic_rate = self.interest_rates[quote_ccy]
                    foreign_rate = self.interest_rates['USD']
                
                forward_rate = self.calculate_forward_rate(
                    spot_rate, domestic_rate, foreign_rate, days
                )
                forward_points = round((forward_rate - spot_rate) * 10000, 2)
            
            forward_data.append({
                'Pair': pair,
                'Tenor': tenor_name,
                'Days': days,
                'Forward_Rate': forward_rate,
                'Forward_Points': forward_points,
                'Settlement_Date': (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
            })
        
        return pd.DataFrame(forward_data)
    
    def get_all_forward_curves(self) -> Dict[str, pd.DataFrame]:
        """Build forward curves for all pairs"""
        spot_df = self.get_spot_rates()
        forward_curves = {}
        
        for _, row in spot_df.iterrows():
            pair = row['Pair']
            spot = row['Spot_Rate']
            curve = self.build_forward_curve(pair, spot)
            forward_curves[pair] = curve
        
        return forward_curves


if __name__ == "__main__":
    simulator = FXDataSimulator()
    
    print("="*60)
    print("SIMULATED SPOT RATES")
    print("="*60)
    spots = simulator.get_spot_rates()
    print(spots.to_string(index=False))
    
    print("\n" + "="*60)
    print("SAMPLE FORWARD CURVE: USD/CAD")
    print("="*60)
    curves = simulator.get_all_forward_curves()
    print(curves['USD/CAD'].to_string(index=False))
