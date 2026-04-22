import os
import logging
from pathlib import Path

from src.core.app_context import AppContext

from src.utils.exceptions import HelpFileNotFoundError, HelpFileOpenError

from src.controller.export_controller import ExportController

from src.ui.views.home_view import HomeView

logger = logging.getLogger(__name__)

class HomeController:
    def __init__(self, app_context: AppContext):
        self.context = app_context

        self.export_controller = ExportController()

        self.paths = app_context.runtime

    def on_open_help(self):
        self._open_help_file(self.paths.reporte_readme_file)

    def on_export(self, view: HomeView):
        data = view.get_form_data()
        view.show_loading_message("Generando", "Generando Excel...")
        try:
            self.export_controller.start(data)
            view.show_info_message("Excel Generado", "Se genero el excel correctamente...")
        finally:
            view.hide_loading_message()
            

    def _open_help_file(self, help_file: Path) -> None:
        if not help_file.exists():
            raise HelpFileNotFoundError("No se encontró el archivo de ayuda.")

        try:
            os.startfile(help_file)
        except Exception as e:
            raise HelpFileOpenError(f"Ocurrió un error al abrir el archivo:\n{e}") from e
