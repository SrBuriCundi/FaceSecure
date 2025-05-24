import logging

# Configura el sistema de logging con nivel INFO y formato definido
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("face_secure.log", encoding="utf-8"),  # Agregar encoding UTF-8
        logging.StreamHandler()
    ]
)

# Logger específico para el proyecto FaceSecure
logger = logging.getLogger("FaceSecure")
