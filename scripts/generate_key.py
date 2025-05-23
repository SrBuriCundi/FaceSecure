from cryptography.fernet import Fernet

key = Fernet.generate_key()

# Guardar la clave en un archivo .key
with open("secret.key", "wb") as key_file:
    key_file.write(key)

print("Clave generada y guardada en secret.key")
