import cv2
import face_recognition
import numpy as np
import mysql.connector
from mysql.connector import Error

# Importa la función para cifrar los datos
from crypto_utils import cifrar_bytes

def capturar_rostro():
    cap = cv2.VideoCapture(0)
    print("Presiona la tecla 'c' para capturar la foto cuando estés listo.")
    rostro_capturado = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo acceder a la cámara.")
            break
        
        cv2.imshow("Captura de rostro - Presiona 'c' para capturar", frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('c'):
            rostro_capturado = frame
            break
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return rostro_capturado

def registrar_usuario_cam():
    # 1. Capturar rostro con cámara
    imagen = capturar_rostro()
    if imagen is None:
        print("No se capturó ninguna imagen.")
        return False

    # Convertir BGR (OpenCV) a RGB (face_recognition)
    rgb_imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    # 2. Obtener codificación facial
    codificaciones = face_recognition.face_encodings(rgb_imagen)
    if len(codificaciones) == 0:
        print("No se detectó ningún rostro en la imagen capturada.")
        return False
    if len(codificaciones) > 1:
        print("Se detectaron varios rostros. Por favor, captura solo un rostro.")
        return False
    face_encoding = codificaciones[0]
    face_encoding_bytes = face_encoding.tobytes()

    # Cifrar la codificación facial antes de guardar
    face_encoding_cifrado = cifrar_bytes(face_encoding_bytes)

    # 3. Pedir datos al usuario
    nombre = input("Ingrese el nombre completo del usuario: ")
    numero_id = input("Ingrese el número de identificación: ")
    rol = input("Ingrese el rol (Estudiante, Docente, etc.): ")
    codigo_institucional = input("Ingrese el código institucional: ")
    sede = input("Ingrese la sede: ")

    # 4. Guardar en base de datos
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="face_secure"
        )
        cursor = conexion.cursor()
        query = """
        INSERT INTO users (numero_identificacion, nombre, face_encoding, rol, codigo_institucional, sede)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (numero_id, nombre, face_encoding_cifrado, rol, codigo_institucional, sede)
        cursor.execute(query, valores)
        conexion.commit()
        print("Usuario registrado exitosamente.")
        return True

    except Error as e:
        print(f"Error al registrar usuario: {e}")
        return False

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

if __name__ == "__main__":
    registrar_usuario_cam()
