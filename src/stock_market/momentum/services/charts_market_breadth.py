import logging
import os
from datetime import date

import matplotlib

from stock_market.db_hub.models import MarketBreadth

matplotlib.use("Agg")
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def generate_y_and_x_values_for_chart(session):
    query50 = session.query(MarketBreadth.ma50_pct_of_stocks_above).all()
    lst50 = []
    for value in query50:
        lst50.append(value[0])

    query100 = session.query(MarketBreadth.ma100_pct_of_stocks_above).all()
    lst100 = []
    for value in query100:
        lst100.append(value[0])

    query200 = session.query(MarketBreadth.ma200_pct_of_stocks_above).all()
    lst200 = []
    for value in query200:
        lst200.append(value[0])

    query_dates = session.query(MarketBreadth.date).all()
    lst_dates = []
    for value in query_dates:
        lst_dates.append(value[0].strftime("%Y-%m-%d"))

    return lst50, lst100, lst200, lst_dates


def chart_creation(y1, y2, y3, x, previous_day: date):
    try:
        _, ax = plt.subplots(figsize=(12, 8))

        ax.plot(x, y1, linewidth=2.0, label="ma50")
        ax.plot(x, y2, linewidth=2.0, label="ma100")
        ax.plot(x, y3, linewidth=2.0, label="ma200")

        ax.set_xticks(x[::20])
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        ax.grid(True, linestyle="--", alpha=0.7)

        ax.legend()
        plt.title("Market Breadth")
        plt.ylabel("percentage of stocks above MA")
        plt.savefig(
            f"{os.getenv('MARKET_BREADTH_SCREENS_FOLDER')}/{str(previous_day).replace('-', '')}.png"
        )

        logger.info("Chart created successfully.")
    except Exception:
        logger.exception("Chart went wrong. Error.")


def chart_managing(session, previous_day):
    y1, y2, y3, x = generate_y_and_x_values_for_chart(session)
    chart_creation(y1, y2, y3, x, previous_day)
