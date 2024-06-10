import pandas as pd
import numpy as np
from strategy_class import strategy_test

data = pd.read_csv(r'C:\Users\thaku\OneDrive\Desktop\College\ProSpace Assignment\asset_1.csv')
strategy = strategy_test(data)

results_df = pd.DataFrame(columns=['liquidate_thresh', 'build_thresh', 'PnL', 'Max_Drawdown', 
                                   'total_trades', 'win_perc', 'avg_ret_per_trade',
                                   'avg_profit_per_win_trade', 'avg_loss_per_loss_trade'])

# multiple iterations were run to narrow down the range for maximum PnL, details mentioned below
"""
Round 1:
for i in np.arange(0.1, 2, 0.01):
    for j in np.arange(i+0.1, 2, 0.01):
16440 iterations, etd runtime of 3h 20m, had to abort

Round 2:
for i in np.arange(0.1, 1, 0.05):
    for j in np.arange(i+0.25, 2, 0.05):
441 iterations, max PnL of 36093.9 achieved at liq, build = 0.15, 0.55

Round 3:
for i in np.arange(0.13, 0.17, 0.005):
    for j in np.arange(0.43, 0.57, 0.005):
252 iterations, max PnL of 36480.96 achieved at liq, build = 0.15, 0.515

Round 4:
for i in np.arange(0.149, 0.156, 0.001):
    for j in np.arange(0.514, 0.516, 0.0001):
168 iterations, max PnL of 36595.56 achieved at liq in range [0.149, 0.151] and build in range [0.5151, 0.5153]
"""

for i in np.arange(0.1489, 0.1513, 0.0001):
    for j in np.arange(0.5150, 0.5156, 0.0001): # 96 iterations, max PnL of round 4 not crossed, same range returned
        strategy.append_posn(i, j)
        strategy.backtest()
        metrics = strategy.evaluate_metrics()
        metrics.insert(0, i)
        metrics.insert(1, j)
        results_df.loc[len(results_df)] = metrics

results_df.to_csv('trade_report.csv', index=False)