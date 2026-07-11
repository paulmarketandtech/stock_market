import os
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from stock_market.momentum.services.tg_bot_calculations import (
    get_commodities_returns,
    get_etfs_returns,
    get_indexes_returns,
    tg_create_DF_for_ytd_weekly_correction,
)
from stock_market.utils import get_large_cap_tickers, logging

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
        logging.info("market_breadth successly sent")
    except Exception as e:
        logger.error("market_breadth Error: %s", e)
    context.application.stop_running()


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

    job_queue.run_once(
        market_breadth_screen,
        23,
        data={
            "date": previous_day,
            "chat_id": os.getenv("CJT_GROUP_ID"),
            "room_id": os.getenv("TICKER_BOT_ROOM"),
        },
    )

    logging.info("job queue ended")

    application.run_polling(allowed_updates=Update.ALL_TYPES)

    logging.info("Finished TG bot")
