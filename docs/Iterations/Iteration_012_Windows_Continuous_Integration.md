Current as of: 2026-09-13

# Iteration 012 - Repository Automation and Discovery

## Objectives

- Run Len's existing automated tests on the operating system and Python line supported for development.
- Give pull requests and changes to `main` an independent, repeatable source-level verification signal.
- Keep the workflow least-privilege and avoid creating packages, releases, or generated user artifacts.
- Improve repository discoverability and add a small, maintainable issue-label taxonomy.
- Enable vulnerability and secret detection without automatically creating pull requests or blocking pushes.

## Design Decisions

- Use one GitHub-hosted `windows-latest` job with Python 3.12. A version matrix is unnecessary while Len supports one primary development runtime and would add cost without a distinct compatibility claim.
- Run on pull requests targeting `main`, pushes to `main`, and manual dispatch. The manual trigger supports diagnosis without introducing a scheduled workload.
- Grant the workflow only read access to repository contents.
- Pin `actions/checkout` v7.0.1 and `actions/setup-python` v7.0.0 to their verified full release commit hashes. Human-readable version comments preserve maintainability.
- Cache downloaded Python packages using `requirements.txt` as the dependency key. The cache contains dependencies, not Len data or generated outputs.
- Cancel a superseded run for the same workflow and ref, and cap each job at 20 minutes.
- Run the existing full unit-test and compilation commands. Do not build a Windows package in ordinary CI because package creation has additional runtime, licensing, privacy, and exact-artifact gates.
- Do not add a README status badge or require the check until the workflow has completed successfully on live GitHub.

## Live Repository Changes

- Replaced the generic description with: `Privacy-first, local-first Windows app for recording PHQ-9 and GAD-7 check-ins and reviewing symptom trends over time.`
- Replaced eleven repetitive or overly broad topics with ten focused topics: `data-visualization`, `gad-7`, `local-first`, `mental-health-app`, `phq-9`, `privacy`, `python`, `sqlite`, `tkinter`, and `windows`. The website field remains blank rather than inventing a project site.
- Added ten labels without deleting or renaming GitHub's nine defaults:
  - Areas: `area: data-storage`, `area: reporting`, `area: workbook`, `area: windows-packaging`, `area: accessibility`, and `area: privacy-safety`.
  - Statuses: `status: needs-reproduction`, `status: needs-decision`, and `status: blocked`.
  - Priority: `priority: high`, reserved for genuinely time-sensitive or high-impact work.
- Enabled Dependabot vulnerability alerts and GitHub secret-scanning alerts.
- Left automatic Dependabot security/version updates, grouped updates, CodeQL, and secret push protection disabled pending a stable live CI run and a separate operational decision.
- Did not open issues, create a milestone, enable Discussions, upload a social-preview image, change a release, or create a branch or tag ruleset.

## Files Added

- `.github/workflows/windows-ci.yml`
- `docs/Iterations/Iteration_012_Windows_Continuous_Integration.md`

## Files Modified

- `CONTRIBUTING.md`
- `ROADMAP.md`
- `DEVELOPMENT_JOURNAL.md`

## Validation Planned and Performed

- Inspected the workflow's trigger, permissions, runner, Python version, pinned actions, commands, timeout, and concurrency behavior. GitHub's live parser remains the authoritative workflow-syntax check after publication.
- All 68 automated tests passed in a dependency-complete Python 3.12.14 environment.
- `src`, `tests`, and `packaging` compiled successfully in the same environment.
- Local Markdown links in the changed documentation resolved successfully.
- The changed-file inventory and tracked/unignored files contained no private or generated artifact.
- `git diff --check` passed; Git emitted only informational LF-to-CRLF working-copy warnings.
- The live repository displayed the revised description, all ten focused topics, 19 total active labels, enabled Dependabot alerts, and enabled secret-scanning alerts.
- After publication, verify the first live GitHub Actions run before requiring the check or adding a badge.

## Privacy and Security Impact

The workflow installs public dependencies and executes repository code on a GitHub-hosted runner. It receives no repository secrets and has read-only contents permission. Tests must continue to use isolated, project-created fictional data. CI logs are public, so tests and diagnostic output must never contain real health information, private paths, credentials, databases, reports, workbooks, or other user artifacts.

Pinning third-party Actions to full release commit hashes reduces exposure to a moved tag or branch. It does not eliminate dependency or runner risk; dependency monitoring and future security scanning remain separate controls.

## Migration

No application, database, user-data, packaging, or local development migration is required.

## Remaining Work

- Publish the workflow after owner review and verify its first live run.
- Add a README CI badge only after the live check is stable.
- Create a `main` ruleset that blocks deletion and force pushes and requires the successful CI check, with an explicitly documented owner-bypass decision.
- Protect published `v*` tags from deletion or movement.
- Review any dependency or secret-scanning alerts, then decide whether automatic update pull requests and secret push protection are useful after CI is proven.
