# FaceSecure

Sistema de control de acceso basado en reconocimiento facial para la Universidad de Cundinamarca.

## Descripción

FaceSecure es una aplicación desarrollada en Python que permite autenticar usuarios en tiempo real mediante reconocimiento facial. El sistema captura imágenes desde una cámara, procesa y compara las codificaciones faciales con una base de datos MySQL cifrada, registrando los intentos de acceso aprobados o denegados. Cumple con la Ley 1581 de protección de datos personales (Colombia) gracias al cifrado de los datos biométricos.

## Características principales

- Captura y procesamiento de video en tiempo real con OpenCV.  
- Reconocimiento facial con la librería `face_recognition` (basada en dlib).  
- Almacenamiento seguro de codificaciones faciales cifradas usando `cryptography`.  
- Base de datos MySQL para usuarios y registros de acceso.  
- Registro automático de intentos de acceso con fecha, hora y estado.  
- Modularidad mediante arquitectura MVC (Modelo-Vista-Controlador).  
- Control de acceso con umbral configurable para autenticación.  

## Tecnologías y librerías

- Python 3.x  
- OpenCV (`opencv-python`)  
- face_recognition  
- NumPy  
- mysql-connector-python  
- cryptography  

## Requisitos previos

- Python 3.7 o superior  
- MySQL (puede ser XAMPP o servidor MySQL local)  
- Herramientas de compilación para `dlib` (CMake, compilador C++)  
- Cámara web o dispositivo de captura compatible  

## Instalación

1. Clonar el repositorio o copiar los archivos del proyecto.

2. Crear y activar un entorno virtual:
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Linux/macOS
source venv/bin/activate

3. Instalar dependencias:
pip install -r requirements.txt

4. Configurar la base de datos MySQL:
- Crear la base de datos face_secure.
- Crear las tablas users y access_logs con los siguientes campos:
    CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_identificacion VARCHAR(50),
    nombre VARCHAR(100),
    face_encoding BLOB,
    rol VARCHAR(50),
    codigo_institucional VARCHAR(50),
    sede VARCHAR(50)
    );

    CREATE TABLE access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    timestamp DATETIME,
    status ENUM('aprobado', 'denegado'),
    FOREIGN KEY (user_id) REFERENCES users(id)
    );

5. Generar la clave de cifrado ejecutando el script que crea el archivo secret.key.

## Uso
- Ejecutar el script para registrar usuarios con cámara:
    python agregar.py
- Ejecutar la aplicación principal para control de acceso en tiempo real:
    python main.py
- Para salir de la cámara, presionar la tecla q.

## Seguridad y privacidad
- Los vectores faciales se almacenan cifrados en la base de datos.
- La clave de cifrado se guarda en secret.key y debe protegerse adecuadamente.
- El sistema registra todos los intentos de acceso para auditoría.

## Consideraciones adicionales
- Para mejorar el rendimiento, se procesan frames cada N ciclos (configurable).
- El umbral de reconocimiento facial es configurable en FaceController.
- La cámara debe tener buena iluminación para mejor precisión.
- Es necesario contar con las dependencias del sistema para compilar dlib y face_recognition.

## Licencia
Este proyecto es para uso académico y de desarrollo interno. No se otorgan garantías ni soporte comercial.

