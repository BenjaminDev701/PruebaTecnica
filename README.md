# Prueba Técnica Didacteca - API

API intermediaria construida con FastAPI que conecta el servicio de contexto de libros (Context Service) con OpenAI para generar contenido educativo (Chat, Quizzes y Actividades interactivas), para que las respuestas sean generadas por material proporcionado .

---

## Decisiones Técnicas y Arquitectura

* **FastAPI + Pydantic:** Utilice FastAPI por su rendimiento asíncrono y la integración nativa con Pydantic. los esquemas de entrada y salida validan estrictamente los tipos de datos, si un cliente envía un JSON incompleto o incorrecto, la API responde automáticamente con un error 422 Unprocessable Entity antes de consumir recursos
* **SDK oficial de OpenAI:** Opte por el SDK nativo de OpenAI para mantener la arquitectura ligera y con menor sobrecarga de dependencias para que el servicio de contexto entrega el texto ya filtrado.
* **Control de Alucinaciones:**
  * **Temperatura en 0.0:** Coloque a este nivel la temperatura para que no alucinara o creara informacion que no debia .
  * **System Prompts con reglas estrictas:** Guiamos al modelo a responder únicamente con la información suministrada y a declarar explícitamente si el contexto no es suficiente.
  * **Structured Outputs (client.chat.completions.parse):** En lugar de pedir JSON en texto plano y parsearlo manualmente, se usa la funcionalidad nativa de salidas estructuradas de OpenAI pasando los modelos de Pydantic (`QuizResponse` y `ActivityResponse`), garantizando el cumplimiento del schema y Pyndantic
     Se utiliza en los esquemas para forzar que el campo `"action"` coincida con la operación solicitada (`"chat"`, `"quiz"`, `"activity"`).
* **Manejo de Errores e Integración HTTP:** Se utiliza `httpx.AsyncClient` con timeout para que el programa no se quede esperando una respuesta y si el servicio de contexto responde con un código de error o no encuentra el recurso, la excepción se captura y se propaga limpiamente a través de un `HTTPException` de FastAPI, evitando caídas del servidor.

## Documento de Decisiones (Respuestas Tecnicas)
**1. ¿Como dividiste el problema?**
Separe las responsabilidades en 3 capas: Controladores (`main.py` para enrutar), Servicios (`context_service` para HTTP externo y `ai_service` para logica de OpenAI) y Esquemas (`schemas` para validacion de datos), todo esta estructuracion fue por que decidi usar Arquitectura en capas.

**2. ¿Por que elegiste esta arquitectura?**
Use Arquitectura en capas porque la arquitectura separa las responsabilidades y nos ayuda a evitar mezclar la logica del negocio, tener mejor escalabilidad,mantenibilidad y simplicidad

**3. ¿Que situaciones consideraste problematicas?**
- **Informacion insuficiente en el texto:** Si la respuesta a la duda del usuario no se encuentra de forma explicita en la seccion recuperada, el sistema esta programado para reconocer esa limitacion y negar la respuesta, en lugar de completar la informacion usando conocimiento general del LLM.
- **Libros o secciones inexistentes:** Si el Context Service devuelve un error 404, la API interrumpe el flujo de inmediato y no realiza llamadas a OpenAI, evitando procesar peticiones sin sustento y cuidando la cuota de la API.
- **Instrucciones fuera de alcance o ambiguas:** Mediante el System Prompt restrictivo y la temperatura en 0.0, se previene que la IA actue como un chat de proposito general o intente responder peticiones que se salgan del contexto educativo proporcionado.
- **Datos incompletos en la solicitud:** Si faltan parametros esenciales (`book_id` o `section_id`), el sistema rechaza la peticion desde la validacion de entrada (Pydantic) en lugar de asumir identificadores por defecto o inventar contenidos.

**4. ¿Que limitaciones tiene tu solucion?**
- **Dependencia de la longitud del contexto:** Asumimos que la seccion recuperada cabe integramente en la ventana de contexto de `gpt-4.1-mini`, si el Context Service devuelve una seccion extremadamente extensa, el modelo podria ignorar fragmentos intermedios del texto o degradar la precision de los Quizzes.
- **Sensibilidad a la calidad del texto de origen:** Si la seccion del libro viene con texto sucio, tablas complejas mal formateadas o referencias a imagenes no convertidas a texto, la calidad del contenido generado disminuira, ya que no se implemento un pipeline de limpieza o normalizacion del texto.
- **Latencia acumulada por procesamiento sincrono:** Cada peticion realiza dos llamadas HTTP consecutivas como Context Service + OpenAI, al generar respuestas estructuradas complejas (como Quizzes o Actividades largas), el tiempo de espera puede ser de varios segundos, lo que podria causar timeouts en clientes con redes lentas.

**5. ¿Que mejorarias si tuvieras mas tiempo?**
Implementaria un sistema de Cache como Redis para guardar el contexto de los libros mas solicitados y no pegarle al Context Service en cada request y tambien implementaria Server-Sent Events Streaming para el Chat, asi el usuario ve la respuesta escribirse en tiempo real.

**6. ¿Como evaluarias si el sistema funciona correctamente?**
A nivel codigo, mediante una suite de pruebas de integracion con `pytest` mockeando las llamadas externas Y al nivel de pruebas con IA, realizaria pruebas de alucinacion 

Se implementaron las 3 capacidades completas que fue el Chat, Quiz, Activity



## Requisitos

* Python 3.10 o superior
* Llave de API de OpenAI (`OPENAI_API_KEY`)
* URL base del servicio de contexto (`BASE_URL`)

---

## Instalación y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/BenjaminDev701/PruebaTecnica.git
cd PruebaTecnica
```

### 2. Crear y activar el entorno virtual
En Windows (PowerShell):
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo .env en la raíz del proyecto con la siguiente estructura:
```env
OPENAI_API_KEY=tu_api_key_de_openai
BASE_URL=https://url-del-context-service
```

### 5. Iniciar el servidor
```bash
uvicorn src.main:app --reload
```

El servidor estara disponible en `http://127.0.0.1:8000`.

## Pruebas y Documentación Interactiva (Swagger)

FastAPI genera automáticamente la documentación de la API, con el servidor en ejecución, abre en tu navegador:

**http://127.0.0.1:8000/docs**

Desde la interfaz de Swagger puedes cunado presionas Try it out en el endpoint `POST /execute` y enviar cualquiera de los siguientes ejemplos en el cuerpo de la peticion la cual Request body:

### 1. Chat educativo
```json
{
  "action": "chat",
  "book_id": "book_001",
  "section_id": "section_04",
  "instructions": "¿Qué es el discriminante en una ecuación cuadrática?"
}
```

### 2. Quiz estructurado
```json
{
  "action": "quiz",
  "book_id": "book_001",
  "section_id": "section_04",
  "instructions": "Genera un quiz de 3 preguntas de opción múltiple"
}
```

### 3. Actividad interactiva
```json
{
  "action": "activity",
  "book_id": "book_001",
  "section_id": "section_04",
  "instructions": "Crea una actividad grupal para entender la fórmula general"
}
```
## Ejecución de pruebas

Con el entorno virtual activado, ejecuta:

```bash
pytest -q