import logging
import os
import time
from datetime import UTC, date, datetime

from telegram import Update
from telegram.ext import Application, ContextTypes

from stock_market.momentum.services.tg_bot_calculations import (
    get_DFs_for_etfs_tickers,
    tg_create_DF_for_ytd_weekly_correction,
)
from stock_market.utils import get_large_cap_tickers

logger = logging.getLogger(__name__)


async def user_info_momentum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s started the conversation.", update)
    await update.message.reply_text("info")


async def tuesday_number_of_tickers(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    session = job_data["session"]
    chat_id = job_data["chat_id"]
    room_id = job_data["room_id"]

    try:
        list_of_tickers = get_large_cap_tickers(session)
        msg = f"Number of tickers this week: {len(list_of_tickers)}"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=room_id,
            text=msg,
        )
        logger.info("tuesday_number_of_tickers successly sent")
    except Exception:
        logger.exception("tuesday_number_of_tickers Error.")


async def ytd_best_worst_returns(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]
    best_worst = job_data["best_worst"]
    chat_id = job_data["chat_id"]
    room_id = job_data["room_id"]

    try:
        ytd_returns_msg = f"{best_worst} performing stocks YTD\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["ytd_returns"]
            ytd_returns_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=room_id,
            text=ytd_returns_msg,
        )
        logger.info("ytd_best_worst_returns successly sent")
    except Exception:
        logger.exception("ytd_best_worst_returns Error.")


async def last_correction_best_worst_returns(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]
    best_worst = job_data["best_worst"]
    chat_id = job_data["chat_id"]
    room_id = job_data["room_id"]

    try:
        correction_returns_msg = f"{best_worst} performing stocks since April 7th\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["correction_returns"]
            correction_returns_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=room_id,
            text=correction_returns_msg,
        )
        logger.info("last_correction_best_worst_returns successly sent")
    except Exception:
        logger.exception("last_correction_best_worst_returns Error.")


async def weekly_best_worst_returns(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]
    best_worst = job_data["best_worst"]
    chat_id = job_data["chat_id"]
    room_id = job_data["room_id"]

    try:
        weekly_returns_msg = f"{best_worst} performing stocks this week\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["weekly_returns"]
            weekly_returns_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=room_id,
            text=weekly_returns_msg,
        )
        logger.info("weekly_best_worst_returns successly sent")
    except Exception:
        logger.exception("weekly_best_worst_returns Error.")


async def weekly_indexes_commodities_etfs_returns(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    string = job_data["string"]
    df = job_data["df"]
    chat_id = job_data["chat_id"]
    room_id = job_data["room_id"]

    try:
        weekly_etfs_msg = f"\n\nThis week {string} performance:\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["weekly_returns"]
            weekly_etfs_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=room_id,
            text=weekly_etfs_msg,
        )
        logger.info("weekly_indexes_commodities_etfs_returns successly sent")
    except Exception:
        logger.exception("weekly_indexes_commodities_etfs_returns Error.")


async def market_breadth_screen(context: ContextTypes.DEFAULT_TYPE) -> None:
    job_data = context.job.data
    previous_day = job_data["date"]
    chat_id = job_data["chat_id"]
    room_id = job_data["room_id"]

    try:
        await context.bot.send_photo(
            chat_id=chat_id,
            message_thread_id=room_id,
            photo=f"{os.getenv('MARKET_BREADTH_SCREENS_FOLDER')}/{str(previous_day).replace('-', '')}.png",
        )
        logger.info("market_breadth successly sent")
    except Exception:
        logger.exception("market_breadth Error.")
    context.application.stop_running()


def tg_sequence(session, previous_day: date):
    (
        df_weekly_top,
        df_weekly_bottom,
        df_ytd_top,
        df_ytd_bottom,
        df_correction_top,
        df_correction_bottom,
    ) = tg_create_DF_for_ytd_weekly_correction(session, previous_day)

    best_worst = ["Best", "Worst"]
    chat_id = os.getenv("CJT_GROUP_ID")
    room_id = os.getenv("TICKER_BOT_ROOM")

    application = Application.builder().token(os.getenv("TG_TOKEN")).build()

    logger.info("starting job queue")
    job_queue = application.job_queue

    # =========== week opening msg ================

    today = datetime.now(UTC).date().strftime("%A")
    if today.lower() == "tuesday":
        job_queue.run_once(
            tuesday_number_of_tickers,
            4,
            data={
                "session": session,
                "chat_id": chat_id,
                "room_id": room_id,
            },
        )

    # =========== saturday etfs msgs ================

    today = datetime.now(UTC).date().strftime("%A")
    if today.lower() == "saturday":
        etfs_list_of_dfs = get_DFs_for_etfs_tickers(session, previous_day)

        string_choices = ["indexes", "commodities", "ETFs"]

        for string, df in zip(string_choices, etfs_list_of_dfs):
            time.sleep(0.5)
            job_queue.run_once(
                weekly_indexes_commodities_etfs_returns,
                4,
                data={
                    "string": string,
                    "df": df,
                    "chat_id": chat_id,
                    "room_id": room_id,
                },
            )

    # =========== weekly msgs ================

    weekly_best_worst_dfs = [df_weekly_top, df_weekly_bottom]

    for string, df in zip(best_worst, weekly_best_worst_dfs):
        time.sleep(0.5)
        job_queue.run_once(
            weekly_best_worst_returns,
            6,
            data={
                "best_worst": string,
                "df": df,
                "chat_id": chat_id,
                "room_id": room_id,
            },
        )

    # =========== ytd msgs ================

    ytd_best_worst_dfs = [df_ytd_top, df_ytd_bottom]

    for string, df in zip(best_worst, ytd_best_worst_dfs):
        time.sleep(0.5)
        job_queue.run_once(
            ytd_best_worst_returns,
            9,
            data={
                "best_worst": string,
                "df": df,
                "chat_id": chat_id,
                "room_id": room_id,
            },
        )

    # =========== last correction msgs ================

    correction_best_worst_dfs = [df_correction_top, df_correction_bottom]

    for string, df in zip(best_worst, correction_best_worst_dfs):
        time.sleep(0.5)
        job_queue.run_once(
            last_correction_best_worst_returns,
            12,
            data={
                "best_worst": string,
                "df": df,
                "chat_id": chat_id,
                "room_id": room_id,
            },
        )

    # =========== market breadth ================

    job_queue.run_once(
        market_breadth_screen,
        15,
        data={
            "date": previous_day,
            "chat_id": chat_id,
            "room_id": room_id,
        },
    )

    logger.info("job queue ended")

    application.run_polling(allowed_updates=Update.ALL_TYPES)

    logger.info("Finished TG bot")
