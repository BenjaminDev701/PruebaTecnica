from src.schemas.request import ExecuteRequest
from fastapi import FastAPI
from dotenv import load_dotenv
from src.services.context_service import get_book_context

load_dotenv()


app = FastAPI(title="Title Prueba tecnica")


@app.post("/execute")
async def execute_task(request: ExecuteRequest):
    # Obtenemos el texto del libro
    texto_del_libro = await get_book_context(request.book_id, request.section_id)

    return {
        "status": "Éxito",
        "texto_recuperado": texto_del_libro
    }
