# Quantitative_Trading_Assignment
This repository will contains my submission for the ProSpace Quantitative Trading assignment, 2024.
<br>
Along with the code, I have attached a project report as well which contains my results, conclusions as well as details my rationale behind every line of code.
The repo also contains the csv files of trade reports generated while finding the optimum threshold values.
<br>
<br>
## Flow of code:
The strategy_class.py file is the backbone of the project and contains the strategy_test class used in other files. This is imported in the remaining two files and thereafter treated like a blackbox. <br>
The finding_optimum.py file iterates through possible values of liquidate and build thresholds, maximizing PnL and finding the optimum threshold values. <br>
The trade_result.py file generates the PnL, max drawdown, win% and other metrics for the finallly obtained optimum values.

