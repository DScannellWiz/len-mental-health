Current as of: 2026-09-17

# Iteration 014 - Extensible Questionnaire Framework

## Status

**Iteration 014 is complete. Gates A through G are closed.** Gate B established immutable definitions and application-owned strategies; Gate C added transactional migrations, immutable definition snapshots, normalized submissions/responses, verified backfill, normalized-first compatibility reads, and atomic compatibility writes. Gate D implemented the approved one-active-form Today interaction and atomic multi-questionnaire saves, then passed its required live Windows GUI validation. Gate E moved profiles and total-score trends behind declared definition capabilities without changing current PHQ-9/GAD-7 results. Gate F made report selection and outputs registry-driven, definition-version-aware, safety-preserving, and exact-artifact validated. Gate G added backup/restore regression coverage, reconciled the directly affected user, privacy, architecture, roadmap, and build documentation, and passed the required owner-run Windows keyboard/reduced-window walkthrough.

- Development branch: `iteration-014-questionnaire-framework`
- Frozen starting commit: `ecfe156324b751c49a36b2a7037d0e1f289a2e24`
- Iteration 013 is closed.
- Published `v0.4.0-alpha.1` and `v0.4.1-alpha.1` artifacts, tags, and release records are immutable and outside this iteration.
- The advance-planning record dated 2026-09-13 is the design input for this checkpoint. This active document preserves its implementation boundaries and gate sequence.
- Gate C changed the database additively. Both legacy tables and their public compatibility behavior remain in place; no table or column was dropped, renamed, or repurposed.

## Objectives

- Extend the completed Iteration 010 questionnaire registry into immutable, validated questionnaire, question, response-option, scoring, profile, interpretation, and behavior contracts.
- Preserve existing PHQ-9 and GAD-7 behavior and all readable historical data.
- Add normalized, versioned storage additively before allowing definitions that do not fit the legacy fixed-column schema.
- Replace fixed questionnaire layouts and output paths with registry-driven UI, analytics, PDF, and workbook behavior in later gates.
- Keep PHQ-9 Item 9 behavior exclusive to PHQ-9.
- Preserve the universal safety message as an application invariant before Question 1 and in clinician outputs.
- Establish safe seams for later custom questionnaires without adding authoring, import, plugins, or automatic clinical interpretation.

## Existing Baseline Confirmed

The starting source matches the planning assumptions:

- Iteration 010 already provides `QuestionnaireDefinition`, `QUESTIONNAIRES`, and `QUESTIONNAIRE_ORDER` as public aliases over the existing assessment vocabulary.
- PHQ-9 and GAD-7 are the only registered built-ins.
- Per-date selection, independent completion status, questionnaire-filtered PDF/workbook generation, questionnaire-specific 14-day profiles, the universal safety message, and PHQ-9-specific Item 9 handling already exist.
- `assessment_entries` is the generic compatibility table and `phq9_entries` remains synchronized for legacy PHQ-9 behavior.
- `assessment_entries` still has fixed `item1` through `item9` columns, integer `0..3` validation, and one row per `(assessment_id, entry_date)`.
- There is no explicit database migration ledger or immutable questionnaire-definition snapshot store.
- Today and History rendering still use fixed Spinboxes and assume `0..3` responses; reports and charts still contain explicit PHQ-9/GAD-7 paths.

The implementation must extend Iteration 010, not replace or rename it.

## Scope

### In scope

- Immutable validated domain contracts and allowlisted strategy/behavior registries.
- Exact PHQ-9/GAD-7 compatibility definitions with explicit response options, versions, rights metadata, scoring, profile, and interpretation policies.
- Additive versioned definition snapshots, normalized submissions/responses, a migration ledger, verified backfill, normalized-read compatibility adapters, and atomic compatibility writes.
- Registry-driven questionnaire selection/status and one active reusable form once its interaction design is approved.
- Definition-driven analytics, questionnaire-specific graphs and 14-day profiles, and registry-driven PDF/workbook selection.
- Synthetic legacy migration, privacy, report-rendering, accessibility, and Windows GUI regression validation.

### Non-goals

- Custom questionnaire authoring, import, download, plugin/community loading, translation authoring, or cloud synchronization.
- Executable formulas, callbacks, scripts, templates, HTML, or report markup supplied by a definition.
- New built-in questionnaires without separate rights, clinical-safety, and owner approval.
- Automatic clinical interpretation, bands, risk flags, diagnosis, or treatment narrative for future custom questionnaires.
- Unrelated refactors, general UI polish, cross-page scrolling backlog, dependency changes, signing, packaging, releases, tags, or GitHub configuration.

