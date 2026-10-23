# Planned Architecture

## Design Goal

Build a modular assessment pipeline in which checks, evidence collection,
finding classification, reporting, and optional AI assistance can be
tested independently.

## Planned Data Flow

Assessment Configuration
        |
        v
Scope and Safety Validation
        |
        v
Assessment Orchestrator
        |
        +----> Website Configuration Checks
        |
        +----> Dependency Analysis
        |
        +----> Static Source Analysis
        |
        v
Evidence Normalization
        |
        v
Finding Classification
        |
        v
Risk and Confidence Assessment
        |
        v
Report Generation
        |
        +----> JSON Report
        |
        +----> Markdown Report
        |
        +----> Optional AI-Assisted Explanation

## Planned Modules

### Assessment configuration

Defines the authorized target, permitted checks, timeouts, and limits.

### Scope validation

Rejects targets and operations outside the approved assessment scope.

### Assessment checks

Implements small, independently testable security checks.

### Finding model

Provides a consistent representation of observations and findings,
including evidence, severity, confidence, and remediation guidance.

### Risk assessment

Prioritizes findings using documented rules and available context.

### Reporting

Generates structured reports that can be compared across assessments.

### AI assistance

Optionally explains validated findings and suggests remediation.
It does not replace evidence collection or deterministic checks.

### Testing

Uses controlled test applications, synthetic data, unit tests,
integration tests, and regression tests.

## Initial Technology Direction

- Python for the assessment engine.
- pytest for automated testing.
- Ruff for linting.
- GitHub Actions for continuous integration.
- JSON and Markdown for initial report formats.
- Docker for reproducible execution as the project matures.

Additional frameworks and AI providers will be selected when justified
by requirements rather than added without a clear purpose.

## Security Considerations

Assessment scope must be enforced before network activity.

External checks must use conservative timeouts and request limits.
Network-related protections must account for redirects, DNS resolution,
and private or reserved addresses.

Secrets must not be embedded in source code or published in reports.

AI outputs must remain distinguishable from measured evidence.

This document describes the intended design; implementation and tests
will determine which protections are actually available.
