import threading
import logging

from src.services.export_service import ExportService

from src.models.forms import HomeFormData

logger = logging.getLogger(__name__)

class ExportController:
    def __init__(self):
        self.export_service = ExportService()

    def start(self, data: HomeFormData):
        self.export_service.start_consulta(data)

    