# Validation Policy

## Purpose

Validation is the main quality layer of the CAD Production Agent.

The system should prefer a blocked job over a bad model.

## Validation categories

### 1. Request validation

Checks whether the request is supported and complete enough to build.

Examples:

- Product type is supported.
- Critical dimensions are known or safely defaultable.
- Exact text is known when text is part of the product.
- Material is supported.

### 2. Spec validation

Checks the structured CAD spec before geometry is generated.

Examples:

- Units are millimeters.
- Width, height, thickness, hole size, text height, and text depth are inside printable ranges.
- Hole has enough edge clearance.
- Text has enough physical space.

### 3. Build artifact validation

Checks that expected output files exist after the CAD build.

Examples:

- Source file exists.
- STL exists.
- STEP exists.
- Preview exists.

### 4. Geometry validation

Checks actual generated geometry where possible.

Examples:

- Mesh loads successfully.
- Mesh has usable volume.
- Mesh extents match expected scale.
- Mesh appears watertight when the backend can determine this reliably.

### 5. Visual/design validation

Checks design warnings that are difficult to express as hard geometry rules.

Examples:

- Text may be too long for the available area.
- Proportions may look weak.
- Hole placement may look awkward.
- Product style may not match premium/commercial expectations.

## Severity levels

### info

The system changed or recorded something useful, but the job can continue.

### warning

The output is probably usable, but quality may be affected.

### error

The job must not be considered complete.

## Completion rule

A job can be complete only when there are no error-level validation issues.

## Normalization rule

The system may auto-normalize non-critical dimensions if the change improves printability and is recorded in the report.

The system must not silently normalize functional intent.

## Blocking rule

The build should be blocked when:

- Product type is unsupported.
- Critical dimensions are missing and cannot be safely defaulted.
- Preflight printability fails.
- CAD builder cannot generate required artifacts.
- Geometry validation produces error-level issues.

## Future validator targets

- Minimum wall analysis from sliced or voxelized geometry.
- Overhang risk detection.
- Text outline validation.
- Assembly fit checks.
- Material-specific tolerance rules.
- Bambu Studio profile recommendations.
