import logging
from datetime import date

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

logger = logging.getLogger(__name__)


def count_daily_routine_returns(
    session, previous_day: date, ytd_date: date, correction_date: date
):

    yesterday_data = get_yesterdays_data(session, previous_day)
    previous_friday = get_previous_friday(session)

    logger.info("Starting weekly returns. Previous Friday: %s", previous_friday)
    count_returns_from_fridays_to_date(
        session, previous_day, yesterday_data, previous_friday
    )

    logger.info("Starting ytd returns.")
    count_returns_from_given_date_to_date(
        session, previous_day, yesterday_data, ytd_date, "ytd"
    )

    logger.info("Starting las correction returns.")
    count_returns_from_given_date_to_date(
        session, previous_day, yesterday_data, correction_date, "last_correction"
    )
