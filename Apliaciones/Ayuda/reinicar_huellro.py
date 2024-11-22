import os
import sys
import tkinter as tk
from tkinter import messagebox
from zk import ZK

# Función para reiniciar el dispositivo
def reiniciar_dispositivo():
    conn = None
    zk = ZK('186.30.160.228', port=4370)
    try:
        conn = zk.connect()
        conn.restart()  # Reinicia el dispositivo
        messagebox.showinfo("Éxito", "El dispositivo se reinició correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo reiniciar el dispositivo: {e}")
    finally:
        if conn:
            conn.disconnect()

# Ventana principal
def ventana_reiniciar_dispositivo():
    ventana = tk.Tk()
    ventana.title("Reiniciar Dispositivo")
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
        text="Reiniciar Dispositivo",
        font=("Arial", 14, "bold"),
        bg="#2C2F38",
        fg="white",
    )
    titulo.pack(pady=10)

    # Botón para reiniciar el dispositivo
    boton_reiniciar = tk.Button(
        contenedor,
        text="Reiniciar Ahora",
        font=("Arial", 12, "bold"),
        bg="#E74C3C",
        fg="white",
        relief="flat",
        activebackground="#C0392B",
        width=20,
        height=2,
        command=reiniciar_dispositivo,
    )
    boton_reiniciar.pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    ventana_reiniciar_dispositivo()
