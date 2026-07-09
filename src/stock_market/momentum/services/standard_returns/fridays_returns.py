from datetime import date, datetime, timedelta
from typing import List, Tuple

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


# TODO: probably won't be used. delete from here but save the algo, it may be needed
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


def count_returns_from_fridays_to_date(
    session,
    previous_day: str,
    yesterday_data: List[Tuple[str, float]],
    friday_date: str,
) -> None:
    """Counts returns from
    previous friday close price and four weeks before friday close price
    (fridays use closing, not opening price)
    to end_date (previous_day/yesterday) closing price"""

    data_for_df = []
    for record in yesterday_data:
        symbol = record[0]
        yesterday_closing_price = record[1]

        try:
            friday_date_closing_price = (
                session.query(StockData.close)
                .filter(StockData.ticker == symbol, StockData.date == friday_date)
                .first()
            )[0]

            pct_return_result = returns_counter_in_pct(
                friday_date_closing_price, yesterday_closing_price
            )
            # print(f"{friday_date}, ticker: {symbol}, return: {pct_return_result}")

            session.query(StockData).filter_by(ticker=symbol, date=previous_day).update(
                {"weekly_change": pct_return_result}
            )
            session.commit()  # i think it can go outside the loop
            """
            check_query = (
                session.query(StockData.weekly_change)
                .filter(StockData.ticker == symbol, StockData.date == "2026-07-07")
                .first()
            )
            print(f"{symbol}: {check_query}")
            """
        except:
            print(f"{friday_date}, {symbol}, did not work out")
