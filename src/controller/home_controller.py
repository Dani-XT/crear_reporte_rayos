import os
import logging
from pathlib import Path

from src.core.app_context import AppContext

logger = logging.getLogger(__name__)

class HomeController:
    def __init__(self, app_context: AppContext):
        self.context = app_context

        self.paths = app_context.runtime

    def on_open_help(self):
        print("Hola")

    def on_export(self):
        print("Enviar")