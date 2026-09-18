Current as of: 2026-09-18
Last substantive update: 2026-09-18

BUG: Iteration 014 displayed frequency wording for daily severity responses

Status: Corrected for the v0.5.0-alpha.1 pre-release; exact-candidate validation pending

Iteration 014 introduced shared response labels reading `Not at all / Several days / More than half the days / Nearly every day` even though Len stores and totals each check-in as single-day symptom severity. PHQ-9 and GAD-7 were both affected. The separate derived 14-day symptom-frequency calculation was not affected.

Resolution:

- Added active PHQ-9 and GAD-7 definition v2 with `Not present / Mild / Moderate / High` labels and an explicit single-day severity instruction.
- Preserved the immutable v1 snapshots and their hashes; existing and backfilled v1 records remain versioned as v1.
- Prevented the known-regressed v1 frequency labels from appearing as historical daily-response interpretation by exporting numeric v1 `response_label` values.
- Kept daily totals, the `> 0` symptom-present rule, 14-day frequency thresholds, version-separated analytics, and PHQ-9 Item 9 behavior unchanged.

---

ITERATION NOTE: Questionnaire selection and completion status

Status: Implemented in Iteration 010; manual Windows GUI validation pending

- PHQ-9 and GAD-7 can be selected independently for a date; an unselected questionnaire is not stored as a zero-score entry.
- Completion state is derived from saved records and is displayed separately for each questionnaire.
- PDF and workbook generation can be limited to selected questionnaires.
- PHQ-9 item 9 context remains PHQ-9-only. A universal safety message appears before questionnaire item 1 and in PDF footers.

---

BUG: Today's Check-In optional submit controls can be clipped

Status: Fixed in Iteration 010; manual Windows confirmation pending

At common Windows display heights, the expanded optional-details section extended below the application window with no way to reach its submit controls.

Resolution:

- Made only the Today's Check-In page vertically scrollable while preserving its existing form and save behavior.
- Added mouse-wheel and visible-scrollbar navigation.
- Automatically scrolls to the optional-details controls after the core check-in is saved, then returns to the top after the optional flow closes.

---

BUG: Report generation dependency detection

Status: Improved in Iteration 007; portable validated in Iteration 007.2; installed validation pending

Iteration 004 note:

- Automated report tests are dependency-gated because the active Python environment in this Codex session did not expose `reportlab`.
- The app still needs a more reliable installed/portable dependency discovery path before report generation can be considered frictionless in all builds.



When generating reports or spreadsheets, the application may incorrectly report missing Python dependencies (openpyxl, reportlab, Pillow, pandas) despite a valid Python environment being available.



Investigate:

\- PHQ9\_TRACKER\_BUNDLED\_PYTHON handling

\- Portable mode behavior

\- Installed mode behavior

\- Launcher environment detection

\- Packaging script dependency validation



Expected:

Application automatically locates bundled Python or installed Python environment and generates reports without requiring user configuration.

Resolution notes:

- Source report generation now checks `PHQ9_TRACKER_BUNDLED_PYTHON`, `.venv`, and `venv` for a compatible Python environment.
- Candidate environments are validated for the packages required by the requested action before a helper process is started.
- Missing-dependency errors identify the required modules and supported configuration paths.
- The source launcher prefers project-local virtual environments.
- The release script performs a dependency preflight before PyInstaller packaging.
- Automated dependency-probe and full report-generation tests passed.
- The Iteration 007.2 portable build generated both the clinician PDF and Analysis Workbook successfully. Installed-mode report generation still requires installer validation.


---

REPORTING NOTE: 14-day executive comparison

Status: Implemented in Iteration 005

- The current period is the 14 calendar days ending on the selected report end date.
- The comparison period is the immediately preceding 14 calendar days.
- PHQ-9 and GAD-7 use the same symptom-frequency conversion already used elsewhere in the app.
- Entry coverage is displayed because missing days count as no recorded symptom-present response.
- If either period has no entries, the report states that there is not enough data for comparison.


---

BUG: Incorrect 14-day PHQ-9 scoring logic

Status: Fixed

The app previously displayed a recent/14-day average as if it were the intended clinical-style 14-day PHQ-9 score.

Fix:

- Added `calculate_14_day_symptom_frequency_score(entries)`.
- Counts item presence across the most recent 14 calendar days ending on the most recent entry date.
- Converts item day counts using:
  - 0 days = 0
  - 1 to 6 days = 1
  - 7 to 11 days = 2
  - 12 to 14 days = 3
