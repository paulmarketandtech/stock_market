import logging
from datetime import date

import pandas as pd
from sqlalchemy.orm import Session

from stock_market.config import ohlc_file_path
from stock_market.db_hub.models import StockData

logger = logging.getLogger(__name__)


class DBPopulation:
    def __init__(self, session: Session, filename: str) -> None:
        self.session = session
        self.filename = filename

    def read_parquet_file(self):
        df = pd.read_parquet(self.filename, engine="pyarrow")
        df["date"] = pd.to_datetime(df["date"])
        return df

    def save_ohlc(self):
        try:
            df = self.read_parquet_file()

            for _, row in df.iterrows():
                stock_price = StockData(
                    date=row["date"],
                    close=row["close"],
                    high=row["high"],
                    low=row["low"],
                    open=row["open"],
                    volume=row["volume"],
                    ticker=row["ticker"],
                )
                self.session.add(stock_price)

            self.session.commit()
            logger.info("DB Populated")

        except Exception as e:
            logger.error("Database population failed %s: ", e, exc_info=True)


def populate_db_from_files(session: Session, previous_day: date) -> None:
    filename = ohlc_file_path(previous_day)
    db_populating = DBPopulation(session, filename)
    db_populating.save_ohlc()
