# src/private_equity.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

class PEAnalyzer:
    def __init__(self, fund_data):
        """
        fund_data: DataFrame with columns ['Fund', 'Vintage', 'Commitment', 'Return', ...]
        """
        self.fund_data = fund_data

    def pme(self, public_returns):
        """
        Calculates Public Market Equivalent (PME).
        public_returns: Series of public market index returns.
        """
        pe_cashflows = self.fund_data['Return']
        public_cf = public_returns.loc[self.fund_data['Vintage']]
        return pe_cashflows.sum() / public_cf.sum()

    def select_funds_ml(self):
        """
        Uses Random Forest to predict fund performance.
        """
        features = self.fund_data.drop(['Fund', 'Return'], axis=1)
        target = self.fund_data['Return']
        model = RandomForestRegressor(n_estimators=100)
        model.fit(features, target)
        self.fund_data['Predicted'] = model.predict(features)
        return self.fund_data.sort_values(by='Predicted', ascending=False)

    def add_deal(self, deal):
        """
        Adds a new deal to the fund database.
        deal: dict with keys matching fund_data columns.
        """
        self.fund_data = self.fund_data.append(deal, ignore_index=True)

