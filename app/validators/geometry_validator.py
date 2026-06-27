# app/validators/geometry_validator.py
from pathlib import Path
from app.schemas.models import ValidationReport, ValidationIssue


class GeometryValidator:
    def run(self, stl_path: Path | str) -> ValidationReport:
        stl_path = Path(stl_path)
        issues = []
        metrics = {"stl_exists": stl_path.exists(), "stl_bytes": stl_path.stat().st_size if stl_path.exists() else 0}
        if not stl_path.exists():
            issues.append(ValidationIssue(code="STL_MISSING", severity="error", message="STL file was not created.", fix_hint="Check CadQuery build/export errors."))
            return ValidationReport(passed=False, issues=issues, metrics=metrics)
        if metrics["stl_bytes"] < 1024:
            issues.append(ValidationIssue(code="STL_TOO_SMALL", severity="warning", message="STL file is unusually small; geometry may be incomplete.", fix_hint="Inspect generated model visually."))
        try:
            import trimesh
            mesh = trimesh.load_mesh(str(stl_path))
            bounds = mesh.bounds.tolist() if hasattr(mesh, "bounds") else []
            extents = mesh.extents.tolist() if hasattr(mesh, "extents") else []
            metrics.update({
                "is_watertight": bool(mesh.is_watertight),
                "bounds": bounds,
                "extents_mm": extents,
                "volume_mm3": float(mesh.volume) if mesh.is_volume else None,
                "faces": int(len(mesh.faces)) if hasattr(mesh, "faces") else None,
            })
            if not mesh.is_watertight:
                issues.append(ValidationIssue(code="NOT_WATERTIGHT", severity="error", message="Mesh is not watertight/manifold.", fix_hint="Repair boolean unions or export tolerances."))
            if mesh.is_volume and mesh.volume <= 0:
                issues.append(ValidationIssue(code="NON_POSITIVE_VOLUME", severity="error", message="Mesh volume is not positive.", fix_hint="Check solid construction."))
        except Exception as exc:
            issues.append(ValidationIssue(code="GEOMETRY_CHECK_FAILED", severity="warning", message=str(exc), fix_hint="Install trimesh dependencies or inspect STL manually."))
        return ValidationReport(passed=not any(i.severity == "error" for i in issues), issues=issues, metrics=metrics)
