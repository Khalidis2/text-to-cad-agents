# app/cad/builder.py
from pathlib import Path
from pydantic import BaseModel
from app.schemas.models import CadSpec
from app.cad.templates.mirror_hanger import build_mirror_hanger, write_source_file
from app.cad.exporters import export_step, export_stl
from app.cad.preview import write_svg_preview


class BuildResult(BaseModel):
    source_path: str
    stl_path: str
    step_path: str
    preview_path: str


class CadBuilder:
    def build(self, spec: CadSpec, job_dir: Path) -> BuildResult:
        if spec.product_type != "car_mirror_hanger":
            raise ValueError(f"Unsupported product_type: {spec.product_type}")
        model = build_mirror_hanger(spec.hanger)
        source_path = job_dir / "model.py"
        stl_path = job_dir / "model.stl"
        step_path = job_dir / "model.step"
        preview_path = job_dir / "preview.svg"
        write_source_file(spec, source_path)
        export_stl(model, stl_path)
        export_step(model, step_path)
        write_svg_preview(spec, preview_path)
        return BuildResult(source_path=str(source_path), stl_path=str(stl_path), step_path=str(step_path), preview_path=str(preview_path))
