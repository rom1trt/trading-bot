#!/usr/bin/env python
# coding: utf-8

# Analyzing financial instruments
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
plt.style.use('seaborn')


class FinancialInstrument():
    ''' Class to analyze any kind of financial instruments
    '''
    def __init__(self, ticker, start, end):
        self._ticker = ticker # _ticker => protected attribute though we can call it with _ticker instead of ticker
        self.start = start
        self.end = end
        self.get_data()
        self.log_returns()
    
    def set_ticker(self, ticker = None):
        if ticker is not None:
            self._ticker = ticker
            self.get_data()
            self.log_returns()
        
    def __repr__(self):
        return 'FinancialInstrument(ticker = {}, start = {}, end = {})'.format(self._ticker, self.start, self.end)
        
    def get_data(self):
        ''' Retrieves and prepares data from Yahoo Finance
        '''
        raw_data = yf.download(self._ticker, self.start, self.end).Close.to_frame()
        raw_data.rename(columns = {'Close': 'Price'}, inplace = True)
        # Make it an attriute
        self.data = raw_data
        
    def log_returns(self):
        ''' Computes logarithmic returns
        '''
        self.data['Log_returns'] = np.log(self.data.Price / self.data.Price.shift(1)) # or use pct_change
        
    def plot_prices(self): 
        ''' Creates a price chart
        '''
        self.data.plot(figsize = (12, 8))
        plt.title('Price chart: {}'.format(self._ticker), fontsize = 15)
        
    def plot_returns(self, kind = 'ts'): # Either you plot the time series or the histogram
        ''' Schemes logarithmic returns either as time series ("ts") or histograms ("hist")
        '''
        if kind == 'ts':
            self.data.Log_returns.plot(figsize = (12, 8))
            plt.title('Returns: {}'.format(self._ticker), fontsize = 15)
        elif kind == 'hist':
            self.data.Log_returns.hist(figsize = (12, 8), bins = int(np.sqrt(len(self.data))))
            plt.title('Frequency of returns: {}'.format(self._ticker), fontsize = 15)


class RiskReturn(FinancialInstrument):
    
    def __init__(self, ticker, start, end, freq = None):
        super().__init__(ticker, start, end)
        self.freq = freq
    
    def __repr__(self):
        return 'RiskReturn(ticker = {}, start = {}, end = {})'.format(self._ticker, self.start, self.end)
    
    def mean_return(self): 
        ''' Computes the mean of returns on a given frequency ("freq")
        '''
        if self.freq is None:
            return self.data.Log_returns.mean()
        else:
            resampled_price = self.data.Price.resample(self.freq).last() # Resample the prices according to the frequence
            resampled_returns = np.log(resampled_price / resampled_price.shift(1)) # Resample/Re-compute returns with the resampled prices
            return resampled_returns.mean()
        
    def std_return(self): 
        ''' Computes the standard deviation of returns according to a given frequency ("freq")
        '''
        if self.freq is None:
            return self.data.Log_returns.std()
        else:
            resampled_price = self.data.Price.resample(self.freq).last() # Resample the prices according to the frequence
            resampled_returns = np.log(resampled_price / resampled_price.shift(1)) # Resample/Re-compute returns with the resampled prices
            return resampled_returns.std()
    
    def annualized_perf(self):
        ''' Computes the annualized return and risk
        '''
        mean_return = round(self.data.Log_returns.mean() * 252, 3)
        risk = round(self.data.Log_returns.std() * np.sqrt(252), 3)
        print(f'Return: {mean_return} | Risk: {risk}')

