import logging
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from stock_market.db_hub.models import StockData

logger = logging.getLogger(__name__)


class DBPopulation:
    def __init__(self, session: Session, filename: str | Path) -> None:
        self.session = session
        self.filename = filename

    def read_parquet_file(self):
        df = pd.read_parquet(self.filename, engine="pyarrow")
        df["date"] = pd.to_datetime(df["date"])
        return df

    def save_ohlc(self):
        """There's no try/except because if the file is missing then it will crush the process as desired"""
        df = self.read_parquet_file()
        if not df.empty:

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

        else:
            logger.exception("Database population failed")
            return False
        return True


def populate_db_from_files(session: Session, filename: Path) -> bool:
    db_populating = DBPopulation(session, filename)
    return db_populating.save_ohlc()
