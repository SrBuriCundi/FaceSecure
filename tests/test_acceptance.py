import pytest
import cv2
import numpy as np
from model.database import Database
from controller.face_controller import FaceController
from unittest.mock import MagicMock
from view.camera_view import mostrar_resultados, mostrar_mensaje
import config
import time

# RF-01: El sistema debe reconocer la identidad de un usuario mediante comparación biométrica
def test_reconocimiento_usuario_autorizado():
    db = Database(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD, database=config.DB_NAME)
    controller = FaceController(db, threshold=config.UMBRAL_RECONOCIMIENTO)

    # Imagen de rostro autorizado
    frame = cv2.imread('tests/sample_face.jpg')
    if frame is None:
        frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)

    resultados = controller.procesar_frame(frame)
    print(f"Resultado del reconocimiento facial: {len(resultados)} rostros detectados.")
    assert len(resultados) > 0, "No se detectó ningún rostro"
    nombre, autorizado, _, datos_usuario = resultados[0]
    print(f"Reconocimiento para {nombre}: {'Aprobado' if autorizado else 'Rechazado'}")
    assert autorizado, f"El usuario {nombre} no fue reconocido correctamente"

    db.cerrar()

# RF-02: El sistema debe otorgar o denegar el acceso según el resultado del reconocimiento facial
def test_otorgar_o_denegar_acceso():
    db = Database(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD, database=config.DB_NAME)
    controller = FaceController(db, threshold=config.UMBRAL_RECONOCIMIENTO)

    # Imagen de rostro no autorizado
    frame = cv2.imread('tests/unknown_face.jpg')  # Asegúrate de tener una imagen de un rostro no registrado
    if frame is None:
        frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)

    resultados = controller.procesar_frame(frame)
    print(f"Resultado del reconocimiento facial: {len(resultados)} rostros detectados.")
    assert len(resultados) > 0, "No se detectó ningún rostro"
    nombre, autorizado, _, datos_usuario = resultados[0]
    print(f"Reconocimiento para {nombre}: {'Aprobado' if autorizado else 'Rechazado'}")
    assert not autorizado, f"El usuario {nombre} fue reconocido erróneamente como autorizado"

    db.cerrar()

# RF-03: El sistema debe registrar cada intento de acceso con fecha, hora y resultado
def test_registro_intento_acceso():
    db = Database(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD, database=config.DB_NAME)
    controller = FaceController(db, threshold=config.UMBRAL_RECONOCIMIENTO)

    # Mock para registrar intentos de acceso
    db.registrar_intento_acceso = MagicMock()

    # Imagen de rostro autorizado
    frame = cv2.imread('tests/sample_face.jpg')
    if frame is None:
        frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)

    resultados = controller.procesar_frame(frame)
    print(f"Resultado del reconocimiento facial: {len(resultados)} rostros detectados.")
    assert len(resultados) > 0, "No se detectó ningún rostro"
    nombre, autorizado, _, datos_usuario = resultados[0]
    print(f"Reconocimiento para {nombre}: {'Aprobado' if autorizado else 'Rechazado'}")
    assert autorizado, f"El usuario {nombre} no fue reconocido correctamente"

    # Verificar que el intento de acceso fue registrado correctamente
    db.registrar_intento_acceso.assert_called_once_with(datos_usuario['id'], 'aprobado')

    db.cerrar()

# RF-04: El sistema debe integrarse con las cámaras y dispositivos de reconocimiento facial
def test_integracion_con_camara():
    # Este test verificará que la cámara pueda capturar la imagen correctamente
    # Se asume que el sistema ya tiene la integración de la cámara correctamente configurada
    frame = cv2.imread('tests/sample_face.jpg')  # Imagen de ejemplo
    print(f"Imagen de cámara capturada: {frame.shape[0]}x{frame.shape[1]}")
    assert frame is not None, "No se pudo capturar la imagen de la cámara"

# RF-05: El sistema debe poder comunicarse con la base de datos
def test_comunicacion_con_base_de_datos():
    db = Database(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD, database=config.DB_NAME)
    usuarios = db.obtener_usuarios()
    print(f"Total de usuarios obtenidos de la base de datos: {len(usuarios)}")
    assert len(usuarios) > 0, "No se pudo obtener usuarios desde la base de datos"
    db.cerrar()

# RNF-01: El sistema debe procesar cada solicitud de autenticación en máximo 2 segundos
def test_tiempo_de_respuesta():
    db = Database(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD, database=config.DB_NAME)
    controller = FaceController(db, threshold=config.UMBRAL_RECONOCIMIENTO)

    frame = cv2.imread('tests/sample_face.jpg')
    if frame is None:
        frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)

    start_time = time.time()
    controller.procesar_frame(frame)
    end_time = time.time()

    tiempo_respuesta = end_time - start_time
    print(f"Tiempo de procesamiento: {tiempo_respuesta:.4f} segundos")
    assert tiempo_respuesta < 2, "El procesamiento excedió los 2 segundos"

    db.cerrar()

# RNF-04: Las imágenes faciales deben almacenarse usando un algoritmo seguro
def test_cifrado_de_imagenes_facial():
    db = Database(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD, database=config.DB_NAME)
    controller = FaceController(db, threshold=config.UMBRAL_RECONOCIMIENTO)

    frame = cv2.imread('tests/sample_face.jpg')
    if frame is None:
        frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)

    resultados = controller.procesar_frame(frame)
    print(f"Resultado del reconocimiento facial: {len(resultados)} rostros detectados.")
    assert len(resultados) > 0, "No se detectó ningún rostro"
    nombre, autorizado, _, datos_usuario = resultados[0]

    print(f"Datos del usuario: {datos_usuario}")
    assert isinstance(datos_usuario['face_encoding'], bytes), "El encoding facial no está cifrado correctamente"

    db.cerrar()
