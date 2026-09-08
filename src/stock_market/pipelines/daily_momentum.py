import logging
from datetime import date

from stock_market.config import ohlc_file_path
from stock_market.db_hub.session import get_session
from stock_market.integrations import tg_main, yfinance_ohlc_client
from stock_market.momentum.repositories import (
    daily_routine_calculations_repo,
    market_breadth_repo,
    ohlc_repo,
)
from stock_market.storage.parquet_io import write_parquet
from stock_market.utils import (
    LAST_CORRECTION_DATE,
    YTD_DATE,
    get_large_cap_tickers,
    get_previous_day,
)

logger = logging.getLogger(__name__)


def run_ohlc_extract(tickers: list[str], previous_day: date) -> None:
    df, missing = yfinance_ohlc_client.download_all_ohlc(tickers, previous_day)
    if not df.empty:
        write_parquet(df, ohlc_file_path(previous_day))
    if missing:
        print("OHLC extract finished with %d missing tickers", len(missing))


def start_daily_momentum():

    with get_session() as session:
        list_of_tickers = get_large_cap_tickers(session)
        previous_day = get_previous_day()

        logger.info(
            "Starting working on %s. Number of ticker: %d",
            previous_day,
            len(list_of_tickers),
        )

        run_ohlc_extract(list_of_tickers, previous_day)

        filename = ohlc_file_path(previous_day)
        if filename:

            ohlc_repo.populate_db_from_files(session, filename)

            daily_routine_calculations_repo.count_daily_routine_returns(
                session, previous_day, YTD_DATE, LAST_CORRECTION_DATE
            )

            market_breadth_repo.market_breadth_manager(
                session, previous_day, list_of_tickers
            )

            tg_main.tg_sequence(session, previous_day)

            logger.info("Daily proccess done.")

        logger.warning("A lot of missing data - probably a bank holiday")
