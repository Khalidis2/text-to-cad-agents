# Engineering Decisions

This file records important decisions so the project stays consistent as it grows.

## Decision 1: Local-first CAD generation

The CAD engine runs locally. This keeps STL, STEP, previews, templates, and validation artifacts under user control.

AI services may be added as optional reasoning adapters, but the CAD engine must not depend on a specific AI provider.

## Decision 2: Two main agents

The system uses two main reasoning roles:

- Product Architect
- CAD Engineer

Specialist helpers can exist internally, but the user-facing mental model remains two agents.

## Decision 3: Validators are code

Validation is deterministic code, not another conversational agent.

This makes printability rules testable and repeatable.

## Decision 4: MVP means final architecture in small form

The MVP must not be throwaway code.

The first product family can be limited, but the folder structure, schemas, validators, and template registry must be designed for expansion.

## Decision 5: Template registry before product expansion

New product families should be added through a registry instead of scattered conditional logic.

This reduces duplicated behavior and keeps product-specific rules contained.

## Decision 6: Build from structured specs only

The CAD builder must not consume raw user text.

Raw text is interpreted by the Product Architect layer. CAD generation receives only approved structured specs.

## Decision 7: Block bad requests

A blocked request is better than a bad model.

The system should block when critical information is missing, when product type is unsupported, or when printability cannot be validated.

## Decision 8: Reports are mandatory

Every job must produce a report that explains the pipeline result, assumptions, warnings, validation issues, and generated files.

## Decision 9: Bambu A1 baseline first

The first production baseline is Bambu Lab A1 with a 0.4 mm nozzle.

Future printer profiles can be added, but the MVP should optimize around this known baseline.

## Decision 10: Prefer editable CAD outputs

STL alone is not enough for a serious production system.

The project should preserve source CAD and STEP output whenever possible.
