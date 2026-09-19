Current as of: 2026-09-19
Last substantive update: 2026-09-19

# Roadmap

## Vision

Build a privacy-first, local-only mental health tracking application that helps users and clinicians identify meaningful trends over time while keeping sensitive health information under the user's control.

## Current Capabilities

- PHQ-9 daily tracking.
- GAD-7 daily tracking.
- Dynamic Today's Check-In workflow with independent questionnaire selection and completion status.
- Correct 14-day symptom-frequency scoring for PHQ-9 and GAD-7.
- Local SQLite storage.
- Multi-assessment dashboard.
- Full-history clinician PDF reports.
- Normalized multi-sheet XLSX analysis workbooks.
- Treatment event tracking.
- Daily notes.
- GitHub-ready project structure.
- Privacy-conscious public support, contribution, security-reporting, issue, and pull-request guidance.
- Focused repository discovery metadata and area, status, and priority labels.
- Dependabot vulnerability alerts and GitHub secret-scanning alerts.
- Automated tests with a Windows/Python 3.12 continuous-integration workflow for pull requests and `main`.
- Installer and portable build scripts.

## Iteration 013: Dependency Security Remediation and v0.4.1-alpha.1 - Complete

- Updated the controlled release/test dependency pins from Pillow 12.2.0 to 12.3.0 and pypdf 6.13.3 to 6.16.1, addressing all 23 inventoried alerts without changing application behavior or accepted inputs.
- Refreshed the exact distributed Pillow license evidence and notice manifest.
- Passed 68 automated tests, compilation, license verification, exact-package checks, Defender checks, and separate-environment direct/portable validation of the frozen `v0.4.1-alpha.1` candidate.
- Preserved the local-first data model and existing database compatibility; no migration is required.
- Published the unchanged exact candidate as the `v0.4.1-alpha.1` GitHub prerelease after protected documentation review, required CI, and owner approval. The tag targets release commit `6c199cc166ac4e107924f0134249c369f0c233dc`; the public asset remains 43,806,172 bytes with SHA-256 `41C9F5DACB1523FE15730FDA21B014825B7D55141D1C754A31C951DF5AE5DE18`.
- Kept future questionnaire-framework and Windows code-signing planning outside this iteration.

## Iteration 014: Versioned Questionnaire Framework - Complete

