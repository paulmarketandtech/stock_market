import pandas as pd

from stock_market.db_hub.models import StockData, YTD20Best
from stock_market.db_hub.session import get_session


def read_parquet_file(filename: str):
    df = pd.read_parquet(filename)
    return df


def save_ohlc(filename: str):
    df = read_parquet_file(filename)

    with get_session() as session:
        """
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
        print("DB Populated")
        """
        stock_data = (
            session.query(StockData.ticker).filter(StockData.date == "2026-07-06").all()
        )

    print(len(stock_data))
    print(stock_data[:10])
