"""
FX Data Fetcher Module
Retrieves spot FX rates and calculates forward rates using interest rate parity
Author: Jordan Ing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from typing import Dict, List, Tuple


class FXDataFetcher:
    """Fetches and processes FX market data for forward curve construction"""
    
    def __init__(self):
        self.major_pairs = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'USDCAD=X', 'AUDUSD=X', 'USDCHF=X']
        self.pair_names = {
            'EURUSD=X': 'EUR/USD',
            'GBPUSD=X': 'GBP/USD', 
            'USDJPY=X': 'USD/JPY',
            'USDCAD=X': 'USD/CAD',
            'AUDUSD=X': 'AUD/USD',
            'USDCHF=X': 'USD/CHF'
        }
        
        # Approximate interest rates (in practice, would fetch from market data)
        # These are illustrative annual rates
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
        """
        Fetch current spot rates for major currency pairs
        
        Returns:
            DataFrame with currency pairs and spot rates
        """
        spot_data = []
        
        for ticker in self.major_pairs:
            try:
                data = yf.Ticker(ticker)
                hist = data.history(period='1d')
                
                if not hist.empty:
                    spot_rate = hist['Close'].iloc[-1]
                    spot_data.append({
                        'Ticker': ticker,
                        'Pair': self.pair_names[ticker],
                        'Spot_Rate': round(spot_rate, 4),
                        'Timestamp': datetime.now()
                    })
            except Exception as e:
                print(f"Error fetching {ticker}: {e}")
                continue
        
        return pd.DataFrame(spot_data)
    
    def calculate_forward_rate(self, spot_rate: float, domestic_rate: float, 
                              foreign_rate: float, days: int) -> float:
        """
        Calculate forward rate using Interest Rate Parity
        
        F = S * (1 + r_domestic * t) / (1 + r_foreign * t)
        
        Args:
            spot_rate: Current spot exchange rate
            domestic_rate: Domestic interest rate (annualized)
            foreign_rate: Foreign interest rate (annualized)
            days: Number of days to forward date
            
        Returns:
            Forward rate
        """
        t = days / 365.0
        forward_rate = spot_rate * ((1 + domestic_rate * t) / (1 + foreign_rate * t))
        return round(forward_rate, 4)
    
    def build_forward_curve(self, pair: str, spot_rate: float) -> pd.DataFrame:
        """
        Construct forward curve for a currency pair across standard tenors
        
        Args:
            pair: Currency pair (e.g., 'EUR/USD')
            spot_rate: Current spot rate
            
        Returns:
            DataFrame with forward rates for different tenors
        """
        # Extract base and quote currencies
        base_ccy = pair.split('/')[0]
        quote_ccy = pair.split('/')[1]
        
        # Standard FX forward tenors
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
                # For pairs like EUR/USD, domestic is USD, foreign is EUR
                # For pairs like USD/CAD, domestic is CAD, foreign is USD
                if quote_ccy == 'USD':
                    domestic_rate = self.interest_rates['USD']
                    foreign_rate = self.interest_rates[base_ccy]
                else:
                    domestic_rate = self.interest_rates[quote_ccy]
                    foreign_rate = self.interest_rates['USD']
                
                forward_rate = self.calculate_forward_rate(
                    spot_rate, domestic_rate, foreign_rate, days
                )
                forward_points = round((forward_rate - spot_rate) * 10000, 2)  # in pips
            
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
        """
        Build forward curves for all major currency pairs
        
        Returns:
            Dictionary mapping pair names to their forward curve DataFrames
        """
        spot_df = self.get_spot_rates()
        forward_curves = {}
        
        for _, row in spot_df.iterrows():
            pair = row['Pair']
            spot = row['Spot_Rate']
            curve = self.build_forward_curve(pair, spot)
            forward_curves[pair] = curve
        
        return forward_curves


if __name__ == "__main__":
    # Example usage
    fetcher = FXDataFetcher()
    
    print("Fetching spot rates...")
    spots = fetcher.get_spot_rates()
    print("\n" + "="*60)
    print("SPOT FX RATES")
    print("="*60)
    print(spots.to_string(index=False))
    
    print("\n\nBuilding forward curves...")
    curves = fetcher.get_all_forward_curves()
    
    for pair, curve_df in curves.items():
        print("\n" + "="*60)
        print(f"FORWARD CURVE: {pair}")
        print("="*60)
        print(curve_df.to_string(index=False))
