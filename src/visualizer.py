"""
FX Visualization Module
Creates professional charts and reports for FX analysis
Author: Jordan Ing
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from typing import Dict, List
import os


class FXVisualizer:
    """Creates visualizations for FX forward curves and hedging analysis"""
    
    def __init__(self, output_dir: str = '../outputs'):
        """
        Initialize visualizer
        
        Args:
            output_dir: Directory to save output charts
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set professional style
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#E74C3C',
            'accent': '#3498DB',
            'positive': '#27AE60',
            'negative': '#E74C3C'
        }
    
    def plot_forward_curve(self, forward_curve: pd.DataFrame, 
                          save_path: str = None) -> str:
        """
        Plot forward curve showing rates across tenors
        
        Args:
            forward_curve: DataFrame with forward rate data
            save_path: Optional custom save path
            
        Returns:
            Path to saved chart
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        pair = forward_curve['Pair'].iloc[0]
        spot_rate = forward_curve[forward_curve['Tenor'] == 'Spot']['Forward_Rate'].iloc[0]
        
        # Filter out Spot for forward curve plot
        forward_only = forward_curve[forward_curve['Tenor'] != 'Spot'].copy()
        
        # Plot 1: Forward Rates
        ax1.plot(forward_only['Tenor'], forward_only['Forward_Rate'], 
                marker='o', linewidth=2, markersize=8, 
                color=self.colors['primary'], label='Forward Rate')
        ax1.axhline(y=spot_rate, color=self.colors['secondary'], 
                   linestyle='--', linewidth=1.5, label=f'Spot Rate: {spot_rate:.4f}')
        
        ax1.set_title(f'{pair} Forward Curve', fontsize=14, fontweight='bold', pad=20)
        ax1.set_xlabel('Tenor', fontsize=11)
        ax1.set_ylabel('Exchange Rate', fontsize=11)
        ax1.legend(loc='best', fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Add value labels on points
        for idx, row in forward_only.iterrows():
            ax1.annotate(f"{row['Forward_Rate']:.4f}", 
                        (row['Tenor'], row['Forward_Rate']),
                        textcoords="offset points", xytext=(0,10), 
                        ha='center', fontsize=8)
        
        # Plot 2: Forward Points
        colors = [self.colors['positive'] if x >= 0 else self.colors['negative'] 
                 for x in forward_only['Forward_Points']]
        
        ax2.bar(forward_only['Tenor'], forward_only['Forward_Points'], 
               color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
        ax2.axhline(y=0, color='black', linewidth=1)
        ax2.set_title('Forward Points (pips)', fontsize=12, fontweight='bold', pad=15)
        ax2.set_xlabel('Tenor', fontsize=11)
        ax2.set_ylabel('Forward Points', fontsize=11)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for idx, row in forward_only.iterrows():
            height = row['Forward_Points']
            ax2.text(row['Tenor'], height, f"{height:.1f}",
                    ha='center', va='bottom' if height >= 0 else 'top',
                    fontsize=8)
        
        plt.tight_layout()
        
        if save_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(self.output_dir, f'forward_curve_{pair.replace("/", "")}_{timestamp}.png')
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def plot_scenario_analysis(self, scenario_df: pd.DataFrame, 
                              hedge_info: Dict,
                              save_path: str = None) -> str:
        """
        Plot P&L across different future spot rate scenarios
        
        Args:
            scenario_df: DataFrame with scenario analysis results
            hedge_info: Dictionary with hedging details
            save_path: Optional custom save path
            
        Returns:
            Path to saved chart
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        x = scenario_df['Future_Spot']
        
        # Plot P&L components
        ax.plot(x, scenario_df['Total_PnL'], marker='o', linewidth=3, 
               markersize=10, color=self.colors['primary'], 
               label='Total P&L', zorder=3)
        ax.plot(x, scenario_df['Hedged_PnL'], marker='s', linewidth=2, 
               markersize=8, color=self.colors['accent'], 
               label='Hedged P&L', linestyle='--', alpha=0.7)
        ax.plot(x, scenario_df['Unhedged_PnL'], marker='^', linewidth=2, 
               markersize=8, color=self.colors['secondary'], 
               label='Unhedged P&L', linestyle='--', alpha=0.7)
        
        # Add zero line
        ax.axhline(y=0, color='black', linewidth=1.5, linestyle='-', alpha=0.3)
        
        # Highlight current spot and forward rates
        current_spot = hedge_info['Spot_Rate']
        forward_rate = hedge_info['Forward_Rate']
        
        ax.axvline(x=current_spot, color=self.colors['positive'], 
                  linestyle=':', linewidth=2, alpha=0.5, label=f'Current Spot: {current_spot:.4f}')
        ax.axvline(x=forward_rate, color=self.colors['negative'], 
                  linestyle=':', linewidth=2, alpha=0.5, label=f'Forward Rate: {forward_rate:.4f}')
        
        # Formatting
        pair = hedge_info['Pair']
        notional = hedge_info['Notional']
        hedge_ratio = hedge_info['Hedge_Ratio']
        tenor = hedge_info['Tenor']
        
        ax.set_title(f'FX Hedging Scenario Analysis: {pair}\n'
                    f'Notional: {notional:,.0f} | Hedge Ratio: {hedge_ratio:.0%} | Tenor: {tenor}',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Future Spot Rate', fontsize=12)
        ax.set_ylabel('P&L', fontsize=12)
        ax.legend(loc='best', fontsize=10, framealpha=0.9)
        ax.grid(True, alpha=0.3)
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Add annotations for key points
        for idx, row in scenario_df.iterrows():
            if idx % 2 == 0:  # Annotate every other point to avoid crowding
                ax.annotate(f"${row['Total_PnL']:,.0f}",
                          xy=(row['Future_Spot'], row['Total_PnL']),
                          xytext=(10, 10), textcoords='offset points',
                          fontsize=8, bbox=dict(boxstyle='round,pad=0.3', 
                          facecolor='yellow', alpha=0.3))
        
        plt.tight_layout()
        
        if save_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(self.output_dir, f'scenario_analysis_{timestamp}.png')
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def plot_hedge_ratio_comparison(self, comparison_df: pd.DataFrame,
                                   pair: str, future_spot: float,
                                   save_path: str = None) -> str:
        """
        Compare outcomes across different hedge ratios
        
        Args:
            comparison_df: DataFrame with hedge ratio comparison
            pair: Currency pair
            future_spot: Future spot rate used in analysis
            save_path: Optional custom save path
            
        Returns:
            Path to saved chart
        """
        fig, ax = plt.subplots(figsize=(12, 7))
        
        x = range(len(comparison_df))
        colors_bar = [self.colors['positive'] if pnl >= 0 else self.colors['negative'] 
                     for pnl in comparison_df['Total_PnL']]
        
        bars = ax.bar(x, comparison_df['Total_PnL'], 
                     color=colors_bar, alpha=0.7, 
                     edgecolor='black', linewidth=1.5)
        
        ax.axhline(y=0, color='black', linewidth=1.5)
        ax.set_xticks(x)
        ax.set_xticklabels(comparison_df['Hedge_Ratio'], fontsize=11)
        
        ax.set_title(f'Hedge Ratio Comparison: {pair}\n'
                    f'Future Spot Scenario: {future_spot:.4f}',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Hedge Ratio', fontsize=12)
        ax.set_ylabel('Total P&L', fontsize=12)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for i, (bar, row) in enumerate(zip(bars, comparison_df.itertuples())):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${row.Total_PnL:,.0f}\n({row.Effective_Rate:.4f})',
                   ha='center', va='bottom' if height >= 0 else 'top',
                   fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(self.output_dir, f'hedge_ratio_comparison_{timestamp}.png')
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def create_summary_dashboard(self, forward_curves: Dict[str, pd.DataFrame],
                                save_path: str = None) -> str:
        """
        Create dashboard showing multiple forward curves
        
        Args:
            forward_curves: Dictionary mapping pair names to forward curve DataFrames
            save_path: Optional custom save path
            
        Returns:
            Path to saved chart
        """
        n_pairs = len(forward_curves)
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        axes = axes.flatten()
        
        for idx, (pair, curve_df) in enumerate(forward_curves.items()):
            if idx >= 6:  # Max 6 pairs on dashboard
                break
            
            ax = axes[idx]
            forward_only = curve_df[curve_df['Tenor'] != 'Spot'].copy()
            spot_rate = curve_df[curve_df['Tenor'] == 'Spot']['Forward_Rate'].iloc[0]
            
            ax.plot(forward_only['Tenor'], forward_only['Forward_Rate'],
                   marker='o', linewidth=2, markersize=6,
                   color=self.colors['primary'])
            ax.axhline(y=spot_rate, color=self.colors['secondary'],
                      linestyle='--', linewidth=1, alpha=0.7)
            
            ax.set_title(pair, fontsize=11, fontweight='bold')
            ax.set_xlabel('Tenor', fontsize=9)
            ax.set_ylabel('Rate', fontsize=9)
            ax.tick_params(labelsize=8)
            ax.grid(True, alpha=0.3)
        
        # Hide unused subplots
        for idx in range(n_pairs, 6):
            axes[idx].axis('off')
        
        fig.suptitle('FX Forward Curves Dashboard', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        plt.tight_layout()
        
        if save_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(self.output_dir, f'fx_dashboard_{timestamp}.png')
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path


if __name__ == "__main__":
    print("FX Visualizer module - import and use with FX data")
