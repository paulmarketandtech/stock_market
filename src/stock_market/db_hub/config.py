import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DB_PATH = BASE_DIR / "db_storage" / "historical_stock_data.db"

DATABASE_URL = os.getenv("DB_STORAGE_URL", f"sqlite:///{DB_PATH}")
