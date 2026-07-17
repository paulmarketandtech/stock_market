from dotenv import load_dotenv

load_dotenv()
from stock_market.db_hub.models import MarketBreadth
from stock_market.db_hub.session import get_session


def delete_data_from_db(session):
    session.query(MarketBreadth).filter(MarketBreadth.id == 372).delete()


if __name__ == "__main__":

    with get_session() as session:
        delete_data_from_db(session)
