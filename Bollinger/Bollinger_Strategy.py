import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
plt.style.use("seaborn")

class Bollinger():
    ''' Class for the vectorized backtesting of Bollinger Bands-based trading strategies.
    '''
    
    def __init__(self, filename, ticker, SMA, gap, start, end, trading_cost):
        '''
        Parameters
        ----------
        ticker: str
            ticker ticker (instrument) to be backtested
        SMA: int
            moving window in bars (e.g. days) for SMA
        gap: int
            distance for Lower/Upper Bands in Standard gapiation units
        start: str
            start date for data import
        end: str
            end date for data import
        trading_cost: float
            proportional transaction/trading costs per trade
        '''
        self.filename = filename
        self.ticker = ticker
        self.SMA = SMA
        self.gap = gap
        self.start = start
        self.end = end
        self.trading_cost = trading_cost
        self.results = None
        self.get_data()
        self.prepare_data()
        
    def __repr__(self):
        return f"Bollinger(ticker = {self.ticker}, SMA = {self.SMA}, gap = {self.gap}, start = {self.start}, end = {self.end})"

    def get_data(self):
        ''' Imports the data from specified source 
        '''
        raw_data = pd.read_csv("intraday_pairs.csv", parse_dates = ["time"], index_col = "time")
        raw_data = raw_data[self.ticker].to_frame().dropna()
        raw_data = raw_data.loc[self.start:self.end]
        raw_data.rename(columns={self.ticker: "price"}, inplace=True)
        raw_data["returns"] = np.log(raw_data / raw_data.shift(1))
        self.data = raw_data
        
    def prepare_data(self):
        '''Prepares the data for Bollinger-based strategy backtesting .
        '''
        data = self.data.copy()
        data["SMA"] = data["price"].rolling(self.SMA).mean()
        data["Lower"] = data["SMA"] - data["price"].rolling(self.SMA).std() * self.gap
        data["Upper"] = data["SMA"] + data["price"].rolling(self.SMA).std() * self.gap
        self.data = data
        
    def set_parameters(self, SMA = None, gap = None):
        ''' Updates parameters (SMA, gap) and the prepared dataset
        '''
        if SMA is not None:
            self.SMA = SMA
            self.data["SMA"] = self.data["price"].rolling(self.SMA).mean()
            self.data["Lower"] = self.data["SMA"] - self.data["price"].rolling(self.SMA).std() * self.gap
            self.data["Upper"] = self.data["SMA"] + self.data["price"].rolling(self.SMA).std() * self.gap
            
        if gap is not None:
            self.gap = gap
            self.data["Lower"] = self.data["SMA"] - self.data["price"].rolling(self.SMA).std() * self.gap
            self.data["Upper"] = self.data["SMA"] + self.data["price"].rolling(self.SMA).std() * self.gap
            
    def test_strategy(self):
        ''' Backtests the Bollinger Bands-based trading strategy.
        '''
        data = self.data.copy().dropna()
        data["distance"] = data.price - data.SMA
        data["position"] = np.where(data.price < data.Lower, 1, np.nan)
        data["position"] = np.where(data.price > data.Upper, -1, data["position"])
        data["position"] = np.where(data.distance * data.distance.shift(1) < 0, 0, data["position"])
        data["position"] = data.position.ffill().fillna(0)
        data["strategy"] = data.position.shift(1) * data["returns"]
        data.dropna(inplace = True)
        
        # determine the number of trades in each bar
        data["trades"] = data.position.diff().fillna(0).abs()
        
        # subtract transaction/trading costs from pre-cost return
        data.strategy = data.strategy - data.trades * self.trading_cost
        
        data["creturns"] = data["returns"].cumsum().apply(np.exp)
        data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)
        self.results = data
       
        perf = data["cstrategy"].iloc[-1] # absolute performance of the strategy
        outperf = perf - data["creturns"].iloc[-1] # out-/underperformance of strategy
        
        return round(perf, 6), round(outperf, 6)
    
    def plot_results(self):
        ''' Plots the performance of the trading strategy and compares to "buy and hold".
        '''
        if self.results is None:
            print("Run test_strategy() first.")
        else:
            title = "{} | SMA = {} | gap = {} | trading_cost = {}".format(self.ticker, self.SMA, self.gap, self.trading_cost)
            self.results[["creturns", "cstrategy"]].plot(title=title, figsize=(12, 8))     
   
    def optimize_parameters(self, SMA_range, gap_range):
        ''' Finds the optimal strategy (global maximum) given the Bollinger Bands parameter ranges.

        Parameters
        ----------
        SMA_range, gap_range: tuple
            tuples of the form (start, end, step size)
        '''
        
        combinations = list(product(range(*SMA_range), range(*gap_range)))
        
        # test all combinations
        results = []
        for comb in combinations:
            self.set_parameters(comb[0], comb[1])
            results.append(self.test_strategy()[0])
        
        best_perf = np.max(results) # best performance
        opt = combinations[np.argmax(results)] # optimal parameters
        
        # run/set the optimal strategy
        self.set_parameters(opt[0], opt[1])
        self.test_strategy()
                   
        # create a df with many results
        many_results =  pd.DataFrame(data = combinations, columns = ["SMA", "gap"])
        many_results["performance"] = results
        self.results_overview = many_results
                            
        return opt, best_perf
