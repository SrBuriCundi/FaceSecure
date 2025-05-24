import pytest
from utils import crypto_utils

# Caso de prueba de cifrado y descifrado
def test_cifrar_y_descifrar():
    # Datos de entrada
    data = b"datos sensibles"
    print(f"Datos de entrada: {data}")

    # Cifrado
    cifrado = crypto_utils.cifrar_bytes(data)
    print(f"Datos cifrados: {cifrado}")

    # Asegurarse de que los datos cifrados no sean iguales a los originales
    assert data != cifrado, "Los datos cifrados no deben ser iguales a los datos originales"
    
    # Descifrado
    descifrado = crypto_utils.descifrar_bytes(cifrado)
    print(f"Datos descifrados: {descifrado}")

    # Asegurarse de que los datos descifrados sean iguales a los datos originales
    assert data == descifrado, "Los datos descifrados deben ser iguales a los datos originales"

    # Confirmar que el cifrado y descifrado funcionaron correctamente
    print("Cifrado y descifrado exitosos.")