## Owner Decision Gate

Production work was paused until the owner approved or changed these linked product defaults:

1. Show one active questionnaire form at a time, selected from a compact status roster.
2. Allow one saved submission per questionnaire per calendar date; a deliberate same-day save updates that submission.
3. Choose the report date range first, then choose among questionnaires eligible in that range.
4. Future custom instruments can never receive automatic clinical interpretation, clinical bands, risk flags, diagnosis, or treatment narrative from Len.

The owner approved all four defaults together on 2026-09-15. Gate A is complete.

Selection of any additional built-in is a separate approval. The Iteration 014 architecture can be completed with PHQ-9 and GAD-7 only.

## Domain and Safety Constraints

- Stable questionnaire and question IDs must not be derived from display text.
- Definition versions are positive integers and historical submissions retain their recorded version.
- Response options store stable values separately from display labels and optional numeric scores; order must not imply score.
- Scoring, profile, interpretation, and behavior capabilities are explicit allowlisted identifiers that fail closed when unknown.
- A custom-origin definition cannot claim the `validated_builtin` interpretation policy.
- PHQ-9 Item 9 context attaches only to stable PHQ-9 question ID `phq9.item9`, never to an ordinal position, prompt, or nonzero answer in another instrument.
- The universal safety message remains owner-controlled copy and is always present immediately before Question 1, once in PDF front matter, in the existing PDF footer treatment, and in workbook metadata/read-me content.
- Built-ins fail closed when exact-version source or redistribution/electronic-administration rights metadata is incomplete.

## Schema and Backward-Compatibility Constraints

- Never drop, rename, repurpose, or destructively rewrite `phq9_entries` or `assessment_entries` in this iteration.
- Add normalized definition snapshots, submissions, responses, and a migration ledger transactionally and idempotently.
- Backfill only after exact PHQ-9/GAD-7 snapshots exist, and verify every legacy row's questionnaire, date, item values, total, severity, source, timestamps, and uniqueness before commit.
- Prefer normalized reads with an explicit compatibility fallback while the legacy stores remain supported.
- PHQ-9/GAD-7 writes update normalized storage and `assessment_entries` atomically; PHQ-9 also continues to update `phq9_entries` in the same transaction.
- Zero is an explicit response and must remain distinguishable from unanswered.
- Selection changes never create, zero-fill, modify, or delete records.
- A failed backfill or reconciliation rolls back and leaves the original database readable.
- Migration validation must include synthetic pre-Iteration-004, Iteration-004-era, and current database shapes plus an idempotent rerun and forced-failure rollback.

## Gate Structure

1. **Gate A - Owner decisions and frozen baseline:** confirm starting behavior, compatibility contracts, risks, test baseline, and the four linked product defaults. No schema or production change.
2. **Gate B - Domain contracts:** add immutable definition/question/option contracts, validators, canonical serialization, and allowlisted scoring/profile/behavior registries behind existing aliases. Reproduce current PHQ-9/GAD-7 behavior exactly. No schema or UI change.
3. **Gate C - Normalized persistence:** add transactional idempotent schema migration, immutable snapshots, verified legacy backfill, compatibility adapters, and atomic dual writes.
4. **Gate D - Dynamic Today UI:** add the approved roster/one-form interaction, explicit unanswered state, preserved unsaved answers, atomic multi-questionnaire save, accessibility, and reduced-window validation.
5. **Gate E - Generic analytics:** move profiles and trends behind explicit definition capabilities while preserving current PHQ-9/GAD-7 output.
6. **Gate F - Report selection and outputs:** make date-range/questionnaire selection, PDF, workbook, and CLI output registry-driven; render and inspect exact fictional outputs.
7. **Gate G - Regression and documentation:** run the full suite, migration restore test, privacy checks, manual Windows walkthrough, and final documentation updates.
8. **Separate release activity:** commit, push, packaging, signing, exact-artifact validation, tag, release, and publication remain separate approval milestones.

No later gate begins after a failed migration, data-integrity, licensing, privacy, or report-fidelity check.

## First Bounded Production Slice

The first production slice was **Gate B1: immutable definition primitives and validation**, with this crisp boundary:

