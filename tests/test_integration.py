import cv2
import numpy as np
from model.database import Database
from controller.face_controller import FaceController
import config

# Prueba de flujo completo
def test_flujo_completo():
    # Paso 1: Conectar a la base de datos y controlador
    db = Database(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD, database=config.DB_NAME)
    controller = FaceController(db, threshold=config.UMBRAL_RECONOCIMIENTO)

    # Paso 2: Cargar una imagen de prueba o crear un frame blanco si no está disponible
    frame = cv2.imread('tests/sample_face.jpg')
    if frame is None:
        frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)  # Si no se encuentra la imagen, usamos un frame blanco
    print(f"Imagen cargada con dimensiones: {frame.shape[0]}x{frame.shape[1]}")

    # Paso 3: Procesar el frame con el controlador
    resultados = controller.procesar_frame(frame)
    print(f"Resultados del procesamiento: {len(resultados)} rostros detectados.")

    # Verificación de los resultados
    assert isinstance(resultados, list), "El resultado no es una lista"
    
    # Detalles adicionales
    if len(resultados) > 0:
        print(f"Rostro detectado: {resultados[0]}")  # Mostrar detalles del primer rostro procesado

    # Cerrar la conexión con la base de datos
    db.cerrar()
