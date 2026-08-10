from datetime import date, datetime, timedelta

from stock_market.db_hub.models import StockData
from stock_market.momentum.services.standard_returns.fridays_returns import (
    count_returns_from_fridays_to_date,
    get_previous_friday,
)


def test_get_previous_friday(db_session):

    last_friday = date(2026, 8, 7)
    previous_friday = date(2026, 7, 31)

    db_session.add_all(
        [
            StockData(
                ticker="AAPL",
                date=last_friday,
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
                date=last_friday,
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

    db_session.commit()
    print("-----------------------------------")
    print(
        len(
            db_session.query(StockData.ticker)
            .filter(StockData.date == last_friday)
            .all()
        )
    )
    print("-----------------------------------")
    assert get_previous_friday(db_session) == last_friday
