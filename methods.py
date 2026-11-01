import numpy as np
import scipy.stats as stats


def historical_var(portfolio_returns, confidence_level):
    hist_var = -np.percentile(portfolio_returns, (1 - confidence_level) * 100)
    return hist_var

def parametric_var(portfolio_returns, confidence_level):
    sigma=np.std(portfolio_returns)
    z_score=stats.norm.ppf(1-confidence_level)
    param_var=-z_score*sigma
    return param_var

def monte_carlo_var(returns, weights, confidence_level, num_sim):
    tick_mean = returns.mean()
    tick_cov = returns.cov()
    simulated_returns = np.random.multivariate_normal(tick_mean, tick_cov, num_sim)
    portfolio_returns = simulated_returns @ weights[returns.columns]
    return historical_var(portfolio_returns, confidence_level)

def conditional_var(portfolio_returns, confidence_level):
    var=historical_var(portfolio_returns, confidence_level)
    cvar=-portfolio_returns[portfolio_returns <= -var].mean() 
    return cvar

def backtest_var(portfolio_returns, var):
    num_exceed=(portfolio_returns < -var).sum()
    num_exceed_precent=num_exceed/len(portfolio_returns)
    return num_exceed, num_exceed_precent