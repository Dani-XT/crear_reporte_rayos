import logging
from queue import Queue, Empty
from threading import Thread
from collections.abc import Callable
from pathlib import Path

from src.models.forms import HomeFormData
from src.models.export_event import (
    ExportStatusUpdate,
    TempReportCreated,
    ExportCompleted,
    ExportFailed,
)
from src.services.export_service import ExportService

logger = logging.getLogger(__name__)


class ExportController:
    def __init__(self):
        self.export_service = ExportService()
        self._queue = Queue()
        self._worker: Thread | None = None
        self._is_running = False

    def build_report(self, data: HomeFormData) -> None:
        task = lambda: self.export_service.build_report(data, emit=self._queue.put)
        self._start_worker(task)

    def copy_report(self, temp_path: Path, final_path: str) -> None:
        task = lambda: self.export_service.copy_report(temp_path, final_path, emit=self._queue.put)
        self._start_worker(task)

    def _start_worker(self, task: Callable[[], None]) -> None:
        if self._is_running:
            raise RuntimeError("Ya existe una exportación en curso.")

        self._queue = Queue()
        self._is_running = True
        self._worker = Thread(target=self._run_worker, args=(task,), daemon=True)
        self._worker.start()

    def _run_worker(self, task: Callable[[], None]) -> None:
        try:
            task()
        except Exception as e:
            logger.exception("Error no controlado en exportación")
            self._queue.put(ExportFailed("Error al exportar", str(e)))
        finally:
            self._is_running = False
            self._worker = None

    def get_next_event(self):
        try:
            return self._queue.get_nowait()
        except Empty:
            return None

    def has_pending_work(self) -> bool:
        return self._is_running or not self._queue.empty()