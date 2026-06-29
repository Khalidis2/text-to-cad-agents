# app/validators/artifact_validator.py
from pathlib import Path
from app.schemas.models import ValidationIssue, ValidationReport


class ArtifactValidator:
    REQUIRED_SUCCESS_FILES = (
        "request.json",
        "refined_prompt.json",
        "requirements.json",
        "cad_spec.raw.json",
        "cad_spec.json",
        "normalization.json",
        "plan.json",
        "preflight_validation.json",
        "model.py",
        "model.stl",
        "model.step",
        "preview.svg",
        "validation.json",
        "report.json",
    )

    REQUIRED_BUILD_FILES = (
        "model.py",
        "model.stl",
        "model.step",
        "preview.svg",
    )

    def run(self, job_dir: Path, final: bool = False) -> ValidationReport:
        required = self.REQUIRED_SUCCESS_FILES if final else self.REQUIRED_BUILD_FILES
        issues: list[ValidationIssue] = []
        metrics = {"required_files": list(required), "missing_files": []}

        for filename in required:
            path = job_dir / filename
            if not path.exists() or not path.is_file():
                metrics["missing_files"].append(filename)
                issues.append(
                    ValidationIssue(
                        code="MISSING_ARTIFACT",
                        severity="error",
                        message=f"Required output artifact is missing: {filename}",
                        fix_hint="Re-run the build stage or inspect the CAD/export failure before marking the job complete.",
                    )
                )

        return ValidationReport(passed=not issues, issues=issues, metrics=metrics)
