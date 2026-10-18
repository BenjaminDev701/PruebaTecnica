import httpx
from src.config import CONTEXT_SERVICE_URL
from fastapi import HTTPException


async def get_book_context(book_id: str, section_id: str) -> str:
    url = f"{CONTEXT_SERVICE_URL}/context"
    # Informacion del cliente
    payload = {
        "book_id": book_id,
        "section_id": section_id
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=10.0)
        if response.status_code != 200:
            error_data = response.json().get("error", {})
            error_code = error_data.get("code", "CONTEXT_ERROR")
            error_msg = error_data.get(
                "message", "Error al consultar el servicio de contexto")
        # Lanzamos un error que será atrapado
            raise HTTPException(
                status_code=response.status_code,
                detail={"code": error_code, "message": error_msg}
            )

    # lo que recibimos esta en formato json y lo parseamos para pasarlo a un diccionario
    data = response.json()
    return data.get("content", "")