- Added immutable, validated questionnaire definitions, stable question/option identities, application-owned deterministic scoring/profile strategies, and fail-closed capability checks.
- Added an append-only migration ledger, immutable definition snapshots, normalized versioned submissions/responses, verified legacy backfill, normalized-first reads, and atomic compatibility writes without dropping or repurposing the existing tables.
- Replaced fixed Today forms with a compact status roster and one reusable definition-driven active form while preserving one submission per questionnaire per calendar date.
- Made Review analytics, report eligibility, PDFs, Analysis Workbooks, and CLI report generation registry-driven and definition-version-aware.
- Preserved exact PHQ-9/GAD-7 behavior, PHQ-9 Item 9 exclusivity, the universal safety message, existing historical records and aliases, and the local-only privacy boundary.
- Kept PHQ-9 and GAD-7 as the only built-in questionnaires. Any future built-in still requires explicit redistribution-rights and clinical-safety approval.
- Deferred custom questionnaire authoring/import. A future custom instrument may explicitly select user-defined deterministic scoring through an allowlisted application-owned strategy, but Len will not automatically add clinical interpretation, severity bands, risk flags, diagnosis, or treatment narrative.
- Automated regression/documentation closeout and the isolated Windows keyboard/reduced-window walkthrough are complete.
- Published the unchanged validated candidate as the [`v0.5.0-alpha.1`](https://github.com/DScannellWiz/len-mental-health/releases/tag/v0.5.0-alpha.1) GitHub prerelease after protected-main evidence review, required Windows Python 3.12 CI, owner approval, and independent public-download verification. Tag `v0.5.0-alpha.1` targets `1fe8af87fe2fb22e73de474a70708f25119e491a`; the public ZIP is 43,700,470 bytes with SHA-256 `F5B4DD956481294BD136345F5C6F02D708943A37851DD80B191A1A987CC0717D`.
- `v0.5.0-alpha.1` is the only supported alpha. `v0.4.1-alpha.1` and earlier prereleases remain downloadable as frozen historical records.

### Post-publication analytical-series correction

- The published `v0.5.0-alpha.1` binary splits definition v1 and v2 trends despite unchanged daily scoring semantics. A narrow source correction explicitly joins PHQ-9 v1/v2 and GAD-7 v1/v2 for trends and derived 14-day analytics, while keeping incompatible future versions separate and preserving exact submission-version provenance.
- A patch-level `v0.5.1-alpha.1` follow-up is recommended after protected-main review and separate candidate/release authorization. No replacement of the `v0.5.0-alpha.1` tag or asset is planned.

## Iteration 010: Extensible Questionnaire Framework - Implementation Complete

- Promoted the reusable assessment registry to a questionnaire extension contract while preserving compatibility names and storage.
- Kept PHQ-9 and GAD-7 as the only built-in, redistributable questionnaires.
- Added per-date questionnaire selection and independent completion state so one or both questionnaires can be recorded on a date.
- Added selectable questionnaire scope for PDFs and Analysis Workbooks.
- Kept PHQ-9 item 9 context specific to PHQ-9 and added a universal safety message before item 1 and in each PDF footer.
- Deferred custom questionnaire authoring, configurable scoring, and external definition files.

### Deferred Cross-Page Scrolling Usability

- Make every primary application page vertically scrollable whenever its content exceeds the available viewport, including when Len is not maximized and at the minimum supported window size.
- Replace large jump-style wheel movement with smooth, fluid scrolling while preserving accessible scrollbar and keyboard navigation.
- Validate the shared behavior across Today, Review, History / Manage Entries, Treatment Events, and How Scoring Works before considering the future usability iteration complete.

## Post-Iteration-009 Housekeeping: Len Product Rename - Completed

The current product name is **Len**, and the canonical repository is [DScannellWiz/len-mental-health](https://github.com/DScannellWiz/len-mental-health). Current window, report, workbook, launcher, installer, README, and product-documentation branding now use Len.

The `phq9_tracker` Python package, `PHQ9Tracker.exe`, `PHQ9_TRACKER_*` environment variables, `%LOCALAPPDATA%\PHQ9Tracker`, `phq9_tracker.sqlite`, and `PHQ9_Tracker.ico` remain compatibility identifiers. Preserving them avoids an unnecessary data-location migration and keeps existing development and packaging contracts stable.

The `v0.3.0-alpha.1` tag, exact artifacts, Iteration 009 record, Closed Alpha archive, and dated validation/provenance statements retain their historical Mental Health Tracker and PHQ9Tracker names. The rename does not rebuild, relabel, validate, publish, or distribute those artifacts.

## Completed Iteration 005

Iteration 005 began the Clarity and Insight work by making recent changes understandable at a glance.

Delivered:

- Executive summary at the beginning of the clinician PDF report.
- Adjacent 14-calendar-day comparisons for PHQ-9 and GAD-7.
- Neutral lower, higher, unchanged, and insufficient-data wording.
- Entry-coverage disclosure so missing check-ins are visible.
- Focused dashboard cards that reuse the same comparison logic.
- Automated comparison tests and rendered PDF validation with synthetic data.

## Completed Iteration 004

Iteration 004 introduced the reusable assessment framework and began the transition from PHQ-9 Tracker to Mental Health Tracker.

Delivered:

- Modular assessment definitions for PHQ-9 and GAD-7.
- New generic `assessment_entries` database table.
- Legacy PHQ-9 migration into the generic assessment table.
- Today's Check-In UI for PHQ-9, GAD-7, notes, and optional treatment events.
- Combined dashboard, reports, and exports.
- Tests for GAD-7 scoring, exports, migration, and dependency-gated report generation.

## Iteration 006: Completed

Iteration 006 delivered data integrity, scoring clarity, and application branding. Automated validation and manual source-GUI validation with the existing production database are complete. Real Windows portable-package validation was completed during Iteration 007.2; installer validation remains pending until Inno Setup is available.

Delivered:

- History / Manage Entries for date-based review, stable-ID assessment editing, note editing, and confirmed deletion.
- Existing-date detection and idempotent daily check-in resubmission.
- Multiple treatment-event checkboxes, explicit custom events, and an Add Another Treatment Event workflow.
- Consistent Daily Severity Score and 14-Day Symptom Frequency Score terminology.
- How Scoring Works guidance in the UI and clinician PDF, including coverage disclosure and the mindful-check-in principle.
- Window, executable, installer, Start Menu, and default desktop shortcut icon wiring.
- Focused automated tests for editing, deletion, migration safety, multiple events, and duplicate prevention.

## Iteration 007: Present-Focused Check-In and Meaningful Review

Delivered:

- Today's Check-In opens first, saves PHQ-9/GAD-7 before optional details, and keeps historical comparisons out of the present-tense assessment experience.
- Previous Day and Next Day navigation handles calendar rollover, existing-entry loading, future-date prevention, and unsaved-change protection.
- Review separates recent trends, current/previous ketamine-cycle observations, and long-term charts.
- Deterministic summaries use neutral, non-causal wording and disclose entry coverage.
- The clinician PDF is a two-to-four-page conversation aid centered on overall pattern, symptom highlights, timeline context, treatment-cycle observations, and discussion prompts.
- Duplicate PHQ-9 response tables and redundant raw-detail sections were removed from the primary PDF.
- Report dependency discovery and release-build preflight checks were improved.
- All 28 automated tests passed with isolated synthetic data, and a representative four-page PDF passed rendered visual inspection.

### Development Narrative and Decision Records

Formal development-narrative capture begins around Iteration 007. Earlier project history is documented as a high-level reconstruction rather than contemporaneous notes. Beginning with this iteration, the development journal and architecture decision records are part of the ongoing process for substantial product and architectural work.

## Iteration 007.1: Navigation and Review Polish

Status: Completed

Implemented small, observable refinements:

- Review charts redraw from live canvas dimensions after resizing and reserve separate vertical bands for the full title, legend, and plot.
- The visible primary-tab order begins with **Today's Check-In**, followed by **Review** and **History / Manage Entries**; startup remains on Today's Check-In.
- **History / Manage Entries** reuses the shared one-day calendar shift behavior for Previous Day and Next Day navigation.
- History has its own unsaved-change snapshot and confirmation, blocks future dates, loads existing records, and disables Next Day on the current date.
- Dates without assessments, notes, or treatment events show a calm manage-only empty state with record-changing controls disabled.
- Nine focused Iteration 007.1 tests were added; all 37 automated tests pass with the dependency-complete project virtual environment.

The project owner completed the manual source-GUI walkthrough against the canonical repository with real-world data. Tab order and startup selection, Review chart titles and resize behavior, History navigation and rollover, existing and empty dates, future-date blocking, and unsaved-change protection passed. This focused polish did not change scoring, storage, reports, exports, or the project's privacy boundary.

## Upcoming Iterations

### Iteration 007.2: Reporting & Analysis - Completed

Delivered:

- Added a separate analysis-ready Excel export with normalized **Daily Assessments**, **Item Responses**, **Notes**, **Treatment Events**, **Treatment Cycles**, and **Metadata** worksheets.
- Added a derived **Daily Summary** convenience worksheet while keeping the normalized worksheets authoritative.
- Used one logical record per row, snake_case field names, ISO dates, stable database-backed or deterministic export identifiers, and documented cross-sheet relationships without merged cells or decorative blank rows.
- Preserved the existing combined CSV/XLSX export for backward compatibility at the time; Iteration 008 later retired this legacy path in favor of the normalized Analysis Workbook.
- Moved a fuller **How to Read This Report** explanation to the beginning of the clinician report and clarified Daily Severity Score, 14-Day Symptom Frequency Score, coverage, and missing check-ins.
- Adopted the compact section flow **Recorded Period Overview**, **Recorded Symptom Trends**, **Treatment Context**, **Journal and Event Context**, and **Conversation Starters**.
- Removed journal-row and character limits. All user-authored notes in the selected period are included verbatim; report length may grow when the recorded narrative requires it.
- Preserved scoring, schema, database routing, legacy PHQ-9 compatibility, and multiple legitimate same-day treatment events.
- Added focused workbook, full-journal, and portable database routing/persistence/reset tests. All 40 automated tests pass with synthetic data.
- Generated and visually inspected a four-page synthetic clinician report.
- Built and validated the real Windows portable package with PyInstaller 6.22.1. The initial folder and ZIP contained no database files; first launch created the portable database in place; the primary screens opened blank; synthetic records persisted across restart; packaged PDF and Analysis Workbook outputs passed review; and database deletion followed by relaunch restored a pristine blank state.
- Validated `PHQ9Tracker-Portable-0.2.0.zip` for the Florida use case. The generic Tk runtime window/taskbar icon remains a deferred cosmetic issue, and installer validation remains pending because Inno Setup is unavailable.

### Future Data Portability & Recovery

Tentative concept; no iteration number is locked:

- Prepare a clean Travel Mode database that contains no historical records.
- Export only records created in that travel database and transactionally append them into an authoritative home database after validating schema, record identity, duplicates, and conflicts.
- After a confirmed import, clear the travel database, create a fresh blank database, and verify that it contains zero assessments, notes, and treatment events.
- Do not implement this as whole-database swapping or silent overwrite behavior.

### Future LAN Sharing

Tentative concept; no iteration number is locked:

- Keep one authoritative database local to a designated host.
- Let LAN clients communicate with an authenticated host/service that is solely responsible for SQLite access.
- Do not open the SQLite file directly over a Windows network share.
- Preserve the local-only boundary: no cloud relay, public Internet service, or automatic external synchronization.

### Iteration 008: Review and Clinician Report Workflow

Status: Complete. Interactive source-GUI validation and the later `0.3.0-alpha.1` packaged validation are recorded below and in the build notes.

Delivered:

- Made Review the single access point for the four agreed actions: **Refresh**, **Import Spreadsheet**, **Generate PDF**, and **Analysis Workbook**.
- Removed the separate Clinician Report tab and its start/end-date controls.
- Made **Generate PDF** calculate the full available assessment-history range each time it is selected.
- Stopped creating a companion CSV beside the clinician PDF.
- Retired the legacy combined CSV/XLSX exporter, its Review and File-menu controls, and its command-line entry point.
- Kept the normalized seven-sheet Analysis Workbook as the sole data-export format.
- Preserved scoring, storage, report content, complete journal text, legacy PHQ-9 data compatibility, and the local-only privacy boundary without a schema migration.
- Added focused workflow/range tests and updated earlier report tests. All 41 automated tests pass with isolated synthetic databases, and source compilation passes.
- Generated and inspected a four-page fictional full-history PDF; all required sections and complete long-form notes were present, the date range was correct, and no companion CSV was created.

### Iteration 008.1: Chart Accessibility and Micro-UX

Status: Completed after Daniel's 2026-08-30 source-GUI walkthrough. Packaged-release validation remains a separate gate.

Delivered:

- Added graph point callouts that show the date, series, and exact score on hover or click. Charts can receive keyboard focus; Left/Right moves between points, Enter displays a point, and Escape clears the callout.
- Added forgiving but bounded point hit targets so value discovery does not depend on precisely tracing a small marker across a wide chart.
- Made valid changed date fields auto-load when focus moves away only if no unsaved edits could be lost. Dates with unsaved edits remain guarded, and saving is blocked when the typed date differs from the loaded check-in.
- Added Enter-to-load on Today and History date fields and F5 refresh; broader global shortcuts were deliberately avoided because their context could be ambiguous or destructive.
- Clarified loaded-date statuses, unsaved-change choices, permanent-deletion confirmations, and save/export completion messages.
- Made PHQ-9 item 9 report context and Conversation Starters recency-aware. Recent above-zero responses use the most recent 14 calendar days; older above-zero responses remain explicitly historical and do not imply current risk; prompts are omitted when no above-zero response exists; recent coverage and missing-information limits are disclosed.
- Applied consistent Segoe UI defaults, roomier notebook tabs, readable table rows, and more consistent button padding and Review action widths without adding a new UI dependency.
- Preserved scoring, the database schema and records, local-only privacy, complete journal text, and the PDF/Analysis Workbook output contracts.
- Added nine focused tests. All 50 automated tests pass in the dependency-complete environment, including PDF and workbook paths, and source compilation passes.
- Daniel confirmed that chart date/score correlation appeared correct, keyboard chart navigation worked, date changes and unsaved-change protection worked, the overall look and feel was acceptable, and several days of ordinary use revealed no general-use issues.
- A non-blocking internal gap between each Spinbox's up/down arrows was carried into 008.2 as minimal visual polish. The walkthrough did not validate packaged 008.1 behavior.

Deferred:

- User-configurable or scalable text and interface sizing remains a future accessibility enhancement because it requires a broader layout and minimum-size review.

### Iteration 008.2: Clinician Output Fidelity and Alpha Output Polish

Status: Complete. Daniel passed the source-GUI walkthrough on August 30, 2026. Closed Alpha candidate `0.3.0-alpha.1` subsequently passed local packaging and fictional packaged validation; distribution remains a separate gate.

Delivered:

- Restore a compact current 14-day symptom profile for PHQ-9 and GAD-7 in the clinician-facing outputs. For each item, present the symptom-present day count and recorded-day coverage as appropriate together with the resulting 0-3 **14-Day Symptom Frequency Score**.
- Reuse the established daily item responses and 14-calendar-day scoring logic. Treat the missing presentation as a regression, not data loss or a scoring-formula defect.
- Preserve the concise conversation-focused PDF and normalized Analysis Workbook purposes; do not bring back the redundant raw-response tables removed in Iteration 007.
- Correct clinician-PDF treatment-event labeling so distinct stored types remain distinguishable. In particular, **Physical Therapy** must not be rendered as counseling **Therapy**, even when the two events share a date and description.
- Add focused regression tests for both assessment types and for two legitimate same-day treatment events with the same description but different stored types. Confirm that the Analysis Workbook preserves the distinct event types.
- Added a normalized **14-Day Item Profile** sheet with one logical current-window record per assessment item; this avoids repeating derived snapshot fields on daily response rows.
- Made `reports` the one generated-output folder for PDF and XLSX files. Portable builds keep it inside the extracted application folder; source runs keep it under the repository.
- Added collision-safe automatic filenames, optional open-after-save prompts, graceful open-failure messages that preserve the saved path, and an **Open Reports Folder** fifth Review action.
- Tightened Spinbox internal arrow padding while retaining spacing between questionnaire items.
- Deliberately deferred user-defined output locations because persistent paths, permissions, removable drives, and settings behavior require a separate design and validation pass before Alpha.

Non-goals:

- No database migration, scoring change, record correction, or deletion of the valid 2026-08-11 events.
- No broader clinician-report redesign, reintroduction of legacy export paths, user-configurable output destination, or database migration.
- The Treatment Cycles comparison chart remains unchanged. A future iteration may overlay the current ketamine cycle and the two previous cycles on one chart using three distinct colors.

### Public Repository Soft Launch - Preparation

Status: Licensing and notice packaging are implemented, the Tcl/Tk startup crash is repaired in a pinned `redistribution.2` candidate, and Daniel's hands-on development-workstation GUI walkthrough passed on that exact hash. Separate-machine validation of `.2` remains unavailable. The sensitive Git history has been rewritten and Daniel selected GPLv3. No repository visibility, release, tag, upload, Form, or social-media action is part of this iteration.

Current direction:

- Preserve `0.3.0-alpha.1` as an explicit alpha/pre-release candidate for an initial public soft launch.
- Use GitHub Releases as the eventual official download path for the validated portable ZIP; do not commit release archives to the repository.
- Keep the project local-first and accept only software-focused feedback. Never request or accept databases, reports, workbooks, tracker-entered content, or screenshots containing health or private data.
- Document unsigned Windows security behavior without instructing users to disable protection or override an actual threat detection.
- Require backup and storage-mode verification before a portable update so users do not confuse portable data with `%LOCALAPPDATA%` data.
- Keep the abandoned Closed Alpha documents as clearly labeled historical provenance. Do not resume tester IDs, acknowledgments, cohort enrollment, or private Form publication.

Before repository publication:

- Push the reviewed local release-readiness commit only with Daniel's separate authorization.
- After the push, re-run the GitHub/server history, tracked-file, and release-readiness privacy checks.
- Make the repository public only after that audit and Daniel's separate visibility decision.

After repository publication:

- Create a GitHub Release only with separate authorization, attach the already validated ZIP, mark it as a pre-release, and publish its SHA-256 hash.
- Consider one focused GitHub issue template if public issue reports show that the no-health-data boundary needs stronger in-form reinforcement.
- Consider code signing as a future trust and publisher-identity improvement; it does not replace antivirus scanning or release validation.

### Closed Alpha Program - Historical and Abandoned

The planned September 2026 Closed Alpha was abandoned before enrollment or distribution. Its tester-ID, acknowledgment, cohort, milestone, and private Google Form workflow is superseded and must not be presented as current instructions. The archived materials remain under [docs/alpha](docs/alpha/README.md) as provenance, and their strict health-data firewall continues to inform public support boundaries.

## Security and Privacy

- Optional encrypted database.
- Optional application password.
- Password-protected PDF reports.
- Encrypted backup and restore.
- Password-manager-friendly unlock flow.

## Data Management

- Backup scheduling.
- Restore wizard.
- Database integrity verification.
- Explicit migration history tracking.

## Reporting

- More compact clinician report templates.
- Improved treatment effectiveness summaries.
- Better trend visualization.
- Symptom correlation charts.

## Architecture

- External assessment definition files.
- Reusable scoring and import adapters.
- Configurable custom questionnaires with explicit deterministic scoring through allowlisted application-owned strategies and raw-only/descriptive outputs; no automatic clinical interpretation.
- Plugin-ready assessment library.

## Long-Term Direction

Support multiple validated mental health assessment instruments while remaining local-first, privacy-first, open source, easy to use, and clinically useful for discussion.
