import os

from tradingview_ta import Interval, TA_Handler, get_multiple_analysis

from stock_market.db_hub.models import StockData
from stock_market.utils import logging


def nasdaq_counting_and_populating_DB_with_SMAs(
    session, last_date: str, nasdaq_list_of_tickers: list[str]
):
    logging.info("Nasdaq SMAa calculations started.")
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
        except AttributeError as e:
            logging.error(f"Error with {ticker} in SMAs: {e}", exc_info=True)

    logging.info("Nasdaq SMAa populated successfully.")
    print("Nasdaq SMAa populated")


def nyse_counting_and_populating_DB_with_SMAs(
    session, last_date: str, nyse_list_of_tickers: list[str]
):
    logging.info("Nyse SMAa calculations started.")
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
        except AttributeError as e:
            logging.error(f"Error with {ticker} in SMAs: {e}", exc_info=True)

    logging.info("Nyse SMAa populated successfully.")
    print("Nyse SMAa populated")


def check_above_below_sma(session, tickers: list[str], last_date: str):
    logging.info("Above/below SMAs counting started.")
    for ticker in tickers:
        try:
            session.query(StockData).filter_by(ticker=ticker, date=last_date).update(
                {
                    "ma50_above": case(
                        (
                            and_(
                                StockData.ma50.isnot(None),
                                StockData.close > StockData.ma50,
                            ),
                            True,
                        ),
                        (StockData.ma50.is_(None), False),
                        else_=False,
                    )
                },
                synchronize_session=False,
            )

            session.query(StockData).filter_by(ticker=ticker, date=last_date).update(
                {
                    "ma100_above": case(
                        (
                            and_(
                                StockData.ma100.isnot(None),
                                StockData.close > StockData.ma100,
                            ),
                            True,
                        ),
                        (StockData.ma100.is_(None), False),
                        else_=False,
                    )
                },
                synchronize_session=False,
            )

            session.query(StockData).filter_by(ticker=ticker, date=last_date).update(
                {
                    "ma200_above": case(
                        (
                            and_(
                                StockData.ma200.isnot(None),
                                StockData.close > StockData.ma200,
                            ),
                            True,
                        ),
                        (StockData.ma200.is_(None), False),
                        else_=False,
                    )
                },
                synchronize_session=False,
            )

            session.commit()

        except Exception as e:
            logging.error(
                f"Error in counting above/below SMAs/Bad ticker {e}", exc_info=True
            )
    logging.info("Above/below SMAs counted.")
    print("Above/below SMAs counted")


def sma_calculations(
    session,
    last_date: str,
    list_of_tickers: list[str],
    nasdaq_list_of_tickers: list[str],
    nyse_list_of_tickers: list[str],
):

    logging.info("Starting Nasdaq SMAs DB populating from TV")

    nasdaq_counting_and_populating_DB_with_SMAs(
        session, last_date, nasdaq_list_of_tickers
    )
    logging.info("Nasdaq SMAs done. Starting Nyse SMAs DB populating from TV")

    nyse_counting_and_populating_DB_with_SMAs(session, last_date, nyse_list_of_tickers)

    logging.info("Nyse SMAs done. Starting check above/below SMA")

    check_above_below_sma(session, list_of_tickers, last_date)
