# app/schemas/models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any


class PromptRefinement(BaseModel):
    clean_prompt: str
    product_intent: str
    style_keywords: List[str] = []
    language: str = "auto"
    confidence: float = Field(ge=0, le=1)
    normalized_text: str = ""
    detected_language: str = "unknown"


class TextSpec(BaseModel):
    content: str
    script: Literal["latin", "arabic", "mixed"] = "latin"
    raised_depth_mm: float = 0.8
    min_text_height_mm: float = 6.0
    font: str = "Arial"
    placement: Literal["center", "lower", "upper"] = "center"


class PrinterSpec(BaseModel):
    model: str = "Bambu Lab A1"
    nozzle_mm: float = 0.4
    material: str = "PLA"
    layer_height_mm: float = 0.2


class HangerSpec(BaseModel):
    width_mm: float = 75.0
    height_mm: float = 45.0
    thickness_mm: float = 4.0
    corner_radius_mm: float = 5.0
    hole_diameter_mm: float = 5.0
    hole_center_y_from_top_mm: float = 7.0
    border_mm: float = 3.0
    text: TextSpec
    printer: PrinterSpec
    style: Literal["standard", "premium", "minimal", "bold"] = "premium"
    add_border: bool = True


class Requirements(BaseModel):
    product_type: str
    supported: bool
    missing_critical_info: List[str] = []
    assumptions: List[str] = []
    warnings: List[str] = []
    hanger: Optional[HangerSpec] = None
    extracted: Dict[str, Any] = {}


class CadSpec(BaseModel):
    product_type: str
    template_id: str
    units: str = "mm"
    engine: str = "cadquery"
    print_orientation: str = "flat_on_back"
    hanger: HangerSpec
    revision: int = 1
    quality_mode: str = "production"


class BuildPlan(BaseModel):
    build_allowed: bool
    reason: str
    risks: List[str] = []
    operations: List[str] = []
    engine: str = "cadquery"
    template_id: str


class ValidationIssue(BaseModel):
    code: str
    severity: Literal["info", "warning", "error"]
    message: str
    fix_hint: str = ""


class ValidationReport(BaseModel):
    passed: bool
    issues: List[ValidationIssue] = []
    metrics: Dict[str, Any] = {}
