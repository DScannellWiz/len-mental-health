# Iteration 014.2: One Built-in Severity Model

## Objective

Implement Dan's September 19, 2026 product decision: PHQ-9 and GAD-7 each have one public identity. Every stored daily item value, including rows associated with the older internal snapshot, is a 0-3 daily severity rating. Keep average item severity separate from derived 14-day frequency scoring.

## Forensic findings and design

- Internal snapshot keys 1 and 2 differ in response labels and instructions. Stable item IDs, numeric response values and scores, total ranges, profile rules, and PHQ-9 Item 9 behavior have the same analytical signature. Earlier version-one frequency labels were an implementation error; they never change the meaning of recorded values.
- Normalized submissions have a composite foreign key to immutable definition snapshots. Snapshot update/delete triggers and reconciliation checks protect stored records. Rewriting keys would require disabling or replacing these safeguards and would not improve a score. This iteration therefore leaves stored snapshots and submission keys intact as **internal compatibility metadata**, while using the approved single severity meaning at every public read boundary.
- No data migration is needed. Existing transactional/idempotent startup reconciliation continues unchanged. New submissions continue to use the active severity-labeled snapshot. Future incompatible definitions retain distinct analytical signatures and series rather than entering the built-in compatibility map automatically.
- The local v0.5.1-alpha.1 candidate built from `95405660507028c9709f356f0081fa2c7250596e` is rejected and permanently superseded. Its SHA-256 is `959FE6DFC5A0F6BE909C27CB1D4369A6EDECF9506CEA6EB7494EA70D91657BB3`.

## Calculations

- Daily questionnaire total: sum of that day's 0-3 item severities, 0-27 for PHQ-9 or 0-21 for GAD-7.
- Item average severity: arithmetic mean of that item's recorded daily 0-3 ratings in the selected period, displayed to one decimal. The denominator is the number of recorded check-ins for that questionnaire and item. Unrecorded days contribute neither a value nor a denominator. No clinical category is assigned to the average.
- Derived 14-day frequency: for each recorded check-in, severity above zero contributes one present day for that item. Map present-day counts 0 to 0, 1-6 to 1, 7-11 to 2, and 12-14 to 3. Sum per-item frequency scores for the derived total. Coverage is recorded check-ins out of 14 calendar days; missing days remain unknown.
- PHQ-9 Item 9 context remains bound only to `phq9.item9`.

## Files modified

- `src/phq9_tracker/app.py`: one public built-in identity, common severity labels, separate average and derived frequency calculations and Review tables, PDF and workbook views, CLI wording, and workbook schema 1.4.
- `tests/test_iteration_014_reports.py`, `tests/test_iteration_014_persistence.py`, `tests/test_iteration_014_questionnaire_contracts.py`, `tests/test_iteration_007_2_reporting_portable.py`: update output contracts and mixed-history checks.
- `README.md`, `ROADMAP.md`, `BugList.md`, `BUILD_AND_RELEASE.md`, `docs/releases/v0.5.1-alpha.1.md`: current behavior and rejected-candidate status.

## Validation

- 112 automated tests pass in the project environment. The new fictional mixed-history check verifies unchanged submission IDs, dates, totals, and notes after restart, one chronological series across internal keys, missing-day exclusion from averages, presence counts, every 14-day threshold boundary, and the derived total.
- A fictional PDF and workbook were generated from mixed stored keys. The PDF text contained no built-in v1/v2 variant, carried separate average and frequency sections and coverage language, and retained Item 9 context. The workbook had ten sheets, no cell errors, unified severity labels, and no v1/v2 string in cell values. All PDF pages were rendered for visual inspection.
- Existing tests cover save/edit/delete, notes, same-day PHQ-9 and GAD-7, treatment events, Review, PDF, workbook, CLI, and Item 9 restriction. The public v0.5.0 release was not modified.

## Remaining work

- Dan's hands-on source-GUI review and protected-main PR/Windows CI are outstanding. A new candidate must use a newly selected version and be validated independently; the rejected v0.5.1 ZIP cannot be reused.

## Lesson

Immutable storage snapshots are valuable integrity evidence, but their implementation identifiers do not have to be public clinical concepts. A public read model can express the owner's corrected semantics without rewriting safe stored data.
