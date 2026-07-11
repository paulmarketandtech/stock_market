import pandas as pd
from sqlalchemy import select

from stock_market.db_hub.models import StockData
from stock_market.utils import (
    get_commodities_tickers,
    get_etfs_tickers,
    get_indexes_tickers,
)


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


def tg_create_DF_for_ytd_weekly_correction(session, previous_day: str):
    df_weekly_top, df_weekly_bottom = get_weekly_top_and_bottoms(
        session, previous_day, 30
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
