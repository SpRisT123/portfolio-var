import matplotlib.pyplot as plot
import matplotlib.ticker as mtick

def plot_var(portfolio_returns, h_var, p_var, mc_var, c_var, conf):
    fig = plot.figure(num='Portfolio Returns and VaR', figsize=(9, 6))
    plot.style.use('bmh')
    plot.hist(portfolio_returns, bins=100, color='#660033', label='Portfolio Returns')
    plot.axvline(x=-h_var, color='#fcba03', linestyle='--', label=f'Historical VaR {conf*100}%: {h_var:.2%}')
    plot.axvline(x=-p_var, color='#d66d22', linestyle='--', label=f'Parametric VaR {conf*100}%: {p_var:.2%}')
    plot.axvline(x=-mc_var, color='#175a8a', linestyle='--', label=f'Monte Carlo VaR {conf*100}%: {mc_var:.2%}')
    plot.axvline(x=-c_var, color='#2c912c', linestyle='--', label=f'Conditional VaR {conf*100}%: {c_var:.2%}')
    plot.xlabel('Daily Returns', fontsize=14)
    plot.ylabel('Days', fontsize=14)
    plot.legend()
    plot.gca().xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    plot.title(f"Portfolio Returns and VaR at {conf:.0%} Confidence Level", fontsize=16)
    plot.savefig(f'portfolio_var_{conf:.0%}_hist.png', dpi=150)
    plot.show()

    
