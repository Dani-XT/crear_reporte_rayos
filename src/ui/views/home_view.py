from typing import Protocol, Callable

from src.ui.views.base_view import BaseView

from src.models.forms import HomeFormData

class HomeView(BaseView, Protocol):
    def get_form_data() -> HomeFormData: ...
    def ask_export_path(self, default_name: str) -> str | None: ...
    def schedule_task(self, delay_ms: int, callback: Callable[[], None]) -> None: ...
