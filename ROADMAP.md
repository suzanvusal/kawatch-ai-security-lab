# Kawatch AI Security Lab — 90-Day Roadmap

The roadmap is a learning and engineering plan, not a promise that
every feature will be production-ready within 90 days.

## Phase 1 — Foundation (Days 1–10)

- [x] Choose project name and product direction.
- [ ] Document product requirements.
- [ ] Define security boundaries.
- [ ] Document the initial architecture.
- [ ] Set up Python packaging and development dependencies.
- [ ] Add linting and automated tests.
- [ ] Create a controlled demonstration target.
- [ ] Add the first tested security check.

## Phase 2 — Website Assessment (Days 11–20)

- [ ] Validate assessment configuration and scope.
- [ ] Implement selected HTTPS and header checks.
- [ ] Normalize observations into structured findings.
- [ ] Add timeouts, error handling, and tests.
- [ ] Document coverage and limitations.

## Phase 3 — Reporting (Days 21–30)

- [ ] Define the finding schema.
- [ ] Generate JSON and Markdown reports.
- [ ] Add evidence and remediation guidance.
- [ ] Add severity and confidence handling.
- [ ] Create reproducible example reports.

## Phase 4 — Dependency Security (Days 31–40)

- [ ] Parse a supported dependency format.
- [ ] Integrate a trustworthy vulnerability data source.
- [ ] Record package versions and source references.
- [ ] Test outdated and vulnerable sample dependencies.
- [ ] Document database freshness and coverage limitations.

## Phase 5 — Source Analysis (Days 41–50)

- [ ] Integrate selected static-analysis tools.
- [ ] Add safe secret-detection tests.
- [ ] Report source locations and evidence.
- [ ] Evaluate false positives.
- [ ] Document supported languages and formats.

## Phase 6 — AI Assistance (Days 51–60)

- [ ] Define the AI input and output schema.
- [ ] Generate explanations from recorded evidence.
- [ ] Add uncertainty and unsupported-claim checks.
- [ ] Evaluate explanation quality.
- [ ] Keep deterministic findings separate from AI commentary.

## Phase 7 — Dashboard (Days 61–70)

- [ ] Design the assessment-results interface.
- [ ] Display findings and severity.
- [ ] Add filtering and historical comparison.
- [ ] Protect report access.
- [ ] Test the interface using sample assessments.

## Phase 8 — Engineering Maturity (Days 71–80)

- [ ] Add Docker support.
- [ ] Improve CI and regression testing.
- [ ] Review permissions and secret handling.
- [ ] Add operational logging and metrics.
- [ ] Document deployment and failure recovery.

## Phase 9 — Portfolio and Evaluation (Days 81–90)

- [ ] Complete end-to-end demonstrations.
- [ ] Evaluate detection performance and limitations.
- [ ] Review the threat model.
- [ ] Improve onboarding and contribution documentation.
- [ ] Prepare a demonstration and architecture overview.
- [ ] Identify work required before any commercial pilot.

## Daily Engineering Log

Each meaningful workday should record:

- Date and objective.
- Changes made.
- Tests and their results.
- Decisions and reasons.
- Known issues or limitations.
- Next steps.

Automation should report genuine work and test outcomes. It must not
invent completed tasks or manufacture empty commits.
