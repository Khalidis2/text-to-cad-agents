# MVP Blueprint

## Design principle

Build a serious MVP that is small in product surface area but not weak in architecture.

The first version should support one product family well, while the internal structure must support many future product families.

## MVP product family

Initial production family: car mirror hanger.

Reason:

- Fits the user's 3D-printing business.
- Tests text handling, hole clearance, rounded geometry, style, preview, STL, and STEP output.
- Simple enough for deterministic CAD, but complex enough to expose real pipeline problems.

## Required outputs

Each successful job should produce:

- request.json
- refined_prompt.json
- requirements.json
- cad_spec.raw.json
- cad_spec.json
- normalization.json
- plan.json
- preflight_validation.json
- model.py
- model.stl
- model.step
- preview.svg
- validation.json
- report.json

## Build states

A job can end in one of these states:

- blocked: the request is unsupported or missing critical information.
- failed: the system crashed or CAD execution failed.
- needs_fix: outputs exist but validation found error-level issues.
- complete: outputs exist and validation passed.

## MVP modules

### API layer

FastAPI provides local endpoints for job creation, health checks, job lookup, and file downloads.

### Product Architect layer

This layer refines prompts, extracts requirements, blocks unsupported requests, and creates a build-ready spec.

### CAD Engineer layer

This layer plans the build, executes CAD generation, exports files, and records build artifacts.

### Validation layer

This layer checks printability, geometry, artifact existence, and visual/design warnings.

### Storage layer

Each job is stored as an immutable folder under outputs/jobs.

## Critical MVP constraints

- Keep all CAD units in millimeters.
- Never build from raw user text.
- Never hide assumptions.
- Never output final files without a report.
- Prefer blocking over generating a bad model.
- Prefer deterministic code over AI-generated raw mesh.

## Future-ready expansion points

The MVP must leave clean extension points for:

- More product templates.
- Local LLM and OpenAI adapters.
- Telegram bot.
- Web UI.
- Image/reference input.
- Cost estimation.
- BOM generation.
- Advanced visual critic.
- Auto-fix loops.
- Multi-part assemblies.

## Definition of done for MVP foundation

The foundation is acceptable when:

1. The repo has a clear product spec.
2. The two-agent workflow is documented.
3. The pipeline runs locally.
4. At least one product template builds a model.
5. Validation blocks unsafe specs.
6. Generated jobs have traceable reports.
7. Tests cover the pipeline and validation rules.
