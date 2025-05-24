# camera_view.py
import cv2
import numpy as np

# Colores institucionales definidos
COLOR_AZUL_OSCURO = (102, 51, 0)
COLOR_VERDE = (57, 150, 0)
COLOR_ROJO = (0, 0, 255)
COLOR_BLANCO = (255, 255, 255)

def fade_out(frame, pasos=10, delay=30):
    """
    Efecto de desvanecimiento (fade out) de una imagen.

    Args:
        frame (numpy.ndarray): Imagen a mostrar.
        pasos (int): Número de pasos para el efecto.
        delay (int): Tiempo en ms entre pasos.
    """
    for alpha in np.linspace(1, 0, pasos):
        overlay = (frame * alpha).astype(np.uint8)
        cv2.imshow("FaceSecure - Control de Acceso", overlay)
        cv2.waitKey(delay)

def fade_in(ventana, pasos=10, delay=30):
    """
    Efecto de aparición (fade in) de una imagen.

    Args:
        ventana (numpy.ndarray): Imagen a mostrar.
        pasos (int): Número de pasos para el efecto.
        delay (int): Tiempo en ms entre pasos.
    """
    for alpha in np.linspace(0, 1, pasos):
        overlay = (ventana * alpha).astype(np.uint8)
        cv2.imshow("FaceSecure - Control de Acceso", overlay)
        cv2.waitKey(delay)

def mostrar_frame(frame):
    """
    Muestra un frame en la ventana principal.

    Args:
        frame (numpy.ndarray): Imagen a mostrar.
    """
    cv2.imshow("FaceSecure - Control de Acceso", frame)

def mostrar_mensaje(texto, datos=None):
    """
    Muestra un mensaje con texto y datos en una ventana con colores institucionales.

    Args:
        texto (str): Mensaje principal (ej. "ACCESO APROBADO").
        datos (dict, optional): Información adicional a mostrar (nombre, ID, etc.).
    """
    w, h = 640, 480
    ventana = np.zeros((h, w, 3), dtype=np.uint8)
    ventana[:] = COLOR_AZUL_OSCURO

    color_texto = COLOR_VERDE if "aprobado" in texto.lower() else COLOR_ROJO
    font = cv2.FONT_HERSHEY_SIMPLEX
    escala = 1.8
    grosor = 4

    (text_w, text_h), _ = cv2.getTextSize(texto, font, escala, grosor)
    x_text = (w - text_w) // 2
    y_text = 120
    cv2.putText(ventana, texto, (x_text, y_text), font, escala, color_texto, grosor)
    cv2.line(ventana, (x_text, y_text + 10), (x_text + text_w, y_text + 10), color_texto, 3)

    if datos:
        y = y_text + 70
        escala_datos = 0.9
        grosor_datos = 2
        for k, v in datos.items():
            texto_linea = f"{k}: {v}"
            (w_text, _), _ = cv2.getTextSize(texto_linea, font, escala_datos, grosor_datos)
            x_dato = (w - w_text) // 2
            cv2.putText(ventana, texto_linea, (x_dato, y), font, escala_datos, COLOR_BLANCO, grosor_datos)
            y += 40

    footer = "Universidad de Cundinamarca"
    (w_footer, _), _ = cv2.getTextSize(footer, font, 0.6, 1)
    x_footer = (w - w_footer) // 2
    cv2.putText(ventana, footer, (x_footer, h - 30), font, 0.6, COLOR_BLANCO, 1)

    fade_out(ventana)
    fade_in(ventana)
    cv2.waitKey(3000)
    cv2.destroyWindow("FaceSecure - Control de Acceso")

def mostrar_advertencia_multirostro():
    """
    Muestra una advertencia cuando se detectan múltiples rostros simultáneamente.
    """
    w, h = 640, 480
    ventana = np.zeros((h, w, 3), dtype=np.uint8)
    ventana[:] = COLOR_ROJO

    texto = "Se detectaron multiples personas.\nPor favor, acerquese uno a la vez."
    font = cv2.FONT_HERSHEY_SIMPLEX
    escala = 1
    grosor = 3

    lineas = texto.split('\n')
    y = 150
    for linea in lineas:
        (w_text, h_text), _ = cv2.getTextSize(linea, font, escala, grosor)
        x_text = (w - w_text) // 2
        cv2.putText(ventana, linea, (x_text, y), font, escala, COLOR_BLANCO, grosor)
        y += h_text + 20

    fade_out(ventana)
    fade_in(ventana)
    cv2.waitKey(3500)
    cv2.destroyWindow("FaceSecure - Control de Acceso")

def mostrar_resultados(frame, resultados):
    """
    Dibuja rectángulos y nombres sobre los rostros detectados en el frame.

    Args:
        frame (numpy.ndarray): Imagen original donde dibujar.
        resultados (list): Lista de tuplas (nombre, autorizado, ubicacion, _).
    """
    for nombre, autorizado, ubicacion, _ in resultados:
        color = COLOR_VERDE if autorizado else COLOR_AZUL_OSCURO
        if ubicacion:
            top, right, bottom, left = ubicacion
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, nombre, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    mostrar_frame(frame)
