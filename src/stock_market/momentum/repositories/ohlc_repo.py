import pandas as pd

from stock_market.db_hub.models import StockData
from stock_market.db_hub.session import get_session


def read_parquet_file(filename: str):
    df = pd.read_parquet(filename)
    df["date"] = pd.to_datetime(df["date"])
    """
    search_date = pd.to_datetime("2026-07-07")
    matching_rows = df[df["date"] == search_date]
    print(f"0707: {matching_rows}")
    print(len(matching_rows))
    # print(df)
    print(len(df))
    """
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
        print("DB Populated")
        # TODO: delete below this
        stock_data = (
            session.query(StockData.ticker).filter(StockData.date == "2026-07-08").all()
        )
        print(len(stock_data))
        print(f"first100 from 20260708: {stock_data[:100]}")

    except Exception as e:
        print(f"Database population failed: {e}")
