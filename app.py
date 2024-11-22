# app.py
from Apliaciones.Status import status  # Importar el archivo status.py
import Apliaciones.ExtraccionArchivos.extraer_datos  # Cambié el nombre del archivo aquí

if __name__ == '__main__':
    # Llamar a la función de extracción de datos primero
    Apliaciones.ExtraccionArchivos.extraer_datos.main()  # Suponiendo que defines una función main en extraer_datos.py

    # Llamar a la función para mostrar el estado
    status.mostrar_estado()
