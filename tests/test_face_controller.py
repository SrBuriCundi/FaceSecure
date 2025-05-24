import numpy as np
from unittest.mock import MagicMock
from controller.face_controller import FaceController
from utils import crypto_utils

# Prueba de carga de usuarios
def test_cargar_usuarios():
    mock_db = MagicMock()
    # Codificación facial dummy cifrada
    raw_encoding = np.random.rand(128).tobytes()
    encrypted_encoding = crypto_utils.cifrar_bytes(raw_encoding)

    usuario = {
        'id': 1,
        'nombre': 'UsuarioTest',
        'face_encoding': encrypted_encoding
    }
    mock_db.obtener_usuarios.return_value = [usuario]
    mock_db.registrar_intento_acceso = MagicMock()

    controller = FaceController(mock_db, threshold=0.6)
    controller.cargar_usuarios()

    # Detalles para el reporte
    print(f"Total de usuarios cargados: {len(controller.codificaciones)}")
    print(f"Primer usuario cargado: {usuario['nombre']}, Codificación facial: {usuario['face_encoding']}")

    assert len(controller.codificaciones) >= 1

# Prueba de procesamiento de frame desconocido
def test_procesar_frame_desconocido():
    mock_db = MagicMock()
    # Codificación facial dummy cifrada
    raw_encoding = np.random.rand(128).tobytes()
    encrypted_encoding = crypto_utils.cifrar_bytes(raw_encoding)

    usuario = {
        'id': 1,
        'nombre': 'UsuarioTest',
        'face_encoding': encrypted_encoding
    }
    mock_db.obtener_usuarios.return_value = [usuario]
    mock_db.registrar_intento_acceso = MagicMock()

    controller = FaceController(mock_db, threshold=0.6)

    # Imagen de prueba (frame vacío)
    frame = np.zeros((480, 640, 3), dtype=np.uint8)

    resultados = controller.procesar_frame(frame)
    
    # Detalles para el reporte
    print(f"Resultado del procesamiento del frame: {len(resultados)} rostros detectados.")
    print(f"¿Resultado esperado?: {'Sí' if isinstance(resultados, list) else 'No'}")
    
    assert isinstance(resultados, list)
