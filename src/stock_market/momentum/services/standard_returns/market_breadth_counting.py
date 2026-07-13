import logging
from datetime import date

from sqlalchemy.sql import and_

from stock_market.db_hub.models import MarketBreadth, StockData

logger = logging.getLogger(__name__)


def get_change(above, number_of_tickers):
    if above == number_of_tickers:
        return 100.0
    try:
        return (above / number_of_tickers) * 100.0
    except ZeroDivisionError:
        return 0


def counting_above_below_SMAs(session, previous_day: date, list_of_tickers: list[str]):
    query_ma = (
        session.query(StockData)
        .filter(
            and_(StockData.ticker.in_(list_of_tickers), StockData.date == previous_day)
        )
        .all()
    )
    logger.info("Number of stocks: %d", len(query_ma))

    # ------ 50
    above50 = 0
    below50 = 0
    for ticker in query_ma:
        if ticker.ma50_above:
            above50 += 1
        else:
            below50 += 1

    logger.info("Number of stocks above ma50 %d", above50)
    logger.info("Number of stocks below ma50 %d", below50)

    market_breadth_50 = get_change(above50, len(query_ma))

    # ------ 100
    above100 = 0
    below100 = 0
    for ticker in query_ma:
        if ticker.ma100_above:
            above100 += 1
        else:
            below100 += 1

    logger.info("Number of stocks above ma100 %d", above100)
    logger.info("Number of stocks below ma100 %d", below100)

    market_breadth_100 = get_change(above100, len(query_ma))

    # ------ 200
    above200 = 0
    below200 = 0
    for ticker in query_ma:
        if ticker.ma200_above:
            above200 += 1
        else:
            below200 += 1

    logger.info("Number of stocks above ma200 %d", above200)
    logger.info("Number of stocks below ma200 %d", below200)

    market_breadth_200 = get_change(above200, len(query_ma))

    stock_data = MarketBreadth(
        date=previous_day,
        ma50_number_of_stocks_above=above50,
        ma50_number_of_stocks_below=below50,
        ma50_pct_of_stocks_above=market_breadth_50,
        ma100_number_of_stocks_above=above100,
        ma100_number_of_stocks_below=below100,
        ma100_pct_of_stocks_above=market_breadth_100,
        ma200_number_of_stocks_above=above200,
        ma200_number_of_stocks_below=below200,
        ma200_pct_of_stocks_above=market_breadth_200,
    )
    session.add(stock_data)
    session.commit()

    query_result_mb = (
        session.query(MarketBreadth).filter(MarketBreadth.date == previous_day).all()
    )
    logger.info(
        "Number of new records in market breadth DB as of %s: %d",
        previous_day,
        len(query_result_mb),
    )

    if len(query_result_mb) > 0:
        logger.info("Market Breadth completed successfully.")
