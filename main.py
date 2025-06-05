import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import pandas as pd
import pyodbc
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

import logging

logging.basicConfig(
    filename="reporte.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class ReportGenerator:
    def __init__(self):
        self.connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={os.getenv('SQL_SERVER')};"
            f"DATABASE={os.getenv('SQL_DATABASE')};"
            f"UID={os.getenv('SQL_USERNAME')};"
            f"PWD={os.getenv('SQL_PASSWORD')};"
        )
        # La línea del engine ya no la necesitamos si usamos pyodbc directamente
        # self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={self.connection_string}")

    def probar_conexion(self):
        try:
            # Intenta hacer una conexión simple
            with pyodbc.connect(self.connection_string) as conn:
                print("Conexión exitosa a la base de datos")
            return True
        except Exception as e:
            print(f"Error al conectar a la base de datos: {str(e)}")
            return False

    # ===> ESTE método DEBE ESTAR AL MISMO NIVEL QUE __init__ y probar_conexion <===
    # Asegúrate de que la línea de abajo empiece con la misma cantidad de espacios
    # que 'def __init__(self):' y 'def probar_conexion(self):'
    def generar_excel(self, ruta, fecha_inicio, fecha_fin):
        try:
            # Convertir las fechas a string en formato SQL Server
            fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
            fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')

            query = """
            SELECT
                pt.PatientID,
                pt.FirstName,
                pt.LastName,
                st.StudyTime,
                iser.SeriesTime,
                img.ImageTime,
                img.ImageGUID,
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
                st.StudyTime BETWEEN ? AND ?
            ORDER BY
                pt.LastName, st.StudyTime, iser.SeriesTime, img.ImageTime;
            """

            # Ejecutar la consulta usando pyodbc directamente
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (fecha_inicio_str, fecha_fin_str))
                columns = [column[0] for column in cursor.description]
                data = cursor.fetchall()

                # Crear DataFrame y guardar en Excel
                df = pd.DataFrame.from_records(data, columns=columns)
                df.to_excel(ruta, index=False)
                logging.info(f"Reporte generado exitosamente. Rango: {fecha_inicio} - {fecha_fin}. Ruta: {ruta}")

        except Exception as e:
            print(f"Error en la conexión: {str(e)}")
            logging.error(f"Error al generar el reporte: {e}")
            raise


class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Reportes CliniView")
        self.root.geometry("500x350")
        self.reporte = ReportGenerator()
        
        # Probar conexión al iniciar
        if not self.reporte.probar_conexion():
            messagebox.showerror("Error de Conexión", 
                               "No se pudo conectar a la base de datos.\n"
                               "Por favor verifica la configuración en el archivo .env")

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
