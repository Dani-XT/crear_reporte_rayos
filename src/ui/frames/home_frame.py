import tkinter as tk
from tkinter import ttk, filedialog
from datetime import date


from src.ui.frames.base_frame import BaseFrame
from src.ui.components.widget import SafeDateEntry

from src.core.app_context import AppContext

from src.controller.home_controller import HomeController

from src.models.forms import HomeFormData

class HomeFrame(BaseFrame):
    def __init__(self, master, context: AppContext, page_controller: HomeController):
        super().__init__(master, context, bg="#72B2E6")
        self.controller: HomeController = page_controller

        self._load_assets()

        self._configure_styles()

        self._build_header()
        self._build_body()
        self._build_footer()

    def _load_assets(self):
        frame_img_dir = self.paths.img_dir / "home_frame"

        self.logo_img = tk.PhotoImage(file = frame_img_dir / "logo.png")
        self.fecha_img = tk.PhotoImage(file = frame_img_dir / "fecha.png")
        self.help_img = tk.PhotoImage(file = frame_img_dir / "helper.png")

        self.calendario_img = tk.PhotoImage(file = frame_img_dir / "calendario_frame.png")
        self.calendario_logo_img = tk.PhotoImage(file = frame_img_dir / "calendario.png")
        self.exportar_img = tk.PhotoImage(file = frame_img_dir / "exportar.png")

    def _build_header(self):
        header = tk.Frame(self, bg="white", height=97)
        header.place(x=0, y=0, relwidth=1)

        logo_label = tk.Label(header, image=self.logo_img, bg="white", bd=0)
        logo_label.place(x=10, y=15)

        tk.Label(header, text="Reporte Rayos de Cliniview", font=("Segoe UI", 17, "bold"), bg="white").place(x=219, y=30)
        help_btn = tk.Button(header, image=self.help_img, bg="white", activebackground="white", borderwidth=0, highlightthickness=0, relief="flat", cursor="hand2", command= self.controller.on_open_help)
        help_btn.place(x=520, y=38)

    def _build_body(self):
        body = tk.Frame(self, bg="#72B2E6")
        body.place(x=0, y=97, relwidth=1, relheight=1, height=-97)

        tk.Label(body, image=self.calendario_logo_img, bg="#72B2E6", bd=0).place(x=250, y=10)
        tk.Label(body, anchor="nw", text="Calendario", font=("OpenSansRoman Bold", 18), bg="#72B2E6", fg="white").place(x=300, y=15)

        calendario = tk.Label(body, image=self.calendario_img, bg="#72B2E6", bd=0)
        calendario.place(x=200, y=60)

        tk.Label(calendario, anchor="nw", text="Fecha Inicio", fg="#246FC6", font=("Segoe UI Semibold", 16 * -1, "bold"), bg="#FAFAFA").place(x=40, y=15)
        fecha_inicio_bg = tk.Label(calendario, image=self.fecha_img, bg="white", bd=0)
        fecha_inicio_bg.place(x=35, y=40)

        self.fecha_inicio = SafeDateEntry(fecha_inicio_bg, date_pattern="dd-mm-yyyy", bd=0, font=("Segoe UI", 10), style="Custom.DateEntry", maxdate=date.today(), state="readonly")
        self.fecha_inicio.place(x=30, y=5, width=180, height=22)

        tk.Label(calendario, anchor="nw", text="Fecha Fin", fg="#246FC6", font=("Segoe UI Semibold", 16 * -1, "bold"), bg="#FAFAFA").place(x=40, y=80)
        fecha_fin_bg = tk.Label(calendario, image=self.fecha_img, bg="white", bd=0)
        fecha_fin_bg.place(x=35, y=110)
        
        self.fecha_fin = SafeDateEntry(fecha_fin_bg, date_pattern="dd-mm-yyyy", bd=0, font=("Segoe UI", 10), style="Custom.DateEntry", maxdate=date.today(), state="readonly")
        self.fecha_fin.place(x=30, y=5, width=180, height=22)


    def _build_footer(self):
        footer = tk.Frame(self, bg="#72B2E6", height=45)
        footer.place(relx=0, rely=1, anchor="sw", relwidth=1, y=-10)

        enviar_btn = tk.Button(footer, image=self.exportar_img, bg="#72B2E6", activebackground="#72B2E6", borderwidth=0, highlightthickness=0, relief="flat", cursor="hand2", command=lambda: self.controller.on_export(self))
        enviar_btn.place(relx=0.5, rely=0.5, anchor="center")

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Custom.DateEntry",
            fieldbackground="#D3D3D3",
            background="#D3D3D3",
            foreground="#1F1F1F",
            borderwidth=0,
            relief="flat",
            arrowsize=14,
            arrowcolor="#246FC6",
            padding=0
        )

    def get_form_data(self):
        return HomeFormData(
            start_date = self.fecha_inicio.get_date(),
            end_date = self.fecha_fin.get_date(),
        )
    
    def ask_export_path(self, default_name: str) -> str | None:
        return filedialog.asksaveasfilename(
            title="Guardar reporte",
            defaultextension=".xlsx",
            initialfile=default_name,
            filetypes=[("Archivos Excel", "*.xlsx")],
        ) or None
    
    def schedule_task(self, delay_ms: int, callback):
        self.after(delay_ms, callback)
    
    
    
