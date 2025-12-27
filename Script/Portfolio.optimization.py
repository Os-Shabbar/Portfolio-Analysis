import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Saudi stocks
saudi_stocks = [
    "1212.SR",  # Alinma Bank
    "4140.SR",  # SABIC Agri‑Nutrients
    "4320.SR",  # ALANDALUS
    "2120.SR",  # SAIC
    "8260.SR",  # Gulf General
    "1210.SR",  # SABIC
    "2222.SR",  # Saudi Aramco
    "1120.SR",  # Al Rajhi Bank
    "7010.SR",  # STC
    "1211.SR",  # Ma’aden (gold & mining)
    "1010.SR",  # Riyad Bank
    "1060.SR",  # Saudi First Bank
    "2380.SR",  # Petro Rabigh
    "4300.SR",  # Dar Al Arkan
    "2280.SR",  # Almarai
]

# Define time period
end_date = datetime.now()
start_date = end_date - timedelta(days=365*5)  # 5 years of data

# Download stock data
stock_data = yf.download(saudi_stocks, start=start_date, end=end_date, progress=False)
print("Data download complete!")

# Extract adjusted close prices
prices = stock_data['Close']

# Check for missing values
print("Missing values in each stock:")
print(prices.isnull().sum())

# Forward fill missing values (if any)
prices = prices.ffill()

# Calculate daily returns
returns = prices.pct_change().dropna()

# Basic statistics
print("\nBasic Statistics of Daily Returns:")
print(returns.describe())

# Plot price trends
plt.figure(figsize=(14, 8))
for stock in saudi_stocks:
    plt.plot(prices.index, prices[stock], label=stock, linewidth=2)
plt.title('Stock Price Trends (3 Years)', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Adjusted Close Price (SAR)', fontsize=12)
plt.legend()
plt.tight_layout()
plt.show()


# Calculate annualized metrics
annual_returns = returns.mean() * 252
annual_volatility = returns.std() * np.sqrt(252)
sharpe_ratio = annual_returns / annual_volatility

# Create metrics dataframe
metrics_df = pd.DataFrame({
    'Annual Return': annual_returns,
    'Annual Volatility': annual_volatility,
    'Sharpe Ratio': sharpe_ratio
})

print("Risk-Return Metrics:")
print(metrics_df)

# Plot risk-return scatter
plt.figure(figsize=(10, 6))
plt.scatter(metrics_df['Annual Volatility'], metrics_df['Annual Return'], 
            s=200, alpha=0.6, edgecolors='w', linewidth=2)

# Annotate points
for i, stock in enumerate(metrics_df.index):
    plt.annotate(stock, 
                (metrics_df['Annual Volatility'][i], metrics_df['Annual Return'][i]),
                xytext=(5, 5), textcoords='offset points')

plt.title('Risk-Return Profile of Saudi Stocks', fontsize=16)
plt.xlabel('Annual Volatility (Risk)', fontsize=12)
plt.ylabel('Annual Return', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Calculate correlation matrix
correlation_matrix = returns.corr()

# Plot heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
            center=0, square=True, linewidths=1, 
            cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix of Saudi Stocks', fontsize=16)
plt.tight_layout()
plt.show()

# Plot rolling correlation
window = 60
pairs = [('1212.SR', '1210.SR'), ('1212.SR', '4140.SR'), ('1210.SR', '4140.SR')]

plt.figure(figsize=(14, 8))
for stock1, stock2 in pairs:
    rolling_corr = returns[stock1].rolling(window=window).corr(returns[stock2])
    plt.plot(rolling_corr.index, rolling_corr, label=f'{stock1} vs {stock2}')

plt.title('Rolling Correlations (60-day)')
plt.xlabel('Date')
plt.ylabel('Correlation')
plt.axhline(y=0, color='r', linestyle='--', alpha=0.3)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()


from scipy.optimize import minimize

# Portfolio optimization functions
def portfolio_performance(weights, returns, cov_matrix):
    """Calculate portfolio return and volatility"""
    port_return = np.sum(weights * returns.mean()) * 252
    port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))
    return port_return, port_volatility

def negative_sharpe(weights, returns, cov_matrix, risk_free_rate=0.04):
    """Negative Sharpe ratio for minimization"""
    port_return, port_volatility = portfolio_performance(weights, returns, cov_matrix)
    return -(port_return - risk_free_rate) / port_volatility

