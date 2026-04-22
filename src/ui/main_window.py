import logging
import tkinter as tk
import ctypes

from src.core.app_context import AppContext

from src.ui.frames.home_frame import HomeFrame

from src.controller.home_controller import HomeController

from src.ui.components.dialogs import show_error

logger = logging.getLogger(__name__)

class MainWindow(tk.Tk):
    def __init__(self, app_context: AppContext):
        super().__init__()
        logger.info("Construyendo frames")

        self.app_context = app_context

        self.config = app_context.config
        self.paths = app_context.paths

        self.current_frame = None

        # Configuracion principal de ventanas
        self._configure_window()
        self._load_task_icon()

        self.ui_ready = False

        # Configuracion controllers
        self.home_controller = HomeController(app_context)

        # Configuracion principal del container
        self.container = tk.Frame(self, bg="#72B2E6")
        self.container.pack(fill="both", expand=True)

        # Construccion de frames
        self.frames = {}
        self._build_frames()
        self.show_frame("home")

        logger.info("Mostrando Frame")
        self.ui_ready = True

    def _configure_window(self):
        self.title(self.config.app_title)
        self.geometry(self.config.app_size)
        self.resizable(False, False)

    def _load_task_icon(self):
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.config.app_id)
        except Exception:
            pass
        try:
            self.iconbitmap(str(self.paths.icon_dir / "favicon.ico"))
        except Exception:
            pass

    def _build_frames(self):
        self.frames["home"] = HomeFrame(self.container, self.app_context, self.home_controller)

        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_frame(self, name: str):
        self.current_frame = self.frames[name]
        self.current_frame.tkraise()
        return self.current_frame
    
    def is_ui_ready(self) -> bool:
        return self.ui_ready and self.winfo_exists()
    
    def show_global_error(self, title: str, message: str):
        if self.current_frame is not None and self.current_frame.winfo_exists():
            self.current_frame.show_error_message(title, message)
        else:
            show_error(self, title, message)



