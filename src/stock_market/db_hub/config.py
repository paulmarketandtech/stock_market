import os
from pathlib import Path

DATABASE_URL = os.getenv("DB_STORAGE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DB_STORAGE_URL is not set. Add it to your .env file, "
        "e.g. DB_STORAGE_URL=sqlite:////srv/apps/stock_market/db_storage/centraldb.db"
    )
