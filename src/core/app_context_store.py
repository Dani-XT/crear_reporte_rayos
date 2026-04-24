from __future__ import annotations

from src.core.app_context import AppContext, AppConfig, AppPaths, AppRuntimePaths

_APP_CONTEXT: AppContext | None = None

def set_app_context(app_context: AppContext) -> None:
    global _APP_CONTEXT
    _APP_CONTEXT = app_context

def get_app_context() -> AppContext:
    if _APP_CONTEXT is None:
        raise RuntimeError("AppContext no ha sido inicializado")
    return _APP_CONTEXT

def get_app_config() -> AppConfig:
    return get_app_context().config

def get_app_paths() -> AppPaths:
    return get_app_context().paths

def get_runtime_paths() -> AppRuntimePaths:
    return get_app_context().runtime

def clear_app_context() -> None:
    global _APP_CONTEXT
    _APP_CONTEXT = None

    
