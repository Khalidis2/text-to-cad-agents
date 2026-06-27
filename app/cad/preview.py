# app/cad/preview.py
from pathlib import Path
from app.schemas.models import CadSpec


def write_svg_preview(spec: CadSpec, path: Path):
    h = spec.hanger
    w, hh = h.width_mm, h.height_mm
    scale = 5
    sw, sh = w * scale, hh * scale
    text = h.text.content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    font_size = max(24, min(54, int(310 / max(5, len(text)))))
    border = ""
    if h.add_border:
        border = f'<rect x="{h.border_mm}" y="{h.border_mm}" width="{w-h.border_mm*2}" height="{hh-h.border_mm*2}" rx="{max(1, h.corner_radius_mm-h.border_mm/2)}" ry="{max(1, h.corner_radius_mm-h.border_mm/2)}" fill="none" stroke="#111" stroke-width="0.55"/>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{sw}" height="{sh}" viewBox="0 0 {w} {hh}">
<rect x="0.5" y="0.5" width="{w-1}" height="{hh-1}" rx="{h.corner_radius_mm}" ry="{h.corner_radius_mm}" fill="#f5f5f5" stroke="#111" stroke-width="0.6"/>
{border}
<circle cx="{w/2}" cy="{h.hole_center_y_from_top_mm}" r="{h.hole_diameter_mm/2}" fill="white" stroke="#111" stroke-width="0.5"/>
<text x="{w/2}" y="{hh*0.60}" text-anchor="middle" dominant-baseline="middle" font-family="Arial" font-size="{font_size/scale}" font-weight="700" fill="#111">{text}</text>
</svg>'''
    path.write_text(svg, encoding="utf-8")
