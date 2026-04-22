from __future__ import annotations

import logging
import pyodbc
from datetime import date
import polars as pl

from src.core.app_context_store import get_app_config

from src.utils.exceptions import DataBaseConnectionError

class DatabaseService:
    def __init__(self):
        config = get_app_config()
        self.connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={config.app_sql_server};"
            f"DATABASE={config.app_sql_database};"
            f"UID={config.app_sql_username};"
            f"PWD={config.app_sql_password};"
        )

        self.test_connection()

    def test_connection(self) -> bool:
        try:
            with pyodbc.connect(self.connection_string) as conn:
                logging.info("Conexión exitosa a la base de datos.")
            return True
        except Exception as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            raise DataBaseConnectionError("No se logro conectar a la Base de Datos")
        
    def fetch_report_data(self, start_date: date, end_date: date) -> tuple[list[tuple], list[str]]:
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        query = """
        SELECT [LogGUID] AS ID,
            [LogTime] AS Fecha,
            [UserName] AS Usuario,
            [WorkstationName] AS Maquina,
            [LogAction] AS Accion,
            [Object],
            [Description] AS Descripcion
        FROM [CliniView].[dbo].[PIDB_Log]
        WHERE Description IS NOT NULL
        AND CAST(LogTime AS DATE) >= CAST(? AS DATE)
        AND CAST(LogTime AS DATE) <= CAST(? AS DATE)
        ORDER BY LogTime ASC
        """

        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (start_date_str, end_date_str))
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [tuple(row) for row in rows]

        return data, columns