import httpx
from src.config import CONTEXT_SERVICE_URL


async def get_book_context(book_id: str, section_id: str) -> str:
    url = f"{CONTEXT_SERVICE_URL}/context"
    # Informacion del cliente
    payload = {
        "book_id": book_id,
        "section_id": section_id
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            # lanzamos error si es de tipo 400 o 500
            response.raise_for_status()
            # lo que recibimos esta en formato json y lo parseamos para pasarlo a un diccionario
            data = response.json()
            return data.get("content", "")

    except Exception as error:
        # atrapamos el error
        return f"ERROR_DETECTADO: {str(error)} , TIPO_DE_ERROR: {type(error)} , URL_INTENTADA: {url}"
