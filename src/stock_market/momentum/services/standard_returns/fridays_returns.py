from datetime import date, datetime, timedelta
from typing import List, Tuple

import pandas as pd

from stock_market.db_hub.models import StockData
from stock_market.momentum.services.standard_returns.helper_functions import (
    returns_counter_in_pct,
)


def get_previous_friday(session):
    """Looks for previous friday. if previous friday was off then it takes thursday"""

    days_shift = {
        "tuesday": 4,
        "wednesday": 5,
        "thursday": 6,
        "friday": 7,
        "saturday": 8,
    }

    today = datetime.today().strftime("%A")
    last_friday = date.today() - timedelta(days=days_shift[today.lower()])

    how_many_records = (
        session.query(StockData.ticker).filter(StockData.date == last_friday).all()
    )

    if len(how_many_records) == 0:
        last_friday = date.today() - timedelta(days=days_shift[today.lower()] + 1)

    return last_friday


def get_four_weeks_ago_friday(session):
    """Looks for four weeks ago friday. if it was off then it takes thursday"""

    four_weeks_ago_friday = date.today() - timedelta(days=29)
    how_many_records_four_weeks_ago = (
        session.query(StockData.ticker)
        .filter(StockData.date == four_weeks_ago_friday)
        .all()
    )

    if len(how_many_records_four_weeks_ago) == 0:
        four_weeks_ago_friday = date.today() - timedelta(days=30)

    return four_weeks_ago_friday


# TODO: add DB population, not just printing
def count_returns_from_fridays_to_date(
    session, yesterday_data: List[Tuple[str, float]], from_friday: str
) -> None:
    """Counts returns from
    previous friday close price and four weeks before friday close price
    (fridays use closing, not opening price)
    to end_date (previous_day/yesterday) closing price"""

    data_for_df = []
    for record in yesterday_data[:5]:
        try:
            from_friday_closing_price = (
                session.query(StockData.close)
                .filter(StockData.ticker == record[0], StockData.date == from_friday)
                .first()
            )[0]
            result = returns_counter_in_pct(from_friday_closing_price, record[1])
            print(f"{from_friday}, ticker: {record[0]}, return: {result}")

            data_for_df.append({"ticker": record[0], "ytd_return": result})
        except:
            print(f"{from_friday}, did not work out")

    df = pd.DataFrame(data_for_df)
    return df
