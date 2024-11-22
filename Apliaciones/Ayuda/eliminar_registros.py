import os
import sys
import tkinter as tk
from tkinter import messagebox
from zk import ZK

# Función para borrar los registros de asistencia
def borrar_registros_asistencia():
    conn = None
    zk = ZK('186.30.160.228', port=4370)
    try:
        conn = zk.connect()
        # Confirmación antes de borrar
        choices = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar todos los registros de asistencia?")
        if choices:
            conn.clear_attendance()  # Borrar solo los registros de asistencia
            messagebox.showinfo("Éxito", "Registros de asistencia eliminados correctamente.")
        else:
            messagebox.showinfo("Cancelado", "La eliminación de registros de asistencia fue cancelada.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar los registros de asistencia: {e}")
    finally:
        if conn:
            conn.disconnect()

# Ventana principal
def ventana_borrar_registros():
    ventana = tk.Tk()
    ventana.title("Eliminar Registros de Asistencia")
    ventana.configure(bg="#2C2F38")

    # Tamaño y posición de la ventana
    ancho_ventana = 400
    alto_ventana = 200
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    pos_x = int((screen_width - ancho_ventana) / 2)
    pos_y = int((screen_height - alto_ventana) / 2)
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")

    # Contenedor principal
    contenedor = tk.Frame(ventana, bg="#2C2F38")
    contenedor.place(relx=0.5, rely=0.5, anchor="center")  # Centrar el contenedor

    # Título
    titulo = tk.Label(
        contenedor,
        text="Eliminar Registros de Asistencia",
        font=("Arial", 14, "bold"),
        bg="#2C2F38",
        fg="white",
    )
    titulo.pack(pady=10)

    # Botón para borrar registros de asistencia
    boton_borrar = tk.Button(
        contenedor,
        text="Eliminar Registros",
        font=("Arial", 12, "bold"),
        bg="#E74C3C",
        fg="white",
        relief="flat",
        activebackground="#C0392B",
        width=20,
        height=2,
        command=borrar_registros_asistencia,
    )
    boton_borrar.pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    ventana_borrar_registros()
