# Product Family Checklist

Use this checklist before adding any new product type.

## 1. Product definition

- Product type name is defined.
- Template ID is defined.
- Product purpose is clear.
- Expected use case is clear.
- Default size is defined in millimeters.
- Safe minimum and maximum sizes are defined.

## 2. Input requirements

- Required user inputs are listed.
- Optional user inputs are listed.
- Safe defaults are documented.
- Critical missing information is documented.
- Examples of supported prompts are included.
- Examples of blocked prompts are included.

## 3. CAD strategy

- Builder strategy is selected.
- Base geometry is defined.
- Holes, cutouts, text, and decorative features are defined.
- Print orientation is defined.
- Source CAD output is preserved.
- STL and STEP export paths are defined.

## 4. Printability rules

- Minimum wall/thickness is defined.
- Minimum feature size is defined.
- Minimum text height is defined where text exists.
- Minimum raised/debossed depth is defined where text exists.
- Hole clearances are defined where holes exist.
- Material-specific concerns are documented.

## 5. Validation rules

- Preflight spec validation exists.
- Build artifact validation exists.
- Geometry validation expectations are defined.
- Visual/design warnings are defined.
- Error-level conditions are defined.

## 6. Tests

- Registry test exists.
- Requirements extraction test exists.
- Blocked prompt test exists.
- Successful prompt test exists.
- Validator test exists.
- Artifact generation test exists when CAD dependencies are available.

## 7. Documentation

- Product family is added to roadmap.
- Template metadata is documented.
- Example API request is documented.
- Known limitations are documented.

## Acceptance rule

A product family is not accepted until it can produce validated output and explain failures through report.json.
