from sqlalchemy.orm import Session

from stock_market.integrations.tradingview_client import sma_calculations
from stock_market.momentum.services.charts_market_breadth import chart_managing
from stock_market.momentum.services.standard_returns.market_breadth_counting import (
    counting_above_below_SMAs,
)
from stock_market.utils import (
    creating_list_of_tickers_nasdaq,
    creating_list_of_tickers_nyse,
)


def market_breadth_manager(
    session: Session, previous_day, list_of_tickers: list[str]
) -> None:

    list_of_tickers_nasdaq = creating_list_of_tickers_nasdaq(session)
    list_of_tickers_nyse = creating_list_of_tickers_nyse(session)

    sma_calculations(
        session,
        previous_day,
        list_of_tickers,
        list_of_tickers_nasdaq,
        list_of_tickers_nyse,
    )

    counting_above_below_SMAs(session, previous_day, list_of_tickers)
    chart_managing(session, previous_day)
