# FX Forward Curve & Hedging Analyzer

A professional-grade Python tool for FX forward curve construction and corporate hedging analysis. Built for sales & trading and treasury risk management applications.

**Author:** Jordan Ing  
**Institution:** Dalhousie University, Rowe School of Business  
**Focus:** Commercial FX Risk Solutions & Capital Markets

---

## 🎯 Project Overview

This tool enables corporate clients and treasury teams to:
- **Build FX forward curves** across standard market tenors using live spot rates
- **Analyze hedging strategies** for managing foreign exchange exposure
- **Generate scenario analyses** showing P&L outcomes under different market conditions
- **Compare hedge ratios** to optimize risk/reward profiles
- **Receive data-driven recommendations** based on market views and risk tolerance
- **Produce professional visualizations** suitable for client presentations

The project demonstrates practical application of **Python, quantitative finance, and financial engineering** in a front-office trading context.

---

## 🚀 Key Features

### 1. **Real-Time Market Data Integration**
- Fetches live FX spot rates for major currency pairs (EUR/USD, GBP/USD, USD/JPY, USD/CAD, AUD/USD, USD/CHF)
- Uses `yfinance` API for reliable market data

### 2. **Forward Curve Construction**
- Calculates forward rates using **Interest Rate Parity** (IRP) theory
- Generates curves across standard tenors: 1W, 1M, 2M, 3M, 6M, 9M, 1Y
- Computes forward points in pips for trader-friendly analysis

### 3. **Hedging Strategy Analysis**
- Analyzes partial and full hedge strategies
- Calculates P&L under multiple future spot scenarios
- Compares outcomes across different hedge ratios (0%, 25%, 50%, 75%, 100%)

### 4. **Scenario Modeling**
- Models +/- 10% spot rate movements
- Shows hedged vs. unhedged P&L components
- Calculates effective exchange rates achieved

### 5. **Professional Visualizations**
- Forward curve charts with spot rate overlays
- Forward points bar charts
- Scenario analysis P&L plots
- Hedge ratio comparison graphs
- Multi-pair FX dashboard

### 6. **Automated Reporting**
- Exports analysis data to CSV format
- Generates timestamp-stamped outputs
- Creates presentation-ready charts

---

## 📊 Business Use Cases

### **Corporate Treasury**
- A Canadian importer expects USD $5M payment in 6 months
- Tool analyzes hedging USD/CAD exposure at forward rates
- Recommends optimal hedge ratio based on risk appetite

### **Risk Management**
- Treasury team evaluates impact of +/- 5% FX moves
- Compares fully hedged vs. partially hedged outcomes
- Quantifies downside protection vs. upside retention

### **Sales & Trading**
- Commercial FX desk presents hedging solutions to clients
- Shows clients visual P&L scenarios to support decision-making
- Demonstrates value of forward contracts vs. remaining unhedged

---

## 🛠️ Technical Implementation

### **Core Technologies**
- **Python 3.8+** - Primary development language
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **matplotlib** - Data visualization
- **yfinance** - Market data API

### **Financial Concepts Applied**
- **Interest Rate Parity (IRP)**: Forward pricing theory
- **Forward Points**: Pip-based forward premium/discount calculation
- **Scenario Analysis**: Risk modeling under market stress
- **Hedge Ratio Optimization**: Balancing protection vs. opportunity cost

### **Code Architecture**
```
fx-hedging-analyzer/
├── main.py                      # Main application orchestrator
├── src/
│   ├── fx_data_fetcher.py      # Market data retrieval & forward pricing
│   ├── hedging_analyzer.py     # Hedging strategy logic & scenario analysis
│   └── visualizer.py           # Chart generation & dashboards
├── outputs/                    # Generated reports and charts
├── data/                       # Sample/historical data (if needed)
├── tests/                      # Unit tests
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 📥 Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- pip package manager
- Internet connection (for live market data)

### **Installation Steps**

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/fx-hedging-analyzer.git
cd fx-hedging-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the tool**
```bash
# Default example (Canadian importer, USD 5M, 6M tenor)
python main.py

