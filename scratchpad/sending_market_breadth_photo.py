from dotenv import load_dotenv

load_dotenv()
import os
from datetime import date, datetime

from sqlalchemy import select
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from stock_market.db_hub.session import get_session, init_db
from stock_market.utils import get_previous_day, logging

logging.info("starting scratching")


async def market_breadth(context: ContextTypes.DEFAULT_TYPE) -> None:
    job_data = context.job.data
    previous_day = job_data["date"]
    chat_id = job_data["chat_id"]

    try:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=f"{os.getenv('MARKET_BREADTH_SCREENS_FOLDER')}/{str(previous_day).replace('-', '')}.png",
        )
        logging.info("market_breadth successly sent")
    except Exception as e:
        logging.error("market_breadth Error: %s", e)
    context.application.stop_running()


def function_caller(previous_day: str):
    application = Application.builder().token(os.getenv("TG_TOKEN")).build()
    job_queue = application.job_queue
    job_queue.run_once(
        market_breadth,
        2,
        data={"date": previous_day, "chat_id": os.getenv("MY_TG_ID")},
    )
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":

    previous_day = get_previous_day()
    # init_db()
    function_caller(previous_day)
