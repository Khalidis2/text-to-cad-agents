# app/agents/visual_critic.py
from app.schemas.models import CadSpec, ValidationIssue


class VisualCriticAgent:
    def run(self, spec: CadSpec) -> list[ValidationIssue]:
        issues = []
        h = spec.hanger
        if len(h.text.content) > 18:
            issues.append(ValidationIssue(code="TEXT_LONG", severity="warning", message="Text may look crowded; use a wider hanger, shorter wording, or stacked layout.", fix_hint="Increase width or shorten text."))
        if h.width_mm / h.height_mm < 1.35:
            issues.append(ValidationIssue(code="PROPORTION", severity="warning", message="Shape is close to square; wider proportions usually look more premium for mirror hangers.", fix_hint="Use width/height ratio of 1.55 to 1.75."))
        if h.hole_center_y_from_top_mm + h.hole_diameter_mm / 2 > h.height_mm * 0.33:
            issues.append(ValidationIssue(code="HOLE_LOW", severity="warning", message="Hanging hole is visually low and may crowd the text area.", fix_hint="Move the hole closer to the top while keeping edge clearance."))
        return issues
