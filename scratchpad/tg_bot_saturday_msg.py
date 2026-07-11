from dotenv import load_dotenv

load_dotenv()
from datetime import date, datetime, timedelta

import pandas as pd
from sqlalchemy import select
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from stock_market.db_hub.models import StockData
from stock_market.db_hub.session import get_session, init_db
from stock_market.momentum.services.standard_returns.fridays_returns import (
    count_returns_from_fridays_to_date,
    get_previous_friday,
)
from stock_market.utils import (
    get_commodities_tickers,
    get_etfs_tickers,
    get_indexes_tickers,
    get_large_cap_tickers,
    logging,
)

logging.info("starting scratching")


def scratch_func():
    with get_session() as session:
        list_of_commodities = get_commodities_tickers(session)
        previous_friday = get_previous_friday(session)

        stmt = (
            select(StockData)
            .where(StockData.ticker.in_(list_of_commodities))
            .filter(StockData.date == previous_friday)
        )

        results = session.scalars(stmt).all()
        print(results)
        for r in results:
            print(f"{r.ticker}: {r.open}")


if __name__ == "__main__":
    init_db()
    scratch_func()
