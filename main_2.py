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
            logging.info("Intentando conectar a la base de datos...")
            # Intenta hacer una conexión simple
            with pyodbc.connect(self.connection_string) as conn:
                print("Conexión exitosa a la base de datos")
                logging.info("Conexión exitosa a la base de datos.")
            return True
        except Exception as e:
            print(f"Error al conectar a la base de datos: {str(e)}")
            logging.error(f"Error al conectar a la base de datos: {e}")
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
            SELECT [LogGUID] AS ID
                ,[LogTime] AS Fecha
                ,[UserName] AS Usuario
                ,[WorkstationName] AS Maquina
                ,[LogAction] AS Accion
                ,[Object]
                ,
            CASE 
                WHEN CHARINDEX('PNa="', Description) > 0 
                THEN SUBSTRING(
                Description,
                CHARINDEX('PNa="', Description) + 5,
                CHARINDEX('"', Description, CHARINDEX('PNa="', Description) + 5) - CHARINDEX('PNa="', Description) - 5
                ) 
                ELSE NULL 
            END AS Nombre,

            CASE 
                WHEN CHARINDEX('PID="', Description) > 0 
                THEN SUBSTRING(
                Description,
                CHARINDEX('PID="', Description) + 5,
                CHARINDEX('"', Description, CHARINDEX('PID="', Description) + 5) - CHARINDEX('PID="', Description) - 5
                ) 
                ELSE NULL 
            END AS RUT,

            CASE 
                WHEN CHARINDEX('Mod="', Description) > 0 
                THEN SUBSTRING(
                Description,
                CHARINDEX('Mod="', Description) + 5,
                CHARINDEX('"', Description, CHARINDEX('Mod="', Description) + 5) - CHARINDEX('Mod="', Description) - 5
                ) 
                ELSE NULL 
            END AS Modo,

            CASE 
                WHEN CHARINDEX('Src="', Description) > 0 
                THEN SUBSTRING(
                Description,
                CHARINDEX('Src="', Description) + 5,
                CHARINDEX('"', Description, CHARINDEX('Src="', Description) + 5) - CHARINDEX('Src="', Description) - 5
                ) 
                ELSE NULL 
            END AS Fuente,

            CASE 
                WHEN CHARINDEX('IGu="', Description) > 0 
                THEN SUBSTRING(
                Description,
                CHARINDEX('IGu="', Description) + 5,
                CHARINDEX('"', Description, CHARINDEX('IGu="', Description) + 5) - CHARINDEX('IGu="', Description) - 5
                ) 
                ELSE NULL 
            END AS IGu

            FROM [CliniView].[dbo].[PIDB_Log]

            WHERE Description IS NOT NULL AND
            CAST(LogTime AS DATE) >= CAST(? AS DATE) AND 
            CAST(LogTime AS DATE) <= CAST(? AS DATE)

            ORDER BY LogTime ASC
            """

            logging.info(f"Ejecutando consulta para rango: {fecha_inicio_str} - {fecha_fin_str}")
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
            logging.error(f"Error al generar el reporte: {e}")
            raise


class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Reportes CliniView")
        self.root.geometry("500x350")
        self.reporte = ReportGenerator()
        
        # Probar conexión al iniciar
        logging.info("Iniciando aplicación GUI...")
        if not self.reporte.probar_conexion():
            messagebox.showerror("Error de Conexión", 
                               "No se pudo conectar a la base de datos.\n"
                               "Por favor verifica la configuración en el archivo .env\n"
                               "Consulta reporte.log para más detalles.") # Agregamos instrucción para ver el log

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
            logging.warning("Intento de generar reporte sin nombre de archivo.")
            return

        carpeta = filedialog.askdirectory(title="Selecciona carpeta de destino")
        if not carpeta:
            logging.info("Selección de carpeta cancelada.")
            return

        ruta = os.path.join(carpeta, f"{nombre}.xlsx")
        fecha_inicio = self.fecha_inicio.get_date()
        fecha_fin = self.fecha_fin.get_date()

        try:
            self.barra["value"] = 25
            self.root.update_idletasks()

            logging.info(f"Iniciando generación de reporte para rango: {fecha_inicio} - {fecha_fin}")
            self.reporte.generar_excel(ruta, fecha_inicio, fecha_fin)

            self.barra["value"] = 100
            messagebox.showinfo("Éxito", f"Reporte guardado en:\n{ruta}")
            logging.info("Reporte generado y guardado con éxito.")
        except Exception as e:
            self.barra["value"] = 0
            messagebox.showerror("Error", f"No se pudo generar el reporte:\n{e}\nConsulta reporte.log para más detalles.") # Agregamos instrucción para ver el log
            logging.error(f"Error al generar el reporte: {e}", exc_info=True)


class Main:
    def __init__(self):
        self.root = tk.Tk()
        AppGUI(self.root)
        self.root.mainloop()


if __name__ == "__main__":
    Main()
