from typing import List, Tuple

from stock_market.momentum.services.standard_returns.fridays_returns import (
    count_returns_from_fridays_to_date,
    get_previous_friday,
)
from stock_market.momentum.services.standard_returns.helper_functions import (
    get_yesterdays_data,
)
from stock_market.momentum.services.standard_returns.last_correction_and_ytd_returns import (
    count_returns_from_given_date_to_date,
)
from stock_market.utils import logging


def count_daily_routine_returns(
    session, previous_day: str, ytd_date: str, correction_date: str
):

    yesterday_data = get_yesterdays_data(session, previous_day)
    previous_friday = get_previous_friday(session)

    logging.info(f"Starting weekly returns. Previous Friday: {previous_friday}")
    current_week_returns = count_returns_from_fridays_to_date(
        session, previous_day, yesterday_data, previous_friday
    )

    logging.info("Starting ytd returns.")
    ytd_returns = count_returns_from_given_date_to_date(
        session, previous_day, yesterday_data, ytd_date, "ytd"
    )

    logging.info("Starting las correction returns.")
    correction_returns = count_returns_from_given_date_to_date(
        session, previous_day, yesterday_data, correction_date, "last_correction"
    )


"""
implement this logic above for ytd/last_correction
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pipeline", choices=["daily", "extra-metrics"])
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    try:
        if args.pipeline == "daily":
            run_daily_momentum()
        elif args.pipeline == "extra-metrics":
            run_extra_metrics()
    except Exception:
        logger.exception("%s pipeline failed", args.pipeline)
        telegram_momentum_bot.send_error_alert(f"{args.pipeline} run failed, check logs")
        raise

if __name__ == "__main__":
    main()
"""
