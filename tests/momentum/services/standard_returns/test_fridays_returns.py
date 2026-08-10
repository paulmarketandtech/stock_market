from datetime import date, datetime, timedelta

from stock_market.db_hub.models import StockData
from stock_market.momentum.services.standard_returns.fridays_returns import (
    count_returns_from_fridays_to_date,
    get_previous_friday,
)
from stock_market.momentum.services.standard_returns.helper_functions import (
    returns_counter_in_pct,
)

previous_day = date(2026, 8, 9)
last_friday = date(2026, 8, 7)
previous_friday = date(2026, 7, 31)


def _test_get_previous_friday(db_session):

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
    assert get_previous_friday(db_session) == last_friday


def test_count_returns_from_fridays_to_date(db_session):

    last_friday = date(2026, 8, 7)
    db_session.add_all(
        [
            StockData(
                ticker="AMKR",
                date=previous_day,
                close=51.4,
                high=111,
                low=111,
                open=111,
                ma50=140,
                ma100=145,
                ma200=160,
            ),
            StockData(
                ticker="AMKR",
                date=last_friday,
                close=46.4,
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

    yesterday_data = [("AMKR", 51.4)]
    friday_data = [("AMKR", 46.4)]
    amkr_return = 10.78

    count_returns_from_fridays_to_date(
        db_session, previous_day, yesterday_data, last_friday
    )
    return_test = (
        db_session.query(StockData).filter_by(ticker="AMKR", date=previous_day).one()
    )
    assert round(return_test.weekly_change, 2) == amkr_return