- introduce immutable `ResponseOption`, `QuestionDefinition`, and expanded `QuestionnaireDefinition` contracts;
- add canonical serialization and validation for stable IDs, positive versions, unique option values, finite numeric scores, known strategies/behaviors, required built-in rights metadata, and prohibited custom `validated_builtin` claims;
- encode current PHQ-9 and GAD-7 definitions with explicit `0..3` options while retaining `ASSESSMENTS`, `ASSESSMENT_ORDER`, current public aliases, current scoring results, and PHQ-9 Item 9 behavior;
- add focused unit tests proving exact built-in compatibility and fail-closed invalid definitions;
- make no database, UI, report, package, or dependency change.

This slice came first because the normalized schema must reference an exact validated versioned definition. Migrating data before freezing that contract would risk storing rows that cannot be interpreted consistently later.

Gate B1 completed this boundary without schema, UI, reporting-layout, package, or dependency changes. Canonical deserialization was included with serialization so future definition snapshots can be reconstructed and revalidated rather than treated as trusted JSON.

### Gate B2 strategy routing

Gate B2 completed the remaining Gate B boundary:

- added immutable `ScoringStrategyDescriptor` and `ProfileStrategyDescriptor` contracts with read-only application-owned registries;
- retained the serialized definition fields and IDs `scoring_rule="sum"` and `profile_rule="symptom_presence_14d"`, so the B1 snapshot representation is unchanged;
- routed PHQ-9/GAD-7 daily totals through the application-owned `sum_option_scores_v1` implementation, using each question's explicit option values and scores;
- routed existing rolling and explicit-window 14-day calculations through the application-owned `symptom_presence_thresholds_14d_v1` implementation while preserving count thresholds, missing-day treatment, coverage, total, severity, and output records;
- retained the existing severity functions as built-in compatibility behavior rather than treating them as definition-provided code;
- allowed the safe contract seam for a future custom definition to select deterministic sum scoring while retaining `raw_only` or `descriptive_only` interpretation; no custom-authoring feature or automatic clinical interpretation was added;
- kept reserved but not implemented strategy descriptors fail-closed at execution time, while unknown IDs continue to fail definition validation;
- made no UI, report-layout, schema, migration, persistence-format, dependency, package, release, or GitHub-state change.

### Gate C1 migration ledger and immutable snapshots

Gate C1 established the persistence foundation without opening normalized submissions or backfill:

- added an append-only `schema_migrations` ledger owned by application ID `len`, with stable migration IDs and SHA-256 checksums over the exact ordered statements;
- applies known migrations through one explicit `BEGIN IMMEDIATE` transaction and individual statements, with an explicit commit only after schema, ledger, and snapshot validation succeeds;
- fails closed on checksum drift, unknown newer migration IDs, an already-active transaction, or reuse of a questionnaire/version identity with different canonical bytes;
- added `questionnaire_definition_snapshots`, keyed by `(questionnaire_id, definition_version)`, storing canonical definition JSON and its SHA-256;
- added database triggers that reject updates or deletes to both migration records and definition snapshots;
- reloads snapshots through canonical deserialization, checksum verification, validation, and exact questionnaire/version identity verification;
- stores exact PHQ-9 v1 and GAD-7 v1 snapshots idempotently during database initialization;
- leaves `phq9_entries` and `assessment_entries` intact and retains the existing additive compatibility copy from legacy PHQ-9 rows;
- does not add normalized submissions/responses, new backfill behavior, UI, reports, dependencies, packages, release work, or GitHub changes.

At the C1 checkpoint, the immutable composite snapshot key and approved `(questionnaire_id, entry_date)` uniqueness boundary were ready for the then-deferred C2 normalized tables described next.

### Gate C2 normalized storage and verified backfill

- added `questionnaire_submissions`, uniquely keyed by `(questionnaire_id, entry_date)` and referencing the immutable `(questionnaire_id, definition_version)` snapshot key;
- added `questionnaire_responses`, keyed by stable question identity with a separate response order, canonical JSON option value, and optional numeric score;
- represents an explicit zero as a stored response row containing JSON `0`; unanswered remains structurally distinct as no response row;
- backfills from the existing authoritative `assessment_entries` compatibility table only after the exact snapshot exists;
- verifies questionnaire identity, required/extra item shape, every option value, calculated total, severity, notes, note tag, source, timestamps, response count/order, and any pre-existing normalized row before commit;
- reruns reconciliation idempotently during initialization and fails closed on unknown questionnaires, missing required responses, extra responses, total/severity disagreement, or normalized disagreement;
- proved a forced reconciliation failure rolls back both new tables and the C2 ledger record while leaving the already-complete C1 migration intact.

