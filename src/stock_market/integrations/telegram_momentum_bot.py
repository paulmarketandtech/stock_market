# for now this file is just for checking if things work

from stock_market.db_hub.models import StockData
from stock_market.db_hub.session import get_session, init_db
from stock_market.utils import (
    get_commodities_tickers,
    get_etfs_tickers,
    get_indexes_tickers,
    get_large_cap_tickers,
    logging,
)

with get_session() as session:
    list_of_commodities = get_commodities_tickers(session)


def jap(session):
    stmt = select(StockData).where(StockData.ticker.in_(list_of_commodities))

    # Execute and get results
    etf_data = session.execute(stmt).all()

    print(etf_data)
    # Or fetch as list of objects
    results = session.scalars(stmt).all()
