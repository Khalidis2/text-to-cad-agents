# app/storage/jobs.py
from pathlib import Path
import json
from app.config import settings


def create_job_dir(job_id: str) -> Path:
    path = settings.output_root / job_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_job_dir(job_id: str) -> Path:
    return settings.output_root / job_id


def write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def list_job_files(job_dir: Path) -> list[str]:
    return sorted([p.name for p in job_dir.iterdir() if p.is_file()])
