import os

# Obtén el directorio de trabajo actual
cwd = os.getcwd()

# Ruta a la base de datos en la raíz del proyecto
db_path_root = os.path.join(cwd, 'tempus.db')

# Ruta a la base de datos en la carpeta DB
db_path_db_folder = os.path.join(cwd, 'DB', 'tempus.db')

# Verifica si el archivo existe en la raíz
if os.path.exists(db_path_root):
    DB_PATH = db_path_root
# Si no, verifica en la carpeta DB
elif os.path.exists(db_path_db_folder):
    DB_PATH = db_path_db_folder
else:
    raise FileNotFoundError("No se encontró la base de datos en la raíz ni en la carpeta 'DB'.")

print(f"Ruta de la base de datos: {DB_PATH}")
