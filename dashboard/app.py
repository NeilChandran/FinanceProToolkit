# dashboard/app.py

import streamlit as st
import pandas as pd
from src.portfolio import Portfolio
from src.wealth_management import NetWorthTracker, GoalPlanner

st.title("FinanceProToolkit Dashboard")

st.sidebar.header("Portfolio Inputs")
tickers = st.sidebar.text_input("Tickers (comma-separated)", "AAPL,MSFT,GOOGL").split(",")
quantities = [int(x) for x in st.sidebar.text_input("Quantities (comma-separated)", "10,5,8").split(",")]
holdings = dict(zip([t.strip().upper() for t in tickers], quantities))

portfolio = Portfolio(holdings)
if st.sidebar.button("Fetch Data"):
    portfolio.fetch_data("2022-01-01", "2023-01-01")
    st.line_chart(portfolio.portfolio_value())
    st.write(portfolio.performance_metrics())

st.sidebar.header("Net Worth Tracker")
assets = st.sidebar.text_input("Assets (Stocks:100000,Bonds:50000)", "Stocks:100000,Bonds:50000")
assets_dict = {k: float(v) for k, v in [x.split(":") for x in assets.split(",")]}
tracker = NetWorthTracker(assets_dict)
st.write("Total Net Worth: $", tracker.total_net_worth())

st.sidebar.header("Goal Planner")
goal = st.sidebar.number_input("Goal Amount", value=1000000)
years = st.sidebar.number_input("Years", value=10)
planner = GoalPlanner(tracker.total_net_worth(), goal, years)
st.write("Future Value: $", planner.simulate())
st.write("Goal Achievable:", planner.is_goal_achievable())
