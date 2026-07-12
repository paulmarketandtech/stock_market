import time

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


def get_returns_for_selected_tickers(
    previous_day: str, list_of_tickers: list[str]
) -> pd.DataFrame:
    """stock_data stores all tickers data.
    User provides list of any tickers
    and the func returns last week returns
    for given list_of_tickers"""

    query_result = (
        select(StockData)
        .where(StockData.ticker.in_(list_of_tickers))
        .filter(StockData.date == previous_day)
    )
    results = session.scalars(query_result).all()

    output = []
    for r in results:
        output.append((r.ticker, r.weekly_change))

    df = pd.DataFrame(output, columns=["ticker", "weekly_returns"])
    df.dropna(inplace=True)
    df.sort_values(by="weekly_returns", inplace=True, ascending=False)

    return df


def get_DFs_for_etfs_tickers(session) -> list[pd.DataFrame]:
    list_of_indexes = get_indexes_tickers(session)
    list_of_commodities = get_commodities_tickers(session)
    list_of_etfs = get_etfs_tickers(session)

    df_indexes = get_returns_for_selected_tickers(previous_day, list_of_indexes)
    df_commodities = get_returns_for_selected_tickers(previous_day, list_of_commodities)
    df_etfs = get_returns_for_selected_tickers(previous_day, list_of_etfs)

    return [df_indexes, df_commodities, df_etfs]


async def weekly_indexes_commodities_etfs_returns(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    string = job_data["string"]
    df = job_data["df"]
    chat_id = job_data["chat_id"]

    try:
        weekly_indexes_msg = f"\n\nThis week {string} performance:\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["weekly_returns"]
            weekly_indexes_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            text=weekly_indexes_msg,
        )
        logging.info("weekly_indexes successly sent")
    except Exception as e:
        logging.error("weekly_indexes Error: %s", e)

    # context.application.stop_running()


if __name__ == "__main__":

    previous_day = date.today() - timedelta(days=2)

    # application.add_handler(CommandHandler("info", user_info_momentum))

    application = Application.builder().token(os.getenv("TG_TOKEN")).build()

    job_queue = application.job_queue

    with get_session() as session:
        list_of_dfs = get_DFs_for_etfs_tickers(session)

    string_choices = ["indexes", "commodities", "ETFs"]

    for string, df in zip(string_choices, list_of_dfs):
        time.sleep(0.5)
        job_queue.run_once(
            weekly_indexes_commodities_etfs_returns,
            1,
            data={
                "string": string,
                "df": df,
                "chat_id": os.getenv("MY_TG_ID"),
            },
        )

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    # init_db()
    # scratch_func()
