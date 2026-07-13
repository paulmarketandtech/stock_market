import logging
import time
from datetime import date, datetime
from typing import Dict

import pandas as pd
import yfinance as yf

from stock_market.db_hub.models import (
    AllTickersMonthlyUpdate,
    ExtraStockMetricsAndStats,
)

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = ["fiftyTwoWeekHigh", "fiftyTwoWeekLow"]
OPTIONAL_FIELDS = [
    "marketCap",
    "longName",
    "fiftyTwoWeekRange",
    "fullExchangeName",
    "shortPercentOfFloat",
    "shortRatio",
    "beta",
    "dateShortInterest",
]


def fetch_stock_data(symbol_list: list[str]) -> pd.DataFrame:
    rows = []
    all_fields = REQUIRED_FIELDS + OPTIONAL_FIELDS

    start = datetime.now()
    for i, ticker in enumerate(symbol_list):
        time.sleep(0.1)
        if (i + 1) % 300 == 0:
            logger.info("Processing %d", (i + 1) / len(symbol_list))
            logger.info(datetime.now() - start)
            print(f"Processing {i + 1}/{len(symbol_list)}")
            print(datetime.now() - start)

        try:
            info = yf.Ticker(ticker).info

            missing_required = [
                field
                for field in REQUIRED_FIELDS
                if field not in info or info[field] is None
            ]

            if missing_required:
                logger.warning(
                    "%s: missing required fields %s, skipping", ticker, missing_required
                )
                continue

            row = {"ticker": ticker}
            for field in all_fields:
                row[field] = info.get(field)

            rows.append(row)

            logger.info("Ticker %s downloaded", ticker)
        except Exception as e:
            logger.error(
                "Error %s while downloading from YF: %s", ticker, e, exc_info=True
            )
            continue

    df = pd.DataFrame(rows)

    end = datetime.now()
    logger.info("total time: %d", (end - start))
    return df


def _insert_new_ticker(session, row: pd.Series, previous_day: date) -> None:
    session.add(
        ExtraStockMetricsAndStats(
            ticker=row["ticker"],
            long_name=row["longName"],
            fifty_two_week_high_value=row["fiftyTwoWeekHigh"],
            date_52week_high=previous_day,
            fifty_two_week_low_value=row["fiftyTwoWeekLow"],
            date_52week_low=previous_day,
            market_cap=row["marketCap"],
            fifty_two_week_range=row["fiftyTwoWeekRange"],
            full_exchange_name=row["fullExchangeName"],
            beta_value=row["beta"],
            short_ratio=row["shortRatio"],
            short_percent_of_float=row["shortPercentOfFloat"],
            date_short_interest=row["dateShortInterest"],
        )
    )
    logging.info("NEW TICKER. Inserted %s", row["ticker"])


def _upsert_metadata(row: pd.Series, record: ExtraStockMetricsAndStats) -> None:
    record.long_name = row["longName"]
    record.market_cap = row["marketCap"]
    record.fifty_two_week_range = row["fiftyTwoWeekRange"]
    record.full_exchange_name = row["fullExchangeName"]
    record.beta_value = row["beta"]
    record.short_ratio = row["shortRatio"]
    record.short_percent_of_float = row["shortPercentOfFloat"]
    record.date_short_interest = row["dateShortInterest"]


def _update_52_week_extremes(
    row: pd.Series, record: ExtraStockMetricsAndStats, previous_day: date
) -> None:
    """
    there are no else statements becasue if is not true then nothing happens
    """
    ticker = row["ticker"]
    currentHigh = record.fifty_two_week_high_value
    newHighValue = row["fiftyTwoWeekHigh"]

    currentLow = record.fifty_two_week_low_value
    newLowValue = row["fiftyTwoWeekLow"]

    if currentHigh is None or newHighValue > currentHigh:
        record.fifty_two_week_high_value = newHighValue
        record.date_52week_high = previous_day
        logger.info(
            "NEW HIGH. Updated %s: high %d → %d on %s",
            ticker,
            currentHigh,
            newHighValue,
            previous_day,
        )

    if currentLow is None or newLowValue < currentLow:
        record.fifty_two_week_low_value = newLowValue
        record.date_52week_low = previous_day
        logger.info(
            f"NEW LOW. Updated %s: low %d → %d on %s",
            ticker,
            currentLow,
            newLowValue,
            previous_day,
        )


def _process_ticker(
    row: pd.Series,
    session,
    previous_day: date,
    records: Dict[str, ExtraStockMetricsAndStats],
) -> None:
    ticker = row["ticker"]
    if ticker not in records:
        _insert_new_ticker(session, row, previous_day)
    else:
        record = records[ticker]
        _upsert_metadata(row, record)
        _update_52_week_extremes(row, record, previous_day)


def update_stock_metrics(session, previous_day: date, df: pd.DataFrame):
    records: Dict[str, ExtraStockMetricsAndStats] = {
        r.ticker: r for r in session.query(ExtraStockMetricsAndStats).all()
    }
    for _, row in df.iterrows():
        try:
            with session.begin_nested():  # savepoint – auto rollback on exception
                _process_ticker(row, session, previous_day, records)
        except Exception as e:
            logging.error(f"Skipping {row['ticker']}: {e}", exc_info=True)
            session.rollback()
    session.commit()


def download_all_fundamentals(session, previous_day: date, list_of_tickers: list[str]):
    df = fetch_stock_data(list_of_tickers)
    update_stock_metrics(session, previous_day, df)
    return df


if __name__ == "__main__":

    download_all_fundamentals()
