import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
from DB.db_config import DB_PATH  # Importar la ruta actual de la base de datos


# Función para crear el respaldo de la base de datos
def crear_respaldo():
    try:
        # Obtener la ruta del archivo de respaldo
        ruta_respaldo = filedialog.asksaveasfilename(
            title="Guardar Respaldo de Base de Datos",
            defaultextension=".db",
            filetypes=[("Archivos SQLite", "*.db;*.sqlite3")],
            initialfile="respaldo_base_de_datos"
        )

        if ruta_respaldo:
            # Verificar si el archivo de base de datos original existe
            if os.path.exists(DB_PATH):
                # Realizar la copia de seguridad de la base de datos
                shutil.copy(DB_PATH, ruta_respaldo)
                messagebox.showinfo("Éxito", f"Copia de seguridad creada en: {ruta_respaldo}")
            else:
                messagebox.showerror("Error", "No se encontró la base de datos original.")
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó una ubicación para guardar el respaldo.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear la copia de seguridad: {e}")


# Crear la ventana para el respaldo de la base de datos
def ventana_respaldo():
    ventana = tk.Tk()
    ventana.title("Crear Respaldo de Base de Datos")
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
    tk.Label(contenedor, text=f"Base de Datos Actual: {DB_PATH}", fg="white", bg="#2C2F38", font=("Arial", 12)).grid(
        row=0, column=0, padx=10, pady=20)

    # Botón para crear el respaldo
    boton_respaldo = tk.Button(
        contenedor, text="Crear Respaldo", font=("Arial", 12, "bold"), bg="#3498DB", fg="white", relief="flat",
        activebackground="#2980B9", width=25, height=2, command=crear_respaldo
    )
    boton_respaldo.grid(row=1, column=0, pady=20)

    ventana.mainloop()


if __name__ == "__main__":
    ventana_respaldo()
