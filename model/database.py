import mysql.connector
from mysql.connector import Error
import datetime
import time

class Database:
    def __init__(self, host, user, password, database, max_retries=3, retry_delay=2):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.conn = None
        self.cursor = None
        self.conectar()

    def conectar(self):
        """Intenta conectar a la base de datos con reintentos."""
        retries = 0
        while retries < self.max_retries:
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    autocommit=True
                )
                self.cursor = self.conn.cursor(dictionary=True)
                print("Conexión a la base de datos establecida.")
                return
            except Error as e:
                print(f"Error de conexión a BD (intento {retries+1}): {e}")
                retries += 1
                time.sleep(self.retry_delay)
        raise Exception("No se pudo conectar a la base de datos después de varios intentos.")

    def verificar_conexion(self):
        """Verifica si la conexión está activa, si no, intenta reconectar."""
        if self.conn is None or not self.conn.is_connected():
            print("Conexión perdida. Intentando reconectar...")
            self.conectar()

    def obtener_usuarios(self):
        try:
            self.verificar_conexion()
            self.cursor.execute("SELECT * FROM users")
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error en obtener_usuarios: {e}")
            return []

    def registrar_intento_acceso(self, user_id, status):
        try:
            self.verificar_conexion()
            timestamp = datetime.datetime.now()
            query = "INSERT INTO access_logs (user_id, timestamp, status) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (user_id, timestamp, status))
        except Error as e:
            print(f"Error en registrar_intento_acceso: {e}")

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Conexión a la base de datos cerrada.")
