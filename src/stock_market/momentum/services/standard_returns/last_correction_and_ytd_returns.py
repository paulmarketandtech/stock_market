from typing import List, Tuple

from stock_market.db_hub.models import StockData
from stock_market.momentum.services.standard_returns.helper_functions import (
    returns_counter_in_pct,
)


# TODO: add DB population, not just printing
def count_returns_from_given_date_to_date(
    session, yesterday_data: List[Tuple[str, float]], from_date: str
) -> None:
    """Counts returns from from_date.open price to end_date.close price
    Example: to count YTD returns it uses opening price from the very first session day in a year
    """
    for record in yesterday_data[:5]:
        try:
            from_date_opening_price = (
                session.query(StockData.open)
                .filter(StockData.ticker == record[0], StockData.date == from_date)
                .first()
            )[0]
            result = returns_counter_in_pct(from_date_opening_price, record[1])
            print(f"{from_date}, ticker: {record[0]}, return: {result}")
        except:
            print(f"{from_date}, did not work out")