### Gate C3 normalized-first compatibility reads

- `fetch_assessment_entries` now verifies and prefers normalized submissions/responses against their immutable snapshot;
- exact checksum, snapshot identity, response identity/order/value/score, total, and built-in severity are checked before constructing an application row;
- legacy-only dates are merged as an explicit transition fallback, and a database without normalized tables continues to use the unchanged legacy query;
- current compatibility row IDs remain stable for existing edit/delete callers.

### Gate C4 atomic compatibility writes

- PHQ-9 saves now write `phq9_entries`, `assessment_entries`, normalized submission metadata, and normalized responses in one transaction;
- GAD-7 saves write `assessment_entries` plus normalized storage in one transaction;
- assessment edits, daily-note updates/clears, and assessment deletes synchronize every applicable store in the same transaction;
- normalized metadata reuses the compatibility row's exact created/updated timestamps, notes, note tag, source, total, and severity;
- a forced normalized-response insertion failure proved that updates to every earlier store roll back together.

### Gate D1 one-active-form Today interaction

- replaced simultaneous side-by-side Today forms with a compact roster that independently shows inclusion and completion status while opening exactly one active questionnaire form;
- generates the active form from each immutable questionnaire definition's questions and response options;
- replaced default-zero Today controls with readonly definition-driven choices whose initial state is explicitly `Select a response`;
- preserves zero as a declared answer distinct from unanswered and blocks saving an included questionnaire until every required question has an answer;
- retains each questionnaire's unsaved variables while the active form changes;
- places the universal safety message inside each active form immediately before Question 1;
- added one batch-save API that validates the selected questionnaire IDs and writes every included questionnaire in one SQLite transaction;
- retained existing History editing controls and all report/analytics layouts unchanged.

### Gate E definition-driven analytics

- added explicit capability checks for total-score trends and 14-day item profiles, including neutral omission reasons for definitions that do not declare or implement those capabilities;
- calculates symptom presence from each response option's declared numeric score rather than assuming that the stored response value is a numeric `0..3` value;
- keeps deterministic custom computation separate from clinical interpretation: a `raw_only` definition may use an explicitly selected deterministic strategy, but Len produces no severity label for it;
- carries each normalized submission's immutable definition version into the analytics adapter and resolves historical definitions from stored snapshots when the version differs from the active registry definition;
- splits trend and profile data by definition version instead of silently combining unlike revisions; comparison summaries use only the latest applicable version and label it when multiple versions are present;
- adds definition version to the in-memory 14-day profile records while retaining the existing workbook columns until Gate F output changes are opened;
- builds Review trend-chart widgets by iterating the questionnaire registry and uses each definition's declared score maximum; existing PHQ-9/GAD-7 chart attributes remain as compatibility aliases;
- limits symptom-frequency summary prose to definitions with the approved built-in interpretation policy and a supported profile capability;
- preserves PHQ-9/GAD-7 totals, severity labels, 14-day thresholds, missing-day treatment, graph titles/colors, treatment-cycle behavior, and current report output structure.

### Gate F report selection and outputs

- validates the report date range before questionnaire selection and offers only registry questionnaires with records in that range;
- keeps the legacy one-click full-history report entry point compatible while the interactive flow follows the approved date-range-first sequence;
- builds PDF definition, overview, trend, and profile sections from registry definitions and exact stored definition-version groups rather than hardcoded PHQ-9/GAD-7 output branches;
- keeps version-incompatible trend/profile records separate and limits PHQ-9 Item 9 context to definition snapshots that declare the `phq9.item9` behavior;
- retains PHQ-9 treatment-cycle reporting without blending incompatible definition versions;
- appends exact definition version, stable question identity, response label/score, interpretation policy, safety, and non-diagnostic metadata to the analysis workbook while preserving the existing column order before appended fields;
- adds paired CLI `--report-start` and `--report-end` options and reports the selected registry questionnaire/version labels;
- adds focused selection, version, safety-copy, privacy-path, workbook, PDF, and CLI contract tests.

## Test Strategy

### Gate A baseline

