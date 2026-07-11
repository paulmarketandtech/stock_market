from dotenv import load_dotenv

load_dotenv()
import os
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
    get_previous_day,
    logging,
)

logging.info("starting scratching")


async def user_info_momentum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("User %s started the conversation.", update)
    await update.message.reply_text("info jap")


def get_commodities_returns(session, previous_day: str):
    """It returns last week returns for indexes, commodities and etfs"""
    list_of_commodities = get_commodities_tickers(session)
    query_result_commodities = (
        select(StockData)
        .where(StockData.ticker.in_(list_of_commodities))
        .filter(StockData.date == previous_day)
    )
    results = session.scalars(query_result_commodities).all()

    output = []
    for r in results:
        output.append((r.ticker, r.weekly_change))

    df_commodities = pd.DataFrame(output, columns=["ticker", "weekly_returns"])
    df_commodities.dropna(inplace=True)
    df_commodities.sort_values(by="weekly_returns", inplace=True, ascending=False)

    return df_commodities


def get_etfs_returns(session, previous_day: str):
    """It returns last week returns of etfs"""
    list_of_etfs = get_etfs_tickers(session)
    query_result_etfs = (
        select(StockData)
        .where(StockData.ticker.in_(list_of_etfs))
        .filter(StockData.date == previous_day)
    )
    results = session.scalars(query_result_etfs).all()

    output = []
    for r in results:
        output.append((r.ticker, r.weekly_change))

    df_etfs = pd.DataFrame(output, columns=["ticker", "weekly_returns"])
    df_etfs.dropna(inplace=True)
    df_etfs.sort_values(by="weekly_returns", inplace=True, ascending=False)

    return df_etfs


def get_indexes_returns(session, previous_day: str):
    """It returns last week indexes returns"""

    list_of_indexes = get_indexes_tickers(session)

    query_result_indexes = (
        select(StockData)
        .where(StockData.ticker.in_(list_of_indexes))
        .filter(StockData.date == previous_day)
    )
    results = session.scalars(query_result_indexes).all()

    output = []
    for r in results:
        output.append((r.ticker, r.weekly_change))

    df_indexes = pd.DataFrame(output, columns=["ticker", "weekly_returns"])
    df_indexes.dropna(inplace=True)
    df_indexes.sort_values(by="weekly_returns", inplace=True, ascending=False)

    return df_indexes


async def weekly_indexes(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]

    try:
        weekly_indexes_msg = "\n\nThis week indexes performance:\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["weekly_returns"]
            weekly_indexes_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id="enter chat_id",
            text=weekly_indexes_msg,
        )
        logging.info("weekly_indexes successly sent")
    except Exception as e:
        logging.error("weekly_indexes Error: %s", e)

    # context.application.stop_running()


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
            print(f"{r.ticker}: {r.weekly_change}")


if __name__ == "__main__":
    application = Application.builder().token(os.getenv("TG_TOKEN")).build()
    job_queue = application.job_queue

    # application.add_handler(CommandHandler("info", user_info_momentum))

    with get_session() as session:
        previous_day = get_previous_day()
        df_commodities = get_commodities_returns(session, previous_day)
        df_etfs = get_etfs_returns(session, previous_day)
        df_indexes = get_indexes_returns(session, previous_day)

    today = datetime.today().strftime("%A")
    if today.lower() == "saturday":
        job_queue.run_once(
            weekly_indexes,
            2,
            data={"df": df_indexes},
        )
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    # init_db()
    # scratch_func()
    """

    """
