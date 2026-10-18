from src.services.ai_service import generate_activity
from src.services.ai_service import generate_quiz
from fastapi.exceptions import HTTPException
from src.schemas.responses import ChatResponse
from src.services.ai_service import generate_content
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

    if request.action == "chat":
        respuesta_ia = await generate_content(texto_del_libro, request.instructions)
        return ChatResponse(
            action="chat",
            answer=respuesta_ia
        )

    elif request.action == "quiz":
        quiz_ia = await generate_quiz(texto_del_libro, request.instructions)
        return quiz_ia

    elif request.action == "activity":
        activity_ia = await generate_activity(texto_del_libro, request.instructions)
        return activity_ia

    raise HTTPException(status_code=400, detail="Acción no soportada todavía")