- Focused Iteration 010 and multi-assessment regression tests.
- Full unit-test suite once after the focused baseline succeeds.
- Git whitespace validation after documentation changes.

### Gate B

- Exact PHQ-9/GAD-7 item order, option values, totals, labels, maximum scores, source/rights metadata, profile rules, and behavior IDs.
- Invalid IDs, versions, duplicate question/option IDs, non-finite scores, missing built-in rights metadata, unknown strategies/behaviors, and custom clinical-interpretation claims fail closed.
- Non-`0..3` and nonscored options serialize and round-trip without entering production storage.
- Existing Iteration 004/006/007.2/008/010 tests remain green.

### Later gates

- Synthetic legacy migration/reconciliation/idempotence/rollback and atomic compatibility writes.
- Independent PHQ-9-only, GAD-7-only, both, and neither selection/save paths; zero-versus-unanswered; edit/delete isolation.
- Registry-driven analytics and every report selection permutation.
- PDF text extraction plus page rendering; workbook schema/content inspection; private-data and unexpected-identifier checks.
- Keyboard-only and reduced-window GUI walkthrough with fictional data.

## Validation at This Checkpoint

- Confirmed branch starts at `ecfe156324b751c49a36b2a7037d0e1f289a2e24`.
- Confirmed the canonical starting tree had only the two expected untracked planning documents; the code-signing plan was not copied into this development branch.
- Focused tests: 9 passed (`test_iteration_010_questionnaires` and `test_multi_assessment`).
- Full suite: 68 passed.
- One non-failing `ResourceWarning` reported an unclosed SQLite connection during the full run; this is recorded for observation and is not expanded into unrelated cleanup in Gate A.
- No production data, database, generated report, export, package, tag, release, or public GitHub state was used or changed.

### Gate B1 validation

- Python compilation passed for the application module and new contract tests.
- Focused Gate B1 plus Iteration 010/multi-assessment compatibility tests: 17 passed.
- Full suite after implementation: 76 passed.
- Git whitespace validation passed. Git emitted only a line-ending normalization notice for `app.py`; no whitespace error was reported.
- The pre-existing non-failing SQLite `ResourceWarning` appeared again during the full suite and remains outside this slice.
- The authoritative PHQ Screeners page confirms PHQ/GAD-7 availability and states that no permission is required to reproduce, display, or distribute them; its URL is recorded as both the source and rights-evidence URL for the two existing built-ins.
- No database schema, stored record, user data, UI behavior, report layout, dependency, package, tag, release, commit, push, or public GitHub state changed.

### Gate B2 validation

- Focused Gate B contract and 14-day scoring tests: 22 passed.
- Relevant multi-assessment, Iteration 010 questionnaire, and Iteration 008.2 clinician-output regression tests: 18 passed in the validated project environment.
- Python compilation passed for `src` and `tests`.
- Full suite after B2: 81 passed.
- The first relevant-subsystem run under the default system Python stopped on missing report/Pillow packages and unusable Tcl; rerunning the same set under the existing validated project environment passed all 18 tests. No dependency was installed or changed.
- The pre-existing non-failing SQLite `ResourceWarning` appeared again and remains outside this bounded slice.
- No database schema, stored record representation, user data, visible UI behavior, report layout, dependency, package, tag, release, commit, push, synchronization, or public GitHub state changed.

### Gate C1 validation

- Focused Gate B/C1 contract and persistence tests: 19 passed.
- Forced-failure validation proved that a table created earlier in a failing migration and the newly created ledger both roll back.
- Idempotence validation ran initialization twice and retained one migration record plus exactly one PHQ-9 v1 and one GAD-7 v1 snapshot.
- Immutability validation proved that SQLite rejects snapshot updates/deletes and migration-record deletes.
- Drift validation proved that changed migration bytes, unknown newer migrations, and changed canonical definition bytes under an existing version fail closed.
- A synthetic older PHQ-9-only database lacking `note_tag` retained its exact row values and remained readable through both legacy and compatibility tables after initialization.
- No production database or user data was opened or modified.

### Gate C2-C4 validation

