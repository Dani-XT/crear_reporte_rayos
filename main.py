import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from dotenv import load_dotenv
import pyodbc
import os

load_dotenv()


class Main:
    
    def __init__(self):
        self.server = os.getenv("SQL_SERVER")
        self.database = os.getenv("SQL_DATABASE")
        self.username = os.getenv("SQL_USERNAME")
        self.password = os.getenv("SQL_PASSWORD")

        