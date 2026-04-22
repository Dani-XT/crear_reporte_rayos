import tkinter as tk

from src.core.app_context import AppContext

from src.ui.components.dialogs import show_info, show_error, show_warning
from src.ui.components.loading_dialog import LoadingDialog


class BaseFrame(tk.Frame):
    def __init__(self, master, context: AppContext, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.context = context

        self.paths = context.paths

        self._loading_dialog: LoadingDialog | None = None

    def show_info_message(self, title: str, message: str):
        show_info(self, title, message)

    def show_error_message(self, title: str, message: str):
        show_error(self, title, message)

    def show_warning_message(self, title: str, message: str):
        show_warning(self, title, message)

    def show_loading_message(self, title: str, message: str):
        if self._loading_dialog is not None and self._loading_dialog.winfo_exists():
            return

        self._loading_dialog = LoadingDialog(self, title, message)
        self.update_idletasks()
        self.update()

    def hide_loading_message(self):
        if self._loading_dialog is not None and self._loading_dialog.winfo_exists():
            self._loading_dialog.destroy()

        self._loading_dialog = None