import cv2
import face_recognition
import numpy as np
import time
from model.database import Database
from utils.crypto_utils import descifrar_bytes

class FaceController:
    def __init__(self, db: Database, threshold=0.6):
        self.db = db
        self.threshold = threshold
        self.usuarios = []
        self.codificaciones = []
        self.cargar_usuarios()

    def cargar_usuarios(self):
        datos = self.db.obtener_usuarios()
        self.usuarios = datos
        # Descifrar face_encoding antes de convertir a np.array
        self.codificaciones = []
        for u in datos:
            try:
                face_enc_cifrado = u['face_encoding']
                face_enc_descifrado = descifrar_bytes(face_enc_cifrado)
                codif = np.frombuffer(face_enc_descifrado, dtype=np.float64)
                self.codificaciones.append(codif)
            except Exception as e:
                print(f"Error al descifrar face_encoding del usuario {u['nombre']}: {e}")
                self.codificaciones.append(None)

    def procesar_frame(self, frame):
        inicio = time.time()  # Tiempo inicial

        # Tu código actual de procesamiento
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        ubicaciones_pequenas = face_recognition.face_locations(rgb_small_frame, model="hog")
        codificaciones_frame = face_recognition.face_encodings(rgb_small_frame, ubicaciones_pequenas)

        resultados = []
        for i, codif in enumerate(codificaciones_frame):
            distancias = face_recognition.face_distance(self.codificaciones, codif)
            min_dist = min(distancias) if len(distancias) > 0 else 1.0
            if min_dist < self.threshold:
                idx = np.argmin(distancias)
                user = self.usuarios[idx]
                self.db.registrar_intento_acceso(user['id'], 'aprobado')
                top, right, bottom, left = ubicaciones_pequenas[i]
                ubicacion_original = (top*4, right*4, bottom*4, left*4)
                resultados.append((user['nombre'], True, ubicacion_original))
            else:
                self.db.registrar_intento_acceso(None, 'denegado')
                top, right, bottom, left = ubicaciones_pequenas[i]
                ubicacion_original = (top*4, right*4, bottom*4, left*4)
                resultados.append(("Desconocido", False, ubicacion_original))

        fin = time.time()  # Tiempo final
        duracion = fin - inicio
        print(f"Tiempo de procesamiento: {duracion:.3f} segundos")
        return resultados
