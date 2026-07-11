import os
from datetime import date, datetime

import pandas as pd
from sqlalchemy import select
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from stock_market.db_hub.models import StockData
from stock_market.utils import (
    get_commodities_tickers,
    get_etfs_tickers,
    get_indexes_tickers,
    get_large_cap_tickers,
    logging,
)

logging.info("Starting telegram bot")

print("TG bot started")

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def user_info_momentum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s started the conversation.", update)
    await update.message.reply_text("info")


async def tuesday_number_of_tickers(context: ContextTypes.DEFAULT_TYPE):
    try:

        list_of_tickers = get_large_cap_tickers()
        msg = f"Number of tickers this week: {len(list_of_tickers)}"

        await context.bot.send_message(
            chat_id=os.getenv("CJT_GROUP_ID"),
            message_thread_id=os.getenv("TICKER_BOT_ROOM"),
            text=msg,
        )
        logging.info("tuesday_number_of_tickers successly sent")
    except Exception as e:
        logger.error("tuesday_number_of_tickers Error: %s", e)


async def ytd_top(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]
    chat_id = job_data["chat_id"]

    try:

        ytd_best_msg = f"Best performing stocks YTD\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["ytd_returns"]
            ytd_best_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=os.getenv("TICKER_BOT_ROOM"),
            text=ytd_best_msg,
        )
        logging.info("ytd_top successly sent")
    except Exception as e:
        logger.error("ytd_top Error: %s", e)


async def ytd_bottom(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]
    chat_id = job_data["chat_id"]

    try:
        ytd_worst_msg = f"Worst performing stocks YTD\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["ytd_returns"]
            ytd_worst_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=os.getenv("TICKER_BOT_ROOM"),
            text=ytd_worst_msg,
        )
        logging.info("ytd_bottom successly sent")
    except Exception as e:
        logger.error("ytd_bottom Error: %s", e)


async def last_correction_top(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]
    chat_id = job_data["chat_id"]

    try:
        last_correction_best_msg = f"Best performing stocks since April 7th\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["correction_returns"]
            last_correction_best_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=os.getenv("TICKER_BOT_ROOM"),
            text=last_correction_best_msg,
        )
        logging.info("last_correction_top successly sent")
    except Exception as e:
        logger.error("last_correction_top Error: %s", e)


async def last_correction_bottom(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]
    chat_id = job_data["chat_id"]

    try:
        last_correction_worst_msg = f"Worst performing stocks since April 7th\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["correction_returns"]
            last_correction_worst_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=os.getenv("TICKER_BOT_ROOM"),
            text=last_correction_worst_msg,
        )
        logging.info("last_correction_bottom successly sent")
    except Exception as e:
        logger.error("last_correction_bottom Error: %s", e)


async def weekly_top(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]
    chat_id = job_data["chat_id"]

    try:
        weekly_best_msg = "This week best performing stocks:\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["weekly_returns"]
            weekly_best_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=os.getenv("TICKER_BOT_ROOM"),
            text=weekly_best_msg,
        )
        logging.info("weekly_top successly sent")
    except Exception as e:
        logger.error("weekly_top Error: %s", e)


async def weekly_bottom(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]
    chat_id = job_data["chat_id"]

    try:
        weekly_worst_msg = "This week worst performing stocks\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["weekly_returns"]
            weekly_worst_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=os.getenv("TICKER_BOT_ROOM"),
            text=weekly_worst_msg,
        )
        logging.info("weekly_bottom successly sent")
    except Exception as e:
        logger.error("weekly_bottom Error: %s", e)


async def weekly_indexes(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]
    chat_id = job_data["chat_id"]

    try:
        weekly_indexes_msg = "\n\nThis week indexes performance:\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["weekly_returns"]
            weekly_indexes_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=os.getenv("TICKER_BOT_ROOM"),
            text=weekly_indexes_msg,
        )
        logging.info("weekly_indexes successly sent")
    except Exception as e:
        logging.error("weekly_indexes Error: %s", e)


async def weekly_commodities(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]
    chat_id = job_data["chat_id"]

    try:
        weekly_commodities_msg = "\n\nThis week commodities performance:\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["weekly_returns"]
            weekly_commodities_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=os.getenv("TICKER_BOT_ROOM"),
            text=weekly_commodities_msg,
        )
        logging.info("weekly_commodities successly sent")
    except Exception as e:
        logging.error("weekly_commodities Error: %s", e)


async def weekly_etfs(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    df = job_data["df"]
    chat_id = job_data["chat_id"]

    try:
        weekly_etfs_msg = "\n\nThis week ETFs performance:\n\n"

        for _, row in df.iterrows():
            ticker = row["ticker"]
            pct_change = row["weekly_returns"]
            weekly_etfs_msg += f"{ticker}: {round(pct_change, 2)}%\n"

        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=os.getenv("TICKER_BOT_ROOM"),
            text=weekly_etfs_msg,
        )
        logging.info("weekly_etfs successly sent")
    except Exception as e:
        logging.error("weekly_etfs Error: %s", e)


