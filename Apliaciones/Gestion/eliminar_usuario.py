import tkinter as tk
from tkinter import messagebox
import sqlite3
from DB.db_config import DB_PATH

# Función para conectar a la base de datos SQLite
def conectar_db():
    conn = sqlite3.connect(DB_PATH)  # Usamos la ruta de la base de datos definida en DB_PATH
    return conn


# Función para buscar un usuario por ID en la base de datos
def buscar_usuario_en_db(id_empleado):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_empleado, nombre, apellido, cedula FROM empleados WHERE id_empleado = ?
    ''', (id_empleado,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario


# Función para eliminar un usuario en la base de datos
def eliminar_usuario_en_db(id_empleado):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM empleados WHERE id_empleado = ?
    ''', (id_empleado,))
    conn.commit()
    conn.close()


# Función para validar que solo se ingresen números en el campo
def validar_numeros(valor):
    if valor == "" or valor.isdigit():
        return True
    return False


# Ventana para eliminar usuario
def ventana_eliminar_usuario():
    ventana = tk.Tk()
    ventana.title("Eliminar Usuario")
    ventana.configure(bg="#2C2F38")  # Fondo oscuro

    # Obtener el tamaño de la pantalla
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    # Obtener el tamaño de la ventana (más grande)
    window_width = 500
    window_height = 400

    # Calcular la posición de la ventana para centrarla
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    # Establecer la geometría de la ventana (centrada en la pantalla)
    ventana.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # Crear un contenedor (Frame) para los campos de entrada y etiquetas
    contenedor = tk.Frame(ventana, bg="#2C2F38")
    contenedor.place(relx=0.5, rely=0.5, anchor="center")  # Centrado dentro de la ventana

    # Etiquetas y campos de entrada para el ID del empleado (para buscar) y los nuevos datos
    tk.Label(contenedor, text="ID Empleado:", fg="white", bg="#2C2F38", font=("Arial", 12)).grid(row=0, column=0,
                                                                                                 padx=20, pady=15)

    # Configuración de la validación de números para el campo ID Empleado
    vcmd = (ventana.register(validar_numeros), '%P')
    entry_id_empleado = tk.Entry(contenedor, font=("Arial", 12), width=30, validate="key", validatecommand=vcmd)
    entry_id_empleado.grid(row=0, column=1, padx=20, pady=15)

    # Campos de entrada para nombre, apellido y cédula del empleado
    tk.Label(contenedor, text="Nombre:", fg="white", bg="#2C2F38", font=("Arial", 12)).grid(row=1, column=0,
                                                                                             padx=20, pady=15)
    entry_nombre = tk.Entry(contenedor, font=("Arial", 12), width=30)
    entry_nombre.grid(row=1, column=1, padx=20, pady=15)

    tk.Label(contenedor, text="Apellido:", fg="white", bg="#2C2F38", font=("Arial", 12)).grid(row=2, column=0,
                                                                                             padx=20, pady=15)
    entry_apellido = tk.Entry(contenedor, font=("Arial", 12), width=30)
    entry_apellido.grid(row=2, column=1, padx=20, pady=15)

    tk.Label(contenedor, text="Cédula:", fg="white", bg="#2C2F38", font=("Arial", 12)).grid(row=3, column=0,
                                                                                             padx=20, pady=15)
    entry_cedula = tk.Entry(contenedor, font=("Arial", 12), width=30)
    entry_cedula.grid(row=3, column=1, padx=20, pady=15)

    # Función para buscar el usuario
    def buscar_usuario():
        id_empleado = entry_id_empleado.get()

        if not id_empleado:
            messagebox.showerror("Error", "Por favor, ingrese el ID del empleado")
            return

        usuario = buscar_usuario_en_db(id_empleado)
        if usuario:
            # Si el usuario existe, mostrar los datos en los campos
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, usuario[1])

            entry_apellido.delete(0, tk.END)
            entry_apellido.insert(0, usuario[2])

            entry_cedula.delete(0, tk.END)
            entry_cedula.insert(0, usuario[3])
        else:
            messagebox.showerror("Error", "Usuario no encontrado")

    # Función para eliminar el usuario
    def eliminar_usuario():
        id_empleado = entry_id_empleado.get()

        if not id_empleado:
            messagebox.showerror("Error", "Por favor, ingrese el ID del empleado")
            return

        # Confirmar la eliminación
        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar este usuario?")
        if respuesta:
            eliminar_usuario_en_db(id_empleado)
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
            ventana.destroy()

    # Botones para buscar el usuario y eliminar el usuario
    boton_buscar = tk.Button(contenedor, text="Buscar Usuario", command=buscar_usuario, font=("Arial", 14, "bold"),
                             bg="#3498DB", fg="white", relief="flat", activebackground="#2980B9", width=15, height=2)
    boton_buscar.grid(row=4, column=0, columnspan=2, pady=15)

    boton_eliminar = tk.Button(contenedor, text="Eliminar Usuario", command=eliminar_usuario, font=("Arial", 14, "bold"),
                               bg="#E74C3C", fg="white", relief="flat", activebackground="#C0392B", width=15, height=2)
    boton_eliminar.grid(row=5, column=0, columnspan=2, pady=15)

    ventana.mainloop()


if __name__ == "__main__":
    ventana_eliminar_usuario()
