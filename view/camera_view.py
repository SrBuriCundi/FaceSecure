import cv2

def mostrar_resultados(frame, resultados):
    for nombre, autorizado, ubicacion in resultados:
        color = (0, 255, 0) if autorizado else (0, 0, 255)
        if ubicacion:
            top, right, bottom, left = ubicacion
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, nombre, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow("FaceSecure - Control de Acceso", frame)
