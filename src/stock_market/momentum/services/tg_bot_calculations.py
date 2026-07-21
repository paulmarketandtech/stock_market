from datetime import date

import pandas as pd
from sqlalchemy import select

from stock_market.db_hub.models import StockData
from stock_market.utils import (
    get_commodities_tickers,
    get_etfs_tickers,
    get_indexes_tickers,
)


def get_weekly_top_and_bottoms(session, previous_day: date, no_of_results: int):
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


def get_ytd_top_and_bottoms(session, previous_day: date, no_of_results: int):
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


def get_correction_top_and_bottoms(session, previous_day: date, no_of_results: int):
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


def tg_create_DF_for_ytd_weekly_correction(session, previous_day: date):
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


# TODO: to be deleted?
def get_indexes_returns(session, previous_day: date):
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


# TODO: to be deleted?
def get_commodities_returns(session, previous_day: date):
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


# TODO: to be deleted?
def get_etfs_returns(session, previous_day: date):
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


def get_returns_for_selected_tickers(
    session, previous_day: date, list_of_tickers: list[str]
) -> pd.DataFrame:
    """stock_data stores all tickers data.
    User provides list of any tickers
    and the func returns last week returns
    for given list_of_tickers"""

    query_result = (
        select(StockData)
        .where(StockData.ticker.in_(list_of_tickers))
        .filter(StockData.date == previous_day)
    )
    results = session.scalars(query_result).all()

    output = []
    for r in results:
        output.append((r.ticker, r.weekly_change))

    df = pd.DataFrame(output, columns=["ticker", "weekly_returns"])
    df.dropna(inplace=True)
    df.sort_values(by="weekly_returns", inplace=True, ascending=False)

    return df


def get_DFs_for_etfs_tickers(session, previous_day: date) -> list[pd.DataFrame]:
    list_of_indexes = get_indexes_tickers(session)
    list_of_commodities = get_commodities_tickers(session)
    list_of_etfs = get_etfs_tickers(session)

    df_indexes = get_returns_for_selected_tickers(
        session, previous_day, list_of_indexes
    )
    df_commodities = get_returns_for_selected_tickers(
        session, previous_day, list_of_commodities
    )
    df_etfs = get_returns_for_selected_tickers(session, previous_day, list_of_etfs)

    return [df_indexes, df_commodities, df_etfs]
