import logging

from stock_market.db_hub.session import get_session
from stock_market.integrations import yfinance_extra_metrics_client
from stock_market.utils import get_large_cap_tickers, get_previous_day

logger = logging.getLogger(__name__)


def start_daily_extra_metrics():

    previous_day = get_previous_day()

    with get_session() as session:
        list_of_tickers = get_large_cap_tickers(session)

        logger.info(
            "Starting working on extra metrics for date: %d. Number of ticker: %s",
            previous_day,
            len(list_of_tickers),
        )

        yfinance_extra_metrics_client.download_all_fundamentals(
            session, previous_day, list_of_tickers
        )
