# app/templates/registry.py
from dataclasses import dataclass
from typing import Callable, Dict, Iterable


@dataclass(frozen=True)
class ProductTemplate:
    product_type: str
    template_id: str
    version: str
    builder_name: str
    supported_materials: tuple[str, ...]
    default_width_mm: float
    default_height_mm: float
    default_thickness_mm: float
    min_width_mm: float
    max_width_mm: float
    min_height_mm: float
    max_height_mm: float
    description: str


MIRROR_HANGER_TEMPLATE = ProductTemplate(
    product_type="car_mirror_hanger",
    template_id="mirror_hanger_rounded_v1",
    version="1.0.0",
    builder_name="CadBuilder",
    supported_materials=("PLA", "PETG", "ABS", "ASA"),
    default_width_mm=75.0,
    default_height_mm=45.0,
    default_thickness_mm=4.0,
    min_width_mm=45.0,
    max_width_mm=140.0,
    min_height_mm=25.0,
    max_height_mm=90.0,
    description="Rounded car mirror hanger with hanging hole, optional raised border, and raised text.",
)


class TemplateRegistry:
    def __init__(self, templates: Iterable[ProductTemplate] | None = None):
        self._templates: Dict[str, ProductTemplate] = {}
        for template in templates or (MIRROR_HANGER_TEMPLATE,):
            self.register(template)

    def register(self, template: ProductTemplate) -> None:
        key = template.product_type.strip().lower()
        if not key:
            raise ValueError("Template product_type cannot be empty")
        if key in self._templates:
            raise ValueError(f"Template already registered for product type: {template.product_type}")
        self._templates[key] = template

    def get(self, product_type: str) -> ProductTemplate | None:
        return self._templates.get(product_type.strip().lower())

    def require(self, product_type: str) -> ProductTemplate:
        template = self.get(product_type)
        if template is None:
            supported = ", ".join(sorted(self._templates))
            raise ValueError(f"Unsupported product type: {product_type}. Supported product types: {supported}")
        return template

    def product_types(self) -> list[str]:
        return sorted(self._templates)


registry = TemplateRegistry()
