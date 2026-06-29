# Runbook

## Purpose

This file is the operational guide for running, testing, and debugging the CAD Production Agent locally.

## Recommended environment

- Python 3.11
- Virtual environment
- Local checkout of the repository
- CadQuery installed from requirements.txt

## First-time setup

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

## Run API server

```bash
python run.py
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Health check

Call:

```text
GET /health
```

Expected result includes:

```json
{"ok": true}
```

## Create a test job

```json
{
  "text": "Make a premium car mirror hanger with name \"Khaled\", width 85mm, height 48mm, rounded corners, raised text, and a 5mm hanging hole.",
  "language": "en",
  "material": "PLA",
  "quality_mode": "production"
}
```

## Expected output folder

Generated jobs should appear under:

```text
outputs/jobs/<job_id>/
```

A successful job should include CAD files, preview files, validation reports, and report.json.

## Run tests

```bash
pytest -q
```

## Debug order

When a job fails, inspect files in this order:

1. report.json
2. requirements.json
3. cad_spec.json
4. preflight_validation.json
5. validation.json
6. model.py

## Common failure causes

### CadQuery install failure

CadQuery can be sensitive to Python version and platform. Use Python 3.11 first.

### Missing output files

Check model.py and CAD builder logs. Then run artifact validation.

### Blocked job

Open report.json and read the missing-info or preflight reason.

### Bad dimensions

Inspect normalization.json to see whether the system changed dimensions for printability.

## Rule

Never judge a job by STL existence alone. Always inspect report.json and validation.json.
