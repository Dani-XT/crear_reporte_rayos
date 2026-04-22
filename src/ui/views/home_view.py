from typing import Protocol

from src.ui.views.base_view import BaseView

from src.models.forms import HomeFormData

class HomeView(BaseView, Protocol):
    def get_form_data() -> HomeFormData: ...
