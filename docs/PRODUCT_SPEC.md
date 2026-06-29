# Product Specification

## Objective

Build a fully automatic product generator that converts normal writing into validated, printable CAD outputs.

The system should behave like a disciplined AI mechanical engineer, not a casual text-to-3D generator.

## Primary user

Single-user system for Khaled. The MVP prioritizes output quality, local-first reliability, and fast iteration over public SaaS concerns.

## Long-term product scope

The system should eventually support mechanical parts, consumer products, organizers, 3D-printable accessories, and specified custom products.

## Non-negotiable rule

Every generated model must be printable. If a request cannot be safely converted into a printable model, the system must block the build and explain what information is missing or which constraint failed.

## MVP definition

MVP means the smallest working version of the final architecture:

1. Two main agents.
2. Strict structured handoff between agents.
3. Deterministic local CAD generation.
4. Local validation before final output.
5. Job artifacts written to disk.
6. Clear audit trail in report.json.
7. Architecture that can grow into a larger CAD production system.

## Main workflow

User request -> Product Architect -> approved product brief -> CAD Engineer -> CAD generation -> local validators -> preview, STL, STEP, source, report.

## Agent 1: Product Architect

The Product Architect understands the request, extracts requirements, identifies missing critical information, applies safe defaults only when appropriate, and produces a structured product brief. It must never generate CAD geometry.

## Agent 2: CAD Engineer

The CAD Engineer receives only approved structured product briefs, chooses a CAD strategy or template, produces deterministic CAD code, exports source/STL/STEP/preview files, and responds to validation failures where possible. It must never build from raw user text.

## Validation tools

Validation is code, not conversation. Validators must check printability, scale, minimum thickness, hole clearance, text depth, text readability, geometry health, watertight mesh where possible, and output artifact existence.

## Bambu A1 baseline

- Printer: Bambu Lab A1
- Nozzle: 0.4 mm
- Default material: PLA
- Minimum nozzle-safe feature: 0.8 mm
- Minimum raised text depth: 0.6 mm
- Minimum readable text height: 6.0 mm
- Units: millimeters

## Anti-goals

The MVP must not generate random AI meshes, silently guess critical dimensions, return an STL without validation, mix raw prompt interpretation with CAD building, or create throwaway architecture.
