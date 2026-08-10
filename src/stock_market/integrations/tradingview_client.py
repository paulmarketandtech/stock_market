import logging
from datetime import date

from tradingview_ta import Interval, get_multiple_analysis

from stock_market.db_hub.models import StockData

logger = logging.getLogger(__name__)


def nasdaq_counting_and_populating_DB_with_SMAs(
    session, last_date: date, nasdaq_list_of_tickers: list[str]
) -> None:
    logger.info("Starting Nasdaq SMAs DB populating from TV")
    nasdaq_ta_symbols = []
    nasdaq_string_ticker = "NASDAQ:"

    for ticker in nasdaq_list_of_tickers:
        nasdaq_ta_symbols.append(nasdaq_string_ticker + ticker)

    nasdaq_analysis = get_multiple_analysis(
        screener="america", interval=Interval.INTERVAL_1_DAY, symbols=nasdaq_ta_symbols
    )

    for ticker, indicator in nasdaq_analysis.items():
        try:
            session.query(StockData).filter_by(
                ticker=ticker.split(":")[1], date=last_date
            ).update({"ma50": indicator.indicators["SMA50"]})
            session.query(StockData).filter_by(
                ticker=ticker.split(":")[1], date=last_date
            ).update({"ma100": indicator.indicators["SMA100"]})
            session.query(StockData).filter_by(
                ticker=ticker.split(":")[1], date=last_date
            ).update({"ma200": indicator.indicators["SMA200"]})
            session.commit()
        except AttributeError:
            logger.exception("Error with %s in SMAs.", ticker)

    logger.info("Nasdaq SMAa populated successfully.")


def nyse_counting_and_populating_DB_with_SMAs(
    session, last_date: date, nyse_list_of_tickers: list[str]
) -> None:
    logger.info("Starting Nyse SMAs DB populating from TV")
    nyse_ta_symbols = []
    nyse_string_ticker = "NYSE:"

    for ticker in nyse_list_of_tickers:
        nyse_ta_symbols.append(nyse_string_ticker + ticker)

    nyse_analysis = get_multiple_analysis(
        screener="america", interval=Interval.INTERVAL_1_DAY, symbols=nyse_ta_symbols
    )

    for ticker, indicator in nyse_analysis.items():
        try:
            session.query(StockData).filter_by(
                ticker=ticker.split(":")[1], date=last_date
            ).update({"ma50": indicator.indicators["SMA50"]})
            session.query(StockData).filter_by(
                ticker=ticker.split(":")[1], date=last_date
            ).update({"ma100": indicator.indicators["SMA100"]})
            session.query(StockData).filter_by(
                ticker=ticker.split(":")[1], date=last_date
            ).update({"ma200": indicator.indicators["SMA200"]})
            session.commit()
        except AttributeError:
            logger.exception("Error with %s in SMAs.", ticker)

    logger.info("Nyse SMAa populated successfully.")


def tradingview_sma_db_population(
    session,
    last_date: date,
    nasdaq_list_of_tickers: list[str],
    nyse_list_of_tickers: list[str],
):

    nasdaq_counting_and_populating_DB_with_SMAs(
        session, last_date, nasdaq_list_of_tickers
    )

    nyse_counting_and_populating_DB_with_SMAs(session, last_date, nyse_list_of_tickers)
