"""
workflow:
pull from DB opening prices from year beggining.
pull from DB closing prices from previous_day.
count returns
populate DB with returns
all in StockData
"""

from datetime import date, datetime, timedelta

from stock_market.db_hub.models import StockData


def returns_counter_in_pct(previous_date_price: float, after_date_price: float):

    return ((after_date_price - previous_date_price) / previous_date_price) * 100


def get_yesterdays_data(session, previous_day):
    return (
        session.query(StockData.ticker, StockData.close)
        .filter(StockData.date == previous_day)
        .all()
    )
