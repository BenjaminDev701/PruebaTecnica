from dotenv import load_dotenv
import os

# carga las variables de entorno
load_dotenv()

# Nuestra variable de la url a la cual hacemos la peticion
CONTEXT_SERVICE_URL = os.getenv("BASE_URL")
# Nuestra varuable de la API de opne AI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
