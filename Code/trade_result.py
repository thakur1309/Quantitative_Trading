import pandas as pd
from strategy_class import strategy_test

data = pd.read_csv(r"C:\Users\thaku\OneDrive\Desktop\College\ProSpace Assignment\asset_1.csv")

liq, build = 0.15, 0.5151
strat = strategy_test(data)
strat.append_posn(liq, build)
per_trade_ret =  strat.backtest()
strat.equity_curve()
metrics = strat.evaluate_metrics(per_trade_ret)

print(f"Liquidate Threshold = {liq}; Build Threshold = {build}")
print(f"Optimised PnL = {metrics[0]:.2f}")
print(f"Total number of trades executed = {metrics[2]}; Win percentage = {metrics[3]:.2f}%")
print(f"Maximum Drawdown (absolute) = {metrics[1]:.2f}")
print(f"Average Return per Trade = {metrics[4]:.2f}")
print(f"Average Return per profitable trade = {metrics[5]:.2f}")
print(f"Average Return per loss-making trade = {metrics[6]:.2f}")