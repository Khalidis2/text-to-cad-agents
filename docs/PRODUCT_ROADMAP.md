# Product Roadmap

## Vision

Text-to-CAD Agents is a production-oriented system that converts natural-language product requests into validated, parametric, 3D-printable CAD outputs.

The target workflow is:

```text
Prompt -> Requirements -> CAD Spec -> Plan -> Model -> Validate -> Repair -> Export -> Report
```

## Phase 1: Agent Architecture Foundation

Status: in progress

Goals:

- Define stable contracts for every pipeline agent.
- Separate reasoning responsibilities from CAD execution.
- Make every pipeline stage traceable and testable.
- Prepare the codebase for repair loops and model routing.

Planned agents:

| Agent | Responsibility |
|---|---|
| Prompt Refiner | Clean and normalize user intent without inventing product requirements. |
| Requirement Extractor | Extract dimensions, names, text, material, product type, constraints, and assumptions. |
| Missing Info Gate | Decide whether defaults are safe or whether the request is under-specified. |
| CAD Spec Agent | Convert requirements into a normalized manufacturing specification. |
| CAD Planner | Create a deterministic build plan from the CAD spec. |
| CAD Engineer | Generate executable parametric CadQuery code. |
| Printability Expert | Validate manufacturability against printer/nozzle/material rules. |
| Visual Critic | Catch proportion, readability, alignment, and design issues. |
| Repair Agent | Modify specs/plans after failed validation. |
| Final Approval Agent | Produce a final decision, warnings, and downloadable artifact list. |

## Phase 2: Product Template Library

Planned first templates:

- Car mirror hangers
- Keychains
- Nameplates
- Logo plates
- Coasters
- Phone stands
- Cable clips
- Wall hooks
- Storage trays
- Small boxes

Each template must include:

- Parametric schema
- Printability limits
- Design variants
- Default dimensions
- Validation rules
- Example prompts
- Regression tests

## Phase 3: Model Providers

Provider strategy:

- Deterministic rules first for safety-critical values.
- Local Ollama for private/offline drafting and planning.
- Optional API-based LLMs for advanced reasoning.
- Hard validation after every model-assisted stage.

## Phase 4: Repair Loop

Target behavior:

1. Generate initial model.
2. Validate geometry and printability.
3. If validation fails, create a repair plan.
4. Apply bounded repairs.
5. Rebuild and revalidate.
6. Stop after a configured maximum number of attempts.

## Phase 5: Production Dashboard

Future UI modules:

- Prompt input
- Live job status
- Preview viewer
- Validation report
- File downloads
- Product template selector
- History and versioning
- Material and cost estimate
