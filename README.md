# Azure OpenAI FastAPI

Endpoint FastAPI para exponer un deployment de Azure OpenAI.

## Requisitos
- Python 3.10+

## Configuracion
Crea un archivo `.env` con:

```
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4.1-nano
```

## Instalacion

```
pip install -r requirements.txt
```

## Ejecutar

```
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

## Uso

```
POST /chat
```

Body ejemplo:

```json
{
  "messages": [
    {"role": "system", "content": "Eres un asistente."},
    {"role": "user", "content": "Hola"}
  ],
  "temperature": 0.7,
  "max_tokens": 256
}
```

Respuesta:

```json
{
  "content": "Hola, en que puedo ayudarte?"
}
```
