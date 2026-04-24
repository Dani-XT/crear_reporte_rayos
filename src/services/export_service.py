import logging
from pathlib import Path
from collections.abc import Callable

from src.services.database_service import DatabaseService
from src.services.excel_service import ExcelService

from src.models.forms import HomeFormData
from src.models.export_event import (
    ExportStatusUpdate,
    TempReportCreated,
    ExportCompleted,
)

logger = logging.getLogger(__name__)

class ExportService:
    def __init__(self):
        self.excel_service = ExcelService()

    def build_report(self, data: HomeFormData, emit: Callable[[object], None]) -> None:
        emit(ExportStatusUpdate("Consultando base de datos..."))
        
        db_service = DatabaseService()
        data, columns = db_service.fetch_report_data(data.start_date, data.end_date)
        
        emit(ExportStatusUpdate("Transformando datos..."))

        df = self.excel_service.convert_to_polars(data, columns)
        
        emit(ExportStatusUpdate("Creando archivo temporal..."))

        tmp_path = self.excel_service.save_temp_excel(df)
        logger.info("Excel temporal creado: %s", tmp_path)

        emit(TempReportCreated(tmp_path))

        return tmp_path

    def copy_report(self, temp_path: Path, final_path: str, emit: Callable[[object], None]) -> None:
        emit(ExportStatusUpdate("Copiando archivo al destino final..."))

        result = self.excel_service.copy_to_destination(temp_path, final_path)
        logger.info("Excel copiado al destino final: %s", result)

        emit(ExportCompleted(result))