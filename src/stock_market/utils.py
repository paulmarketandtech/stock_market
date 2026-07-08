import logging
import os
from datetime import date, timedelta
from typing import Dict

from stock_market.db_hub.models import (
    AllTickersMonthlyUpdate,
    ListOfCommodities,
    ListOfETFs,
    ListOfIndexes,
)

YTD_DATE = date(2026, 1, 2)
LAST_CORRECTION_DATE = date(2025, 4, 7)

logging.basicConfig(
    filename=os.getenv("LOG_FILE"),
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


"""
For now it will stay 2B and 5B 
but in the future 2B will probably be gone and 5B will be dynamic
"""


def get_previous_day() -> date:
    return date.today() - timedelta(days=1)


def get_large_cap_tickers(session, min_market_cap: int = 2_000_000_000) -> list[str]:
    list_of_commodities = [t.ticker for t in session.query(ListOfCommodities).all()]
    list_of_indexes = [t.ticker for t in session.query(ListOfIndexes).all()]
    list_of_etfs = [t.ticker for t in session.query(ListOfETFs).all()]
    list_of_tickers = [
        t.ticker
        for t in session.query(AllTickersMonthlyUpdate)
        .filter(AllTickersMonthlyUpdate.market_cap > min_market_cap)
        .all()
    ]

    list_of_tickers.extend(list_of_indexes)
    list_of_tickers.extend(list_of_commodities)
    list_of_tickers.extend(list_of_etfs)

    return list_of_tickers


def creating_list_of_tickers_nasdaq(session) -> list[str]:
    nasdaq_list_of_tickers = [
        t.ticker
        for t in session.query(AllTickersMonthlyUpdate)
        .filter(AllTickersMonthlyUpdate.nasdaq_tickers == True)
        .all()
    ]
    return nasdaq_list_of_tickers


def creating_list_of_tickers_nyse(session) -> list[str]:
    nyse_list_of_tickers = [
        t.ticker
        for t in session.query(AllTickersMonthlyUpdate)
        .filter(AllTickersMonthlyUpdate.nyse_tickers == True)
        .all()
    ]
    return nyse_list_of_tickers


"""
helper functions

def populate_table(session, tickers):
    print(f"len of tickers list: {tickers}")

    for ticker in tickers:
        stock_price = ListOfETFs(ticker=ticker)
        session.add(stock_price)

    session.commit()
    print("DB Populated")
    stock_data = session.query(ListOfETFs.ticker).all()

list_of_tickers_nasdaq = creating_list_of_tickers_nasdaq()
list_of_tickers_nyse = creating_list_of_tickers_nyse()
"""
