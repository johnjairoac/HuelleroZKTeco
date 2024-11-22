import os
import sys
import tkinter as tk
from tkinter import messagebox
from zk import ZK

# Función para conectarse al dispositivo ZKTeco y obtener información
def obtener_datos_dispositivo(texto_resultados):
    conn = None
    zk = ZK('186.30.160.228', port=4370)
    try:
        conn = zk.connect()
        # Obtener información del dispositivo
        datos_dispositivo = (
            "-- Información del Dispositivo --\n"
            f"Hora Actual            : {conn.get_time()}\n"
            f"Versión del Firmware   : {conn.get_firmware_version()}\n"
            f"Nombre del Dispositivo : {conn.get_device_name()}\n"
            f"Número de Serie        : {conn.get_serialnumber()}\n"
            f"Dirección MAC          : {conn.get_mac()}\n"
            f"Versión Alg. Facial    : {conn.get_face_version()}\n"
            f"Versión Alg. Huella    : {conn.get_fp_version()}\n"
            f"Plataforma             : {conn.get_platform()}\n"
        )
        # Obtener información de red
        network_info = conn.get_network_params()
        datos_red = (
            "-- Información de Red --\n"
            f"IP                    : {network_info.get('ip')}\n"
            f"Máscara de Red        : {network_info.get('mask')}\n"
            f"Puerta de Enlace      : {network_info.get('gateway')}\n"
        )
        # Mostrar resultados en el cuadro de texto
        texto_resultados.config(state="normal")  # Habilitar edición temporal
        texto_resultados.delete("1.0", tk.END)  # Limpiar contenido previo
        texto_resultados.insert(tk.END, datos_dispositivo + "\n" + datos_red)
        texto_resultados.tag_add("centrado", "1.0", tk.END)
        texto_resultados.tag_configure("centrado", justify="center")  # Centrar texto
        texto_resultados.config(state="disabled")  # Deshabilitar edición
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener los datos: {e}")
    finally:
        if conn:
            conn.disconnect()

# Ventana principal
def ventana_consulta_dispositivo():
    ventana = tk.Tk()
    ventana.title("Consulta de Datos del Dispositivo")
    ventana.configure(bg="#2C2F38")

    # Tamaño y posición de la ventana
    ancho_ventana = 600
    alto_ventana = 400
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
        text="Consulta de Datos del Dispositivo",
        font=("Arial", 14, "bold"),
        bg="#2C2F38",
        fg="white",
    )
    titulo.pack(pady=10)

    # Cuadro de texto para mostrar los datos
    texto_resultados = tk.Text(
        contenedor,
        width=70,
        height=15,
        wrap="word",
        bg="#1E1E1E",
        fg="white",
        font=("Courier", 10),
        state="disabled",
        relief="flat",
    )
    texto_resultados.pack(pady=10)

    # Botón para iniciar la consulta
    boton_consultar = tk.Button(
        contenedor,
        text="Consultar Datos",
        font=("Arial", 12, "bold"),
        bg="#3498DB",
        fg="white",
        relief="flat",
        activebackground="#2980B9",
        command=lambda: obtener_datos_dispositivo(texto_resultados),
    )
    boton_consultar.pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    ventana_consulta_dispositivo()
