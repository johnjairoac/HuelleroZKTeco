import tkinter as tk
from tkinter import filedialog, messagebox
import os
import importlib
from DB import db_config  # Importamos el módulo completo


# Función para actualizar la ruta de la base de datos en el archivo de configuración
def actualizar_db_path(nueva_ruta, etiqueta_db):
    try:
        # Verificar si la carpeta DB existe, si no, crearla
        if not os.path.exists("DB"):
            os.makedirs("DB")

        # Escribir la nueva ruta de la base de datos en el archivo de configuración
        with open("DB/db_config.py", "w") as config_file:
            config_file.write(f"DB_PATH = '{nueva_ruta}'\n")

        # Recargar el módulo de configuración para obtener la nueva ruta
        importlib.reload(db_config)

        # Actualizar la etiqueta con la nueva ruta
        etiqueta_db.config(text=f"Base de Datos Actual: {db_config.DB_PATH}")

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "La base de datos se cambió correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar la base de datos: {e}")


# Función para seleccionar la nueva base de datos
def seleccionar_db(etiqueta_db):
    nueva_ruta = filedialog.askopenfilename(
        title="Seleccionar Base de Datos",
        filetypes=[("Archivos SQLite", "*.sqlite;*.db;*.sqlite3")]
    )
    if nueva_ruta:
        # Actualizar la ruta de la base de datos y la etiqueta
        actualizar_db_path(nueva_ruta, etiqueta_db)


# Crear la ventana para cambiar la base de datos
def ventana_cambio_db():
    ventana = tk.Tk()
    ventana.title("Cambiar Base de Datos")
    ventana.configure(bg="#2C2F38")  # Fondo oscuro

    # Obtener el tamaño de la pantalla
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    # Obtener el tamaño de la ventana
    window_width = 600
    window_height = 300

    # Calcular la posición de la ventana para centrarla
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    # Establecer la geometría de la ventana (centrada en la pantalla)
    ventana.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # Contenedor de la ventana
    contenedor = tk.Frame(ventana, bg="#2C2F38")
    contenedor.place(relx=0.5, rely=0.5, anchor="center")  # Centrado dentro de la ventana

    # Etiqueta para mostrar la base de datos actual
    etiqueta_db = tk.Label(contenedor, text=f"Base de Datos Actual: {db_config.DB_PATH}", fg="white", bg="#2C2F38",
                           font=("Arial", 12))
    etiqueta_db.grid(row=0, column=0, padx=10, pady=20)

    # Botón para seleccionar la nueva base de datos
    boton_seleccionar_db = tk.Button(
        contenedor, text="Seleccionar Nueva Base de Datos", font=("Arial", 12, "bold"), bg="#3498DB", fg="white",
        relief="flat",
        activebackground="#2980B9", width=25, height=2, command=lambda: seleccionar_db(etiqueta_db)
    )
    boton_seleccionar_db.grid(row=1, column=0, pady=20)

    ventana.mainloop()


if __name__ == "__main__":
    ventana_cambio_db()
