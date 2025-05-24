import mysql.connector
from mysql.connector import Error
import datetime
import time
from utils.logger_config import logger  # Importa el logger

class Database:
    """
    Clase para manejar la conexión y operaciones básicas con la base de datos MySQL.

    Parámetros:
        host (str): Host de la base de datos.
        user (str): Usuario de la base de datos.
        password (str): Contraseña del usuario.
        database (str): Nombre de la base de datos.
        max_retries (int): Número máximo de intentos para conectar.
        retry_delay (int): Tiempo en segundos a esperar entre intentos.
    """
    
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
        """
        Intenta conectar a la base de datos con reintentos.
        En caso de error, registra en el logger y espera antes de reintentar.
        """
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
                logger.info("Conexión a la base de datos establecida.")
                return
            except Error as e:
                logger.error(f"Error de conexión a BD (intento {retries+1}): {e}")
                retries += 1
                time.sleep(self.retry_delay)
        raise Exception("No se pudo conectar a la base de datos después de varios intentos.")

    def verificar_conexion(self):
        """
        Verifica si la conexión está activa.
        Si no, intenta reconectar para mantener la disponibilidad.
        """
        if self.conn is None or not self.conn.is_connected():
            logger.warning("Conexión perdida. Intentando reconectar...")
            self.conectar()

    def obtener_usuarios(self):
        """
        Recupera todos los usuarios de la tabla 'users' en la base de datos.

        Returns:
            list: Lista de diccionarios con la información de los usuarios.
            Si hay error, devuelve lista vacía.
        """
        try:
            self.verificar_conexion()
            self.cursor.execute("SELECT * FROM users")
            return self.cursor.fetchall()
        except Error as e:
            logger.error(f"Error en obtener_usuarios: {e}")
            return []

    def registrar_intento_acceso(self, user_id, status):
        """
        Registra un intento de acceso en la tabla 'access_logs'.

        Args:
            user_id (int or None): ID del usuario que intentó acceso (puede ser None si desconocido).
            status (str): 'aprobado' o 'denegado' según resultado.
        """
        try:
            self.verificar_conexion()
            timestamp = datetime.datetime.now()
            query = "INSERT INTO access_logs (user_id, timestamp, status) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (user_id, timestamp, status))
        except Error as e:
            logger.error(f"Error en registrar_intento_acceso: {e}")

    def cerrar(self):
        """
        Cierra el cursor y la conexión a la base de datos.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Conexión a la base de datos cerrada.")
