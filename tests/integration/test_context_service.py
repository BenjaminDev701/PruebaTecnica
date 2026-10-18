from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import AsyncMock, MagicMock, patch
from src.main import app

client = TestClient(app)


@patch("src.main.get_book_context", new_callable=AsyncMock)
def test_libro_inexistente_retorna_404(mock_get_book_context):
    #Verifica que la API propague el error 404 cuando el libro solicitado no existe, sin ejecutar servicios posteriores.
    payload_404 = {
        "action": "chat",
        "book_id": "book_inexistente",
        "section_id": "section_04",
        "instructions": "Hola"
    }

    mock_get_book_context.side_effect = HTTPException(
        status_code=404,
        detail={"code": "BOOK_NOT_FOUND", "message": "Book not found"}
    )

    response = client.post("/execute", json=payload_404)

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "BOOK_NOT_FOUND"


@patch("src.main.get_book_context", new_callable=AsyncMock)
def test_seccion_inexistente_retorna_404(mock_get_book_context):
    #Confirma que una sección inexistente devuelva 404 correctamente cuando el libro sí existe en el Context Service.
    payload_404_seccion = {
        "action": "quiz",
        "book_id": "book_001",
        "section_id": "section_inexistente",
        "instructions": "Genera un quiz"
    }

    mock_get_book_context.side_effect = HTTPException(
        status_code=404,
        detail={"code": "SECTION_NOT_FOUND", "message": "Section not found"}
    )

    response = client.post("/execute", json=payload_404_seccion)

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "SECTION_NOT_FOUND"


@patch("src.main.generate_content", new_callable=AsyncMock)
@patch("src.services.context_service.httpx.AsyncClient.post", new_callable=AsyncMock)
def test_404_no_invoca_openai(mock_httpx_post, mock_generate_content):
    #Comprueba que un error 404 del contexto detenga el flujo y evite cualquier llamada posterior al servicio de OpenAI.
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {
        "error": {
            "code": "BOOK_NOT_FOUND",
            "message": "Book not found"
        }
    }
    mock_httpx_post.return_value = mock_response

    payload_404 = {
        "action": "chat",
        "book_id": "cualquier_libro",
        "section_id": "section_04",
        "instructions": "Hola"
    }
    response = client.post("/execute", json=payload_404)

    assert response.status_code == 404
    mock_generate_content.assert_not_awaited()