# tests/test_pipeline.py
import importlib.util
import pytest

cadquery_available = importlib.util.find_spec("cadquery") is not None


@pytest.mark.skipif(not cadquery_available, reason="CadQuery is required for full CAD export test")
def test_pipeline_generates_job():
    from app.schemas.api import JobRequest
    from app.pipeline.orchestrator import run_pipeline

    result = run_pipeline(JobRequest(text="Make a premium car mirror hanger with name Khaled", material="PLA"))
    assert result.job_id
    assert result.build_allowed is True
    assert "report.json" in result.files
