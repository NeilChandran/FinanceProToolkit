# src/quant.py

import pandas as pd
import numpy as np

class AlgoTrading:
    def __init__(self, price_data):
        self.price_data = price_data

    def pairs_trading(self, ticker1, ticker2, lookback=30):
        spread = self.price_data[ticker1] - self.price_data[ticker2]
        spread_mean = spread.rolling(lookback).mean()
        spread_std = spread.rolling(lookback).std()
        zscore = (spread - spread_mean) / spread_std
        signals = pd.Series(0, index=spread.index)
        signals[zscore > 1] = -1  # Short spread
        signals[zscore < -1] = 1  # Long spread
        return signals

    def momentum_strategy(self, ticker, window=20):
        returns = self.price_data[ticker].pct_change()
        momentum = returns.rolling(window).mean()
        signals = pd.Series(0, index=returns.index)
        signals[momentum > 0] = 1
        signals[momentum < 0] = -1
        return signals

    def mean_reversion(self, ticker, window=20):
        price = self.price_data[ticker]
        mean = price.rolling(window).mean()
        std = price.rolling(window).std()
        zscore = (price - mean) / std
        signals = pd.Series(0, index=price.index)
        signals[zscore > 1] = -1
        signals[zscore < -1] = 1
        return signals

class RiskManagement:
    def __init__(self, returns):
        self.returns = returns

    def var(self, alpha=0.05):
        return np.percentile(self.returns, 100 * alpha)

    def cvar(self, alpha=0.05):
        var = self.var(alpha)
        return self.returns[self.returns <= var].mean()

    def stress_test(self, shock):
        return self.returns + shock

    def scenario_analysis(self, scenarios):
        results = {}
        for name, shock in scenarios.items():
            results[name] = self.stress_test(shock)
        return results

class FactorAnalysis:
    def __init__(self, returns, factors):
        self.returns = returns
        self.factors = factors

    def run_regression(self):
        import statsmodels.api as sm
        X = sm.add_constant(self.factors)
        model = sm.OLS(self.returns, X).fit()
        return model.summary()
