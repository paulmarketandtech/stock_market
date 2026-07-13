import logging

import pandas as pd

from stock_market.db_hub.models import StockData
from stock_market.db_hub.session import get_session

logger = logging.getLogger(__name__)


def read_parquet_file(filename: str):
    df = pd.read_parquet(filename)
    df["date"] = pd.to_datetime(df["date"])
    return df


def save_ohlc(filename: str):
    try:
        df = read_parquet_file(filename)

        with get_session() as session:
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
                session.add(stock_price)

        session.commit()
        logger.info("DB Populated")

    except Exception as e:
        logger.error("Database population failed %s: ", e, exc_info=True)
