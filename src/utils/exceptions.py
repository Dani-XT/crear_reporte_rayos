# src/utils/exceptions.py

class AppError(Exception):
    default_title = "Error"
    default_level = "error"

    def __init__(self, message: str | None = None):
        self.message = message or "Ocurrió un error inesperado."
        super().__init__(self.message)

    @property
    def title(self) -> str:
        return self.default_title

    @property
    def level(self) -> str:
        return self.default_level

    def __str__(self) -> str:
        return self.message

class InternalError(AppError):
    default_title = "Ocurrio un error inesperado."

class ExportError(AppError):
    default_title = "Ocurrio un error al exportar"


# =========================
# EXCEL
# =========================
class ExcelError(AppError):
    default_title = "Error con el Excel"


# =========================
# ARCHIVOS README
# =========================
class TemplateError(AppError):
    default_title = "Error con la plantilla"


class TemplateNotFoundError(TemplateError):
    default_title = "Plantilla no encontrada"

class TemplateNotFoundError(TemplateError):
    default_title = "Plantilla no encontrada"
    
class HelpFileError(AppError):
    default_title = "Error con la ayuda"


class HelpFileNotFoundError(HelpFileError):
    default_title = "Archivo no encontrado"


class HelpFileOpenError(HelpFileError):
    default_title = "Error al abrir ayuda"

class DateRangeError(AppError):
    default_title = "Rango de fechas invalido"

class DataBaseConnectionError(AppError):
    default_title = "Error conectando a la Base de Datos"