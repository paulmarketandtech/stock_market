from dotenv import load_dotenv

load_dotenv()
from stock_market.config import fundamentals_file_path, ohlc_file_path
from stock_market.db_hub.session import get_session, init_db
from stock_market.integrations import yfinance_client
from stock_market.integrations.telegram_momentum_bot import jap
from stock_market.integrations.tg_main import (
    tg_create_DF_for_ytd_weekly_correction,
    tg_sequence,
)
from stock_market.integrations.tradingview_client import sma_calculations
from stock_market.momentum.repositories.ohlc_repo import read_parquet_file, save_ohlc
from stock_market.momentum.services.charts_market_breadth import chart_managing
from stock_market.momentum.services.daily_routine_calculations import (
    count_daily_routine_returns,
)
from stock_market.momentum.services.standard_returns.market_breadth_counting import (
    counting_above_below_SMAs,
)
from stock_market.storage.parquet_io import read_parquet, write_parquet
from stock_market.utils import (
    LAST_CORRECTION_DATE,
    YTD_DATE,
    creating_list_of_tickers_nasdaq,
    creating_list_of_tickers_nyse,
    get_large_cap_tickers,
    get_previous_day,
    logging,
)


def run_ohlc_extract(tickers: list[str], previous_day: str) -> None:
    df, missing = yfinance_client.download_all_ohlc(tickers, previous_day)
    if not df.empty:
        write_parquet(df, ohlc_file_path(previous_day))
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
    with get_session() as session:
        list_of_tickers = get_large_cap_tickers(session)
        previous_day = get_previous_day()

        jap(session)
        """
        logging.info(
            f"Starting working on {previous_day}. Number of ticker: {len(list_of_tickers)}"
        )
        logging.info("Starting YF download.")
        run_ohlc_extract(list_of_tickers, previous_day)

        logging.info("Finished YF and populating the DB")
        populate_db_from_files(previous_day)

        logging.info(
            "DB populated, starting daily routine: weekly, ytd, last correction returns"
        )
        count_daily_routine_returns(
            session, previous_day, YTD_DATE, LAST_CORRECTION_DATE
        )

        logging.info("Daily routine done. Starting SMAs calculations")
        # SMAs have to be moved to something like daily routine - it cannot be 3 calls in main()
        list_of_tickers_nasdaq = creating_list_of_tickers_nasdaq(session)
        list_of_tickers_nyse = creating_list_of_tickers_nyse(session)
        sma_calculations(
            session,
            previous_day,
            list_of_tickers,
            list_of_tickers_nasdaq,
            list_of_tickers_nyse,
        )
        counting_above_below_SMAs(session, previous_day, list_of_tickers)
        chart_managing(session, previous_day)

        logging.info("SMAs related finished. Sending TG messages")
        tg_sequence(session, previous_day)

        logging.info("Daily proccess done.")
        """
    # DONT run fundamentals for now. have to write the whole logic of DB populating
    # run_fundamentals_extract(list_of_tickers[:50])


if __name__ == "__main__":
    init_db()
    main()
