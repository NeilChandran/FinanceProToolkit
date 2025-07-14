# src/wealth_management.py

import pandas as pd
import numpy as np

class NetWorthTracker:
    def __init__(self, assets):
        """
        assets: dict, e.g. {'Stocks': 100000, 'Bonds': 50000, 'Real Estate': 200000}
        """
        self.assets = assets

    def total_net_worth(self):
        return sum(self.assets.values())

    def add_asset(self, asset, value):
        self.assets[asset] = self.assets.get(asset, 0) + value

    def remove_asset(self, asset, value):
        if asset in self.assets:
            self.assets[asset] -= value
            if self.assets[asset] <= 0:
                del self.assets[asset]

class GoalPlanner:
    def __init__(self, net_worth, goal, years, expected_return=0.05):
        self.net_worth = net_worth
        self.goal = goal
        self.years = years
        self.expected_return = expected_return

    def simulate(self):
        """
        Simulates future net worth based on expected return.
        """
        future_value = self.net_worth * ((1 + self.expected_return) ** self.years)
        return future_value

    def is_goal_achievable(self):
        return self.simulate() >= self.goal

class TaxOptimizer:
    def __init__(self, investments, tax_rates):
        """
        investments: dict, e.g. {'Stocks': 100000, 'Bonds': 50000}
        tax_rates: dict, e.g. {'Stocks': 0.15, 'Bonds': 0.25}
        """
        self.investments = investments
        self.tax_rates = tax_rates

    def after_tax_returns(self, returns):
        """
        returns: dict, e.g. {'Stocks': 0.08, 'Bonds': 0.04}
        """
        after_tax = {}
        for asset, ret in returns.items():
            after_tax[asset] = ret * (1 - self.tax_rates.get(asset, 0))
        return after_tax

