import unittest
import cv2
import numpy as np
from model.database import Database
from controller.face_controller import FaceController
from unittest.mock import MagicMock
from view.camera_view import mostrar_resultados, mostrar_mensaje  # Importar las funciones necesarias
import config

class TestSystem(unittest.TestCase):

    def test_flujo_completo(self):
        # Paso 1: Conectar a la base de datos y controlador
        db = Database(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD, database=config.DB_NAME)
        controller = FaceController(db, threshold=config.UMBRAL_RECONOCIMIENTO)

        # Mock para registrar intentos de acceso
        db.registrar_intento_acceso = MagicMock()

        # Paso 2: Simular la captura de una imagen
        frame = cv2.imread('tests/sample_face.jpg')
        if frame is None:
            frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)  # Si no se encuentra la imagen, usamos un frame blanco

        print(f"Imagen cargada: {frame.shape[0]}x{frame.shape[1]} px")
        
        # Paso 3: Procesar el frame con el controlador
        resultados = controller.procesar_frame(frame)

        # Paso 4: Verificar si el sistema ha identificado al usuario correctamente
        self.assertIsInstance(resultados, list)

        if resultados:
            nombre, autorizado, _, datos_usuario = resultados[0]
            if autorizado:
                print(f"Acceso aprobado para {nombre}. Datos de usuario: {datos_usuario}")
                # Simula la presentación de resultados en la interfaz
                mostrar_resultados(frame, resultados)
                mostrar_mensaje("ACCESO APROBADO", datos_usuario)
            else:
                print(f"Acceso denegado para {nombre}.")
                mostrar_resultados(frame, resultados)
                mostrar_mensaje("ACCESO DENEGADO", datos_usuario)

        # Paso 5: Verificar que el acceso se haya registrado correctamente en la base de datos
        db.registrar_intento_acceso.assert_called()
        print("Registro de intento de acceso verificado.")
        
        # Paso 6: Cerrar la conexión de la base de datos
        db.cerrar()
        print("Conexión a la base de datos cerrada.")

if __name__ == '__main__':
    unittest.main()
