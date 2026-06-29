# tests/test_artifact_validator.py
from app.validators.artifact_validator import ArtifactValidator


def test_artifact_validator_passes_when_build_files_exist(tmp_path):
    for filename in ArtifactValidator.REQUIRED_BUILD_FILES:
        (tmp_path / filename).write_text("ok", encoding="utf-8")

    report = ArtifactValidator().run(tmp_path)

    assert report.passed is True
    assert report.issues == []


def test_artifact_validator_fails_when_build_file_is_missing(tmp_path):
    (tmp_path / "model.py").write_text("ok", encoding="utf-8")

    report = ArtifactValidator().run(tmp_path)

    assert report.passed is False
    assert any(issue.code == "MISSING_ARTIFACT" for issue in report.issues)
    assert "model.stl" in report.metrics["missing_files"]
