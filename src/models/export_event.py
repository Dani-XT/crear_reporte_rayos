from dataclasses import dataclass
from pathlib import Path

@dataclass
class ExportStatusUpdate:
    message: str

@dataclass
class TempReportCreated:
    temp_path: Path

@dataclass
class ExportCompleted:
    final_path: Path

@dataclass
class ExportFailed:
    title: str
    message: str