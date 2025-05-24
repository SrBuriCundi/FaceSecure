from cryptography.fernet import Fernet

def cargar_clave(ruta_archivo="secret.key"):
    """
    Carga la clave de cifrado almacenada en un archivo.

    Args:
        ruta_archivo (str): Ruta al archivo que contiene la clave.

    Returns:
        bytes: Clave cargada en formato bytes.
    """
    with open(ruta_archivo, "rb") as file:
        return file.read()

# Cargar la clave para usarla globalmente
FERNET_KEY = cargar_clave()
cipher_suite = Fernet(FERNET_KEY)

def cifrar_bytes(data: bytes) -> bytes:
    """
    Cifra datos en bytes usando Fernet.

    Args:
        data (bytes): Datos a cifrar.

    Returns:
        bytes: Datos cifrados.
    """
    return cipher_suite.encrypt(data)

def descifrar_bytes(token: bytes) -> bytes:
    """
    Descifra datos cifrados en bytes usando Fernet.

    Args:
        token (bytes): Datos cifrados.

    Returns:
        bytes: Datos descifrados originales.
    """
    return cipher_suite.decrypt(token)
