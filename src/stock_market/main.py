from dotenv import load_dotenv

load_dotenv()
from stock_market.config import fundamentals_file_path, ohlc_file_path
from stock_market.integrations import yfinance_client
from stock_market.momentum.repositories.ohlc_repo import read_parquet_file, save_ohlc
from stock_market.storage.parquet_io import read_parquet, write_parquet
from stock_market.utils import get_large_cap_tickers, get_previous_day


def run_ohlc_extract(tickers: list[str]) -> None:
    df, missing = yfinance_client.download_all_ohlc(tickers)
    if not df.empty:
        write_parquet(df, ohlc_file_path(get_previous_day()))
    if missing:
        print("OHLC extract finished with %d missing tickers", len(missing))


def run_fundamentals_extract(tickers: list[str]) -> None:
    df, missing = yfinance_client.download_all_fundamentals(tickers)
    if not df.empty:
        write_parquet(df, fundamentals_file_path(get_previous_day()))


def populate_db_from_files(run_date) -> None:
    # filename = f"ohlc_{str(run_date).replace('-', '')}.parquet"
    filename = ohlc_file_path(run_date)
    # read_parquet_file(filename)
    save_ohlc(filename)


def main():
    print("Hello from stock market!")
    list_of_tickers = get_large_cap_tickers()
    # yf download works - just clean the code
    # run_ohlc_extract(list_of_tickers[:100])
    # db populations works - just clean the code
    # populate_db_from_files(get_previous_day())
    # DONT run fundamentals for now. have to write the whole logic of DB populating
    # run_fundamentals_extract(list_of_tickers[:50])


if __name__ == "__main__":
    main()
