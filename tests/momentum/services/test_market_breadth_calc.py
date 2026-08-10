from datetime import date

from stock_market.db_hub.models import StockData
from stock_market.momentum.services.market_breadth_calc import (
    above_below_sma_calculations,
)


def test_above_below_sma_calculations(db_session):
    test_date = date(2024, 6, 1)

    db_session.add_all(
        [
            StockData(
                ticker="AAPL",
                date=test_date,
                close=150,
                high=111,
                low=111,
                open=111,
                ma50=140,
                ma100=145,
                ma200=160,
            ),
            StockData(
                ticker="MSFT",
                date=test_date,
                close=100,
                high=111,
                low=111,
                open=111,
                ma50=None,
                ma100=90,
                ma200=80,
            ),
        ]
    )
    db_session.commit()

    above_below_sma_calculations(db_session, test_date, ["AAPL", "MSFT"])

    aapl = db_session.query(StockData).filter_by(ticker="AAPL", date=test_date).one()
    assert aapl.ma50_above is True  # 150 > 140
    assert aapl.ma100_above is True  # 150 > 145
    assert aapl.ma200_above is False  # 150 < 160

    msft = db_session.query(StockData).filter_by(ticker="MSFT", date=test_date).one()
    assert msft.ma50_above is False  # ma50 is None -> False, per your case()
    assert msft.ma100_above is True  # 100 > 90
    assert msft.ma200_above is True  # 100 > 80
