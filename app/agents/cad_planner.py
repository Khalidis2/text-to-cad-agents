# app/agents/cad_planner.py
from app.schemas.models import CadSpec, BuildPlan


class CadPlannerAgent:
    def run(self, spec: CadSpec) -> BuildPlan:
        risks = []
        operations = [
            "Create rounded rectangular base in millimeters",
            "Cut centered hanging hole with edge clearance",
            "Add raised border if requested",
            "Generate raised text as solid geometry",
            "Export STL and STEP",
            "Run printability and mesh validation",
        ]
        h = spec.hanger
        if h.text.script in {"arabic", "mixed"}:
            risks.append("Arabic or mixed-script text may need vector-outline typography for commercial final output.")
        if len(h.text.content) > 18:
            risks.append("Long text may reduce visual quality; width was normalized where possible.")
        return BuildPlan(
            build_allowed=True,
            reason="Template, dimensions, and material are supported by deterministic production mode.",
            risks=risks,
            operations=operations,
            engine=spec.engine,
            template_id=spec.template_id,
        )
