# Contributing to Len

Thank you for helping improve Len. Contributions should preserve the project's local-first design, privacy boundary, factual clinical framing, and backward compatibility.

## Before You Start

- Read the [Support Guide](SUPPORT.md), [Security Policy](SECURITY.md), and [Code of Conduct](CODE_OF_CONDUCT.md).
- Search existing [issues](https://github.com/DScannellWiz/len-mental-health/issues) before opening a new one.
- Use the structured issue forms for bugs and feature requests.
- Privately report suspected vulnerabilities through [GitHub private vulnerability reporting](https://github.com/DScannellWiz/len-mental-health/security/advisories/new). Do not disclose a suspected vulnerability in a public issue.

Len is not medical advice, diagnosis, treatment, monitoring, crisis support, or emergency software. Repository participation is for software development and documentation, not interpretation of a person's symptoms or care.

## Privacy Rules

Use only project-created fictional data that does not describe a real person.

Do not commit, upload, paste, or link to:

- assessment responses, scores, journal entries, or treatment or clinician information;
- a Len database, report, workbook, export, or log containing entered data;
- PHI, PII, credentials, private correspondence, or identifying file paths;
- screenshots or other generated artifacts; or
- release archives, executables, build directories, or environment folders.

If a test needs a realistic scenario, create the minimum synthetic fixture in code or under `sample_data/`, label it clearly as fictional, and avoid details that could be mistaken for a real person's history.

## Development Setup

Len's supported development environment is Windows with Python 3.12 or later.

```powershell
py -3.12 -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
& ".\Launch Len.bat"
```

The application keeps source-run data under `data/` and generated outputs under `reports/`. Those locations are ignored except for intentional scaffolding. Never use real personal data in a development checkout.

## Making a Change

- Keep each pull request focused on one feature, bug fix, or closely related documentation change.
- Prefer incremental, readable changes over broad refactors.
- Preserve existing database records, storage locations, internal compatibility identifiers, and public file formats unless an approved design explicitly changes them.
- Add or update automated tests when business logic changes.
- Update user and developer documentation when behavior, privacy boundaries, packaging, or release procedures change.
- Explain new dependencies and why the existing runtime cannot reasonably meet the need.
- Create an iteration record under `docs/Iterations/` for a substantial feature or architectural change.

## Validation

Run the full test suite from the project root:

```powershell
& ".\.venv\Scripts\python.exe" -m unittest discover -s tests -v
& ".\.venv\Scripts\python.exe" -m compileall src tests packaging
git diff --check
```

Also run focused validation appropriate to the change. GUI, packaging, PDF, and workbook claims require the corresponding current validation; a passing source test suite must not be presented as proof that a packaged Windows artifact works.

GitHub Actions runs the same automated test and compilation commands on Windows with Python 3.12 for pull requests targeting `main` and pushes to `main`. The hosted check is an additional signal, not a substitute for any required GUI, packaging, privacy, licensing, or exact-artifact validation.

## Pull Requests

A pull request should:

- explain the problem and the chosen approach;
- link the relevant issue when one exists;
- list tests and manual checks performed;
- identify privacy, security, compatibility, and migration effects;
- update documentation or explain why no update is needed; and
- contain no private data or generated artifacts.

Maintainers may ask for a change to be split, narrowed, tested further, or revised before review. Opening a pull request does not authorize a release, binary distribution, or change to the project's clinical or privacy boundaries.

## Licensing

Len is licensed under `GPL-3.0-only`. By submitting a contribution, you agree that it may be distributed under the project's GNU General Public License version 3 terms. Do not contribute material that you do not have the right to license this way.

## AI-Assisted Contributions

Disclose material AI assistance in the pull-request description. The contributor remains responsible for understanding the submitted change, verifying its licenses and provenance, testing it, and reviewing it for privacy, security, and correctness.
