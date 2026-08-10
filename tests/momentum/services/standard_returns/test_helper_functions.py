from datetime import date

from stock_market.db_hub.models import StockData
from stock_market.momentum.services.standard_returns.helper_functions import (
    get_yesterdays_data,
    returns_counter_in_pct,
)


def test_pct_returns_counter():
    previous_date_price = 100
    after_date_price = 123

    pct_change = returns_counter_in_pct(previous_date_price, after_date_price)

    assert pct_change == 23


def test_negative_pct_returns():
    assert returns_counter_in_pct(100, 81) == -19


def test_get_yesterdays_data(db_session):
    today_date = date(2026, 8, 10)
    yesterday_date = date(2026, 8, 9)

    db_session.add_all(
        [
            StockData(
                ticker="AAPL",
                date=yesterday_date,
                close=150,
                high=111,
                low=111,
                open=111,
                ma50=140,
                ma100=145,
                ma200=160,
            ),
            StockData(
                ticker="AAPL",
                date=today_date,
                close=100,
                high=111,
                low=111,
                open=111,
                ma50=None,
                ma100=90,
                ma200=80,
            ),
        ]
    )
    assert isinstance(get_yesterdays_data(db_session, yesterday_date), list)
