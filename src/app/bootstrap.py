import logging
import shutil

from src.core.logger import setup_logging
from src.core.app_context import AppContext, build_app_context
from src.core.app_context_store import set_app_context


logger = logging.getLogger(__name__)

def ensure_runtime_dirs(app_context: AppContext) -> None:
    runtime_dirs = [
        app_context.runtime.data_dir,
        app_context.runtime.logs_dir,
        app_context.runtime.templates_dir,
    ]

    for directory in runtime_dirs:
        directory.mkdir(parents=True, exist_ok=True)

def bootstrap_app() -> AppContext:
    app_context = build_app_context()
    set_app_context(app_context)

    ensure_runtime_dirs(app_context)

    setup_logging(app_context)

    return app_context

    