import yfinance as yf
import numpy as np
import pandas as pd
import scipy.stats as stats
import warnings
import methods 
import plots
warnings.filterwarnings("ignore", message=".*inplace keyword.*")

date='2010-01-01'
benchmark = yf.download('SPY', progress=False, start=date)['Close'].squeeze()
bench_returns = np.log(benchmark / benchmark.shift(1)).iloc[1:]

portfolio=pd.read_csv('portfolio.csv', index_col='ticker')
weights = portfolio['weight']
stocks = portfolio.index.tolist()

if not np.isclose(weights.sum(), 1):
    raise ValueError("The sum of the weights must be equal to 1.")

prices = yf.download(stocks, progress=False, start=date)['Close']
returns = np.log(prices / prices.shift(1)).iloc[1:]

for ticker in returns.columns:
    if returns[ticker].isna().any():
        vol_ratio=returns[ticker].std()/bench_returns.std()
        returns[ticker]=returns[ticker].fillna(bench_returns*vol_ratio)

portfolio_returns = returns @ weights[returns.columns]

conf=float(input("Enter confidence level in decimal form: "))

h_var = methods.historical_var(portfolio_returns, conf)
p_var = methods.parametric_var(portfolio_returns, conf)
mc_var = methods.monte_carlo_var(returns, weights, conf, 100000)
c_var = methods.conditional_var(portfolio_returns, conf)
print(f"Historical VaR {conf*100}%: {h_var:.2%}")
print(f"Parametric VaR {conf*100}%: {p_var:.2%}")
print(f"Monte Carlo VaR {conf*100}%: {mc_var:.2%}")
print(f"Conditional VaR {conf*100}%: {c_var:.2%}")

h_exceed, h_pct = methods.backtest_var(portfolio_returns, h_var)
p_exceed, p_pct = methods.backtest_var(portfolio_returns, p_var)
mc_exceed, mc_pct = methods.backtest_var(portfolio_returns, mc_var)
print(f"\nBacktest (expected exceedances: {1-conf:.2%}):")
print(f"Historical exceedances: {h_exceed} days ({h_pct:.2%})")
print(f"Parametric exceedances: {p_exceed} days ({p_pct:.2%})")
print(f"Monte Carlo exceedances: {mc_exceed} days ({mc_pct:.2%})")

plots.plot_var(portfolio_returns, h_var, p_var, mc_var, c_var, conf)

  

