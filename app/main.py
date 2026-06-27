# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from app.pipeline.orchestrator import run_pipeline
from app.schemas.api import JobRequest, JobResponse
from app.storage.jobs import get_job_dir, list_job_files


app = FastAPI(title="CAD Production Agent", version="0.2.0")


@app.get("/health")
def health():
    return {"ok": True, "version": "0.2.0", "engine": "cadquery", "mode": "deterministic-production"}


@app.post("/jobs", response_model=JobResponse)
def create_job(request: JobRequest):
    return run_pipeline(request)


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job_dir = get_job_dir(job_id)
    report = job_dir / "report.json"
    if not report.exists():
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "files": list_job_files(job_dir), "report_path": str(report)}


@app.get("/jobs/{job_id}/files/{filename}")
def download_file(job_id: str, filename: str):
    safe_name = Path(filename).name
    path = get_job_dir(job_id) / safe_name
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)
