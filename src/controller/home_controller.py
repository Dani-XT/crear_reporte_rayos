import os
import logging
from pathlib import Path

from src.core.app_context import AppContext

from src.controller.export_controller import ExportController

from src.ui.views.home_view import HomeView

from src.models.export_event import (
    ExportStatusUpdate,
    TempReportCreated,
    ExportCompleted,
    ExportFailed
)

from src.utils.exceptions import HelpFileNotFoundError, HelpFileOpenError, DateRangeError

logger = logging.getLogger(__name__)

class HomeController:
    def __init__(self, app_context: AppContext):
        self.context = app_context
        self.export_controller = ExportController()
        self.paths = app_context.runtime

        self.view: HomeView | None = None

    def on_open_help(self):
        self._open_help_file(self.paths.reporte_readme_file)

    def on_export(self, view: HomeView):
        data = view.get_form_data()
        self.view = view

        if data.start_date > data.end_date:
            raise DateRangeError("La fecha de inicio no puede ser mayor que la fecha de fin")
        
        self.view.show_loading_message("Generando", "Generando Excel...")

        self.export_controller.build_report(data=data)
        self._poll_export_events()

    def _poll_export_events(self) -> None:
        if self.view is None:
            return
        
        while True:
            event = self.export_controller.get_next_event()
            if event is None:
                break

            self._handle_export_event(event)
        
        if self.export_controller.has_pending_work():
            self.view.schedule_task(100, self._poll_export_events)

    def _handle_export_event(self, event: object) -> None:
        if self.view is None:
            return

        if isinstance(event, ExportStatusUpdate):
            # si después quieres actualizar el loading dialog con texto dinámico,
            # aquí es donde lo haces
            return

        if isinstance(event, TempReportCreated):
            self.view.hide_loading_message()

            final_path = self.view.ask_export_path(event.temp_path.name)
            if not final_path:
                self.view.show_warning_message(
                    "Exportación cancelada",
                    "No se seleccionó una ruta para guardar el archivo."
                )
                return

            self.view.show_loading_message("Guardando", "Copiando Excel...")
            self.export_controller.copy_report(event.temp_path, final_path)
            self._poll_export_events()
            return

        if isinstance(event, ExportCompleted):
            self.view.hide_loading_message()
            self.view.show_info_message(
                "Éxito",
                f"Reporte exportado correctamente en:\n{event.final_path}"
            )
            return

        if isinstance(event, ExportFailed):
            self.view.hide_loading_message()
            self.view.show_error_message(event.title, event.message)
            return

        logger.warning("Evento de exportación no reconocido: %r", event)
