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
from stock_market.momentum.services.tg_bot_calculations import (
    tg_create_DF_for_ytd_weekly_correction,
)
from stock_market.utils import get_previous_day, logging

logging.info("starting scratching")


async def ytd_best_worst_returns(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]
    best_worst = job_data["best_worst"]
    chat_id = job_data["chat_id"]

    try:
        ytd_returns_msg = f"{best_worst} performing stocks YTD\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["ytd_returns"]
            ytd_returns_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            # message_thread_id=os.getenv("TICKER_BOT_ROOM"),
            text=ytd_returns_msg,
        )
        logging.info("ytd_top successly sent")
    except Exception as e:
        logging.error("ytd_top Error: %s", e)
    # context.application.stop_running()


if __name__ == "__main__":

    previous_day = date.today() - timedelta(days=2)

    # application.add_handler(CommandHandler("info", user_info_momentum))

    application = Application.builder().token(os.getenv("TG_TOKEN")).build()

    job_queue = application.job_queue

    with get_session() as session:
        (
            df_weekly_top,
            df_weekly_bottom,
            df_ytd_top,
            df_ytd_bottom,
            df_correction_top,
            df_correction_bottom,
        ) = tg_create_DF_for_ytd_weekly_correction(session, previous_day)

    best_worst = ["Best", "Worst"]
    ytd_best_worst_dfs = [df_ytd_top, df_ytd_bottom]

    for string, df in zip(best_worst, ytd_best_worst_dfs):
        time.sleep(0.5)
        job_queue.run_once(
            ytd_best_worst_returns,
            3,
            data={
                "best_worst": string,
                "df": df,
                "chat_id": os.getenv("MY_TG_ID"),
            },
        )

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    # init_db()
    # scratch_func()
