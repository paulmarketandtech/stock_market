"""
workflow:
pull from DB opening prices from year beggining.
pull from DB closing prices from previous_day.
count returns
populate DB with returns
all in StockData
"""

from stock_market.db_hub.models import StockData


def count_returns(previous_date_price: str, after_date_price: str):

    return ((after_date_price - previous_date_price) / previous_date_price) * 100


def count_ytd_returns(session, last_date, ytd_date, ytd_tickers_list):
    for ticker in ytd_tickers_list:
        try:
            last_day_closing_price = (
                session.query(StockData)
                .filter(
                    StockData.ticker == ticker,
                    StockData.date == last_date,
                )
                .first()
            )
            if last_day_closing_price:
                year_opening_price = (
                    session.query(StockData)
                    .filter(
                        StockData.ticker == ticker,
                        StockData.date == ytd_date,
                    )
                    .first()
                )
            result = count_returns(
                year_opening_price.open, last_day_closing_price.close
            )
            print(f"ticker: {ticker}, ytd return: {result}")
        except Exception as e:
            print(f"error ytd_returns: {e}")


"""
def counting_and_populating_ytd_corrections_return(
    tickers: list[str], last_date: str, session: Session
):
    logging.info("YTD, corrections calculations started.")
    for ticker in tickers:
        last_day_closing_price = (
            session.query(StockData)
            .filter(
                StockData.ticker == ticker,
                StockData.date == last_date,
            )
            .first()
        )
        if last_day_closing_price:
            try:
                year_opening_price = (
                    session.query(StockData)
                    .filter(
                        StockData.ticker == ticker,
                        StockData.date == YTD_DATE,
                    )
                    .first()
                )

                ytd_return = (
                    (last_day_closing_price.close - year_opening_price.open)
                    / year_opening_price.open
                ) * 100
                session.query(StockData).filter_by(
                    ticker=ticker, date=last_date
                ).update({"ytd": ytd_return})

                session.commit()
            except AttributeError as e:
                logging.error(
                    f"Error with {ticker} in YTD calculations: {e}", exc_info=True
                )
"""
