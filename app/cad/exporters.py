# app/cad/exporters.py
from pathlib import Path
import cadquery as cq


def export_stl(model: cq.Workplane, path: Path):
    cq.exporters.export(model, str(path), exportType="STL", tolerance=0.05, angularTolerance=0.1)


def export_step(model: cq.Workplane, path: Path):
    cq.exporters.export(model, str(path), exportType="STEP")
