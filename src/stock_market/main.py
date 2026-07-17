import argparse
import logging
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from stock_market.db_hub.session import init_db  # noqa: E402
from stock_market.pipelines import daily_momentum, extra_metrics  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(
            Path(__file__).resolve().parents[2] / "logs" / "stock_market.log"
        ),
        logging.StreamHandler(),  # also print to console
    ],
)

logger = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("pipeline", choices=["daily", "extra"])
    args = parser.parse_args()

    if args.pipeline == "daily":
        print("dailyaaa")
        daily_momentum.start_daily_momentum()
    elif args.pipeline == "extra":
        print("extraeee")
        extra_metrics.start_daily_extra_metrics()


if __name__ == "__main__":
    init_db()
    main()
