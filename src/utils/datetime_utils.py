import polars as pl

def split_fecha_hora_pl(df: pl.DataFrame) -> pl.DataFrame:
    
    source_col = "Fecha"
    fecha_col = "Fecha"
    hora_col = "Hora"

    # Si viene como string, intenta convertirlo a datetime
    if df.schema[source_col] == pl.Utf8:
        df = df.with_columns(
            pl.col(source_col).str.to_datetime(strict=False)
        )

    df = df.with_columns([
        pl.col(source_col).dt.strftime("%d-%m-%Y").alias(fecha_col),
        pl.col(source_col).dt.strftime("%H:%M:%S").alias(hora_col),
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