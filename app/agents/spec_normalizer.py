# app/agents/spec_normalizer.py
from copy import deepcopy
from app.schemas.models import CadSpec, ValidationIssue
from app.validators import rules


class SpecNormalizerAgent:
    def run(self, spec: CadSpec) -> tuple[CadSpec, list[ValidationIssue]]:
        fixed = deepcopy(spec)
        h = fixed.hanger
        issues: list[ValidationIssue] = []

        def clamp(attr: str, minimum: float | None = None, maximum: float | None = None):
            value = getattr(h, attr)
            new_value = value
            if minimum is not None and value < minimum:
                new_value = minimum
            if maximum is not None and new_value > maximum:
                new_value = maximum
            if new_value != value:
                setattr(h, attr, new_value)
                issues.append(ValidationIssue(code="AUTO_NORMALIZED", severity="info", message=f"{attr} changed from {value} mm to {new_value} mm for printability."))

        clamp("width_mm", rules.MIN_HANGER_WIDTH_MM, rules.MAX_HANGER_WIDTH_MM)
        clamp("height_mm", rules.MIN_HANGER_HEIGHT_MM, rules.MAX_HANGER_HEIGHT_MM)
        clamp("thickness_mm", rules.MIN_STRUCTURAL_THICKNESS_MM, rules.MAX_STRUCTURAL_THICKNESS_MM)
        clamp("hole_diameter_mm", rules.MIN_HOLE_DIAMETER_MM, rules.MAX_HOLE_DIAMETER_MM)
        clamp("border_mm", rules.MIN_EDGE_CLEARANCE_MM, 8.0)
        clamp("corner_radius_mm", 1.0, min(h.width_mm, h.height_mm) / 3)
        h.text.raised_depth_mm = max(h.text.raised_depth_mm, rules.MIN_RAISED_TEXT_DEPTH_MM)
        h.text.min_text_height_mm = max(h.text.min_text_height_mm, rules.MIN_READABLE_TEXT_HEIGHT_MM)
        min_hole_y = h.hole_diameter_mm / 2 + rules.MIN_EDGE_CLEARANCE_MM
        max_hole_y = h.height_mm / 2 - rules.MIN_EDGE_CLEARANCE_MM
        if h.hole_center_y_from_top_mm < min_hole_y:
            old = h.hole_center_y_from_top_mm
            h.hole_center_y_from_top_mm = min_hole_y
            issues.append(ValidationIssue(code="AUTO_NORMALIZED", severity="info", message=f"hole_center_y_from_top_mm changed from {old} mm to {h.hole_center_y_from_top_mm} mm."))
        if h.hole_center_y_from_top_mm > max_hole_y:
            old = h.hole_center_y_from_top_mm
            h.hole_center_y_from_top_mm = max_hole_y
            issues.append(ValidationIssue(code="AUTO_NORMALIZED", severity="info", message=f"hole_center_y_from_top_mm changed from {old} mm to {h.hole_center_y_from_top_mm} mm."))
        fixed.revision = spec.revision + (1 if issues else 0)
        return fixed, issues
