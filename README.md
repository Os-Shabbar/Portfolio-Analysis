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
