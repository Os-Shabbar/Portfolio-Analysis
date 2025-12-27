# Portfolio-Analysis
portfolio optimization Using Python 
# Saudi Stock Portfolio Analysis and Optimization

## Overview
This project performs a comprehensive analysis of selected Saudi stocks over the past 5 years. The analysis includes:

- Historical stock price trends and correlation analysis.
- Calculation of daily returns, annualized returns, volatility, and Sharpe ratio.
- Optimal portfolio allocation using Modern Portfolio Theory (MPT) and Sharpe ratio maximization.
- Monte Carlo simulations to assess portfolio risk and estimate Value at Risk (VaR) and Conditional VaR (CVaR).
- Comparison of optimal portfolio with individual stocks and equal-weight portfolios.
- Export of results to Excel for further analysis.

---

## Saudi Stocks Included
| Ticker | Company Name |
|--------|--------------|
| 1212.SR | Alinma Bank |
| 4140.SR | SABIC Agri‑Nutrients |
| 4320.SR | ALANDALUS |
| 2120.SR | SAIC |
| 8260.SR | Gulf General |
| 1210.SR | SABIC |
| 2222.SR | Saudi Aramco |
| 1120.SR | Al Rajhi Bank |
| 7010.SR | STC |
| 1211.SR | Ma’aden |
| 1010.SR | Riyad Bank |
| 1060.SR | Saudi First Bank |
| 2380.SR | Petro Rabigh |
| 4300.SR | Dar Al Arkan |
| 2280.SR | Almarai |

---
## Analysis Result of the Saudi stocks:
# Expected Annual Return: 34.29%

# Expected Annual Volatility: 22.15%

# Sharpe Ratio: 1.458

-Expected Annual Return (34.29%): This is the mean return the optimized portfolio is expected to generate in a year based on historical data. It’s relatively high, but possible in emerging markets like Saudi Arabia, which can have periods of strong growth.
-Expected Annual Volatility (22.15%): This measures the risk (standard deviation of returns). A 22% volatility is moderate-to-high, which aligns with a high-growth portfolio.
-Sharpe Ratio (1.458): This is a measure of risk-adjusted return. Values above 1 are generally considered very good. A Sharpe > 1.4 suggests the portfolio has strong returns relative to its risk.

##Monte Carlo Risk Metrics Result:
# 95% VaR: -4.33%
# 95% CVaR: -12.92%
# Maximum Simulated Return: 210.89%
# Minimum Simulated Return: -39.96%
# Probability of Positive Return: 92.8%

- 95% VaR (-4.33%): There is a 5% chance that the portfolio will lose more than 4.33% over one year. This shows that extreme losses are limited but possible.
- 95% CVaR (-12.92%): If losses exceed the 95% VaR threshold, the expected average loss is -12.92%. This gives insight into the “tail risk.”
- Maximum Simulated Return (210.89%): Some Monte Carlo simulations produced very high returns, reflecting extreme positive outcomes.
- Minimum Simulated Return (-39.96%): Some simulations show significant downside risk, reflecting market crashes or high volatility periods.
- Probability of Positive Return (92.8%): The model suggests a high likelihood of a positive return over a year.

## Plots / Visualizations

### 1. Stock Prices (5 Years)
![Stock Prices 5 Year](Plots/Stock%20Prices%205%20Year.png)  
Shows the adjusted closing prices for all selected Saudi stocks over the past 5 years.

---

### 2. Optimal Portfolio Allocation
![Optimal Portfolio Allocation](Plots/Optimal%20Portfolio%20allocation.png)  
Visual representation of the weights of each stock in the optimal portfolio based on Sharpe ratio maximization.

---

### 3. Correlation Heatmap
![Correlation Heatmap](Plots/correlation_heatmap.png)  
Displays the correlation matrix of daily returns for all selected stocks.  
- Red → positive correlation  
- Blue → negative correlation  
- White → weak or no correlation

---

### 4. Monte Carlo Simulation - Portfolio Returns Distribution
![Monte Carlo Simulation - Portfolio Returns Distribution](Plots/Monte%20Carlo%20Simulation%20-%20Portfolio%20Returns%20Distribution.png)  
Distribution of simulated portfolio returns based on Monte Carlo simulations (historical data).

---

### 5. Monte Carlo Simulation - 1 Year Portfolio Returns Distribution
![Monte Carlo Simulation - 1 year Portfolio Returns Distribution](Plots/Monte%20Carlo%20Simulation%20-%201%20year%20Portfolio%20Returns%20Distribution.png)  
Distribution of simulated portfolio returns for 1-year ahead projection using Monte Carlo simulation.