- Progressive affected persistence, questionnaire-contract, multi-assessment, entry-management, and Iteration 010 regression set: 40 passed.
- C2 idempotence preserved one normalized submission and exact response set across repeated initialization.
- C2 stored explicit zero as JSON `0`, retained nullable legacy padding only outside the response set, and preserved exact metadata/timestamps.
- C2 uniqueness and foreign-key tests rejected duplicate same-questionnaire/date submissions and submissions without a matching definition snapshot.
- C2 forced mismatch validation rolled back both normalized tables and its migration record.
- C3 proved normalized rows are preferred while legacy-only and wholly unmigrated databases remain readable.
- C4 verified PHQ-9 save parity across all three stores and injected a normalized-response failure that left all stores unchanged.
- The existing non-failing SQLite `ResourceWarning` remains visible in affected regressions and remains outside this iteration slice.

### Gate C full checkpoint and Gate D1 validation

- Gate C full suite: 94 passed; compilation and Git whitespace validation passed.
- Gate D1 focused questionnaire, persistence, entry-management, Iteration 010, UX, and accessibility regressions: 55 passed.
- Gate D1 full suite: 97 passed; compilation and Git whitespace validation passed.
- Response-choice tests prove unanswered is `None` while the declared zero option round-trips as numeric `0`.
- Batch-save tests prove PHQ-9 and GAD-7 produce 2 submissions and 16 responses in one transaction.
- A forced failure on the second questionnaire proved the first questionnaire's legacy and normalized writes also roll back.
- Automated Windows/Tk geometry validation was attempted once in the validated project environment and stopped before application construction because the local Python runtime cannot find a usable `init.tcl`.
- Consequently, one-visible-form mapping, active-form switching, safety-message placement, scroll reachability at `1180x780` and `980x680`, and keyboard-only interaction are implemented and code-tested but **not live-GUI validated** at this checkpoint.
- No alternative-runtime cycling, Tcl installation, dependency change, packaging, or policy workaround was attempted.

### Gate D live Windows GUI validation

- Dan completed the required local Windows live-GUI walkthrough against the acceptance criteria already recorded in this checkpoint and reported **PASS**.
- Gate D is therefore formally closed. No additional GUI observations are claimed beyond that authoritative PASS result.
- The user validation made no code, documentation, Git, or GitHub changes.

### Gate E validation

- Focused Gate E contract and persistence tests: 32 passed.
- Relevant analytics, persistence, Review/UX, questionnaire-selection, and clinician-output regressions: 78 passed.
- Full suite after Gate E: 101 passed.
- Application and test compilation passed; Git whitespace validation passed.
- Tests prove string-valued response options use their declared numeric scores, `raw_only` custom profiles receive no severity label, unsupported capabilities return neutral omission reasons, normalized reads retain definition version, and unlike definition versions are split for trends and not compared across profile windows.
- Existing PHQ-9/GAD-7 profile, period-comparison, selected-questionnaire, PDF, and workbook regressions remain exact-test clean.
- The existing non-failing SQLite `ResourceWarning` appeared during validation and remains outside this iteration slice.

### Gate F automated validation checkpoint

- Focused Gate F/report compatibility: **19 passed**.
- Relevant reporting, analytics, persistence, questionnaire-contract, and compatibility subsystem: **88 passed**.
- The first subsystem run exposed two report-layer regressions (empty default-selection profile handling and shifted legacy workbook columns); both were corrected, their exact tests passed, and the 88-test subsystem rerun passed.
- The existing non-failing SQLite `ResourceWarning` remains unchanged and out of scope.
- Exact fictional artifacts were generated with PHQ-9 v1 plus GAD-7 v1/v2 data. PDF text extraction confirmed definition versions, non-diagnostic wording, universal safety copy, and fictional context; the final PDF SHA-256 was `673E4BFB052C66C91A234C84A22797BFCFE3694FCBF4290C98E9C10BE064F72F`.
- All seven PDF pages were rendered and inspected. A one-line spill page and orphaned chart heading found on the first render were corrected with bounded flow grouping; the second render had no clipping, overlap, orphaned chart heading, broken table, or unreadable footer.
- All eight workbook sheets loaded successfully. Changed sheets (`Daily Assessments`, `Item Responses`, `Metadata`, and `14-Day Item Profile`) were structurally inspected and rendered; no formula-error token was present; the final workbook SHA-256 was `D25619F82261A3CFBBEA7622E72B96646B9DA1A395F77F02A66D3A2A277046A1`.
- PDF and workbook privacy scans found only fictional validation content and no database path, Windows user/path, Dan/Scannell identifier, email marker, SSN, or DOB string.
- Final full suite: **105 passed**. Application/tests compilation passed. Git whitespace validation passed; Git emitted only its line-ending notice. The existing non-failing SQLite `ResourceWarning` remained unchanged.

