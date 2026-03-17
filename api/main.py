from __future__ import annotations

import logging
import os
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import APIConnectionError, APIStatusError, APITimeoutError, AzureOpenAI
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="Azure OpenAI FastAPI")
logger = logging.getLogger("function_app")

class ChatMessage(BaseModel):
    role: str = Field(..., description="system|user|assistant")
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 512

class ChatResponse(BaseModel):
    content: str

@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "configured": {
            "endpoint": bool(os.getenv("AZURE_OPENAI_ENDPOINT")),
            "api_key": bool(os.getenv("AZURE_OPENAI_API_KEY")),
            "deployment": bool(os.getenv("AZURE_OPENAI_DEPLOYMENT")),
        },
    }

def get_client() -> AzureOpenAI:
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    if not endpoint or not api_key:
        raise HTTPException(
            status_code=500,
            detail="Missing AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_API_KEY",
        )

    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not deployment:
        raise HTTPException(status_code=500, detail="Missing AZURE_OPENAI_DEPLOYMENT")

    client = get_client()
    try:
        result = client.chat.completions.create(
            model=deployment,
            messages=[m.model_dump() for m in req.messages],
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        )
    except APIConnectionError as exc:
        logger.exception("Azure OpenAI connection failed")
        raise HTTPException(
            status_code=502,
            detail="Azure OpenAI connection failed",
        ) from exc
    except APITimeoutError as exc:
        logger.exception("Azure OpenAI request timed out")
        raise HTTPException(
            status_code=504,
            detail="Azure OpenAI request timed out",
        ) from exc
    except APIStatusError as exc:
        logger.exception("Azure OpenAI returned status %s", exc.status_code)
        raise HTTPException(
            status_code=502,
            detail=f"Azure OpenAI returned status {exc.status_code}",
        ) from exc

    content = result.choices[0].message.content or ""
    return ChatResponse(content=content)
