# app/agents/prompt_refiner.py
import re
from app.schemas.models import PromptRefinement


class PromptRefinerAgent:
    PRODUCT_KEYWORDS = {
        "car_mirror_hanger": ["hanger", "mirror", "rearview", "تعليقة", "مراية", "سيارة", "علاقة"],
        "keychain": ["keychain", "key ring", "keyring", "ميدالية", "مفتاح"],
        "nameplate": ["nameplate", "desk sign", "sign", "لوحة", "اسم"],
    }

    STYLE_WORDS = ["premium", "luxury", "uae", "rounded", "arabic", "minimal", "commercial", "bold", "thin", "large", "small"]

    def run(self, text: str, language: str) -> PromptRefinement:
        normalized = re.sub(r"\s+", " ", text.strip())
        lowered = normalized.lower()
        detected_language = "arabic" if any("\u0600" <= c <= "\u06FF" for c in normalized) else "english"
        product_intent = "unknown"
        confidence = 0.25
        for product, words in self.PRODUCT_KEYWORDS.items():
            score = sum(1 for word in words if word in lowered)
            if score:
                product_intent = product
                confidence = min(0.95, 0.55 + score * 0.15)
                break
        style_keywords = [word for word in self.STYLE_WORDS if word in lowered]
        clean = normalized
        if product_intent == "car_mirror_hanger":
            clean = f"Create a production-ready 3D-printable car mirror hanger from this request: {normalized}"
        return PromptRefinement(
            clean_prompt=clean,
            normalized_text=normalized,
            product_intent=product_intent,
            style_keywords=style_keywords,
            language=language,
            detected_language=detected_language,
            confidence=confidence,
        )