### Gate G automated closeout checkpoint

- Added and passed the planned closed-database backup/restore regression: **1 passed**. The test restores a synthetic pre-Iteration-014 database after an initial migration, reruns initialization, and verifies exact legacy, compatibility, normalized, response-count, timestamp, and migration-ledger state.
- Full Iteration 014 persistence module: **16 passed**.
- Focused Gate F report/privacy contracts: **4 passed**.
- Final full suite after documentation and restore-test changes: **106 passed**.
- Application and test compilation passed. Git whitespace validation passed; Git emitted only its line-ending notices.
- Final working-tree privacy inventory found no staged files and no new generated Gate G artifact. The only database/PDF/XLSX files present are the already-ignored fictional Gate F validation database and exact artifacts whose content/privacy checks are recorded above.
- The existing non-failing SQLite `ResourceWarning` appeared during the focused report run and full suite and remains unchanged and out of scope.
- The known Work Tk runtime limitation was not retried or repaired. The final keyboard-only/reduced-window source walkthrough was instead completed through the owner-run Windows acceptance gate recorded below.

### Gate G live Windows validation

- Dan completed the required isolated source walkthrough with fictional data and reported **PASS** against the Gate G keyboard-only/reduced-window checklist.
- The PASS covers the reduced supported window, questionnaire roster and active-form usability, universal safety-message placement, keyboard questionnaire selection/switching, preservation of unsaved answers across forms, explicit-zero handling, unanswered-required-item blocking, independent completion status after saving both questionnaires, and persistence after close/reopen.
- This authoritative owner result closes the final Gate G acceptance criterion. No additional GUI observations are claimed.

## Files Changed Through Gate B2

- Added `docs/Iterations/Iteration_014_Extensible_Questionnaire_Framework.md`.
- Modified `src/phq9_tracker/app.py` with the Gate B1 immutable definition contracts and Gate B2 application-owned strategy descriptors/resolvers, deterministic total calculation, and descriptor-routed 14-day profile calculation. Existing aliases and persistence APIs remain in place.
- Added `tests/test_iteration_014_questionnaire_contracts.py` with Gate B1 validation coverage plus Gate B2 exact PHQ-9/GAD-7 total/profile compatibility, missing/unknown-response boundaries, deterministic custom-scoring separation from interpretation, and unsupported-strategy fail-closed coverage.

## Files Changed in Gate C1

- Modified `src/phq9_tracker/app.py` with the checksummed transactional migration runner, append-only ledger, immutable snapshot schema/storage, and verified snapshot loader.
- Added `tests/test_iteration_014_persistence.py` with C1 idempotence, immutability, rollback, drift, exact-snapshot, and legacy-database compatibility coverage.
- Updated this checkpoint document with the implemented schema boundaries and validation evidence.

## Files Changed Through Gate C

- Modified `src/phq9_tracker/app.py` with the C1 migration/snapshot foundation, C2 normalized schema and verified backfill, C3 normalized-first read adapter, and C4 atomic compatibility writes.
- Added and expanded `tests/test_iteration_014_persistence.py` through C1-C4 rollback, compatibility, integrity, fallback, and atomicity coverage.
- Updated this checkpoint document after each clean persistence slice.

## Files Changed in Gate D1

- Modified `src/phq9_tracker/app.py` with definition-driven response-choice helpers, the status roster/one-active-form Today layout, explicit unanswered validation, state-preserving form switching, and atomic batch saves.
- Expanded `tests/test_iteration_014_questionnaire_contracts.py` with explicit unanswered-versus-zero coverage.
- Expanded `tests/test_iteration_014_persistence.py` with successful and forced-failure multi-questionnaire transaction coverage.
- Updated this checkpoint document with automated validation and the exact GUI-runtime limitation.

## Files Changed in Gate E

- Modified `src/phq9_tracker/app.py` with capability-gated, definition-version-aware profile/trend helpers, option-score-based profile computation, version-separated trend/profile data, and registry-driven Review chart construction.
- Expanded `tests/test_iteration_014_questionnaire_contracts.py` with deterministic custom-profile, no-clinical-interpretation, omission-reason, and definition-version boundary coverage.
- Expanded `tests/test_iteration_014_persistence.py` to verify normalized analytics rows and derived profiles retain their stored definition version while legacy-only fallback rows remain explicitly unversioned.
- Updated this checkpoint with the Gate D live-GUI PASS and Gate E implementation/validation evidence.

