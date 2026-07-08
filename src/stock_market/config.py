from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
print(REPO_ROOT)

OHLC_DIR = REPO_ROOT / "data_lake" / "ohlc"
FUNDAMENTALS_DIR = REPO_ROOT / "data_lake" / "fundamentals"


def ohlc_file_path(run_date: date) -> Path:
    return OHLC_DIR / f"ohlc_{str(run_date).replace('-', '')}.parquet"


def fundamentals_file_path(run_date: date) -> Path:
    return FUNDAMENTALS_DIR / f"fundamentals_{str(run_date).replace('-', '')}.parquet"
