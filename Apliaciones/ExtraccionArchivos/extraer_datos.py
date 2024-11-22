# extraer_datos.py
import os
import sys
import sqlite3
from zk import ZK
from datetime import datetime
from DB.db_config import DB_PATH

# Conectar a la base de datos solo una vez
def connect_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        print("Conexión exitosa a la base de datos.")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        sys.exit(1)

# Verificar si el registro ya existe
def record_exists(cursor, user_id, date, time):
    check_query = '''
        SELECT 1 FROM archivos_extraidos
        WHERE user_id = ? AND date = ? AND time = ?
        LIMIT 1;
    '''
    cursor.execute(check_query, (user_id, date, time))
    return cursor.fetchone() is not None

# Insertar un nuevo registro si no existe
def insert_record(cursor, user_id, user_name, date, time):
    if not record_exists(cursor, user_id, date, time):
        insert_query = '''
            INSERT INTO archivos_extraidos (user_id, user_name, date, time)
            VALUES (?, ?, ?, ?);
        '''
        cursor.execute(insert_query, (user_id, user_name, date, time))
        print(f"Insertado: {user_id}, {user_name}, {date}, {time}")
    else:
        print(f"Registro duplicado encontrado: {user_id}, {user_name}, {date}, {time} - No se insertó.")

# Función principal que ejecuta el proceso de extracción de datos
def main():
    conn = None
    zk = ZK('186.30.160.228', port=4370)  # Dirección IP y puerto del dispositivo

    try:
        conn = zk.connect()

        # Leer los registros de asistencia
        print("-- Attendance Records --")
        records = conn.get_attendance()

        users = conn.get_users()

        user_names = {user.user_id: user.name for user in users}

        db_conn = connect_db()
        cursor = db_conn.cursor()

        if records:
            for record in records:
                user_id = record.user_id
                timestamp = record.timestamp

                user_name = user_names.get(user_id, 'Unknown User')

                if isinstance(timestamp, (int, float)):
                    timestamp_obj = datetime.fromtimestamp(timestamp)
                    date = timestamp_obj.strftime('%Y-%m-%d')
                    time = timestamp_obj.strftime('%H:%M:%S')
                else:
                    date = timestamp.strftime('%Y-%m-%d')
                    time = timestamp.strftime('%H:%M:%S')

                print(f"User ID: {user_id}, User Name: {user_name}, Date: {date}, Time: {time}")

                insert_record(cursor, user_id, user_name, date, time)

            db_conn.commit()

        else:
            print("No attendance records found.")

    except Exception as e:
        print(f"Proceso terminado: {e}")
    finally:
        if conn:
            conn.disconnect()
        if db_conn:
            db_conn.close()
