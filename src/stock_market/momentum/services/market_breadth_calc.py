import logging
from datetime import date

from sqlalchemy import case
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from stock_market.db_hub.models import StockData

logger = logging.getLogger(__name__)


def above_below_sma_calculations(
    session: Session,
    last_date: date,
    list_of_tickers: list[str],
):
    logger.info("Above/below SMAs counting started.")
    ma_pairs = [
        ("ma50", "ma50_above"),
        ("ma100", "ma100_above"),
        ("ma200", "ma200_above"),
    ]

    for ticker in list_of_tickers:
        try:
            update_values = {}
            for ma_col_name, above_col_name in ma_pairs:
                ma_col = getattr(StockData, ma_col_name)

                update_values[above_col_name] = case(
                    (
                        and_(
                            ma_col.isnot(None),
                            StockData.close > ma_col,
                        ),
                        True,
                    ),
                    (ma_col.is_(None), False),
                    else_=False,
                )

            session.query(StockData).filter_by(ticker=ticker, date=last_date).update(
                update_values,
                synchronize_session=False,
            )
            session.commit()

        except Exception as e:
            logger.error(
                "Error in counting above/below SMAs for ticker %s: %s",
                ticker,
                e,
                exc_info=True,
            )

            session.rollback()  # good practice so the next ticker starts clean

    logger.info("Above/below SMAs counted.")