- Sums converted item scores for the 14-day total score.
- Assigns severity using normal PHQ-9 total score bands.
- Missing calendar days count as no recorded symptom-present day and are documented via `entries_included`.
- Updated GUI dashboard, item summaries, clinician report, and data export labels/calculations.

---

Application Branding

Status: Open; packaged runtime discrepancy confirmed in Iteration 007.2

Description:
Executable and running application do not consistently use the Len application icon.

Expected:
- EXE icon uses the current `PHQ9_Tracker.ico` compatibility asset (or a future Len-specific replacement)
- Window icon uses the same icon
- Installer uses the same icon
- Desktop shortcut defaults to the same icon

Priority:
Low

Iteration 007.2 validation note:

- Source code calls `iconbitmap` with `packaging\assets\PHQ9_Tracker.ico`.
- PyInstaller embeds the same asset through `--icon`; Inno Setup and installed shortcuts also reference it.
- PyInstaller 6.22.1 embedded the intended icon in the portable executable.
- The packaged application launched successfully, but its running window/taskbar representation still showed the generic Tk feather.
- This is a deferred low-priority cosmetic packaging issue and does not block the validated Florida portable ZIP.
- Inno Setup remains unavailable, so installer, Start Menu, and desktop-shortcut icon behavior is still unvalidated.

---

BUG: Duplicate notes and treatment events when updating an existing daily check-in

Status: Fixed in Iteration 006

Priority: High

Description:

When a user resubmits a check-in for a date that already contains data, the application may create additional note and treatment-event records instead of updating the existing records.

Observed behavior:

- A user updated an existing date to add a therapy treatment tag and appointment note.
- The user then submitted the same date again after correcting the GAD-7 responses and changing one word in the note.
- The assessment scores did not appear to duplicate.
- The therapy treatment event and note were duplicated.

Expected:

- The application detects when data already exists for the selected date.
- The user can review and edit the existing PHQ-9, GAD-7, note, and treatment-event data.
- Resubmitting a daily check-in updates existing records by default rather than silently creating duplicates.
- The application provides an explicit option to add an additional treatment event when multiple legitimate events occurred on the same date.
- Users can delete accidental notes, treatment events, or assessment entries.
- Destructive actions require confirmation.

Implementation considerations:

- Add a History or Manage Entries screen.
- Allow users to select a date and view all associated records.
- Provide edit and delete controls for assessments, notes, and treatment events.
- Preserve stable record IDs when updating existing records.
- Distinguish between “Update existing entry” and “Add another event.”
- Add automated tests covering repeated submissions, edits, deletions, and multiple valid treatment events on one date.

Resolution:

- Today's Check-In detects and loads existing dates and uses assessment upserts plus synchronized day-level note updates.
- Daily event selections update the first matching date/type record rather than appending another copy.
- History / Manage Entries preserves stable assessment and event IDs during edits and requires confirmation before deletion.
- The explicit Add Another Treatment Event action can intentionally create a second legitimate event, including another event of the same type.
- Automated duplicate-prevention, editing, deletion, migration, and multiple-event tests passed with synthetic data.
- Manual GUI validation completed successfully with the existing production database: prior entries loaded, edits persisted after restart, repeated saves created no duplicates, multiple same-day treatment events were retained, and confirmed deletion behaved as intended.
- Portable persistence and reset behavior passed in the real Windows package. Installed distribution validation remains pending because Inno Setup is unavailable; this packaging limitation does not affect the duplicate-entry fix.

---

## BUG: Duplicate PHQ-9 14-day response table in clinician report

Status: Fixed in Iteration 007

Priority: Medium

Description:

The clinician report renders the same PHQ-9 14-day response data twice:

- “Most Recent 14-Day Symptom Responses”
- “Recent Symptom Detail”

Both sections contain the same dates, item values, totals, and severity labels.

Expected:

- Keep a single PHQ-9 14-day response table.
- Remove the duplicate section unless it is redesigned to provide genuinely different information.
- Prefer retaining “Most Recent 14-Day Symptom Responses” and removing the redundant “Recent Symptom Detail” section.
- Add a regression test that verifies the table is rendered only once.

Resolution:

