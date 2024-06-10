import pandas as pd
import numpy as np
import plotly.express as px

class strategy_test(object):
    def __init__ (self, df):
        self.df = df

    def append_posn(self, liq, build):
        if (liq < 0): liq *= -1 # ensuring positive thresholds entered
        if (build < 0): build *= -1
        if (liq > build): # ensuring thresholds are set in order
            copy = build
            build = liq
            liq = copy

        self.df['position'] = np.nan
        self.df.at[0, 'position'] = 0 # first position always 0 

        for i in range(1, len(self.df.index)):
            curr_alpha = self.df.at[i, 'alpha']
            # setting zone flags, exact description in report
            if (liq != build):
                z1 = 1 if curr_alpha <= (-1*build) else 0
                z5 = 1 if curr_alpha >= build else 0
            else:
                z1 = 1 if curr_alpha < (-1*build) else 0
                z5 = 1 if curr_alpha > build else 0
            z2 = 1 if ((-1*build) < curr_alpha and curr_alpha < (-1*liq)) else 0
            z3 = 1 if ((-1*liq) <= curr_alpha and curr_alpha <= liq) else 0
            z4 = 1 if (liq < curr_alpha and curr_alpha < build) else 0

            prev_posn = self.df.at[i-1, 'position']
            # setting condition flags, exact description in report
            c0 = 1 if prev_posn == 0 else 0
            c1 = 1 if prev_posn == 1 else 0
            c2 = 1 if prev_posn == -1 else 0
            
            # condesnsed boolean logic expression for current position
            self.df.at[i, 'position'] = 1 if (z5 or (z4 and c1)) else  0 if (z3 or (z4 and (c0 or c2)) or (z2 and (c0 or c1))) else -1 if (z1 or (z2 and c2)) else np.nan

        return 0
    
    def backtest(self):\
        # raise error if position not appended
        if 'position' not in self.df.columns:
            raise Exception("Run append_posn method first!")
        
        #computing array storing delta in price
        delta_arr = []
        delta_arr.append(0)
        for i in range(1, len(self.df.index)):
            delta_arr.append(self.df.at[i, 'price'] - self.df.at[i-1, 'price'])

        # adding a column storing portfolio value at the end of each instant
        self.df['pfolio_val'] = np.nan
        self.df.at[0, 'pfolio_val'] = 0
        per_trade_ret = [] # array storing return of each trade made; trade marked when position liquidated
        entry_val = np.nan # store nan value, helps in debugging; incorrect entry_val calculation will return nan for return_val

        for i in range(1, len(self.df.index)):
            curr_posn = self.df.at[i, 'position']
            last_posn = self.df.at[i-1, 'position']
            abs_posn_delta = abs(curr_posn - last_posn)

            # logic for below calculations explained in report
            self.df.at[i, 'pfolio_val'] = self.df.at[i-1, 'pfolio_val'] +  (last_posn * delta_arr[i]) 
            curr_pfval = self.df.at[i, 'pfolio_val']
            
            if (abs_posn_delta * abs(last_posn)):
                per_trade_ret.append(curr_pfval - entry_val)
                entry_val = np.nan

            if (abs_posn_delta * abs(curr_posn)):
                entry_val = curr_pfval

        return per_trade_ret
    
    def max_drawdown(self, arr): # O(n) solution for calculating maximum drawdown
        max_dd = 0
        curr_max_element = 0
        curr_dd = 0
        for i in range(len(arr)):
            curr_val = arr[i]
            if (curr_val > curr_max_element):
                curr_max_element = curr_val
            if ((curr_val - curr_max_element) < curr_dd):
                curr_dd = curr_val - curr_max_element
            if (curr_dd < max_dd):
                max_dd = curr_dd
        return (-1 * max_dd)
    
    def evaluate_metrics(self, per_trade_ret):
        # raise error if backtest not run
        if 'pfolio_val' not in self.df.columns:
            raise Exception("Run backtest method first!")
        
        max_dd = self.max_drawdown(np.array(self.df['pfolio_val']))
        PnL = self.df.at[len(self.df.index)-1, 'pfolio_val']
        total_trades = len(per_trade_ret)
        if (total_trades != 0):
            avg_ret_per_trade = np.sum(np.array(per_trade_ret)) / total_trades
        else: avg_ret_per_trade = 0

        win_cnt, loss_cnt, win_sum, loss_sum = 0, 0, 0, 0
        for i in range(len(per_trade_ret)):
            if (per_trade_ret[i] > 0):
                win_cnt += 1
                win_sum += per_trade_ret[i]
            else:
                loss_cnt += 1
                loss_sum += per_trade_ret[i]
        
        if (total_trades != 0):
            win_perc = (win_cnt / total_trades) * 100
        else: win_perc = 0
        if (win_cnt != 0):
            avg_profit_per_win_trade = win_sum / win_cnt
        else: avg_profit_per_win_trade = 0
        if (loss_cnt != 0):
            avg_loss_per_loss_trade = loss_sum / loss_cnt
        else: avg_loss_per_loss_trade = 0

        return [PnL, max_dd, total_trades, win_perc, avg_ret_per_trade, avg_profit_per_win_trade, avg_loss_per_loss_trade]
    
    def equity_curve(self):
        # raise error if backtest not run
        if 'pfolio_val' not in self.df.columns:
            raise Exception("Run backtest method first!")
        # generate line graph using plotly (interactive graph returned)
        fig = px.line(self.df, x=self.df.index, y='pfolio_val', title='Portfolio Value Over Time')
        fig.show()
        return 0
        







        



    



                   

            

        

        

        