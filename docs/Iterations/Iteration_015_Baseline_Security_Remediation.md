# Iteration 015: Baseline Security Remediation

## Objectives

- Remove temporary clinician-report chart files after successful and failed report generation.
- Make one spreadsheet import transactional across assessment data, notes, normalized questionnaire records, and imported treatment events.
- Prevent spreadsheet applications from interpreting exported user-authored text as formulas while preserving the exact text.
- Prevent chart-file collisions when one questionnaire produces more than one analytical series.

## Design Decisions

- The public questionnaire-save and treatment-event functions retain their existing behavior. Small connection-aware internal functions allow spreadsheet import to reuse the same write logic inside one caller-owned SQLite transaction.
- The import workbook is closed in a `finally` block. A late invalid row therefore closes the input and causes the transaction context to roll back all earlier writes from that workbook.
- Every non-empty string in analysis-workbook data rows is explicitly marked as an OOXML string after the dataframe is written. This preserves leading `=`, `+`, `-`, and `@` characters without adding an apostrophe or changing the visible value.
- PDF charts are generated inside `TemporaryDirectory`, whose lifetime includes the complete ReportLab build. Cleanup therefore occurs only after the PDF has finished consuming the images, and also occurs when the build raises an exception.
- Chart filenames use a one-based analytical-series index. This is intentionally independent of stored definition-version labels, which remain an internal compatibility detail for the current built-in questionnaires.

## Files Modified

- `src/phq9_tracker/app.py`
- `tests/test_baseline_security_remediation.py`
- `BugList.md`
- `ROADMAP.md`
- `docs/Iterations/Iteration_015_Baseline_Security_Remediation.md`

## Validation Performed

- Forced an error on a later imported row and verified that all database tables remained byte-for-byte equivalent at the row level to their pre-import snapshots.
- Imported a fully valid fictional workbook twice and verified complete normalized records plus deduplicated treatment events.
- Exported fictional text beginning with `=`, `+`, `-`, and `@`; reopened the workbook in formula and calculated-value modes; and verified exact values, string cell types, and no formula cells.
- Generated a report successfully and forced a controlled ReportLab build failure; verified no report chart directory remained in either case.
- Simulated two analytical series for one questionnaire and verified distinct filenames and correct chart-to-caption association.
- Ran the directly related reporting, clinician-output, entry-management, and persistence regression suites.

## Privacy and Security Implications

- Temporary chart images derived from sensitive local health information no longer persist after report generation.
- A malformed import cannot silently leave a partial health-data history.
- Exported user text cannot become an active spreadsheet formula merely because of its first character.
- Tests use only fictional records and temporary databases, workbooks, images, and reports.

## Remaining Work

- The remediation implementation did not perform release packaging, executable/runtime validation, publication, or a broader security scan. Subsequent source-assessment results are recorded below; they do not establish release/artifact readiness.
- Existing import acceptance behavior is unchanged: rows without a parseable date or a complete set of item values are skipped, and numeric cells are converted with the legacy integer conversion before the 0-3 range check. A fresh review flagged stricter malformed-row and fractional-value rejection as potential follow-up work, but changing that policy is outside this validated-finding remediation.
- Existing unrelated SQLite `ResourceWarning` messages observed in report tests remain outside this bounded remediation.

## Lessons Learned

- Transaction boundaries should follow the user's complete operation, not individual helper calls.
- Temporary-file ownership must cover the entire lazy-consumption lifetime of downstream document builders.
- Spreadsheet safety requires controlling the stored cell type, not visually modifying the user's text.

## Baseline Assessment Closure Checkpoint — 2026-10-03

### Source and Evidence

