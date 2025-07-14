# src/portfolio.py

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

class Portfolio:
    def __init__(self, holdings):
        """
        holdings: dict, e.g. {'AAPL': 100, 'MSFT': 50}
        """
        self.holdings = holdings
        self.data = None

    def fetch_data(self, start, end):
        """
        Fetches historical price data for all tickers in holdings.
        """
        print("Fetching price data...")
        tickers = list(self.holdings.keys())
        self.data = yf.download(tickers, start=start, end=end)['Adj Close']
        print("Data fetched.")

    def calculate_returns(self):
        """
        Calculates daily returns for each asset.
        """
        if self.data is None:
            raise ValueError("No data. Run fetch_data() first.")
        return self.data.pct_change().dropna()

    def portfolio_value(self):
        """
        Calculates the portfolio value over time.
        """
        prices = self.data
        shares = pd.Series(self.holdings)
        return prices.multiply(shares, axis=1).sum(axis=1)

    def plot_allocation(self):
        """
        Plots the asset allocation.
        """
        values = {ticker: self.data[ticker].iloc[-1] * qty for ticker, qty in self.holdings.items()}
        plt.figure(figsize=(6,6))
        plt.pie(values.values(), labels=values.keys(), autopct='%1.1f%%')
        plt.title('Portfolio Allocation')
        plt.show()

    def performance_metrics(self):
        """
        Calculates CAGR, Sharpe ratio, max drawdown, volatility.
        """
        returns = self.calculate_returns()
        portfolio_returns = (returns * pd.Series(self.holdings)).sum(axis=1)
        cagr = ((self.portfolio_value().iloc[-1] / self.portfolio_value().iloc[0]) ** (252/len(self.portfolio_value())) - 1)
        sharpe = (portfolio_returns.mean() / portfolio_returns.std()) * np.sqrt(252)
        max_drawdown = self.max_drawdown(self.portfolio_value())
        volatility = portfolio_returns.std() * np.sqrt(252)
        return {
            'CAGR': cagr,
            'Sharpe Ratio': sharpe,
            'Max Drawdown': max_drawdown,
            'Volatility': volatility
        }

    @staticmethod
    def max_drawdown(series):
        """
        Calculates the maximum drawdown of a time series.
        """
        roll_max = series.cummax()
        drawdown = (series - roll_max) / roll_max
        return drawdown.min()

