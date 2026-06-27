# tests/test_printability.py
from app.schemas.models import CadSpec, HangerSpec, TextSpec, PrinterSpec
from app.validators.printability_validator import PrintabilityValidator
from app.agents.spec_normalizer import SpecNormalizerAgent


def test_valid_hanger_rules_pass():
    spec = CadSpec(product_type="car_mirror_hanger", template_id="mirror_hanger_rounded_v1", hanger=HangerSpec(text=TextSpec(content="Khaled"), printer=PrinterSpec()))
    report = PrintabilityValidator().run(spec)
    assert report.passed is True


def test_normalizer_repairs_small_hole_and_thickness():
    spec = CadSpec(product_type="car_mirror_hanger", template_id="mirror_hanger_rounded_v1", hanger=HangerSpec(thickness_mm=1, hole_diameter_mm=2, text=TextSpec(content="Khaled"), printer=PrinterSpec()))
    fixed, issues = SpecNormalizerAgent().run(spec)
    assert fixed.hanger.thickness_mm >= 3
    assert fixed.hanger.hole_diameter_mm >= 4.5
    assert issues