The security-remediated protected-main baseline is `dfa669168dca77caf684970e5c7387d21eaa0cc1`, resulting from [PR #12](https://github.com/DScannellWiz/len-mental-health/pull/12). Repository identity and the existing remediation documentation were checked during this reconciliation. CodeQL and Semgrep execution results below are established owner-supplied evidence; those tools were not rerun during this documentation-only task. The Deep Scan status comes from the recorded authoritative scan-context inspection, not an inference from worker activity.

### Threat Model, Targeted Review, and Remediation

Phase 1 threat modeling and attack-surface mapping completed. Subsequent targeted source review validated three Medium findings:

1. Sensitive temporary report-chart residue.
2. Non-atomic spreadsheet import, allowing earlier valid rows to persist when a later row was invalid.
3. XLSX formula interpretation of user-controlled note text.

All three were remediated and merged through PR #12. The implementation and regression validation are documented above.

Lower-severity observations retain their original boundaries: chart filename collision was Low/future-facing (distinct filenames were subsequently added in this iteration); GUI destination TOCTOU remains Low defense-in-depth; helper-interpreter selection remains an Informational/Low local trust-boundary observation. This checkpoint does not silently close those latter observations or the import-policy and SQLite warning follow-ups listed above.

### CodeQL — PASS for This Static-Analysis Layer

CodeQL CLI 2.27.1 ran locally against a pristine detached worktree at exactly `dfa669168dca77caf684970e5c7387d21eaa0cc1`. Database creation and `python-security-extended.qls` completed successfully. The invocation executed 52 queries and reported 25/25 Python files and 1/1 GitHub Actions files scanned. Its SARIF contained zero security findings. This result is not proof that Len is vulnerability-free.

### Semgrep — Zero Validated Security Findings

Semgrep Community Edition 1.179.0 completed locally against the same pristine baseline using `p/security-audit`: 113 Git-tracked targets, approximately 100% of parsed lines, and 80 applicable rules executed.

One candidate, `python.lang.security.use-defused-xml.use-defused-xml`, flagged `from xml.sax.saxutils import escape`. Targeted validation established that the ReportLab output path uses:

```python
safe_value = escape(str(value)).replace("\n", "<br/>")
```

The escaped value is then used to construct a ReportLab `Paragraph`. This site performs output escaping, not XML parsing, so the XXE/XML-bomb threat model does not apply. Disposition: **not applicable / false positive**. Validated Semgrep security findings: **zero**.

### Codex Security Deep Scan — INCOMPLETE / NON-BLOCKING

The scoped `packaging/` scan `24491e83-63f9-4d0b-be0b-ce67aa7c5516` terminally failed during discovery after three consecutive unsuccessful discovery workers. The last failure was `transient_error` because the Work usage limit was reached.

The authoritative inspection reported:

- 0 active workers and 3 completed workers.
- No saved validated findings (`findings: []`, count `0`).
- No successfully completed security report; the scan is not resumable.
- 14 scoped files, 0 worklist rows, 0 closed rows, and review pass 2.
- Incomplete coverage; no measured `usage.totalTokens`, `usage.inputTokens`, `usage.cachedInputTokens`, or `usage.coverage` returned.

**Zero saved findings from this failed scan is not a clean-scan result.** Completed-worker counts do not establish completed scope coverage. This scoped attempt also provides no repository-wide Deep Scan assurance. No Deep Scan was run, resumed, retried, or recovered during this reconciliation.

Deep Scan is optional additional assurance, not a required Len security/release gate under the current workflow. Its disposition is **INCOMPLETE / NON-BLOCKING due to tooling/resource limits**.

### Qualified Baseline Conclusion

Across the completed threat modeling, targeted reasoning review, remediation, CodeQL analysis, and Semgrep analysis, there are presently no unresolved validated Medium-or-higher security findings from this baseline assessment. This is not a claim that Len is vulnerability-free. Codex Security Deep Scan did not complete and provides no clean-scan evidence.

This closes the baseline assessment with the limitations and follow-ups recorded here. Tests/CI, dependency scanning, secret scanning, deterministic static analysis, targeted reasoning review for high-consequence changes, and release/artifact verification remain complementary controls. This checkpoint neither enables new tooling nor substitutes source-assessment evidence for Windows trust, signing, packaged-runtime, or exact-artifact verification.

### Documentation Reconciliation

Only this existing checkpoint and its `ROADMAP.md` summary were updated. Validation is limited to source-identity checks, documentation diff review, and consistency checks; no application tests or scanners were rerun. Application code, tests, dependencies, configuration, GitHub state, release artifacts, signing state, and Windows security controls were not changed.
