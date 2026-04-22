import polars as pl

from src.utils.text_utils import reorder_nombre, format_rut, expand_fuente

class ExcelService:
    
    def convert_to_polars(self, data, columns):
        df = pl.DataFrame(data, schema=columns, orient="row")

        df = df.with_columns([
            pl.col("Descripcion").str.extract(r'PNa="([^"]*)"', 1).alias("Nombre"),
            pl.col("Descripcion").str.extract(r'PID="([^"]*)"', 1).alias("RUT"),
            pl.col("Descripcion").str.extract(r'Mod="([^"]*)"', 1).alias("Modo"),
            pl.col("Descripcion").str.extract(r'Src="([^"]*)"', 1).alias("Fuente"),
            pl.col("Descripcion").str.extract(r'IGu="([^"]*)"', 1).alias("IGu"),
        ]).drop("Descripcion")

        df = df.with_columns([
            pl.col("Fecha").dt.strftime("%d-%m-%Y").alias("Fecha"),
            pl.col("Fecha").dt.strftime("%H:%M:%S").alias("Hora"),
        ])

        df = df.with_columns([
            pl.col("Nombre").map_elements(reorder_nombre, return_dtype=pl.Utf8).alias("Nombre"),
            pl.col("RUT").map_elements(format_rut, return_dtype=pl.Utf8).alias("RUT"),
            pl.col("Fuente").map_elements(expand_fuente, return_dtype=pl.Utf8).alias("Fuente"),
        ])

        return df.select([
            "ID",
            "Fecha",
            "Hora",
            "Usuario",
            "Maquina",
            "Accion",
            "Object",
            "Nombre",
            "RUT",
            "Modo",
            "Fuente",
            "IGu",
        ])

    def load_to_excel(self, df: pl.DataFrame):
        df.write_excel("prueba.xlsx")