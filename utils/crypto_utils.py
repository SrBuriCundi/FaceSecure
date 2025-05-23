from cryptography.fernet import Fernet

def cargar_clave(ruta_archivo="secret.key"):
    with open(ruta_archivo, "rb") as file:
        return file.read()

FERNET_KEY = cargar_clave()
cipher_suite = Fernet(FERNET_KEY)

def cifrar_bytes(data: bytes) -> bytes:
    return cipher_suite.encrypt(data)

def descifrar_bytes(token: bytes) -> bytes:
    return cipher_suite.decrypt(token)