def portfolio_variance(weights, cov_matrix):
    """Calculate portfolio variance"""
    return np.dot(weights.T, np.dot(cov_matrix * 252, weights))

# Initialize parameters
n_assets = len(saudi_stocks)
cov_matrix = returns.cov()

# Generate random portfolios for efficient frontier
n_portfolios = 30000
results = np.zeros((3, n_portfolios))
weights_record = []

np.random.seed(42)
for i in range(n_portfolios):
    weights = np.random.random(n_assets)
    weights /= np.sum(weights)
    weights_record.append(weights)
    
    port_return, port_volatility = portfolio_performance(weights, returns, cov_matrix)
    sharpe = (port_return - 0.02) / port_volatility  # Assuming 2% risk-free rate
    
    results[0,i] = port_volatility
    results[1,i] = port_return
    results[2,i] = sharpe

# Find optimal portfolio
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bounds = tuple((0, 1) for _ in range(n_assets))
initial_weights = n_assets * [1./n_assets]

# Maximize Sharpe ratio
opt_sharpe = minimize(negative_sharpe, initial_weights, args=(returns, cov_matrix, 0.02),
                     method='SLSQP', bounds=bounds, constraints=constraints)

optimal_weights = opt_sharpe.x
optimal_return, optimal_volatility = portfolio_performance(optimal_weights, returns, cov_matrix)
optimal_sharpe = -negative_sharpe(optimal_weights, returns, cov_matrix, 0.02)

print("\n" + "="*50)
print("OPTIMAL PORTFOLIO ALLOCATION")
print("="*50)
for stock, weight in zip(saudi_stocks, optimal_weights):
    print(f"{stock}: {weight*100:.2f}%")
print(f"\nExpected Annual Return: {optimal_return*100:.2f}%")
print(f"Expected Annual Volatility: {optimal_volatility*100:.2f}%")
print(f"Sharpe Ratio: {optimal_sharpe:.3f}")

# Plot efficient frontier
plt.figure(figsize=(12, 8))
plt.scatter(results[0,:], results[1,:], c=results[2,:], cmap='viridis', 
            alpha=0.4, s=20)
plt.colorbar(label='Sharpe Ratio')
plt.scatter(optimal_volatility, optimal_return, c='red', 
            s=200, marker='*', label='Optimal Portfolio', edgecolors='black')
plt.xlabel('Annual Volatility', fontsize=12)
plt.ylabel('Annual Return', fontsize=12)
plt.title('Efficient Frontier - Saudi Stocks Portfolio', fontsize=16)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Plot portfolio weights
plt.figure(figsize=(10, 6))
colors = plt.cm.Set3(np.linspace(0, 1, n_assets))
bars = plt.bar(saudi_stocks, optimal_weights*100, color=colors, edgecolor='black')
plt.title('Optimal Portfolio Allocation', fontsize=16)
plt.ylabel('Weight (%)', fontsize=12)
plt.axhline(y=100/n_assets, color='r', linestyle='--', alpha=0.5, label='Equal Weight')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{height:.1f}%', ha='center', va='bottom')

plt.legend()
plt.tight_layout()
plt.show()

# Monte Carlo simulation for portfolio returns
def monte_carlo_simulation(weights, returns, cov_matrix, n_simulations=10000, days=252):
    """Run Monte Carlo simulation for portfolio returns"""
    mean_returns = returns.mean()
    portfolio_returns = []
    
    for _ in range(n_simulations):
        # Generate random returns
        random_returns = np.random.multivariate_normal(mean_returns, cov_matrix, days)
        # Calculate portfolio value
        portfolio_value = np.dot(random_returns, weights)
        # Calculate cumulative return
        cumulative_return = np.prod(1 + portfolio_value) - 1
        portfolio_returns.append(cumulative_return)
    
    return np.array(portfolio_returns)

# Run simulation
simulated_returns = monte_carlo_simulation(optimal_weights, returns, cov_matrix)

# Calculate VaR (Value at Risk) and CVaR (Conditional VaR)
confidence_level = 0.95
var_95 = np.percentile(simulated_returns, (1 - confidence_level) * 100)
cvar_95 = simulated_returns[simulated_returns <= var_95].mean()

