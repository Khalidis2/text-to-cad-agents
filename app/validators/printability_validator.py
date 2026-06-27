# app/validators/printability_validator.py
from app.schemas.models import CadSpec, ValidationReport, ValidationIssue
from app.validators import rules


class PrintabilityValidator:
    def run(self, spec: CadSpec) -> ValidationReport:
        h = spec.hanger
        issues = []
        if h.width_mm < rules.MIN_HANGER_WIDTH_MM or h.height_mm < rules.MIN_HANGER_HEIGHT_MM:
            issues.append(ValidationIssue(code="SIZE_TOO_SMALL", severity="error", message="Part is too small for reliable mirror-hanger use.", fix_hint="Use at least 45 x 30 mm."))
        if h.thickness_mm < rules.MIN_STRUCTURAL_THICKNESS_MM:
            issues.append(ValidationIssue(code="THICKNESS_TOO_SMALL", severity="error", message=f"Structural thickness must be at least {rules.MIN_STRUCTURAL_THICKNESS_MM} mm.", fix_hint="Increase thickness to 3-4 mm."))
        if h.thickness_mm > rules.MAX_STRUCTURAL_THICKNESS_MM:
            issues.append(ValidationIssue(code="THICKNESS_LARGE", severity="warning", message="Part may be unnecessarily heavy for a mirror hanger.", fix_hint="Use 3.5-5 mm unless strength is critical."))
        if h.text.raised_depth_mm < rules.MIN_RAISED_TEXT_DEPTH_MM:
            issues.append(ValidationIssue(code="TEXT_DEPTH_TOO_SMALL", severity="error", message=f"Raised text depth must be at least {rules.MIN_RAISED_TEXT_DEPTH_MM} mm.", fix_hint="Use 0.6-1.0 mm raised depth."))
        if h.text.raised_depth_mm > rules.MAX_RAISED_TEXT_DEPTH_MM:
            issues.append(ValidationIssue(code="TEXT_DEPTH_LARGE", severity="warning", message="Raised text is tall and may print with rough sidewalls.", fix_hint="Use 0.6-1.0 mm for clean raised text."))
        if h.text.min_text_height_mm < rules.MIN_READABLE_TEXT_HEIGHT_MM:
            issues.append(ValidationIssue(code="TEXT_HEIGHT_TOO_SMALL", severity="error", message=f"Text height must be at least {rules.MIN_READABLE_TEXT_HEIGHT_MM} mm.", fix_hint="Use 6 mm or larger for a 0.4 mm nozzle."))
        if h.hole_diameter_mm < rules.MIN_HOLE_DIAMETER_MM:
            issues.append(ValidationIssue(code="HOLE_TOO_SMALL", severity="error", message=f"Hole diameter must be at least {rules.MIN_HOLE_DIAMETER_MM} mm.", fix_hint="Use 5 mm for mirror-hanger strings/chains."))
        edge_clearance = h.hole_center_y_from_top_mm - h.hole_diameter_mm / 2
        if edge_clearance < rules.MIN_EDGE_CLEARANCE_MM:
            issues.append(ValidationIssue(code="HOLE_EDGE_CLEARANCE", severity="error", message="Hole is too close to the top edge.", fix_hint="Keep at least 3 mm material above the hole."))
        side_clearance = min(h.width_mm, h.height_mm) / 2 - h.corner_radius_mm
        if side_clearance < rules.MIN_EDGE_CLEARANCE_MM:
            issues.append(ValidationIssue(code="RADIUS_TOO_LARGE", severity="error", message="Corner radius leaves too little usable material.", fix_hint="Reduce corner radius."))
        if h.width_mm > rules.MAX_HANGER_WIDTH_MM or h.height_mm > rules.MAX_HANGER_HEIGHT_MM:
            issues.append(ValidationIssue(code="SIZE_LARGE", severity="warning", message="Part may be larger than a typical mirror hanger product size.", fix_hint="Stay under 120 x 80 mm for most cars."))
        metrics = {
            "width_mm": h.width_mm,
            "height_mm": h.height_mm,
            "thickness_mm": h.thickness_mm,
            "hole_edge_clearance_mm": edge_clearance,
            "material": h.printer.material,
            "nozzle_mm": h.printer.nozzle_mm,
            "estimated_text_chars": len(h.text.content),
        }
        return ValidationReport(passed=not any(i.severity == "error" for i in issues), issues=issues, metrics=metrics)
