import tkinter as tk
import psutil
import subprocess
import socket
import sqlite3
import os
import threading
from tkinter import messagebox
from DB.db_config import DB_PATH
from DescargasExcel.excel_config import EXCEL_PATH
from Apliaciones.Gestion.crear_usuario import ventana_crear_usuario
from Apliaciones.Gestion.editar_usuario import ventana_editar_usuario
from Apliaciones.Gestion.eliminar_usuario import ventana_eliminar_usuario
from Apliaciones.Gestion.consultar_usuarios import ventana_consultar_usuarios
from Apliaciones.Calendario.Festivos.feriados import ventana_consultar_festivos
from Apliaciones.Autoajustes.reporte_tablas import ventana_consultar_empleados_archivos
from Apliaciones.CambioEnDB.cambiodb import ventana_cambio_db
from Apliaciones.Backup.CopiaSeguridad import ventana_respaldo
from Apliaciones.CambioEnExcel.cambioexcel import ventana_cambio_excel_folder
from Apliaciones.Ayuda.infodispositivo import ventana_consulta_dispositivo
from Apliaciones.Ayuda.reinicar_huellro import ventana_reiniciar_dispositivo
from Apliaciones.Autoajustes.reevaluar_horarios import ventana_cargar_excel
from Apliaciones.Ayuda.eliminar_registros import ventana_borrar_registros


