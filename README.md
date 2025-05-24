# FaceSecure

Sistema de control de acceso basado en reconocimiento facial para la Universidad de Cundinamarca.

## Descripción

FaceSecure es una aplicación desarrollada en Python que permite autenticar usuarios en tiempo real mediante reconocimiento facial. El sistema captura imágenes desde una cámara, procesa y compara las codificaciones faciales con una base de datos MySQL cifrada, registrando los intentos de acceso aprobados o denegados. Cumple con la Ley 1581 de protección de datos personales (Colombia) gracias al cifrado de los datos biométricos. Está diseñado bajo una arquitectura MVC para facilitar su mantenimiento y escalabilidad.

## Características principales

- Captura y procesamiento de video en tiempo real con OpenCV.  
- Reconocimiento facial con la librería `face_recognition` (basada en dlib).  
- Almacenamiento seguro de codificaciones faciales cifradas usando `cryptography`.  
- Base de datos MySQL para usuarios y registros de acceso con manejo de conexión robusto.  
- Registro automático de intentos de acceso con fecha, hora y estado.  
- Modularidad mediante arquitectura MVC (Modelo-Vista-Controlador).  
- Control de acceso con umbral configurable para autenticación.  
- Manejo profesional de logs para auditoría y depuración.
- Manejo de múltiples rostros detectados con advertencia visual.
- Pruebas unitarias, de integración y de aceptación para asegurar calidad.



## Tecnologías y librerías

- Python 3.7 o superior
- OpenCV (`opencv-python`)  
- face_recognition  
- NumPy  
- mysql-connector-python  
- cryptography  
- pytest y unittest para testing

## Requisitos previos

- Python 3.7 o superior  
- MySQL (puede ser XAMPP o servidor MySQL local)  
- Herramientas de compilación para `dlib` (CMake, compilador C++)  
- Cámara web o dispositivo de captura compatible
- Dependencias del sistema instaladas (según requirements.txt)  

## Instalación

1. Clonar el repositorio o copiar los archivos del proyecto.

2. Crear y activar un entorno virtual:
python -m venv venv
- Windows PowerShell
.\venv\Scripts\Activate.ps1
- Linux/macOS
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
- Los logs se almacenan en face_secure.log con codificación UTF-8.
- En caso de detectar múltiples rostros simultáneos, el sistema muestra una advertencia visual y no concede acceso para evitar falsos positivos.

## Configuración
- Parámetros de conexión a la base de datos y otros valores globales se definen en config.py.
- Umbral de reconocimiento facial configurable (distancia máxima aceptada).
- Tiempo para mostrar mensajes de aprobación o denegación configurable.

## Arquitectura
- Modelo: Gestiona la base de datos y la persistencia de datos (model/database.py).
- Controlador: Lógica de reconocimiento facial y manejo de usuarios (controller/face_controller.py).
- Vista: Interfaz visual con OpenCV para mostrar cámara, resultados y mensajes (view/camera_view.py).
- Utils: Funciones auxiliares para cifrado y logging (utils/crypto_utils.py, utils/logger_config.py).
- Ejecución: Archivo principal que coordina la captura de video y la lógica (main.py).

## Testing
El proyecto cuenta con pruebas automatizadas para asegurar la calidad:
- Unitarias: Validan componentes individuales (test_database.py, test_crypto_utils.py, test_face_controller.py).
- Integración: Verifican flujo completo entre módulos (test_integration.py, test_system.py).
- Aceptación: Aseguran que requisitos funcionales se cumplan (test_acceptance.py).

Los reportes de pruebas se pueden generar con pytest y se excluyen del repositorio para evitar subir archivos temporales.

## Consideraciones adicionales
- El sistema procesa frames cada 5 ciclos para mejorar rendimiento.
- El umbral de reconocimiento facial es configurable en config.py.
- La cámara debe tener buena iluminación para mayor precisión.
- El sistema advierte visualmente si se detectan múltiples rostros simultáneamente, rechazando el acceso.
- Se usa arquitectura MVC para una mejor organización del código.
- Es necesario contar con las dependencias del sistema para compilar dlib y face_recognition.
- Se debe proteger el archivo de clave secret.key y no compartirlo públicamente.
- Se ignoran archivos sensibles en .gitignore (logs, claves, cache).

## Licencia
Este proyecto es para uso académico y de desarrollo interno. No se otorgan garantías ni soporte comercial.