print("\n" + "="*50)
print("RISK METRICS (Monte Carlo Simulation)")
print("="*50)
print(f"95% VaR (Value at Risk): {var_95*100:.2f}%")
print(f"95% CVaR (Expected Shortfall): {cvar_95*100:.2f}%")
print(f"Maximum Simulated Return: {simulated_returns.max()*100:.2f}%")
print(f"Minimum Simulated Return: {simulated_returns.min()*100:.2f}%")
print(f"Probability of Positive Return: {(simulated_returns > 0).mean()*100:.1f}%")

# Plot distribution of simulated returns
plt.figure(figsize=(12, 6))
plt.hist(simulated_returns * 100, bins=50, edgecolor='black', alpha=0.7)
plt.axvline(var_95 * 100, color='red', linestyle='--', linewidth=2, label=f'95% VaR: {var_95*100:.2f}%')
plt.axvline(cvar_95 * 100, color='darkred', linestyle='--', linewidth=2, label=f'95% CVaR: {cvar_95*100:.2f}%')
plt.axvline(0, color='green', linestyle='-', linewidth=1, alpha=0.5)
plt.title('Monte Carlo Simulation - Portfolio Returns Distribution', fontsize=16)
plt.xlabel('Portfolio Return (%)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Compare optimal portfolio with individual stocks and equal weight
equal_weights = np.array([1/n_assets] * n_assets)

# Calculate performance metrics for different portfolios
portfolios = {
    'Optimal Portfolio': optimal_weights,
    'Equal Weight': equal_weights
}

# Add individual stocks
for i, stock in enumerate(saudi_stocks):
    weights = np.zeros(n_assets)
    weights[i] = 1
    portfolios[stock] = weights

# Calculate metrics for each portfolio
portfolio_metrics = {}
for name, weights in portfolios.items():
    port_return, port_volatility = portfolio_performance(weights, returns, cov_matrix)
    sharpe = (port_return - 0.02) / port_volatility
    portfolio_metrics[name] = {
        'Return': port_return,
        'Volatility': port_volatility,
        'Sharpe': sharpe
    }

# Create comparison dataframe
comparison_df = pd.DataFrame(portfolio_metrics).T
comparison_df = comparison_df.sort_values('Sharpe', ascending=False)

print("\n" + "="*50)
print("PORTFOLIO PERFORMANCE COMPARISON")
print("="*50)
print(comparison_df)

# Plot comparison
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

metrics_to_plot = ['Return', 'Volatility', 'Sharpe']
colors = ['green', 'red', 'blue']

for idx, (ax, metric, color) in enumerate(zip(axes, metrics_to_plot, colors)):
    ax.bar(comparison_df.index, comparison_df[metric], color=color, alpha=0.7, edgecolor='black')
    ax.set_title(f'Portfolio {metric}', fontsize=14)
    ax.set_xticklabels(comparison_df.index, rotation=45, ha='right')
    ax.grid(True, alpha=0.3)
    
    # Add value labels
    for i, v in enumerate(comparison_df[metric]):
        ax.text(i, v + 0.01 * max(comparison_df[metric]), 
                f'{v:.3f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# Save all results to Excel
with pd.ExcelWriter('saudi_portfolio_analysis.xlsx') as writer:
    # Save prices and returns
    prices.to_excel(writer, sheet_name='Prices')
    returns.to_excel(writer, sheet_name='Returns')
    
    # Save metrics
    metrics_df.to_excel(writer, sheet_name='Stock_Metrics')
    
    # Save correlation matrix
    correlation_matrix.to_excel(writer, sheet_name='Correlation')
    
    # Save optimal portfolio
    optimal_portfolio_df = pd.DataFrame({
        'Stock': saudi_stocks,
        'Weight': optimal_weights,
        'Weight %': optimal_weights * 100
    })
    optimal_portfolio_df.to_excel(writer, sheet_name='Optimal_Portfolio', index=False)
    
    # Save comparison
    comparison_df.to_excel(writer, sheet_name='Portfolio_Comparison')

print("\nAnalysis complete! Results saved to 'saudi_portfolio_analysis.xlsx'")


def generate_summary_report():
    """Generate a comprehensive summary report"""
    
    print("="*60)
    print("SAUDI STOCKS PORTFOLIO ANALYSIS - SUMMARY REPORT")
    print("="*60)
    
    print("\n1. STOCK PERFORMANCE RANKING (by Sharpe Ratio):")
    print("-"*50)
    ranked_stocks = metrics_df.sort_values('Sharpe Ratio', ascending=False)
    for i, (stock, row) in enumerate(ranked_stocks.iterrows(), 1):
        print(f"{i}. {stock}: Return={row['Annual Return']*100:.1f}%, "
              f"Risk={row['Annual Volatility']*100:.1f}%, "
              f"Sharpe={row['Sharpe Ratio']:.2f}")
    
    print("\n2. PORTFOLIO OPTIMIZATION RESULTS:")
    print("-"*50)
    print(f"Optimal Sharpe Ratio: {optimal_sharpe:.3f}")
    print(f"Expected Annual Return: {optimal_return*100:.2f}%")
    print(f"Expected Annual Volatility: {optimal_volatility*100:.2f}%")
    
    print("\n3. RISK ASSESSMENT:")
    print("-"*50)
    print(f"95% Value at Risk (VaR): {var_95*100:.2f}%")
    print(f"95% Expected Shortfall (CVaR): {cvar_95*100:.2f}%")
    
    print("\n4. DIVERSIFICATION BENEFITS:")
    print("-"*50)
    avg_correlation = correlation_matrix.values[np.triu_indices_from(correlation_matrix.values, k=1)].mean()
    print(f"Average Correlation between stocks: {avg_correlation:.3f}")
    print("(Lower correlation indicates better diversification potential)")
    
    print("\n5. RECOMMENDATIONS:")
    print("-"*50)
    if optimal_sharpe > 1.0:
        print("✓ Portfolio has good risk-adjusted returns")
    else:
        print("⚠ Consider reviewing portfolio allocation")
    
    if optimal_volatility < 0.25:
        print("✓ Portfolio volatility is reasonable")
    else:
        print("⚠ Portfolio may be too volatile for conservative investors")
    
    if avg_correlation < 0.5:
        print("✓ Good diversification potential")
    else:
        print("⚠ High correlation suggests limited diversification benefits")

# Generate report
generate_summary_report()



n_simulations = 10000
days = 252  # number of trading days in a year (for reference if using daily returns)
years = 1   # simulate 1 year ahead

# Annualized mean returns and covariance matrix
annual_mean_returns = returns.mean() * 252  # annualized mean
annual_cov_matrix = returns.cov() * 252     # annualized covariance

# Convert to NumPy arrays
mean_returns = annual_mean_returns.values    # 1D array
cov_matrix = annual_cov_matrix.values        # 2D array

simulated_portfolio_returns = []

for _ in range(n_simulations):
    # Generate correlated returns for 1 year
    random_returns = np.random.multivariate_normal(mean_returns, cov_matrix, years)
    # Portfolio return (dot product with weights)
    portfolio_return = np.dot(random_returns, optimal_weights)
    # Since we simulate 1 year, cumulative return is just the portfolio return
    simulated_portfolio_returns.append(portfolio_return.sum())

simulated_portfolio_returns = np.array(simulated_portfolio_returns)

# -------------------------
# Risk Metrics
# -------------------------
confidence_level = 0.95
var_95 = np.percentile(simulated_portfolio_returns, (1 - confidence_level) * 100)
cvar_95 = simulated_portfolio_returns[simulated_portfolio_returns <= var_95].mean()

print("\nMonte Carlo Simulation - 1 Year Ahead (Annual Returns)")
print("="*50)
print(f"Mean simulated return: {simulated_portfolio_returns.mean()*100:.2f}%")
print(f"Standard deviation: {simulated_portfolio_returns.std()*100:.2f}%")
print(f"95% Value at Risk (VaR): {var_95*100:.2f}%")
print(f"95% Conditional VaR (Expected Shortfall): {cvar_95*100:.2f}%")
print(f"Max simulated return: {simulated_portfolio_returns.max()*100:.2f}%")
print(f"Min simulated return: {simulated_portfolio_returns.min()*100:.2f}%")

# -------------------------
# Plot Distribution
# -------------------------
plt.figure(figsize=(12,6))
plt.hist(simulated_portfolio_returns*100, bins=50, edgecolor='black', alpha=0.7)
plt.axvline(var_95*100, color='red', linestyle='--', linewidth=2, label=f'95% VaR: {var_95*100:.2f}%')
plt.axvline(cvar_95*100, color='darkred', linestyle='--', linewidth=2, label=f'95% CVaR: {cvar_95*100:.2f}%')
plt.axvline(0, color='green', linestyle='-', linewidth=1, alpha=0.5)
plt.title('Monte Carlo Simulation - 1 Year Portfolio Return Distribution', fontsize=16)
plt.xlabel('Cumulative Return (%)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
