# Kawatch AI Security Lab

**An AI-assisted website security assessment and remediation platform.**

Kawatch aims to help website owners, developers, and small businesses
identify common security weaknesses, understand their potential impact,
and prioritize practical remediation.

The project is being developed through a documented, 90-day engineering
journey. Its initial release will be a controlled, testable prototype.

## The Problem

Modern applications are built using many technologies, frameworks,
third-party dependencies, and AI coding assistants.

Developers may deploy applications without fully understanding their
security configuration. Older applications can also accumulate outdated
dependencies, insecure settings, and other weaknesses.

Security tools can identify potential problems, but their findings may
be difficult for non-specialists to understand or prioritize.

Kawatch aims to make security assessments more understandable,
evidence-based, and actionable.

## Planned Capabilities

- HTTPS and website security-header assessments.
- Identification of potentially vulnerable software dependencies.
- Static analysis of supported source-code formats.
- Detection of exposed secrets in authorized code repositories.
- Evidence-backed findings with severity and confidence information.
- AI-assisted explanations and remediation guidance.
- Assessment reports and historical progress tracking.
- Automated testing, continuous integration, and quality checks.

These are planned capabilities, not claims that the current prototype
already implements them.

## Development Principles

1. Permission-based assessments.
2. Evidence before conclusions.
3. Human review of important security decisions.
4. Clear explanations and actionable remediation guidance.
5. Automated tests for repeatable behavior.
6. Explicit documentation of limitations and uncertainty.
7. Responsible handling of code, credentials, and assessment results.

AI will assist with explanations and prioritization. It will not be
treated as an infallible security scanner.

### Current Status

**Phase:** Foundation and local security assessment prototype

**Implemented:**
- Product vision, requirements, security boundaries, and roadmap.
- Python package foundation and automated CI.
- Security-header analysis for selected HTTP response headers.
- Local HTTP response collection restricted to 127.0.0.1.
- Local demonstration server for controlled testing.
- Automated tests for header analysis and HTTP collection.

**Validation:** Ruff passes and all 10 tests pass locally without warnings.

**Current limitations:** The collector supports local HTTP only. The
analyzer checks selected header presence, not the effectiveness of
security policies. No external website scanning is implemented.

**Next milestone:** Integrate HTTP collection and header analysis into
a command-line assessment that produces readable security findings.



See [ROADMAP.md](ROADMAP.md) for the development plan and
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the planned design.

## Getting Started

The initial documentation does not yet represent a working scanner.

Setup instructions, dependencies, supported checks, and example reports
will be added and tested as the application is implemented.

## Who Is This For?

The project is intended to support developers, learners, and small
organizations that need clearer explanations of common application
security findings.

It is also an engineering portfolio project demonstrating Python,
security assessment, testing, automation, and continuous improvement.

## Responsible Use

Only assess systems you own or have explicit authorization to test.

The initial prototype will prioritize controlled demonstrations,
non-destructive checks, and reproducible sample data.

Kawatch cannot guarantee that a website is secure or that every
vulnerability will be detected.

## Development Log

A dated engineering log will record completed work, test results,
decisions, limitations, and next steps.

- **Day 1:** Establishing project documentation and development scope.

## Contributing

Contributions will be welcomed as the project matures. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the planned contribution process.

## Project Status

This is an experimental project under active development. It is not
yet a production security service and must not be represented as one.
