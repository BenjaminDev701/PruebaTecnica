from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Title Prueba tecnica")


@app.get("/healt")
def prueba():
    return {"status": "ok"}
