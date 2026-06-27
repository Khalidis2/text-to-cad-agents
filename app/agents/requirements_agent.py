# app/agents/requirements_agent.py
import re
from app.schemas.models import Requirements, HangerSpec, TextSpec, PrinterSpec, PromptRefinement
from app.config import settings


class RequirementsAgent:
    SKIP_WORDS = {
        "make", "create", "premium", "luxury", "car", "mirror", "hanger", "with", "name", "the", "a", "an", "and",
        "raised", "text", "rounded", "corners", "hole", "for", "please", "uae", "commercial", "printable", "3d", "model",
        "تعليقة", "مراية", "سيارة", "اسم", "على", "مع", "ثري", "دي"
    }

    def run(self, original_text: str, refined: PromptRefinement, material: str) -> Requirements:
        if refined.product_intent != "car_mirror_hanger":
            return Requirements(
                product_type=refined.product_intent,
                supported=False,
                missing_critical_info=["Supported product type not detected. Current production template supports car mirror hangers only."],
                warnings=["Router detected an unsupported or unclear product category."],
            )
        extracted = self._extract_dimensions(original_text)
        name = self._extract_text(original_text)
        assumptions = []
        warnings = []
        missing = []
        if not name:
            name = "Khaled"
            assumptions.append("No explicit text was found; demo text 'Khaled' was used to keep the pipeline executable.")
        script = self._detect_script(name)
        selected_material = self._normalize_material(material or self._extract_material(original_text) or settings.default_material)
        if selected_material not in {"PLA", "PETG", "ABS", "ASA"}:
            warnings.append(f"Material '{selected_material}' is not in the validated baseline set; PLA rules will be used conservatively.")
        style = "minimal" if "minimal" in refined.style_keywords else "bold" if "bold" in refined.style_keywords else "premium"
        width = extracted.get("width_mm", 75.0)
        height = extracted.get("height_mm", 45.0)
        thickness = extracted.get("thickness_mm", 4.0)
        if len(name) > 12 and "width_mm" not in extracted:
            width = min(110.0, max(width, 75.0 + (len(name) - 12) * 3.0))
            assumptions.append("Width was increased automatically because the requested text is long.")
        spec = HangerSpec(
            width_mm=width,
            height_mm=height,
            thickness_mm=thickness,
            corner_radius_mm=extracted.get("corner_radius_mm", 5.0),
            hole_diameter_mm=extracted.get("hole_diameter_mm", 5.0),
            hole_center_y_from_top_mm=extracted.get("hole_center_y_from_top_mm", 7.0),
            border_mm=extracted.get("border_mm", 3.0),
            text=TextSpec(content=name, script=script, raised_depth_mm=extracted.get("raised_depth_mm", 0.8), min_text_height_mm=extracted.get("text_height_mm", 6.0)),
            printer=PrinterSpec(model=settings.default_printer, nozzle_mm=settings.default_nozzle_mm, material=selected_material),
            style=style,
            add_border="no border" not in original_text.lower(),
        )
        return Requirements(product_type="car_mirror_hanger", supported=True, missing_critical_info=missing, assumptions=assumptions, warnings=warnings, hanger=spec, extracted=extracted)

    def _extract_text(self, text: str) -> str:
        patterns = [
            r'(?:name|text|word|says|write)\s*(?:is|=|:)?\s*["“”\']([^"“”\']{1,50})["“”\']',
            r'["“”\']([^"“”\']{1,50})["“”\']',
            r'(?:name|text|word|says|write)\s*(?:is|=|:)?\s*([\w\u0600-\u06FF -]{2,50})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                candidate = self._clean_candidate(match.group(1))
                if candidate:
                    return candidate
        arabic = re.findall(r'[\u0600-\u06FF]{2,30}', text)
        if arabic:
            return arabic[-1].strip()
        words = [self._clean_candidate(w) for w in text.split()]
        candidates = [w for w in words if w and w.lower() not in self.SKIP_WORDS and len(w) >= 3 and not re.fullmatch(r"\d+(?:\.\d+)?", w)]
        return candidates[-1] if candidates else ""

    def _clean_candidate(self, value: str) -> str:
        value = re.sub(r"\b(width|height|thickness|mm|cm|hole|diameter|rounded|corners|raised|depth)\b.*", "", value, flags=re.IGNORECASE)
        return value.strip(" .,;:!؟")[:50]

    def _detect_script(self, value: str) -> str:
        has_ar = any("\u0600" <= c <= "\u06FF" for c in value)
        has_lat = any("a" <= c.lower() <= "z" for c in value)
        if has_ar and has_lat:
            return "mixed"
        return "arabic" if has_ar else "latin"

    def _normalize_material(self, value: str) -> str:
        return re.sub(r"[^A-Za-z0-9]", "", value).upper() or settings.default_material

    def _extract_material(self, text: str) -> str:
        match = re.search(r"\b(PLA|PETG|ABS|ASA)\b", text, flags=re.IGNORECASE)
        return match.group(1) if match else ""

    def _extract_dimensions(self, text: str) -> dict:
        out = {}
        for key, aliases in {
            "width_mm": ["width", "wide", "w"],
            "height_mm": ["height", "tall", "h"],
            "thickness_mm": ["thickness", "thick", "depth"],
            "hole_diameter_mm": ["hole", "hole diameter"],
            "corner_radius_mm": ["corner radius", "radius"],
            "border_mm": ["border"],
            "raised_depth_mm": ["raised depth", "emboss", "text depth"],
            "text_height_mm": ["text height"],
        }.items():
            for alias in aliases:
                m = re.search(rf"\b{re.escape(alias)}\b\s*(?:=|:|is)?\s*(\d+(?:\.\d+)?)\s*(mm|cm)?", text, flags=re.IGNORECASE)
                if m:
                    value = float(m.group(1)) * (10 if (m.group(2) or "mm").lower() == "cm" else 1)
                    out[key] = value
                    break
        pair = re.search(r"(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)\s*(mm|cm)?", text, flags=re.IGNORECASE)
        if pair:
            mult = 10 if (pair.group(3) or "mm").lower() == "cm" else 1
            out.setdefault("width_mm", float(pair.group(1)) * mult)
            out.setdefault("height_mm", float(pair.group(2)) * mult)
        return out