# Función para hacer un ping
def ping(host="8.8.8.8"):
    try:
        result = subprocess.run(["ping", "-n", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False

# Función para verificar si un puerto está abierto
def puerto_abierto(host, puerto):
    try:
        with socket.create_connection((host, puerto), timeout=5):
            return True
    except (socket.timeout, socket.error):
        return False

# Función para obtener el estado de la red
def obtener_estado_red():
    conectado = False
    try:
        if psutil.net_if_addrs():
            conectado = True
    except Exception:
        conectado = False

    if not conectado:
        return "Desconectado"
    if ping():
        return "Conectado"
    else:
        return "Conexión a Internet Inestable"

# Función para verificar la conexión a la base de datos SQLite
def verificar_base_datos():
    if not os.path.exists(DB_PATH):
        return "Base de datos no encontrada"
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.close()
        return "Base de datos conectada"
    except sqlite3.Error:
        return "Error al conectar con la base de datos"

# Función para verificar el huellero
def verificar_huellero():
    # Verificar si hay conexión a Internet
    if ping():  # Si la red está conectada
        huellero_ip = "186.30.160.228"
        if ping(huellero_ip):  # Si el ping al huellero es exitoso
            return "Huellero conectado"
        else:
            return "Error de conexión al huellero"
    else:
        return "Sin conexión a Internet"

# Función para actualizar el estado de la red
def actualizar_estado_red(label_red):
    estado_red = obtener_estado_red()
    label_red.config(text=f"Estado Red: {estado_red}")
    if estado_red == "Conectado":
        label_red.config(fg="#76D7C4")  # Verde
    elif estado_red == "Conexión a Internet Inestable":
        label_red.config(fg="#F39C12")  # Amarillo
    else:
        label_red.config(fg="#E74C3C")  # Rojo


# Función para actualizar el estado de la base de datos
def actualizar_estado_db(label_db):
    estado_db = verificar_base_datos()
    label_db.config(text=f"Estado DB: {estado_db}")
    if estado_db == "Base de datos conectada":
        label_db.config(fg="#76D7C4")  # Verde
    elif estado_db == "Base de datos no encontrada":
        label_db.config(fg="#E74C3C")  # Rojo
    else:
        label_db.config(fg="#F39C12")  # Amarillo

# Función para actualizar el estado del huellero
def actualizar_estado_huellero(label_huellero):
    estado_huellero = verificar_huellero()
    label_huellero.config(text=f"Estado Huellero: {estado_huellero}")
    if estado_huellero == "Huellero conectado":
        label_huellero.config(fg="#76D7C4")  # Verde
    else:
        label_huellero.config(fg="#E74C3C")  # Rojo


# Función para refrescar los estados (solo actualiza una vez)
def refrescar_estado(label_red, label_db, label_huellero):
    # Actualiza el estado de cada elemento
    actualizar_estado_red(label_red)
    actualizar_estado_db(label_db)
    actualizar_estado_huellero(label_huellero)

# Función para refrescar los estados con el botón
def refrescar_button(label_red, label_db, label_huellero):
    refrescar_estado(label_red, label_db, label_huellero)


# Función acerca de
def acerca_de():
    messagebox.showinfo("Consultar Usuarios", "Elaborado por: Johnjairoac")

# Función para cerrar todas las ventanas
def cerrar_todas_ventanas(ventanas):
    for ventana in ventanas:
        ventana.destroy()

# Función principal para mostrar la ventana de estado
def mostrar_estado():
    ventanas = []
    ventana = tk.Tk()
    ventanas.append(ventana)
    ventana.title("TiempoActivo")
    ventana.configure(bg="#2C2F38")



    menu_bar = tk.Menu(ventana)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="cambiar base de datos", command=ventana_cambio_db)
    file_menu.add_command(label="cambiar ruta descargas de excel", command=ventana_cambio_excel_folder)
    file_menu.add_command(label="Respaldo DB", command=ventana_respaldo)
    file_menu.add_command(label="Salir", command=ventana.quit)

    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Acerca del programa", command=acerca_de)
    help_menu.add_command(label="informacion del Huellero", command=ventana_consulta_dispositivo)
    help_menu.add_command(label="Reiniciar Huellero", command=ventana_reiniciar_dispositivo)
    help_menu.add_command(label="Borrar registros", command=ventana_borrar_registros)
    menu_bar.add_cascade(label="Archivo", menu=file_menu)
    menu_bar.add_cascade(label="Ayuda", menu=help_menu)


    menu_gestion = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Gestión de Usuarios", menu=menu_gestion)
    menu_gestion.add_command(label="Crear Usuario", command=ventana_crear_usuario)
    menu_gestion.add_command(label="Editar Usuario", command=ventana_editar_usuario)
    menu_gestion.add_command(label="Eliminar Usuario", command=ventana_eliminar_usuario)
    menu_gestion.add_command(label="Consultar Usuarios", command=ventana_consultar_usuarios)

    menu_gestion = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Tablero de Resultados", menu=menu_gestion)
    menu_gestion.add_command(label="Consolidado", command=ventana_consultar_empleados_archivos)
    menu_gestion.add_command(label="Reevaluar Horarios", command=ventana_cargar_excel)


    menu_gestion = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Calendario Laboral", menu=menu_gestion)
    menu_gestion.add_command(label="Consultar festivos", command=ventana_consultar_festivos)




    ventana.config(menu=menu_bar)

    ancho_ventana = 600
    alto_ventana = 350
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla - ancho_ventana) // 2
    y = (alto_pantalla - alto_ventana) // 2
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    frame_contenedor = tk.Frame(ventana, bg="#2C2F38")
    frame_contenedor.place(relx=0.5, rely=0.4, anchor="center")

    # Etiqueta para el estado de la red
    network_icon = tk.Label(frame_contenedor, text="📶 Red", font=("Arial", 20), bg="#2C2F38", fg="#E0E0E0")
    network_icon.grid(row=0, column=0, padx=10, pady=10)
    etiqueta_estado_red = tk.Label(frame_contenedor, text="Estado Red: Cargando...", font=("Arial", 14), bg="#2C2F38", fg="#E0E0E0")
    etiqueta_estado_red.grid(row=0, column=1, padx=20, pady=10)

    # Etiqueta para el estado de la base de datos
    db_icon = tk.Label(frame_contenedor, text="🗄️ DB", font=("Arial", 20), bg="#2C2F38", fg="#E0E0E0")
    db_icon.grid(row=1, column=0, padx=10, pady=10)
    etiqueta_estado_db = tk.Label(frame_contenedor, text="Estado DB: Cargando...", font=("Arial", 14), bg="#2C2F38", fg="#E0E0E0")
    etiqueta_estado_db.grid(row=1, column=1, padx=20, pady=10)

    # Etiqueta para el estado del huellero
    huellero_icon = tk.Label(frame_contenedor, text="📡 Huellero", font=("Arial", 20), bg="#2C2F38", fg="#E0E0E0")
    huellero_icon.grid(row=2, column=0, padx=10, pady=10)
    etiqueta_estado_huellero = tk.Label(frame_contenedor, text="Estado Huellero: Cargando...", font=("Arial", 14), bg="#2C2F38", fg="#E0E0E0")
    etiqueta_estado_huellero.grid(row=2, column=1, padx=20, pady=10)

    # Botón para refrescar los estados
    boton_refrescar = tk.Button(
        ventana, text="Refrescar", font=("Arial", 14, "bold"), bg="#28B463", fg="white", relief="flat",
        command=lambda: refrescar_estado(etiqueta_estado_red, etiqueta_estado_db, etiqueta_estado_huellero)
    )

    # Botón para refrescar los estados
    boton_refrescar = tk.Button(
        ventana, text="Refrescar", font=("Arial", 14, "bold"), bg="#28B463", fg="white", relief="flat",
        command=lambda: refrescar_button(etiqueta_estado_red, etiqueta_estado_db, etiqueta_estado_huellero)
    )

    # Colocamos el botón en la parte inferior con pack y lo centramos
    boton_refrescar.pack(side="bottom", pady=(10, 20), anchor="center")  # Ajusta el padding superior y inferior

    # Llamada a refrescar_estado() por primera vez
    refrescar_estado(etiqueta_estado_red, etiqueta_estado_db, etiqueta_estado_huellero)

    # Configura el cierre de la ventana para cerrar todas las ventanas abiertas
    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_todas_ventanas(ventanas))

    # Ejecutar el loop principal
    ventana.mainloop()

# Ejecutar la función para mostrar el estado
if __name__ == "__main__":
    mostrar_estado()
