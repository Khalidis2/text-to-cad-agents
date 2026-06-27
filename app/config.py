# app/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    llm_provider: str = "deterministic"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen2.5-coder:14b"
    output_root: Path = Path("outputs/jobs")
    default_printer: str = "Bambu Lab A1"
    default_nozzle_mm: float = 0.4
    default_material: str = "PLA"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
