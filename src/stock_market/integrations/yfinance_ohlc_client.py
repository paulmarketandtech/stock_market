import logging
import time
from datetime import date

import pandas as pd
import yfinance as yf

BATCH_SIZE = 250
SLEEP_BETWEEN = 10


logger = logging.getLogger(__name__)

# ====================== 1. OHLCV Download ======================

COLUMN_RENAME = {
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume",
}


def fetch_ohlc_batch(tickers: list[str], previous_day: date) -> pd.DataFrame:
    """Download OHLC for a batch of tickers, return long format:
    [ticker, date, open, high, low, close, volume]
    """
    raw = yf.download(
        tickers=tickers,
        start=previous_day,
        end=date.today(),
        group_by="ticker",
        auto_adjust=False,
        threads=False,
        progress=False,
    )

    frames = []
    if len(tickers) == 1:
        df = raw.copy()
        if not df.dropna(how="all").empty:
            df["ticker"] = tickers[0]
            frames.append(df)
    else:
        for ticker in tickers:
            if ticker not in raw.columns.get_level_values(0):
                logger.warning("No data returned for %s", ticker)
                continue
            df = raw[ticker].copy()
            if df.dropna(how="all").empty:
                logger.warning("Empty data for %s", ticker)
                continue
            df["ticker"] = ticker
            frames.append(df)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames).reset_index().rename(columns=COLUMN_RENAME)
    combined = combined.dropna(subset=["date", "open", "high", "low", "close"])
    return combined[["ticker", "date", "open", "high", "low", "close", "volume"]]


def download_all_ohlc(
    tickers: list[str],
    previous_day: date,
    batch_size: int = BATCH_SIZE,
    sleep_seconds: float = SLEEP_BETWEEN,
) -> tuple[pd.DataFrame, list[str]]:
    """Returns (combined_dataframe, list_of_tickers_with_no_data)."""
    all_frames = []
    missing: list[str] = []

    for i in range(0, len(tickers), batch_size):
        batch = tickers[i : i + batch_size]
        logger.info("Fetching OHLC batch %d-%d of %d", i, i + len(batch), len(tickers))

        try:
            df = fetch_ohlc_batch(batch, previous_day)
        except Exception:
            logger.exception("Batch failed entirely: %s", batch)
            missing.extend(batch)
            time.sleep(sleep_seconds)
            continue

        if df.empty:
            missing.extend(batch)
        else:
            fetched = set(df["ticker"].unique())
            missing.extend(set(batch) - fetched)
            all_frames.append(df)

        time.sleep(sleep_seconds)

    if missing:
        logger.warning("Missing OHLC for %d/%d tickers", len(missing), len(tickers))
        print("Missing OHLC for %d/%d tickers", len(missing), len(tickers))

    combined = (
        pd.concat(all_frames, ignore_index=True) if all_frames else pd.DataFrame()
    )
    return combined, missing


# TODO: not in use? to be deleted
# ====================== 2. .info (Fundamentals) ======================
def fetch_fundamentals(ticker: str) -> dict:
    info = yf.Ticker(ticker).info
    return {
        "ticker": ticker,
        "market_cap": info.get("marketCap"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        "beta_value": info.get("beta"),
        "full_exchange_name": info.get("fullExchangeName"),
    }


def download_all_fundamentals(
    tickers: list[str],
    sleep_seconds: float = 1.0,
) -> tuple[pd.DataFrame, list[str]]:
    rows = []
    missing: list[str] = []

    for i, ticker in enumerate(tickers, start=1):
        try:
            rows.append(fetch_fundamentals(ticker))
        except Exception:
            logger.exception("Failed to fetch fundamentals for %s", ticker)
            missing.append(ticker)

        if i % 10 == 0:
            logger.info("Fundamentals progress: %d/%d", i, len(tickers))

        time.sleep(sleep_seconds)

    if missing:
        logger.warning(
            "Missing fundamentals for %d/%d tickers", len(missing), len(tickers)
        )

    return pd.DataFrame(rows), missing