# Interactive mode (custom parameters)
python main.py --interactive
```

---

## 💡 Usage Examples

### **Example 1: Default Analysis**
```bash
python main.py
```
Analyzes a Canadian importer hedging USD $5M receivable in 6 months using a 75% hedge ratio with neutral market view.

### **Example 2: Interactive Mode**
```bash
python main.py --interactive
```
Prompts user for:
- Currency pair selection
- Exposure amount
- Hedging tenor
- Hedge ratio
- Market view (bullish/neutral/bearish)

### **Example 3: Programmatic Usage**
```python
from fx_data_fetcher import FXDataFetcher
from hedging_analyzer import HedgingAnalyzer

# Fetch market data
fetcher = FXDataFetcher()
curves = fetcher.get_all_forward_curves()

# Analyze EUR/USD hedging
eur_curve = curves['EUR/USD']
analyzer = HedgingAnalyzer(eur_curve)

# Get recommendation
recommendation = analyzer.generate_hedge_recommendation(
    notional=10_000_000,
    tenor='3M',
    market_view='bearish'
)
print(recommendation)
```

---

## 📈 Sample Outputs

### **Forward Curve**
![Forward Curve Example](outputs/sample_forward_curve.png)

### **Scenario Analysis**
![Scenario Analysis Example](outputs/sample_scenario_analysis.png)

### **Hedge Ratio Comparison**
![Hedge Comparison Example](outputs/sample_hedge_comparison.png)

---

## 🧪 Testing

Run unit tests (once implemented):
```bash
python -m pytest tests/
```

---

## 🔮 Future Enhancements

- [ ] **Options Pricing**: Add FX options (calls/puts) for hedging analysis
- [ ] **Live Bloomberg API Integration**: Replace yfinance with institutional data feeds
- [ ] **Monte Carlo Simulation**: Run 10,000+ scenarios for robust risk assessment
- [ ] **VaR Calculation**: Compute Value-at-Risk for hedged vs. unhedged portfolios
- [ ] **Multi-Currency Exposure**: Handle baskets of FX exposures simultaneously
- [ ] **Database Integration**: Store historical analysis for backtesting strategies
- [ ] **Web Dashboard**: Flask/Django interface for browser-based analysis
- [ ] **PDF Report Generation**: Automated client-ready reports

---

## 📚 Theoretical Background

### **Interest Rate Parity (IRP)**
The forward rate is determined by the interest rate differential between two currencies:

```
F = S × [(1 + r_domestic × t) / (1 + r_foreign × t)]
```

Where:
- `F` = Forward rate
- `S` = Spot rate
- `r_domestic` = Domestic interest rate (annualized)
- `r_foreign` = Foreign interest rate (annualized)
- `t` = Time to maturity (in years)

### **Forward Points**
Forward points represent the difference between forward and spot rates, quoted in pips:

```
Forward Points = (Forward Rate - Spot Rate) × 10,000
```

Positive points = Forward premium (base currency trading at premium)  
Negative points = Forward discount (base currency trading at discount)

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add your feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👤 About the Author

**Jordan Ing**  
Bachelor of Commerce (Finance) - Dalhousie University  
Previous Intern: TD Securities (Global Markets - Securities Lending & Electronic Equities)  
Upcoming: TD Securities (Commercial FX Risk Solutions Group)

**Technical Skills:** Python, SQL, VBA, Excel, Financial Modeling  
**Interests:** Sales & Trading, Quantitative Finance, Market Microstructure

Connect: [LinkedIn](https://linkedin.com/in/yourprofile) | Email: jordaning11@gmail.com

---

## 📞 Contact & Support

For questions, suggestions, or collaboration opportunities:
- **Email**: jordaning11@gmail.com
- **GitHub Issues**: [Submit an issue](https://github.com/yourusername/fx-hedging-analyzer/issues)

---

## 🙏 Acknowledgments

- **Dalhousie Investment Society (DALIS)** - For fostering applied finance skills
- **TD Securities** - For providing real-world trading context and inspiration
- **Open-source community** - For the amazing Python finance ecosystem

---

**Last Updated:** December 2024  
**Version:** 1.0.0
