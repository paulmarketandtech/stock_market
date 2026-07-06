from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
print(REPO_ROOT)

OHCL_DIR = REPO_ROOT / "data_lake" / "ohcl"
FUNDAMENTALS_DIR = REPO_ROOT / "data_lake" / "fundamentals"


def ohcl_file_path(run_date: date) -> Path:
    return OHCL_DIR / f"ohcl_{str(run_date).replace('-', '')}.parquet"


def fundamentals_file_path(run_date: date) -> Path:
    return FUNDAMENTALS_DIR / f"fundamentals_{str(run_date).replace('-', '')}.parquet"
