"""
workflow:
YTD returns
last correction returns. remove previous correction. count also over here weekly change returns
market breadth:
- trading view, download indicators and populate DB.
  based on that check if close price above or below SMAs - booleans.
  count above/below SMAs for nasdaq and nyse.
  create chart screens

ytd corrections: pull data from stock_market, sort it and populate desired tables
like YTD20Best, LastCorrectionBest etc.

weekly change: calculate weekly returns and then populate tables: Weekly20Best

indexes returns: works only on saturday. put the calculations in the 1 step.
weekly change is calculated everyday.
it should be counted everyday, but only displayed on Sat? have to think this through
"""

from stock_market.db_hub.models import StockData
from stock_market.momentum.services.standard_returns.ytd_returns import (
    count_ytd_returns,
)


def get_last_correction_opening_prices(session, correction_date):
    list_of_tickers = [
        t.ticker
        for t in session.query(StockData)
        .filter(StockData.date == correction_date)
        .all()
    ]
    return list_of_tickers


def get_ytd_tickers_list(session, ytd_date):
    return [
        t.ticker
        for t in session.query(StockData).filter(StockData.date == ytd_date).all()
    ]


def get_yesterday_closing_prices(session, last_date):
    list_of_tickers = (
        session.query(StockData.ticker, StockData.close)
        .filter(StockData.date == "2026-07-06")
        .all()
    )
    return list_of_tickers


def get_four_weeks_ago_friday_close():
    pass


def count_daily_routine_returns(session, previous_day, ytd_date, correction_date):

    # yesterdays_closing_prices = get_yesterday_closing_prices(session, previous_day)
    ytd_tickers_list = get_ytd_tickers_list(session, ytd_date)
    count_ytd_returns(session, previous_day, ytd_date, ytd_tickers_list[:20])


from datetime import datetime

today = datetime.today().strftime("%A")
if today.lower() == "saturday":
    get_four_weeks_ago_friday_close()
