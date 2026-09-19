# Iteration 014.1: Compatible Analytical Series

## Objective

Correct the artificial PHQ-9 and GAD-7 v1/v2 trend break observed after publication of `v0.5.0-alpha.1`. This is a source correction for a later release. The published tag, release, and ZIP remain immutable.

## Forensic finding and design

Iteration 014 grouped every trend and 14-day comparison by exact definition version. Review then displayed only the newest group; the PDF created one trend chart per group. Definition v2 changed daily response labels and instructions, while item IDs, option values and numeric scores, total bounds, profile rule, and PHQ-9 Item 9 behavior remained the same as v1. The version boundary therefore introduced an analytical break that did not exist in the underlying stored observations.

An application-owned `ANALYTICAL_SERIES_IDS` registry explicitly assigns PHQ-9 v1/v2 to one series and GAD-7 v1/v2 to another. Unknown versions default to their own series. The grouping helper checks that all joined definitions have equal scoring/profile signatures before combining entries chronologically. It does not edit definitions, snapshots, submissions, or migrations. Raw/detail rows still report each stored definition version. A derived profile spanning versions reports both in `definition_versions`, leaves the singular `definition_version` blank, and carries the analytical series ID. The Analysis Workbook schema advances to 1.3 for those appended derived-profile fields.

Review recent and long-term charts, 14-day comparisons and item tables, treatment-cycle displays, PDF score trends and profiles, and workbook derived profiles now use the approved series boundary. The PDF questionnaire-definition and recorded-check-in tables retain exact version provenance. PHQ-9 Item 9 context remains tied to the stable PHQ-9 item identity. Historical v1 response labels remain numeric; v2 keeps `Not present / Mild / Moderate / High`.

## Files modified

- `src/phq9_tracker/app.py`: explicit series registry, signature guard, joined analytics, derived-profile provenance, and workbook schema update.
- `tests/test_iteration_014_questionnaire_contracts.py`: compatible series, chronological order, incompatible synthetic future version, and cross-version comparison.
- `tests/test_iteration_014_reports.py`: PDF trend grouping and workbook profile/provenance checks.
- `README.md`, `ROADMAP.md`, `BugList.md`, `BUILD_AND_RELEASE.md`: current known issue, source correction, and next-candidate validation guidance.

## Validation

Fictional isolated data only: 25 focused tests, 71 affected-subsystem tests, and 111 full-suite tests passed in the project environment. Application and test compilation passed. A generated six-page PDF rendered and was inspected on every page: one continuous PHQ-9 trend, one continuous GAD-7 trend, combined 14-day profile tables, separate definition/check-in provenance tables, and PHQ-9 Item 9 context all appeared correctly. The generated XLSX was checked structurally and rendered through LibreOffice: raw rows included v1 and v2, while its 16 derived profile rows had 14-day coverage, `v1|v2` source versions, and no misleading singular version. The patch passed `git apply --check --whitespace=error` against a clean source-file copy of the starting checkout. The known non-failing SQLite resource warnings remain unchanged.

## Remaining work

The canonical checkout's Git metadata is read only in this sandbox, and a local clone was stopped by Git's dubious-ownership check. The prepared source patch requires a trusted checkout for commit, protected-main PR, required Windows Python 3.12 CI, merge, and main synchronization. This source correction is not a new release. A patch prerelease such as `v0.5.1-alpha.1` is recommended only after separate candidate validation and owner authorization.
