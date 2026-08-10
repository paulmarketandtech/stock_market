import logging
from datetime import date

from stock_market.db_hub.models import StockData
from stock_market.momentum.services.standard_returns.helper_functions import (
    returns_counter_in_pct,
)

logger = logging.getLogger(__name__)


def count_returns_from_given_date_to_date(
    session,
    previous_day: date,
    yesterday_data: list[tuple[str, float]],
    from_date: date,
    ytd_or_correction: str,
) -> None:
    """Counts returns from from_date.open price to end_date.close price
    Example: to count YTD returns it uses opening price from the very first session day in a year
    """

    for record in yesterday_data:
        symbol = record[0]
        yesterday_closing_price = record[1]

        try:
            from_date_opening_price = (
                session.query(StockData.open)
                .filter(StockData.ticker == symbol, StockData.date == from_date)
                .first()
            )[0]

            pct_return_result = returns_counter_in_pct(
                from_date_opening_price, yesterday_closing_price
            )

            session.query(StockData).filter_by(ticker=symbol, date=previous_day).update(
                {ytd_or_correction: pct_return_result}
            )
        except Exception as e:
            logger.error("%s, %s did not work out. Error: %s", from_date, symbol, e)

    session.commit()
    logger.info("Done count_returns_from_given_date_to_date")
