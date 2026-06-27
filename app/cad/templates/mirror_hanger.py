# app/cad/templates/mirror_hanger.py
from pathlib import Path
import cadquery as cq
from app.schemas.models import HangerSpec, CadSpec


def rounded_rect_2d(width: float, height: float, radius: float):
    radius = max(0.5, min(radius, width / 2 - 0.5, height / 2 - 0.5))
    x = width / 2 - radius
    y = height / 2 - radius
    return (
        cq.Workplane("XY")
        .moveTo(-x, -height / 2)
        .lineTo(x, -height / 2)
        .radiusArc((width / 2, -y), radius)
        .lineTo(width / 2, y)
        .radiusArc((x, height / 2), radius)
        .lineTo(-x, height / 2)
        .radiusArc((-width / 2, y), radius)
        .lineTo(-width / 2, -y)
        .radiusArc((-x, -height / 2), radius)
        .close()
    )


def build_mirror_hanger(spec: HangerSpec):
    base = rounded_rect_2d(spec.width_mm, spec.height_mm, spec.corner_radius_mm).extrude(spec.thickness_mm)
    hole_y = spec.height_mm / 2 - spec.hole_center_y_from_top_mm
    base = base.faces(">Z").workplane().center(0, hole_y).hole(spec.hole_diameter_mm)
    if spec.add_border and spec.border_mm >= 1.2:
        border_height = min(0.55, spec.text.raised_depth_mm * 0.7)
        outer = rounded_rect_2d(spec.width_mm - spec.border_mm, spec.height_mm - spec.border_mm, max(0.5, spec.corner_radius_mm - spec.border_mm / 2))
        inner = rounded_rect_2d(spec.width_mm - spec.border_mm * 2.3, spec.height_mm - spec.border_mm * 2.3, max(0.5, spec.corner_radius_mm - spec.border_mm))
        border = outer.extrude(border_height).cut(inner.extrude(border_height + 0.2)).translate((0, 0, spec.thickness_mm))
        base = base.union(border)
    text_y = -spec.height_mm * 0.08 if spec.text.placement == "center" else (-spec.height_mm * 0.22 if spec.text.placement == "lower" else spec.height_mm * 0.14)
    text_height = _text_height(spec)
    try:
        text_solid = (
            cq.Workplane("XY")
            .text(spec.text.content, text_height, spec.text.raised_depth_mm, font=spec.text.font, halign="center", valign="center")
            .translate((0, text_y, spec.thickness_mm))
        )
        return base.union(text_solid)
    except Exception:
        safe_width = min(spec.width_mm - spec.border_mm * 4, max(18.0, len(spec.text.content) * text_height * 0.45))
        fallback = cq.Workplane("XY").rect(safe_width, text_height * 0.55).extrude(spec.text.raised_depth_mm).translate((0, text_y, spec.thickness_mm))
        return base.union(fallback)


def _text_height(spec: HangerSpec) -> float:
    chars = max(1, len(spec.text.content))
    max_by_width = (spec.width_mm - spec.border_mm * 4) / max(3.5, chars * 0.62)
    return max(spec.text.min_text_height_mm, min(14.0, max_by_width))


def write_source_file(spec: CadSpec, path: Path):
    content = f'''# model.py
import cadquery as cq
from app.cad.templates.mirror_hanger import build_mirror_hanger
from app.schemas.models import HangerSpec, TextSpec, PrinterSpec

spec = HangerSpec(
    width_mm={spec.hanger.width_mm},
    height_mm={spec.hanger.height_mm},
    thickness_mm={spec.hanger.thickness_mm},
    corner_radius_mm={spec.hanger.corner_radius_mm},
    hole_diameter_mm={spec.hanger.hole_diameter_mm},
    hole_center_y_from_top_mm={spec.hanger.hole_center_y_from_top_mm},
    border_mm={spec.hanger.border_mm},
    text=TextSpec(content={spec.hanger.text.content!r}, script={spec.hanger.text.script!r}, raised_depth_mm={spec.hanger.text.raised_depth_mm}, min_text_height_mm={spec.hanger.text.min_text_height_mm}, font={spec.hanger.text.font!r}, placement={spec.hanger.text.placement!r}),
    printer=PrinterSpec(model={spec.hanger.printer.model!r}, nozzle_mm={spec.hanger.printer.nozzle_mm}, material={spec.hanger.printer.material!r}, layer_height_mm={spec.hanger.printer.layer_height_mm}),
    style={spec.hanger.style!r},
    add_border={spec.hanger.add_border!r},
)
model = build_mirror_hanger(spec)
'''
    path.write_text(content, encoding="utf-8")
