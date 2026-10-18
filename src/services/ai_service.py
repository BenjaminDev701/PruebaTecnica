
from openai import AsyncOpenAI
from src.config import OPENAI_API_KEY


client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def generate_content(context_text: str, instructions: str) -> str:

    system_prompt = f"""
    Eres un asistente educativo experto y muy estricto.
    Tu tarea es responder a la instrucción del usuario utilizando ÚNICAMENTE la información de contexto proporcionada abajo.
    
    REGLAS INNEGOCIABLES:
    - NO utilices conocimiento previo ni información externa.
    - NO inventes ni deduzcas datos que no estén explícitamente en el contexto.
    - Si la información en el contexto no es suficiente para responder la pregunta de forma completa y precisa, DEBES responder textualmente: "Lo siento, la información del libro no es suficiente para responder a esto."
    
    INFORMACIÓN DE CONTEXTO:
    {context_text}"""

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": instructions}
        ],
        temperature=0.0
    )

    return response.choices[0].message.content
