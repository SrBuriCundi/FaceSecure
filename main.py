import cv2
import time
from model.database import Database
from controller.face_controller import FaceController
from view.camera_view import (
    mostrar_resultados, mostrar_mensaje, mostrar_advertencia_multirostro, mostrar_frame
)
import config
from utils.logger_config import logger  # Importar logger para eventos y errores

def main():
    """
    Función principal que ejecuta el ciclo de captura de video,
    procesamiento de reconocimiento facial y manejo de la interfaz.

    Controla la lógica de mostrar mensajes de acceso aprobado/denegado
    y advierte si hay múltiples rostros.
    """
    
    db = Database(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )
    controller = FaceController(db, threshold=config.UMBRAL_RECONOCIMIENTO)

    cap = cv2.VideoCapture(0)
    frame_count = 0
    tiempo_espera = config.TIEMPO_ESPERA_MENSAJE
    tiempo_inicio = None
    ultimo_resultado = None
    mensaje_mostrado = False

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.error("No se pudo leer el frame de la cámara.")
                break

            if frame_count % 5 == 0:
                resultados = controller.procesar_frame(frame)

                if resultados:
                    if len(resultados) > 1:
                        mostrar_advertencia_multirostro()
                        tiempo_inicio = None
                        ultimo_resultado = None
                        mensaje_mostrado = True
                        logger.warning("Se detectaron múltiples rostros simultáneamente.")
                    else:
                        ultimo_resultado = resultados[0]
                        if tiempo_inicio is None:
                            tiempo_inicio = time.time()
                            mensaje_mostrado = False
                else:
                    tiempo_inicio = None
                    ultimo_resultado = None
                    mensaje_mostrado = False

            if ultimo_resultado:
                mostrar_resultados(frame, [ultimo_resultado])
            else:
                mostrar_frame(frame)

            if tiempo_inicio and not mensaje_mostrado:
                if time.time() - tiempo_inicio >= tiempo_espera:
                    nombre, autorizado, _, datos_usuario = ultimo_resultado
                    if autorizado:
                        texto = "ACCESO APROBADO"
                        datos_mostrar = {
                            "Nombre": datos_usuario['nombre'],
                            "ID": datos_usuario['numero_identificacion'],
                            "Rol": datos_usuario['rol'],
                            "Sede": datos_usuario['sede']
                        }
                        logger.info(f"Acceso aprobado para {datos_usuario['nombre']} (ID: {datos_usuario['numero_identificacion']})")
                    else:
                        texto = "ACCESO DENEGADO"
                        datos_mostrar = None
                        logger.info("Acceso denegado para rostro desconocido.")

                    mostrar_mensaje(texto, datos_mostrar)

                    tiempo_inicio = None
                    mensaje_mostrado = True
                    ultimo_resultado = None

            frame_count += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                logger.info("Saliendo por petición del usuario.")
                break

    except Exception as e:
        logger.exception(f"Error inesperado en el ciclo principal: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        db.cerrar()
        logger.info("Recursos liberados y conexión a base de datos cerrada.")

if __name__ == "__main__":
    main()
