import tkinter as tk
from tkinter import messagebox
import sqlite3
from DB.db_config import DB_PATH

# Función para conectar a la base de datos SQLite
def conectar_db():
    conn = sqlite3.connect(DB_PATH)  # Usamos la ruta de la base de datos definida en DB_PATH
    return conn

# Función para verificar si el id_empleado ya existe en la base de datos
def verificar_usuario_existente(id_empleado):
    conn = conectar_db()
    cursor = conn.cursor()
    # Verificamos si el id_empleado ya está en la base de datos
    cursor.execute('''SELECT COUNT(*) FROM empleados WHERE id_empleado = ?''', (id_empleado,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0  # Si el resultado es mayor que 0, significa que ya existe

# Función para crear un nuevo usuario en la base de datos
def crear_usuario_en_db(id_empleado, nombre, apellido, cedula):
    # Verificar si el id_empleado ya existe
    if verificar_usuario_existente(id_empleado):
        return False  # Si ya existe, retornar False
    conn = conectar_db()
    cursor = conn.cursor()
    # Insertar los datos en la tabla 'empleados'
    cursor.execute(''' 
        INSERT INTO empleados (id_empleado, nombre, apellido, cedula)
        VALUES (?, ?, ?, ?)
    ''', (id_empleado, nombre, apellido, cedula))
    conn.commit()
    conn.close()
    return True  # Si la inserción fue exitosa, retornar True

# Función para validar que el id_empleado solo contenga números
def validar_id_empleado(input):
    if input.isdigit() or input == "":  # Acepta solo números
        return True
    else:
        return False

# Ventana para crear usuario
def ventana_crear_usuario():
    ventana = tk.Tk()
    ventana.title("Crear Usuario")
    ventana.configure(bg="#2C2F38")  # Fondo oscuro

    # Obtener el tamaño de la pantalla
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    # Obtener el tamaño de la ventana
    window_width = 400
    window_height = 300

    # Calcular la posición de la ventana para centrarla
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    # Establecer la geometría de la ventana (centrada en la pantalla)
    ventana.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # Crear un contenedor (Frame) para los campos de entrada y etiquetas
    contenedor = tk.Frame(ventana, bg="#2C2F38")
    contenedor.place(relx=0.5, rely=0.5, anchor="center")  # Centrado dentro de la ventana

    # Etiquetas y campos de entrada para el nuevo usuario con fuentes más grandes
    tk.Label(contenedor, text="ID Empleado:", fg="white", bg="#2C2F38", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
    tk.Label(contenedor, text="Nombre:", fg="white", bg="#2C2F38", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
    tk.Label(contenedor, text="Apellido:", fg="white", bg="#2C2F38", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
    tk.Label(contenedor, text="Cédula:", fg="white", bg="#2C2F38", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10)

    entry_id_empleado = tk.Entry(contenedor, validate="key", validatecommand=(ventana.register(validar_id_empleado), '%P'))
    entry_nombre = tk.Entry(contenedor)
    entry_apellido = tk.Entry(contenedor)
    entry_cedula = tk.Entry(contenedor)

    entry_id_empleado.grid(row=0, column=1, padx=10, pady=10)
    entry_nombre.grid(row=1, column=1, padx=10, pady=10)
    entry_apellido.grid(row=2, column=1, padx=10, pady=10)
    entry_cedula.grid(row=3, column=1, padx=10, pady=10)

    # Función para guardar el usuario
    def guardar_usuario():
        id_empleado = entry_id_empleado.get()
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        cedula = entry_cedula.get()

        if not id_empleado or not nombre or not apellido or not cedula:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
        else:
            # Intentar guardar el usuario en la base de datos
            if crear_usuario_en_db(id_empleado, nombre, apellido, cedula):
                messagebox.showinfo("Éxito", "Usuario creado correctamente")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "Ya existe un usuario con ese ID Empleado")

    # Botón para guardar el usuario con las características que solicitaste
    boton_guardar = tk.Button(contenedor, text="Crear Usuario", font=("Arial", 14, "bold"), bg="#3498DB", fg="white", relief="flat",
                              activebackground="#2980B9", width=15, height=2, command=guardar_usuario)
    boton_guardar.grid(row=4, column=0, columnspan=2, pady=20)

    ventana.mainloop()

if __name__ == "__main__":
    ventana_crear_usuario()
