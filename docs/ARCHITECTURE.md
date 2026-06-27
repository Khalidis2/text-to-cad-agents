# Architecture

```text
User Request
→ Prompt Refiner
→ Requirements Extractor
→ Missing Info Gate
→ CAD Spec Builder
→ Spec Normalizer
→ CAD Planner
→ Preflight Validation
→ CadQuery Builder
→ Geometry Validation
→ Visual Critic
→ Final Report
```

The builder never receives raw user text. It receives only a normalized `CadSpec`.

## Production behavior

- Unsupported product categories are blocked before CAD execution.
- Unsafe dimensions are normalized before build when they are recoverable.
- Non-recoverable printability failures are blocked at preflight.
- Every job writes a stage trace and all intermediate JSON artifacts.
