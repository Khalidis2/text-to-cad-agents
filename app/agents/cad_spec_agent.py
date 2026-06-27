# app/agents/cad_spec_agent.py
from app.schemas.models import Requirements, CadSpec


class CadSpecAgent:
    def run(self, requirements: Requirements, quality_mode: str = "production") -> CadSpec:
        if not requirements.hanger:
            raise ValueError("Hanger specification is required")
        return CadSpec(
            product_type="car_mirror_hanger",
            template_id="mirror_hanger_rounded_v1",
            hanger=requirements.hanger,
            quality_mode=quality_mode,
        )
