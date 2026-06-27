# app/agents/missing_info_gate.py
from app.schemas.models import Requirements


class MissingInfoGate:
    def run(self, requirements: Requirements) -> tuple[bool, str]:
        hard_missing = [x for x in requirements.missing_critical_info if "Supported product" in x]
        if hard_missing:
            return False, "; ".join(hard_missing)
        if not requirements.supported:
            return False, "Request is outside the currently supported CAD production templates."
        return True, "Build may continue with safe defaults, auto-normalization, and recorded assumptions."