- Replaced the raw-detail-heavy primary PDF with a compact conversation-focused report.
- Removed both redundant PHQ-9 raw response-table headings from the primary PDF; detailed records remain in data exports.
- Added a rendered-report regression test that confirms the old duplicate sections are absent. Typical reports remain compact, while narrative-heavy reports may grow rather than truncate user text.

---

## BUG: Per-item 14-Day Symptom Frequency Scores are no longer presented

Status: Resolved in Iteration 008.2

Priority: Medium

Description:

The current clinician report and Analysis Workbook do not present the resulting 0-3 **14-Day Symptom Frequency Score** for each PHQ-9 and GAD-7 item. The underlying daily item responses remain available, and the established 14-day scoring logic remains intact. This is an information-presentation regression, not data loss or a scoring-formula defect.

Expected:

- Add a compact current 14-day symptom profile for both PHQ-9 and GAD-7.
- Show each assessment item, the symptom-present day count and recorded-day coverage as appropriate, and the resulting 0-3 14-Day Symptom Frequency Score.
- Reuse the established 14-calendar-day scoring logic and disclose the effect of missing check-ins consistently with the existing report guidance.
- Do not restore the redundant raw-response tables removed in Iteration 007.
- Preserve the database schema, stored responses, scoring formulas, and the distinct purposes of the readable clinician PDF and analysis-ready workbook.

Resolution:

- Added a compact current-window profile to the clinician PDF and a normalized **14-Day Item Profile** worksheet with one derived record per PHQ-9/GAD-7 item.
- Each record shows symptom-present days, recorded-day coverage out of 14 calendar days, and the established 0-3 frequency score. Missing days remain identified as missing information.
- Added complete- and incomplete-coverage regression tests without restoring redundant daily raw-response tables.

---

## BUG: Clinician PDF collapses Physical Therapy into Therapy

Status: Resolved in Iteration 008.2

Priority: High

Description:

On 2026-08-11, the database and application UI correctly contain two distinct legitimate treatment events, **Therapy** and **Physical Therapy**, with the same description. The generated clinician PDF renders both event types as **Therapy**. The stored records are valid; this is a report presentation/mapping defect, not a duplicate-record or data-integrity problem.

Expected:

- Preserve enough of the stored treatment-event type in the clinician PDF to distinguish Physical Therapy from counseling Therapy.
- Do not infer the event type from a shared description or collapse distinct stored types into one display label.
- Add regression coverage using two legitimate same-day events with the same description and different stored types.
- Confirm that the Analysis Workbook continues to preserve the distinct event types while implementing the PDF correction.

Resolution:

- Physical Therapy is matched before the broader Therapy display category, so the PDF preserves the distinction without inferring type from the description.
- Synthetic regression coverage uses same-day Therapy and Physical Therapy records with the same description and confirms that the PDF and workbook both retain distinct labels.

---

## Iteration 007.1: Navigation and Review Polish

Status: Completed

Priority: Small polish batch

Scope:

- Fix the overlapping or clipped Review chart titles.
- Reorder the tabs so **Today's Check-In** is the first tab and remains the startup selection.
- Add **Previous Day** and **Next Day** navigation to **History / Manage Entries** by reusing the established date-navigation behavior.
- Preserve unsaved-change protection and future-date prevention.
- Show a calm empty state for dates with no historical records.

Expected:

- PHQ-9 and GAD-7 Review chart titles remain fully readable and do not collide with chart or legend content, including at smaller supported window sizes.
- The visible tab order follows the primary workflow: today's recording first, intentional Review second, and historical maintenance afterward.
- History navigation handles month and year rollover, loads existing records, and does not discard unsaved edits without confirmation.
- Users cannot navigate to or create future-dated check-ins through the shared controls.
- A date without assessments, notes, or treatment events is described calmly and provides an understandable path to another date.

Implementation:

- Review charts now redraw using the live canvas width and height and place the legend below the rendered title before the plot begins.
- The tab order is Today's Check-In, Review, History / Manage Entries, Treatment Events, Clinician Report, and How Scoring Works; startup explicitly selects Today's Check-In.
- History reuses the shared calendar-day shift logic, preserves month/year rollover, loads existing records, blocks future dates, and confirms before discarding unsaved edits.
- Empty dates use a calm manage-only status and disable record-changing controls so History does not become an accidental new-entry flow.
- Nine focused tests cover tab order, History navigation and rollover, existing and empty dates, future-date blocking, unsaved-change protection, and responsive chart layout. The dependency-complete test run passed all 37 tests.

