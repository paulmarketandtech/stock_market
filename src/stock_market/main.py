from dotenv import load_dotenv

load_dotenv()
from stock_market.config import fundamentals_file_path, ohcl_file_path
from stock_market.integrations import yfinance_client
from stock_market.storage.parquet_io import write_parquet
from stock_market.utils import get_large_cap_tickers, get_previous_day


def run_ohcl_extract(tickers: list[str]) -> None:
    df, missing = yfinance_client.download_all_ohcl(tickers)
    if not df.empty:
        write_parquet(df, ohcl_file_path(get_previous_day()))
    if missing:
        print("OHCL extract finished with %d missing tickers", len(missing))


def run_fundamentals_extract(tickers: list[str]) -> None:
    df, missing = yfinance_client.download_all_fundamentals(tickers)
    if not df.empty:
        write_parquet(df, fundamentals_file_path(get_previous_day()))


def main():
    print("Hello from stock-market!")
    list_of_tickers = get_large_cap_tickers()
    # run_ohcl_extract(list_of_tickers[:100])
    # DONT run fundamentals for now. have to write the whole logic of DB populating
    run_fundamentals_extract(list_of_tickers[:50])


if __name__ == "__main__":
    main()
