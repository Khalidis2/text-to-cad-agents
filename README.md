# CAD Production Agent

A local-first CAD production pipeline for generating 3D-printable product files from structured or natural-language requests.

## Current production template

- Car mirror hanger, optimized for Bambu Lab A1 / 0.4 mm nozzle baseline

## What was upgraded in v0.2.0

- Stronger prompt routing and language detection
- Dimension/material/text extraction from natural language
- Explicit assumptions, warnings, and extracted fields in every job
- CAD spec normalization before build
- Preflight printability validation before CadQuery execution
- Richer printability checks: structural thickness, hole clearance, text size/depth, radius, size envelope
- Mesh validation metrics: watertight status, extents, volume, face count
- Visual critic warnings for proportions, long text, and low hole placement
- Stage trace in `report.json` for easier debugging
- Safer API job lookup and file download handling
- Raised border geometry and safer text fallback if local font text generation fails

## Install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Example request

```json
{
  "text": "Make a premium car mirror hanger with name \"Khaled\", width 85mm, height 48mm, rounded corners, raised text, and a 5mm hanging hole.",
  "language": "en",
  "material": "PLA",
  "quality_mode": "production"
}
```

## Output files

Each job is saved under `outputs/jobs/<job_id>/`:

```text
request.json
refined_prompt.json
requirements.json
cad_spec.raw.json
cad_spec.json
normalization.json
plan.json
preflight_validation.json
model.py
model.stl
model.step
preview.svg
validation.json
report.json
```

## Production rules

- Minimum structural thickness: 3.0 mm
- Minimum wall/nozzle-safe feature: 0.8 mm
- Minimum raised text depth: 0.6 mm
- Minimum readable text height: 6.0 mm
- Minimum hole diameter: 4.5 mm
- Minimum material above hole: 3.0 mm
- Default material: PLA

## Tests

```bash
pytest
```

CadQuery must be installed for full pipeline/STL tests.
