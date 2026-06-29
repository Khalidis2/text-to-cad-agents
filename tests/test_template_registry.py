# tests/test_template_registry.py
import pytest

from app.templates.registry import ProductTemplate, TemplateRegistry


def test_default_registry_contains_car_mirror_hanger():
    registry = TemplateRegistry()

    template = registry.require("car_mirror_hanger")

    assert template.product_type == "car_mirror_hanger"
    assert template.template_id == "mirror_hanger_rounded_v1"
    assert "PLA" in template.supported_materials


def test_registry_rejects_duplicate_product_type():
    template = ProductTemplate(
        product_type="test_product",
        template_id="test_v1",
        version="1.0.0",
        builder_name="TestBuilder",
        supported_materials=("PLA",),
        default_width_mm=10.0,
        default_height_mm=10.0,
        default_thickness_mm=3.0,
        min_width_mm=5.0,
        max_width_mm=50.0,
        min_height_mm=5.0,
        max_height_mm=50.0,
        description="Test product.",
    )
    registry = TemplateRegistry([template])

    with pytest.raises(ValueError):
        registry.register(template)


def test_registry_blocks_unknown_product_type():
    registry = TemplateRegistry()

    with pytest.raises(ValueError):
        registry.require("unsupported_product")