## Files Changed in Gate F

- Modified `src/phq9_tracker/app.py` with date-range-first report eligibility, registry/definition-version-driven PDF sections, appended workbook version/identity/safety metadata, and explicit CLI report ranges.
- Added `tests/test_iteration_014_reports.py` with Gate F selection, definition-version, safety-copy, privacy-path, workbook, PDF, and CLI contract coverage.
- Updated this checkpoint with Gate F decisions, compatibility corrections, validation evidence, and the exact next action.

## Files Changed in Gate G

- Expanded `tests/test_iteration_014_persistence.py` with the planned closed-database backup/restore and repeat-migration regression.
- Updated `README.md` with the delivered Today/report behavior and whole-database migration/restore guidance.
- Updated `ROADMAP.md` with the Iteration 014 delivered architecture, Windows closeout status, built-in redistribution gate, and future custom deterministic-scoring/no-clinical-interpretation boundary.
- Updated `BUILD_AND_RELEASE.md` with the Iteration 014 migration/backfill/compatibility design, backup/restore distinction, and final integrated validation criteria.
- Updated `docs/PRIVACY_AND_DATA_HANDLING.md` with normalized/snapshot sensitivity, whole-database backup guidance, local-only definition handling, built-in rights limits, and custom-instrument interpretation boundaries.
- Updated `docs/PROJECT_STRUCTURE.md` with the one-file database architecture and location of source-owned definitions/migrations versus private runtime records.
- Updated this checkpoint with exact automated results and the remaining manual acceptance gate.
- No Gate G application-code change was required.

## Planning Corrections and Clarifications

- Iteration 014 extends the completed Iteration 010 foundation; it does not introduce questionnaire selection from scratch.
- The kickoff's phrase “multiple questionnaires per day” is satisfied by independent questionnaires on one date and does not itself authorize repeated same-questionnaire administrations within that date.
- “Dynamic/dropdown questionnaire UI” identifies the need for scalable selection but does not by itself settle the planning document's recommended status-roster/one-active-form interaction.
- Report questionnaire selection is already partially present; Iteration 014 must make eligibility, definition versions, record counts, and output paths fully registry-driven rather than recreate the chooser.
- No new built-in is required for the architecture and none is approved by this checkpoint.

## Remaining Work and Exact Next Action

Gate G and Iteration 014 are complete. All planned automated and manual acceptance criteria passed, and the completed iteration is merged on protected `main` at `47a8655489dda4dfbf0e330f4139777156e034a7`.

The separately authorized `v0.5.0-alpha.1` release-preparation phase is in progress. Release-facing documentation is being reconciled before a clean candidate build from the resulting merged `main`. The candidate filename is planned as `Len-Portable-0.5.0-alpha.1.zip`; its build-source commit, size, inventory, SHA-256, signature status, Defender results, and exact-candidate execution/output evidence remain pending. No tag, GitHub release, asset upload, or publication has occurred, and publication requires a later explicit owner approval.

## Pre-release Daily-Severity Regression Correction

The v0.5.0-alpha.1 pre-release review found that Iteration 014's shared v1 response metadata used conventional multi-day frequency labels for values that Len records and totals as single-day severity. The numeric storage, daily totals, derived 14-day frequency calculation, and PHQ-9 Item 9 safety behavior remained correct.

The owner-approved correction preserves exact immutable PHQ-9/GAD-7 v1 snapshots, adds active v2 definitions with `Not present / Mild / Moderate / High`, and places the instruction “For today, rate how severe each symptom was from 0 (not present) to 3 (high).” above each active form. Previously unnormalized compatibility rows backfill against v1; new saves use v2; existing normalized rows reconcile against their stored version. Analytics remain split across definition versions. For known-regressed built-in v1 responses, the Analysis Workbook emits the numeric daily-severity value as `response_label` rather than reproducing the v1 frequency wording as user-facing interpretation. No schema or stored-snapshot mutation is performed.

Correction validation on the regression branch: 39 focused definition/persistence/report tests passed; 104 affected-subsystem tests passed; the full suite passed 109 tests. Application/tests compilation, Git whitespace validation, and the controlled Python 3.12.10 release-license verifier passed (34 notice files and 11 pinned package versions). The existing non-failing SQLite `ResourceWarning` remained unchanged and out of scope.