async def market_breadth(context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await context.bot.send_photo(
            chat_id=os.getenv("CJT_GROUP_ID"),
            message_thread_id=os.getenv("TICKER_BOT_ROOM"),
            photo=f"{os.getenv('MARKET_BREADTH_SCREENS_FOLDER')}/{str(previous_day).replace('-', '')}.png",
        )
        logging.info("market_breadth successly sent")
    except Exception as e:
        logger.error("market_breadth Error: %s", e)
    context.application.stop_running()


def get_weekly_top_and_bottoms(session, previous_day: str, no_of_results: int):
    query_result_weekly = (
        session.query(StockData.ticker, StockData.weekly_change)
        .filter(StockData.date == previous_day)
        .all()
    )
    df_weekly = pd.DataFrame(query_result_weekly, columns=["ticker", "weekly_returns"])
    df_weekly.dropna(inplace=True)
    df_weekly.sort_values(by="weekly_returns", inplace=True, ascending=False)
    df_weekly_tail = df_weekly.tail(no_of_results)
    df_weekly_tail.sort_values(by="weekly_returns", inplace=True)

    return df_weekly.head(no_of_results), df_weekly_tail


def get_ytd_top_and_bottoms(session, previous_day: str, no_of_results: int):
    query_result_ytd = (
        session.query(StockData.ticker, StockData.ytd)
        .filter(StockData.date == previous_day)
        .all()
    )
    df_ytd = pd.DataFrame(query_result_ytd, columns=["ticker", "ytd_returns"])
    df_ytd.dropna(inplace=True)
    df_ytd.sort_values(by="ytd_returns", inplace=True, ascending=False)
    df_ytd_tail = df_ytd.tail(no_of_results)
    df_ytd_tail.sort_values(by="ytd_returns", inplace=True)

    return df_ytd.head(no_of_results), df_ytd_tail


def get_correction_top_and_bottoms(session, previous_day: str, no_of_results: int):
    query_result_correction = (
        session.query(StockData.ticker, StockData.last_correction)
        .filter(StockData.date == previous_day)
        .all()
    )
    df_correction = pd.DataFrame(
        query_result_correction, columns=["ticker", "correction_returns"]
    )
    df_correction.dropna(inplace=True)
    df_correction.sort_values(by="correction_returns", inplace=True, ascending=False)
    df_correction_tail = df_correction.tail(no_of_results)
    df_correction_tail.sort_values(by="correction_returns", inplace=True)

    return df_correction.head(no_of_results), df_correction_tail


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


def get_commodities_returns(session, previous_day: str):
    """It returns last week commodities returns"""

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
    """It returns last week etfs returns"""

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


def tg_create_DF_for_ytd_weekly_correction(session, previous_day: str):
    df_weekly_top, df_weekly_bottom = get_weekly_top_and_bottoms(
        session, previous_day, 20
    )
    df_ytd_top, df_ytd_bottom = get_ytd_top_and_bottoms(session, previous_day, 20)
    df_correction_top, df_correction_bottom = get_correction_top_and_bottoms(
        session, previous_day, 20
    )
    return (
        df_weekly_top,
        df_weekly_bottom,
        df_ytd_top,
        df_ytd_bottom,
        df_correction_top,
        df_correction_bottom,
    )


def tg_sequence(session, previous_day: str):
    (
        df_weekly_top,
        df_weekly_bottom,
        df_ytd_top,
        df_ytd_bottom,
        df_correction_top,
        df_correction_bottom,
    ) = tg_create_DF_for_ytd_weekly_correction(session, previous_day)

    application = Application.builder().token(os.getenv("TG_TOKEN")).build()

    logging.info("starting job queue")
    job_queue = application.job_queue

    # =========== week opening msg ================

    today = datetime.today().strftime("%A")
    if today.lower() == "tuesday":
        job_queue.run_once(tuesday_number_of_tickers, 2)

    # =========== saturday etfs msgs ================

    today = datetime.today().strftime("%A")
    if today.lower() == "saturday":
        job_queue.run_once(
            weekly_indexes,
            1,
            data={
                "df": get_indexes_returns(session, previous_day),
                "chat_id": os.getenv("CJT_GROUP_ID"),
            },
        )

        job_queue.run_once(
            weekly_commodities,
            2,
            data={
                "df": get_commodities_returns(session, previous_day),
                "chat_id": os.getenv("CJT_GROUP_ID"),
            },
        )

        job_queue.run_once(
            weekly_etfs,
            3,
            data={
                "df": get_etfs_returns(session, previous_day),
                "chat_id": os.getenv("CJT_GROUP_ID"),
            },
        )

    # =========== weekly msgs ================

    job_queue.run_once(
        weekly_top,
        5,
        data={"df": df_weekly_top, "chat_id": os.getenv("CJT_GROUP_ID")},
    )
    job_queue.run_once(
        weekly_bottom,
        8,
        data={"df": df_weekly_bottom, "chat_id": os.getenv("CJT_GROUP_ID")},
    )

    # =========== ytd msgs ================

    job_queue.run_once(
        ytd_top,
        11,
        data={"df": df_ytd_top, "chat_id": os.getenv("CJT_GROUP_ID")},
    )
    job_queue.run_once(
        ytd_bottom,
        14,
        data={"df": df_ytd_bottom, "chat_id": os.getenv("CJT_GROUP_ID")},
    )

    # =========== ytd msgs ================

    job_queue.run_once(
        last_correction_top,
        17,
        data={"df": df_correction_top, "chat_id": os.getenv("CJT_GROUP_ID")},
    )
    job_queue.run_once(
        last_correction_bottom,
        20,
        data={"df": df_correction_bottom, "chat_id": os.getenv("CJT_GROUP_ID")},
    )

    # =========== market breadth ================

    job_queue.run_once(market_breadth, 23)

    logging.info("job queue ended")

    application.run_polling(allowed_updates=Update.ALL_TYPES)

    logging.info("Finished TG bot")
    """
    application.add_handler(CommandHandler("info", user_info_momentum))
    if today.lower() == "saturday":
        job_queue.run_once(weekly_indexes, 4)
        job_queue.run_once(weekly_etfs, 6)


    """
