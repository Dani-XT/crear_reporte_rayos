from src.app.env import IS_DEV, IS_PROD, APP_NAME
from src.app.paths import PROJECT_DIR

from pathlib import Path
import os

def _get_appdata_dir() -> Path:
    local_appdata = os.environ.get("LOCALAPPDATA")

    if local_appdata:
        return Path(local_appdata)
    
    return Path.home() / "AppData" / "Local"


if IS_DEV:
    DATA_DIR = PROJECT_DIR / "storages"

if IS_PROD:
    DATA_DIR = _get_appdata_dir() / APP_NAME

CACHE_DIR = DATA_DIR / "cache"

LOGS_DIR = DATA_DIR / "logs"
TEMPLATE_DIR = DATA_DIR / "templates"
REPORTE_README_FILE = TEMPLATE_DIR / "reporte_readme.html"

