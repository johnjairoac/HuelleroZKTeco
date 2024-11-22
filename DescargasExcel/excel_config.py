# excel_config.py
import os

# Obtén el directorio de trabajo actual
cwd = os.getcwd()

# Construye la ruta a la carpeta DescargasExcel relativa al directorio de trabajo
EXCEL_PATH = os.path.join(cwd, 'DescargasExcel')