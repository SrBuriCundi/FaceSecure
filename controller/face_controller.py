import cv2
import face_recognition
import numpy as np
from model.database import Database
from utils.crypto_utils import descifrar_bytes
from utils.logger_config import logger  # Importa el logger

class FaceController:
    """
    Controlador encargado de manejar la lógica de reconocimiento facial,
    carga de usuarios y procesamiento de frames.

    Args:
        db (Database): Instancia de la clase Database para acceso a datos.
        threshold (float): Umbral de distancia para reconocer un rostro como conocido.
    """
    
    def __init__(self, db: Database, threshold=0.6):
        self.db = db
        self.threshold = threshold
        self.usuarios = []
        self.codificaciones = []
        self.cargar_usuarios()

    def cargar_usuarios(self):
        """
        Carga los usuarios desde la base de datos y descifra las codificaciones faciales.
        Almacena las codificaciones en un arreglo para comparación posterior.
        """
        datos = self.db.obtener_usuarios()
        self.usuarios = datos
        self.codificaciones = []
        for u in datos:
            try:
                face_enc_cifrado = u['face_encoding']
                face_enc_descifrado = descifrar_bytes(face_enc_cifrado)
                codif = np.frombuffer(face_enc_descifrado, dtype=np.float64)
                self.codificaciones.append(codif)
            except Exception as e:
                logger.error(f"Error al descifrar face_encoding del usuario {u.get('nombre', 'desconocido')}: {e}")

    def procesar_frame(self, frame):
        """
        Procesa un frame capturado por la cámara para detectar y reconocer rostros.

        Args:
            frame (numpy.ndarray): Imagen capturada de la cámara.

        Returns:
            list: Lista de tuplas con (nombre, autorizado, ubicacion, datos_usuario)
            para cada rostro detectado en el frame.
        """
        try:
            # Reduce tamaño para acelerar procesamiento
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            ubicaciones_pequenas = face_recognition.face_locations(rgb_small_frame, model="hog")
            codificaciones_frame = face_recognition.face_encodings(rgb_small_frame, ubicaciones_pequenas)

            resultados = []
            if not self.codificaciones or any(c is None for c in self.codificaciones):
                # No hay codificaciones válidas, marca todos como desconocidos
                for ubicacion in ubicaciones_pequenas:
                    resultados.append(("Desconocido", False, self._escalar_ubicacion(ubicacion), None))
                return resultados

            for i, codif in enumerate(codificaciones_frame):
                distancias = face_recognition.face_distance(self.codificaciones, codif)
                min_dist = min(distancias) if len(distancias) > 0 else 1.0
                if min_dist < self.threshold:
                    idx = np.argmin(distancias)
                    user = self.usuarios[idx]
                    self.db.registrar_intento_acceso(user['id'], 'aprobado')
                    resultados.append((user['nombre'], True, self._escalar_ubicacion(ubicaciones_pequenas[i]), user))
                else:
                    self.db.registrar_intento_acceso(None, 'denegado')
                    resultados.append(("Desconocido", False, self._escalar_ubicacion(ubicaciones_pequenas[i]), None))

            return resultados
        except Exception as e:
            logger.error(f"Error al procesar frame: {e}", exc_info=True)
            return []

    def _escalar_ubicacion(self, ubicacion_pequena):
        """
        Escala las coordenadas del rostro desde tamaño reducido al tamaño original.

        Args:
            ubicacion_pequena (tuple): Coordenadas (top, right, bottom, left) en frame reducido.

        Returns:
            tuple: Coordenadas escaladas al tamaño original.
        """
        top, right, bottom, left = ubicacion_pequena
        return (top*4, right*4, bottom*4, left*4)
