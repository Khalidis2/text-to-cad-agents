# Template System

## Purpose

The template system is how the project grows from one product family into many product families without turning the codebase into scattered special cases.

Every supported product type should have a registered template.

## Product template responsibilities

Each product template should define:

- Product type
- Template ID
- Version
- Default dimensions
- Safe dimension ranges
- Supported materials
- Builder implementation
- Product-specific validation rules
- Example prompts
- Test cases

## Template registry

The registry maps a product type to its template metadata.

Current first template:

- product_type: car_mirror_hanger
- template_id: mirror_hanger_rounded_v1
- builder: CadBuilder
- materials: PLA, PETG, ABS, ASA

## Why registry first

Without a registry, adding products usually creates fragile code like repeated if/else branches across agents, builders, and validators.

A registry allows future products to be added in a controlled way.

## Product addition checklist

Before adding a new product family, create:

1. Product template metadata.
2. Builder or builder strategy.
3. Defaults and dimension limits.
4. Requirements extraction examples.
5. Preflight validation rules.
6. Geometry expectations.
7. Tests.
8. Documentation.

## Product family priority

Recommended order:

1. Car mirror hanger
2. Keychain
3. Nameplate
4. Cable clip
5. Organizer tray
6. Box/container
7. Phone stand
8. Wall hook

## Template quality rule

A new product template is not accepted when it only generates geometry.

A product template is accepted only when it can also validate its own basic printability constraints and generate useful reports.
