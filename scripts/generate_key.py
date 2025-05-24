from cryptography.fernet import Fernet

# Genera una nueva clave simétrica para cifrado con Fernet
key = Fernet.generate_key()

# Guarda la clave generada en un archivo llamado secret.key
with open("secret.key", "wb") as key_file:
    key_file.write(key)

print("Clave generada y guardada en secret.key")
