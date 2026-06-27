# app/llm/ollama_client.py
import requests
from app.config import settings

class OllamaClient:
    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{settings.ollama_base_url}/api/generate",
            json={"model": settings.ollama_model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "")
