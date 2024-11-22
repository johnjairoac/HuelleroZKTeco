import tkinter as tk
from tkinter import ttk
import sqlite3
from DB.db_config import DB_PATH

# Función para conectar a la base de datos SQLite
def conectar_db():
    conn = sqlite3.connect(DB_PATH)  # Usamos la ruta de la base de datos definida en DB_PATH
    return conn

# Función para obtener todos los festivos de la base de datos
def obtener_todos_los_festivos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT fecha, descripcion FROM festivos''')
    festivos = cursor.fetchall()
    conn.close()
    return festivos

# Función para actualizar la vista de los festivos en el Treeview
def actualizar_festivos(treeview):
    # Eliminar todas las filas existentes
    for row in treeview.get_children():
        treeview.delete(row)
    # Obtener la lista de festivos
    festivos = obtener_todos_los_festivos()
    # Insertar los nuevos festivos en el Treeview
    for festivo in festivos:
        treeview.insert("", tk.END, values=festivo)

# Ventana para consultar todos los festivos
def ventana_consultar_festivos():
    ventana = tk.Tk()
    ventana.title("Consultar Festivos")
    ventana.configure(bg="#2C2F38")  # Fondo oscuro

    # Obtener el tamaño de la pantalla
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    # Establecer el tamaño de la ventana (más pequeño)
    window_width = 800
    window_height = 500

    # Calcular la posición de la ventana para centrarla
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    # Establecer la geometría de la ventana (centrada en la pantalla)
    ventana.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # Crear un contenedor (Frame) para los elementos
    contenedor = tk.Frame(ventana, bg="#2C2F38")
    contenedor.pack(padx=20, pady=20, fill="both", expand=True)

    # Etiqueta principal
    tk.Label(contenedor, text="Festivos Registrados", fg="white", bg="#2C2F38", font=("Arial", 14, "bold")).pack(pady=10)

    # Crear un marco para el Treeview y su scrollbar
    frame_treeview = tk.Frame(contenedor, bg="#2C2F38", bd=2, relief="solid")  # Trazos alrededor del marco
    frame_treeview.pack(pady=10, fill="both", expand=True)

    # Crear un Treeview para mostrar los festivos en formato tabla
    columnas = ("Fecha", "Descripción")
    treeview = ttk.Treeview(frame_treeview, columns=columnas, show="headings", height=15)
    treeview.pack(side="left", fill="both", expand=True)

    # Configurar las columnas del Treeview
    for col in columnas:
        treeview.heading(col, text=col)
        treeview.column(col, width=200, anchor="center")

    # Estilo para el Treeview (colores alternos en las filas)
    treeview.tag_configure("evenrow", background="#f0f0f0")  # Fondo claro para filas pares
    treeview.tag_configure("oddrow", background="#dfe4ea")   # Fondo gris claro para filas impares

    # Barra de desplazamiento vertical dentro del marco del Treeview
    scrollbar = ttk.Scrollbar(frame_treeview, orient="vertical", command=treeview.yview)
    treeview.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Llamada inicial para cargar los festivos
    festivos = obtener_todos_los_festivos()
    for idx, festivo in enumerate(festivos):
        tag = "evenrow" if idx % 2 == 0 else "oddrow"
        treeview.insert("", tk.END, values=festivo, tags=(tag,))

    ventana.mainloop()

# Llamada para abrir la ventana solo si se ejecuta directamente
if __name__ == "__main__":
    ventana_consultar_festivos()
