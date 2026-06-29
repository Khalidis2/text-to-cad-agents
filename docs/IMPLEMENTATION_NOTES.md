# Implementation Notes

## Current foundation

The repository already contains the first working foundation:

- FastAPI application entry point
- Job creation endpoint
- Pipeline orchestrator
- Prompt refinement
- Requirement extraction
- Missing-information gate
- CAD specification generation
- Specification normalization
- CAD planning
- CadQuery build step
- Printability validation
- Geometry validation
- Visual critic scaffold
- Job output folders and reports

## Immediate implementation priority

The next build phase should strengthen the existing foundation instead of replacing it.

Priority order:

1. Introduce a product template registry.
2. Add artifact validation for required output files.
3. Tighten missing-critical-info behavior.
4. Add more tests around blocking and validation.
5. Rename internal concepts gradually toward Product Architect and CAD Engineer without breaking current code.

## Why not rewrite now

The current pipeline already follows the correct shape. A rewrite would slow the project and risk breaking a working foundation.

The right move is controlled refactoring:

- Add contracts.
- Add tests.
- Add registries.
- Add validators.
- Then add product families.

## Next code targets

### Template registry

A registry should map product types to template metadata, defaults, supported materials, builders, and validation rules.

### Artifact validator

A validator should confirm required files exist after build:

- model.py
- model.stl
- model.step
- preview.svg
- validation.json
- report.json

### Product family expansion

Second product family should be keychain, because it reuses many mirror-hanger concepts while testing different proportions and hole placement.

## Project rule

Do not add new product families until the template registry exists.
