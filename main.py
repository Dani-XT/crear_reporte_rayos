import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import pandas as pd
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()


class ReportGenerator:
    def __init__(self):
        self.connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={os.getenv('SQL_SERVER')};"
            f"DATABASE={os.getenv('SQL_DATABASE')};"
            f"UID={os.getenv('SQL_USERNAME')};"
            f"PWD={os.getenv('SQL_PASSWORD')};"
        )

    def generar_excel(self, ruta, fecha_inicio, fecha_fin):
        query = f"""
        SELECT 
            pt.PatientID,
            pt.FirstName,
            pt.LastName,
            st.StudyDate,
            iser.SeriesTime,
            img.ImageTime,
            img.ImageGUID,
            img.Modality,
            img.SeriesGUID
        FROM 
            PIDB_Patient pt
        JOIN 
            PIDB_Study st ON pt.PatientGUID = st.PatientGUID
        JOIN 
            PIDB_ImageSeries iser ON st.StudyGUID = iser.StudyGUID
        JOIN 
            PIDB_Image img ON iser.SeriesGUID = img.SeriesGUID
        WHERE 
            st.StudyDate BETWEEN ? AND ?
        ORDER BY 
            pt.LastName, st.StudyDate, iser.SeriesTime, img.ImageTime;
        """
        with pyodbc.connect(self.connection_string) as conn:
            df = pd.read_sql(query, conn, params=[fecha_inicio, fecha_fin])
            df.to_excel(ruta, index=False)


class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Reportes CliniView")
        self.root.geometry("500x350")
        self.reporte = ReportGenerator()

        self.build_gui()

    def build_gui(self):
        tk.Label(self.root, text="Nombre del archivo:").pack(pady=5)
        self.nombre_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.nombre_var, width=40).pack()

        tk.Label(self.root, text="Desde (fecha inicio):").pack(pady=5)
        self.fecha_inicio = DateEntry(self.root, date_pattern="yyyy-mm-dd")
        self.fecha_inicio.pack()

        tk.Label(self.root, text="Hasta (fecha fin):").pack(pady=5)
        self.fecha_fin = DateEntry(self.root, date_pattern="yyyy-mm-dd")
        self.fecha_fin.pack()

        tk.Button(self.root, text="Generar Reporte", command=self.generar).pack(pady=20)

        self.barra = ttk.Progressbar(self.root, orient="horizontal", length=350, mode="determinate")
        self.barra.pack(pady=10)

    def generar(self):
        nombre = self.nombre_var.get().strip()
        if not nombre:
            messagebox.showwarning("Falta nombre", "Debes ingresar un nombre para el archivo.")
            return

        carpeta = filedialog.askdirectory(title="Selecciona carpeta de destino")
        if not carpeta:
            return

        ruta = os.path.join(carpeta, f"{nombre}.xlsx")
        fecha_inicio = self.fecha_inicio.get_date()
        fecha_fin = self.fecha_fin.get_date()

        try:
            self.barra["value"] = 25
            self.root.update_idletasks()

            self.reporte.generar_excel(ruta, fecha_inicio, fecha_fin)

            self.barra["value"] = 100
            messagebox.showinfo("Éxito", f"Reporte guardado en:\n{ruta}")
        except Exception as e:
            self.barra["value"] = 0
            messagebox.showerror("Error", f"No se pudo generar el reporte:\n{e}")


class Main:
    def __init__(self):
        self.root = tk.Tk()
        AppGUI(self.root)
        self.root.mainloop()


if __name__ == "__main__":
    Main()
