import importlib
from DescargasExcel import excel_config
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Función para actualizar la ruta de la carpeta de Excel en el archivo de configuración
def actualizar_excel_folder(nueva_carpeta, etiqueta_excel):
    try:
        # Verificar si el directorio DescargasExcel existe, si no, crearlo
        carpeta_destino = "DescargasExcel"
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)  # Crear la carpeta si no existe

        # Escribir la nueva ruta de la carpeta de Excel en el archivo de configuración
        config_file_path = os.path.join(carpeta_destino, "excel_config.py")
        with open(config_file_path, "w") as config_file:
            config_file.write(f"EXCEL_PATH = '{nueva_carpeta}'\n")

        # Recargar el módulo de configuración para obtener la nueva ruta
        importlib.reload(excel_config)

        # Verificar la ruta cargada después de recargar el módulo
        print(f"Ruta actualizada en el archivo: {excel_config.EXCEL_PATH}")

        # Actualizar la etiqueta con la nueva ruta
        etiqueta_excel.config(text=f"Carpeta de Archivos Excel Actual: {excel_config.EXCEL_PATH}")

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", f"La carpeta de archivos Excel se cambió correctamente a: {excel_config.EXCEL_PATH}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar la carpeta de archivo Excel: {e}")

# Función para seleccionar la nueva carpeta para los archivos Excel
def seleccionar_excel_folder(etiqueta_excel):
    nueva_carpeta = filedialog.askdirectory(
        title="Seleccionar Carpeta para Archivos Excel"
    )
    if nueva_carpeta:
        # Actualizar la ruta de la carpeta y la etiqueta
        actualizar_excel_folder(nueva_carpeta, etiqueta_excel)

# Crear la ventana para cambiar la carpeta de los archivos Excel
def ventana_cambio_excel_folder():
    ventana = tk.Tk()
    ventana.title("Cambiar Carpeta de Archivos Excel")
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

    # Inicializar EXCEL_PATH si no está en excel_config.py
    try:
        current_excel_folder = excel_config.EXCEL_PATH
    except AttributeError:
        current_excel_folder = "No definido"

    # Etiqueta para mostrar la ruta actual de la carpeta Excel
    etiqueta_excel = tk.Label(contenedor, text=f"Carpeta de Archivos Excel Actual: {current_excel_folder}", fg="white", bg="#2C2F38",
                              font=("Arial", 12))
    etiqueta_excel.grid(row=0, column=0, padx=10, pady=20)

    # Botón para seleccionar la nueva carpeta de archivos Excel
    boton_seleccionar_excel_folder = tk.Button(
        contenedor, text="Seleccionar Nueva Carpeta", font=("Arial", 12, "bold"), bg="#3498DB", fg="white",
        relief="flat",
        activebackground="#2980B9", width=25, height=2, command=lambda: seleccionar_excel_folder(etiqueta_excel)
    )
    boton_seleccionar_excel_folder.grid(row=1, column=0, pady=20)

    ventana.mainloop()

if __name__ == "__main__":
    ventana_cambio_excel_folder()
