"""
workflow:
YTD returns
last correction returns. remove previous correction. count also over here weekly change returns
market breadth:
- trading view, download indicators and populate DB.
  based on that check if close price above or below SMAs - booleans.
  count above/below SMAs for nasdaq and nyse.
  create chart screens

weekly change is calculated everyday.
it should be counted everyday, but only displayed on Sat? have to think this through
"""

from typing import List, Tuple

from stock_market.db_hub.models import StockData
from stock_market.momentum.services.standard_returns.fridays_returns import (
    count_returns_from_fridays_to_date,
    get_previous_friday,
)
from stock_market.momentum.services.standard_returns.helper_functions import (
    get_yesterdays_data,
)
from stock_market.momentum.services.standard_returns.last_correction_and_ytd_returns import (
    count_returns_from_given_date_to_date,
)


def count_daily_routine_returns(
    session, previous_day: str, ytd_date: str, correction_date: str
):

    yesterday_data = get_yesterdays_data(session, previous_day)
    previous_friday = get_previous_friday(session)
    current_week_returns = count_returns_from_fridays_to_date(
        session, previous_day, yesterday_data, previous_friday
    )
    print("-" * 40)
    print(current_week_returns)
    """
    ytd_returns = count_returns_from_given_date_to_date(
        session, previous_day, yesterday_data, ytd_date, "ytd"
    )
    correction_returns = count_returns_from_given_date_to_date(
        session, previous_day, yesterday_data, correction_date, "last_correction"
    )
    from datetime import datetime

    #TODO: probably wont be used - to be deleted
    today = datetime.today().strftime("%A")
    if today.lower() == "saturday":
        four_weeks_ago_friday = get_four_weeks_ago_friday_close(session)
        four_weeks_returns = count_returns_from_fridays_to_date(
            session, previous_day, yesterday_data, four_weeks_ago_friday
        )
    """
