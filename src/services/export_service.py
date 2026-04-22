import logging

from src.services.database_service import DatabaseService
from src.services.excel_service import ExcelService

from src.models.forms import HomeFormData

import polars as pl

logger = logging.getLogger(__name__)


class ExportService:
    def __init__(self):
        self.excel_service = ExcelService()

    def start_consulta(self, data: HomeFormData):
        print("dentro de start consulta")
        db_service = DatabaseService()
    
        data, columns = db_service.fetch_report_data(data.start_date, data.end_date)
        
        df = self.excel_service.convert_to_polars(data, columns)
        
        self.excel_service.load_to_excel(df)
        logger.info("Excel creado")