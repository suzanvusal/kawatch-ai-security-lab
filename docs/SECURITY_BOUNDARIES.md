# Security Boundaries and Responsible Use

## Purpose

Kawatch is intended to help authorized users assess and improve
the security of websites and applications.

The product must not assume that a target is authorized merely because
it is publicly accessible.

## Authorization

Before assessing a real external target, the user must have ownership
or explicit permission to perform the planned checks.

The assessment process must clearly define the target and permitted scope.

## Initial Assessment Limits

The initial prototype will prioritize:

- Controlled demonstration websites.
- Local test applications.
- Non-destructive HTTP checks.
- Analysis of user-provided source code and dependency manifests.
- Synthetic data for tests.

Active exploit attempts and destructive testing are outside the scope
of the initial release.

## Scope Enforcement

As external assessment capabilities are added, the design must consider:

- Explicit target allowlists.
- Rejection of targets outside the approved scope.
- Request timeouts and rate limits.
- Restrictions on redirects and private or reserved network addresses.
- Safe handling of DNS resolution and changing network destinations.
- Clear audit records of assessment actions.

These protections must be implemented and tested before the product
is used for broader external assessments.

## Evidence and Reporting

Every finding should include available evidence, the check performed,
and relevant limitations.

The application must distinguish between an observed configuration
issue and a confirmed exploitable vulnerability.

Severity and confidence must not be treated as interchangeable.

## Data Protection

- Never commit real credentials, API keys, or customer secrets.
- Use synthetic examples in tests and documentation.
- Avoid logging sensitive request data unnecessarily.
- Restrict access to private assessment reports.
- Define retention and deletion practices before handling customer data.

## AI Safety

AI-generated explanations must be grounded in recorded findings.
The system must communicate uncertainty and avoid inventing evidence.

AI-generated remediation suggestions require appropriate validation
before being presented as verified fixes.

## Limitations

No automated assessment can prove that an application is completely
secure. Coverage depends on available evidence, supported checks,
configuration, and assessment scope.
