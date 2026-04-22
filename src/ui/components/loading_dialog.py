import tkinter as tk

from src.core.app_context_store import get_app_paths

class LoadingDialog(tk.Toplevel):
    def __init__(self, master, title: str, message: str):
        super().__init__(master)

        paths = get_app_paths().icon_dir

        self.withdraw()
        self.title(title)
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.iconbitmap(paths / "favicon.ico")


        self._angle = 0
        self._job = None

        self._build_ui(message)

        self.update_idletasks()

        x = master.winfo_rootx() + (master.winfo_width() // 2) - (self.winfo_reqwidth() // 2)
        y = master.winfo_rooty() + (master.winfo_height() // 2) - (self.winfo_reqheight() // 2)
        self.geometry(f"+{x}+{y}")

        self.deiconify()
        self.focus_force()

        self._animate()

    def _build_ui(self, message: str):
        container = tk.Frame(self, bg="#1e1e1e")
        container.pack(fill="both", expand=True, padx=25, pady=20)

        self.canvas = tk.Canvas(
            container,
            width=50,
            height=50,
            bg="#1e1e1e",
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(pady=(0, 12))

        self.arc = self.canvas.create_arc(
            5, 5, 45, 45,
            start=0,
            extent=300,
            style="arc",
            outline="#FF4D4D",
            width=5
        )

        tk.Label(
            container,
            text=message,
            bg="#1e1e1e",
            fg="white",
            font=("Segoe UI", 11)
        ).pack()

    def _animate(self):
        self._angle = (self._angle + 12) % 360
        self.canvas.itemconfig(self.arc, start=self._angle)
        self._job = self.after(30, self._animate)

    def destroy(self):
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None
        super().destroy()