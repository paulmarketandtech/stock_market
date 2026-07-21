import logging
import time
from datetime import date, datetime
from typing import Dict

import pandas as pd
import yfinance as yf
from sqlalchemy.orm import Session

from stock_market.config import fundamentals_file_path
from stock_market.db_hub.models import ExtraStockMetricsAndStats
from stock_market.storage.parquet_io import write_parquet

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
        time.sleep(0.2)
        if (i + 1) % 300 == 0:
            logger.info(f"Processing {i + 1}/{len(symbol_list)}")
            logger.info(datetime.now() - start)

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

        except Exception as e:
            logger.error(
                "Error %s while downloading from YF: %s", ticker, e, exc_info=True
            )
            continue

    df = pd.DataFrame(rows)

    end = datetime.now()
    logger.info("total time: %s", (end - start))
    return df


class ExtraMetricsUpdater:
    def __init__(self, session: Session, previous_day: date) -> None:
        self.session = session
        self.previous_day = previous_day

    def _insert_new_ticker(self, row: pd.Series) -> None:
        self.session.add(
            ExtraStockMetricsAndStats(
                ticker=row["ticker"],
                long_name=row["longName"],
                fifty_two_week_high_value=row["fiftyTwoWeekHigh"],
                date_52week_high=self.previous_day,
                fifty_two_week_low_value=row["fiftyTwoWeekLow"],
                date_52week_low=self.previous_day,
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

    def _upsert_metadata(
        self, row: pd.Series, record: ExtraStockMetricsAndStats
    ) -> None:
        record.long_name = row["longName"]
        record.market_cap = row["marketCap"]
        record.fifty_two_week_range = row["fiftyTwoWeekRange"]
        record.full_exchange_name = row["fullExchangeName"]
        record.beta_value = row["beta"]
        record.short_ratio = row["shortRatio"]
        record.short_percent_of_float = row["shortPercentOfFloat"]
        record.date_short_interest = row["dateShortInterest"]

    def _update_52_week_extremes(
        self, row: pd.Series, record: ExtraStockMetricsAndStats
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
            record.date_52week_high = self.previous_day
            logger.info(
                "NEW HIGH. Updated %s: high %f → %f on %s",
                ticker,
                currentHigh,
                newHighValue,
                self.previous_day,
            )

        if currentLow is None or newLowValue < currentLow:
            record.fifty_two_week_low_value = newLowValue
            record.date_52week_low = self.previous_day
            logger.info(
                "NEW LOW. Updated %s: low %f → %f on %s",
                ticker,
                currentLow,
                newLowValue,
                self.previous_day,
            )

    def _process_ticker(
        self,
        row: pd.Series,
        records: Dict[str, ExtraStockMetricsAndStats],
    ) -> None:
        ticker = row["ticker"]
        if ticker not in records:
            self._insert_new_ticker(row)
        else:
            record = records[ticker]
            self._upsert_metadata(row, record)
            self._update_52_week_extremes(row, record)

    def update_stock_metrics(self, df: pd.DataFrame):
        records = {
            r.ticker: r for r in self.session.query(ExtraStockMetricsAndStats).all()
        }
        for _, row in df.iterrows():
            try:
                with self.session.begin_nested():
                    self._process_ticker(row, records)
            except Exception as e:
                logger.error("Skipping %s. Error: %s", row["ticker"], e, exc_info=True)
        self.session.commit()


# TODO: add another function which reads the DF from the file instead of passing it in a return - think about is it really needed now?
def download_all_fundamentals(
    session: Session, previous_day: date, list_of_tickers: list[str]
):
    df = fetch_stock_data(list_of_tickers)

    if not df.empty:
        write_parquet(df, fundamentals_file_path(previous_day))

        updater = ExtraMetricsUpdater(session=session, previous_day=previous_day)
        updater.update_stock_metrics(df=df)
