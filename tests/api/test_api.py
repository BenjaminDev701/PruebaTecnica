from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_peticion_incompleta():
    
    #Verifica que la API rechace peticiones a las que les faltan campos obligatorios.
    
    
    payload_incompleto = {
        "action": "chat",
        "book_id": "book_001"
    }

    response = client.post("/execute", json=payload_incompleto)

    assert response.status_code == 422
    assert "detail" in response.json()


def test_accion_no_soportada_retorna_422():
    
    #Verifica que si un usuario envia una action invalida de las que no estan en el schema  Pydantic lo bloquee respetando el esquema.
   
    
    payload_invalido = {
        "action": "resumen",
        "book_id": "book_001",
        "section_id": "section_04",
        "instructions": "Haz un resumen"
    }

    response = client.post("/execute", json=payload_invalido)

    assert response.status_code == 422
    assert "detail" in response.json()