Validation:

- The project owner completed the manual source-GUI walkthrough against the canonical repository with real-world data. Tab order and startup selection, Review chart titles and resize behavior, History navigation and rollover, existing and empty dates, future-date blocking, and unsaved-change protection passed.
- Iteration 007.1 is complete. Installed and portable package validation remains outside this iteration.

---

## Iteration 008: Legacy export and report workflow cleanup

Status: Implementation, automated validation, and rendered synthetic-PDF validation complete; interactive GUI validation pending

Resolved:

- Review now exposes exactly **Refresh**, **Import Spreadsheet**, **Generate PDF**, and **Analysis Workbook**.
- The separate Clinician Report tab and its manual start/end-date controls were removed.
- PDF generation recalculates the earliest and latest assessment dates each time and produces no companion CSV.
- The legacy combined CSV/XLSX exporter, its UI controls, and its command-line entry point were removed.
- The normalized seven-sheet Analysis Workbook remains the sole data-export format.

Validation:

- All 41 automated tests pass with isolated synthetic databases.
- Source compilation passes.
- Focused tests cover the four Review actions, tab removal, refreshed full-history bounds, PDF-only output, and removal of the legacy export function.
- A four-page fictional full-history PDF passed text extraction and page-by-page rendered inspection with the correct range, complete long-form notes, and no companion CSV.

---

## Iteration 008.1: Chart accessibility and micro-UX

Status: Completed; source-GUI validation passed on 2026-08-30. Packaged validation remains a release gate.

Resolved:

- Review chart points now expose date, series, and exact score by hover or click, with a larger bounded hit target and keyboard point navigation.
- Valid changed dates auto-load only when no unsaved edit could be lost. Unsafe focus changes preserve the current edits, and Today's Check-In cannot save visible responses to a date that has not been loaded.
- Loaded-date statuses, unsaved-change choices, permanent-deletion confirmations, and save/export messages state their consequence more clearly.
- PHQ-9 item 9 report context uses the latest 14-day window, discloses recent check-in coverage, labels older responses as historical without inferring current risk, and omits the item 9 prompt when no above-zero response exists.
- Button padding, Review action widths, notebook tabs, table rows, and default typography use more consistent readable sizing.

Validation:

- Nine focused Iteration 008.1 tests were added.
- All 50 automated tests pass with isolated fictional databases in the dependency-complete environment; PDF and normalized workbook paths ran without skips.
- Source and test compilation passes.
- On 2026-08-30, Daniel confirmed during ordinary source-GUI use that chart dates/scores appeared correctly correlated, keyboard chart navigation worked, date changes worked, the unsaved-change warning worked, the overall look and feel was acceptable, and no general-use issues had appeared over several days.
- Daniel noted one non-blocking cosmetic issue: the PHQ-9/GAD-7 Spinbox up/down arrows had an awkward internal gap. Iteration 008.2 tightens that padding while retaining spacing between questionnaire items.
- This walkthrough did not validate a packaged 008.1 build. Packaged portable validation remains open, and scalable text/interface sizing remains a future enhancement.

---

## Iteration 008.2: Clinician output fidelity and Alpha output polish

Status: Resolved. Daniel's source-GUI walkthrough passed on 2026-08-30; candidate `0.3.0-alpha.1` passed local fictional packaged validation on 2026-08-31.

Resolved:

- Restored the compact per-item current 14-day profile for PHQ-9 and GAD-7 in both clinician outputs.
- Preserved Physical Therapy as distinct from counseling Therapy in the PDF and Analysis Workbook.
- Unified PDF and workbook generation under the local `reports` folder, including portable-relative containment, collision-safe filenames, optional open-after-save prompts, and **Open Reports Folder** as the approved fifth Review action.
- Tightened Spinbox internal arrow padding without redesigning the questionnaire or adding a dependency.
- Preserved scoring, schema, records, migration behavior, complete journal text, 008.1 interaction safeguards, and the no-legacy-CSV contract.

Validation:

- Source/test compilation and the 59-test dependency-complete suite passed.
- Daniel passed repeat PDF/workbook generation, Open Reports Folder, real-output fidelity/readability, Spinbox, and 008.1 regression checks.
- The packaged five-page PDF and eight-sheet workbook passed content, structure, and rendered visual inspection using project-created fictional data only.
- A packaging-only Tcl/Tk discovery defect found in the first attempt was corrected before the candidate was accepted.
