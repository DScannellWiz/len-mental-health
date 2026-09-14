Current as of: 2026-09-13
Last substantive update: 2026-09-13

# Development Journal

This journal records the human context behind significant product and engineering choices. Formal narrative capture begins around Iteration 007; the earlier entries below are a concise reconstruction from surviving documentation rather than contemporaneous notes.

## September 10, 2026: Product Renamed to Len

After Iteration 009, the current product and repository identity changed from **Mental Health Tracker** to **Len**, with the canonical repository at [DScannellWiz/len-mental-health](https://github.com/DScannellWiz/len-mental-health). The rename updates current-facing application, report, workbook, launcher, installer, and project-documentation language.

The change deliberately preserves technical compatibility identifiers that existing installations, data paths, scripts, and imports may rely on: `phq9_tracker`, `PHQ9Tracker.exe`, `PHQ9_TRACKER_*`, `%LOCALAPPDATA%\PHQ9Tracker`, `phq9_tracker.sqlite`, and the existing icon filename. Historical iteration, alpha, release, and validation records also retain the names that were accurate when those records were created. In particular, the `v0.3.0-alpha.1` tag and exact artifacts were neither rebuilt nor relabeled.

## Reconstructed Prehistory

### Spreadsheet era

The project began as a spreadsheet created to preserve symptom information across the time between appointments. It established the core practice of recording PHQ-9 responses and looking across a 14-day period rather than relying entirely on memory at the next conversation with a clinician.

### First PHQ-9 application

The spreadsheet evolved into a local PHQ-9 Tracker. The application introduced a more deliberate daily-entry workflow, local SQLite storage, reports, and exports while keeping sensitive information under the user's control. Early scoring work corrected the 14-day calculation so the application followed the symptom-frequency approach established in the spreadsheet prototype.

### Reusable assessments and GAD-7

Iteration 004 changed the project from a single-purpose PHQ-9 tool into a reusable multi-assessment framework. PHQ-9 compatibility was preserved while a generic assessment model and GAD-7 were added. The visible identity shifted to **Mental Health Tracker**, reflecting a broader foundation without discarding established data contracts.

### Data integrity and history management

As daily use exposed the risks of duplicate or hard-to-correct records, Iteration 006 added History / Manage Entries, stable-ID editing, confirmed deletion, and idempotent daily resubmission. It also distinguished **Daily Severity Score** from **14-Day Symptom Frequency Score** and retained explicit support for multiple legitimate treatment events on one date.

### Shift toward conversation-focused reporting

Iteration 005 introduced adjacent 14-day comparisons with neutral language and coverage disclosure. Iteration 007 carried that direction further: detailed records remained available in exports, while the primary clinician report became a compact aid for discussion rather than a long collection of repeated raw tables.

## Iteration 007: Present-Focused Check-In and Meaningful Review

### Context

The application had accumulated useful dashboard, reporting, treatment, and history features, but those capabilities competed with the most immediate task: recording the current day. Showing historical scores while a user was answering today's questions could influence the entry and increase cognitive burden. At the same time, trend and treatment context remained valuable when the user intentionally wanted to review it or prepare for a clinical conversation.

### Decisions

- Make **Today's Check-In** the primary opening experience.
- Keep prior scores, charts, comparisons, and interpretations out of the present-focused check-in.
- Save PHQ-9 and GAD-7 first, then gently offer optional treatment, appointment, or note details.
- Provide **Previous Day** and **Next Day** navigation for short-distance catch-up, with automatic calendar rollover, existing-entry loading, unsaved-change protection, and future-date prevention.
- Place historical interpretation in a separate **Review** experience.
- Divide Review into understandable time horizons: recent trends, simplified current and previous treatment cycles, and long-term trends.
- Use deterministic, neutral language that describes recorded patterns and coverage without diagnosing or claiming that treatment caused a change.
- Replace the long, detail-heavy clinician PDF with a compact, nonjudgmental conversation aid. Keep detailed raw records available through exports.

### Why these choices were made

The Today experience is intentionally present-focused because each symptom response should be considered on its own rather than copied, autofilled, or anchored by prior results. Saving the core assessments before optional detail protects the shortest useful path while still helping users remember relevant context.

Date navigation supports recovery from a recently missed entry without turning the tracker into a second calendar. Its safeguards prevent accidental loss of unsaved work and prevent future-dated check-ins.

Review is separate because reflection is a different activity from recording. Recent trends answer what has been happening lately; the current and previous treatment-cycle views provide limited timeline context around recorded events; long-term charts retain the broader view. Treatment-cycle language remains observational because the recorded sequence alone cannot establish causation.

The clinician report was shortened so it could support a focused conversation. It emphasizes overall patterns, symptom highlights, timeline context, treatment-cycle observations, coverage, and neutral prompts. The app supplies memory and structure; the user supplies lived meaning; the clinician supplies professional interpretation.

### Consequences and lessons

- The interface now distinguishes recording, reviewing, and managing information more clearly.
- The same underlying records continue to support both concise reports and detailed exports.
- Neutral wording and coverage disclosure are product requirements, not cosmetic editing choices.
- Missed days require both honest data handling and a guilt-free recovery path.
- A local-first application can still support rich clinical conversations without automatic sharing or automated clinical judgment.

## August 1, 2026: Reporting and Export Design Workshop

### Context

Review of the clinician report exposed a mismatch between narrative information and a compact table layout: longer journal entries could be shortened even though the user's words may carry context that symptom scores cannot. The discussion also clarified that a clinician report and an analysis workbook serve different purposes.

### Planned refinements

- Optimize the clinician report for reading and the analysis-ready workbook for independent analysis.
- Treat user-authored journal text as primary-source information. Clinician reports should preserve it in full rather than abbreviating or summarizing it.
- Present application observations alongside the user's recorded context without implying that an event caused a symptom or score change.
- Plan a separate, normalized Excel workbook while keeping the clinician report human-readable.

### Open design questions

Report section names, sequence, and narrative flow remain intentionally open. They will be workshopped and tested before implementation rather than being fixed by this planning entry.

## August 7, 2026: Iteration 007.1 Navigation and Review Polish

### Context

Daily use exposed a small group of observable interface issues after Iteration 007: Review titles could collide with legends or draw beyond a canvas after resizing, Today's Check-In opened first but was not the first visible primary tab, and History required manual date entry even though Today already had guarded day navigation. An entirely empty History date also looked too much like an editable new record.

### Decisions

- Keep the scope to navigation, empty-state, and Review-layout polish; do not begin reporting or export work.
- Make the visible primary-tab order match the intended workflow: record today, review intentionally, then manage historical records.
- Reuse the existing calendar-day shift logic in History while keeping a separate History edit snapshot and confirmation message.
- Treat History as a manager of existing records. When a date is entirely empty, explain that calmly and disable record-changing controls rather than implying a load error or offering an accidental creation path.
- Redraw Review charts from their live canvas dimensions and derive legend/plot positions from the rendered title bounds, so resizing preserves the full title and separates it from chart content.

### Validation and status

All 37 automated tests pass in the dependency-complete project virtual environment. The nine focused Iteration 007.1 tests cover tab order, History navigation and rollover, existing and empty dates, future-date blocking, unsaved-change cancellation, and the responsive chart-layout rules. Python compilation also passes.

The project owner subsequently completed the manual source-GUI walkthrough against the canonical repository with real-world data. Tab order and startup selection, Review chart titles and resize behavior, History navigation and rollover, existing and empty dates, future-date blocking, and unsaved-change protection passed. Iteration 007.1 is complete. No scoring, schema, export, report, or privacy-boundary changes were made, and Iteration 007.2 was not started.

## August 8, 2026: Iteration 007.1 Review with Synthetic Data

### Context

Reviewing Iteration 007.1 with synthetic data showed that the application now feels more coherent and intentionally layered: record today, review recent patterns, and prepare for a clinician discussion. The revised hierarchy and Review experience made the product's purpose easier to understand without changing its local-first or non-diagnostic role.

### Design observations

- The XLSX export should support independent analysis through separate logical worksheets rather than combining unlike records into a presentation-oriented sheet. The normalized workbook planned for Iteration 007.2 should preserve one logical record per row and stable relationships between datasets.
- The current short scoring explanation is accurate, but it is not sufficient as the only explanation. A fuller **How to Read This Report** section should explain **Daily Severity Score**, **14-Day Symptom Frequency Score**, and the effect of entry coverage and missing check-ins; a concise version may remain as a reminder.
- Exact graph values should be directly discoverable through a tooltip or click callout that shows the date and score. Requiring a user to visually trace a point across a wide chart can make important numerical information difficult to read.
- Possible automatic date loading, cleaner status and confirmation wording, more consistent button spacing, useful keyboard shortcuts, and typography and readability refinements belong together as micro-UX work.

### Deliberate deferral

These refinements were deliberately assigned to Iteration 007.2 and Iteration 008 rather than being rushed into the focused Iteration 007.1 polish scope. This keeps the current iteration observable and contained while preserving the newly agreed reporting, analysis, and accessibility needs for deliberate design and validation.

## August 15, 2026: Iteration 007.2 Reporting, Analysis, and Portable Validation

### Context

The clinician report and spreadsheet export had diverging purposes. The report needed to support a focused conversation without discarding the user's own narrative, while independent analysis needed normalized, machine-friendly records rather than a wide presentation sheet. An immediate Florida use case also required proof that portable mode could start from a blank local database without carrying historical PHI.

### Decisions

- Keep the existing combined CSV/XLSX export unchanged and add a separate normalized analysis workbook.
- Treat database-backed assessment and event IDs as stable within an application database, and use deterministic day and item identifiers for export-only relationships. Avoid a schema migration in this iteration.
- Keep **Daily Summary** explicitly derived. The normalized event rows remain authoritative so two legitimate same-day events are never collapsed into one source record.
- Put **How to Read This Report** first, followed by **Recorded Period Overview**, **Recorded Symptom Trends**, **Treatment Context**, **Journal and Event Context**, and **Conversation Starters**.
- Include every selected-period journal entry in full. Compactness is a normal-case design goal, not permission to truncate primary-source narrative.
- Validate the Florida path with a blank portable database and synthetic records only. Do not use or package the production database.
- Defer Travel Mode ingestion and LAN sharing. A future travel workflow should append validated travel-created records into an authoritative home database and verify a secure clear. Future LAN clients should use an authoritative host/service rather than opening SQLite over a network share.

### Validation and consequences

All 40 automated tests passed with isolated synthetic databases. The normalized workbook passed structural and relationship checks, including two legitimate same-day therapy events. A four-page synthetic clinician report was extracted, rendered, and visually inspected; long notes, special characters, section transitions, tables, charts, footers, and page numbers remained readable.

Portable path selection, synthetic persistence, and pristine reinitialization passed at the source level. The actual Windows ZIP could not be built because PyInstaller was unavailable and an attempted workspace-only download stalled; Inno Setup was also unavailable. Icon references were verified in source and packaging configuration, but packaged icon behavior remains deferred rather than expanding this iteration.

The final source-GUI smoke attempt could not create a window because the available Python runtime lacked a usable Tcl/Tk `init.tcl`. Automated validation remains green, but interactive GUI behavior is not claimed from this environment.

Later the same day, the owner completed the real Windows portable validation on a suitable workstation. PyInstaller 6.22.1 built the folder-based application, portable folder, and `PHQ9Tracker-Portable-0.2.0.zip`. Inspection before first launch confirmed that neither the folder nor the ZIP contained `.sqlite`, `.db`, or `.sqlite3` files. First launch created `phq9_tracker.sqlite` inside the portable folder; Review, History / Manage Entries, Treatment Events, Clinician Report, and How Scoring Works opened cleanly with no prior data.

Synthetic entries persisted across a full close and reopen. The packaged clinician PDF passed manual review. The packaged Analysis Workbook contained the seven expected worksheets and passed structural/data-integrity inspection, including relationship reconciliation, complete narrative/event text, no merged cells, and consistent calculations. Deleting the portable database and relaunching recreated a pristine blank state. This validates the portable ZIP for the immediate Florida use case without placing the generated database or synthetic artifacts in the distribution ZIP.

The runtime window/taskbar icon still displayed the generic Tk feather even though PyInstaller embedded the intended icon. That discrepancy remains a deferred cosmetic packaging issue rather than a release blocker. Inno Setup remains unavailable, so installer validation is still pending.

No scoring formulas, database schema, production records, or privacy boundaries changed.

## August 22, 2026: Iteration 008 Review and Clinician Report Workflow

### Context

The application exposed overlapping output paths: a clinician PDF with an automatically generated companion CSV, a legacy combined CSV/XLSX exporter, and the normalized Analysis Workbook introduced in Iteration 007.2. The legacy files were presentation-oriented and did not provide the separate logical datasets needed for flexible external analysis. The dedicated Clinician Report tab also required a manual date range even though the desired workflow was a one-click full-history conversation aid from Review.

### Decisions

- Keep two clear outputs: a clinician PDF for conversation and the normalized XLSX Analysis Workbook for independent analysis.
- Make Review the single access point for **Refresh**, **Import Spreadsheet**, **Generate PDF**, and **Analysis Workbook**.
- Remove the Clinician Report tab and calculate the earliest/latest assessment dates when PDF generation is requested.
- Retire the legacy combined CSV/XLSX export and the clinician-report companion CSV rather than leaving dormant production paths.
- Preserve all existing database records, scoring behavior, full journal text, report structure, and the local-only privacy boundary.
- Keep chart value callouts and the broader micro-UX/accessibility work in Iteration 008.1 so this iteration remains focused.

### Validation and consequences

All 41 automated tests pass with isolated synthetic databases, and source compilation passes. Focused coverage confirms the four Review actions, absence of the Clinician Report tab, fresh full-history bounds, PDF-only report output, and removal of the legacy export function. The normalized workbook tests continue to validate all seven worksheets, stable relationships, complete narrative/event text, and multiple legitimate same-day events. A four-page fictional full-history PDF passed text extraction and page-by-page rendered inspection with the correct range, complete long-form notes, and no companion CSV.

No migration is required, and previously generated CSV/XLSX files are not deleted. Interactive source-GUI and packaged-release validation remain separate gates.

## August 28, 2026: Iteration 008.1 Chart Accessibility and Micro-UX

### Context

The Review charts showed trends but required visually tracing small points across a wide canvas to estimate a value. Date fields also retained a separate Load Date step even when changing dates could be handled safely, while several statuses and confirmations did not make the loaded-date boundary or consequence of a choice explicit. The full-history PDF treated every above-zero PHQ-9 item 9 response the same regardless of age, which could make older recorded information sound current.

### Decisions

- Treat exact chart values as accessibility information. Hover and click callouts show date, series, and score; keyboard-focused charts expose the same points through Left/Right, Enter, and Escape.
- Auto-load a valid changed date only when no unsaved edit could be lost. If edits exist, preserve the current loaded state and require an explicit Load Date decision. Prevent saving when the typed date differs from the check-in actually loaded on screen.
- Keep keyboard additions limited to established, low-ambiguity actions: Enter in date fields, F5 refresh, and navigation within a focused chart.
- Improve readability with consistent existing-font defaults, padding, tab spacing, and table row height rather than adding a theme or UI dependency.
- Anchor item 9 recency to the 14 calendar days ending on the report end date. Recent above-zero responses can lead the discussion prompt; older-only responses remain dated historical context and explicitly do not establish current risk; no item 9 prompt appears when no above-zero response was recorded. Every item 9 context statement discloses recent check-in coverage and missing-information limits.
- Preserve the scoring formulas, database schema and contents, local-only data boundary, complete journal text, and established PDF/XLSX output purposes.

### Validation and consequences

Nine focused tests were added for chart callout text and hit targets, recent/older/absent item 9 cases, guarded date auto-loading, and extracted historical-item-9 PDF wording. The dependency-complete environment passed all 50 automated tests, including PDF generation and the normalized workbook path, and Python compilation passed. Only isolated fictional database paths and temporary generated artifacts were used.

Interactive source-GUI review remains necessary for callout placement at chart edges and extremes, keyboard focus visibility, spacing at the minimum supported window size, safe date focus transitions, and final wording. Packaged portable/installer validation remains a separate release gate. Scalable or user-configurable text sizing is deliberately deferred because it requires broader layout validation.

## August 28, 2026: Clinician Output Information-Fidelity Issues Identified

### Context

Review of current clinician-facing outputs confirmed two presentation problems while also confirming that the underlying records and scoring remain sound. First, the daily PHQ-9 and GAD-7 item responses and established 14-day scoring logic are still available, but the current clinician report and Analysis Workbook no longer present the resulting per-item 0-3 14-Day Symptom Frequency Scores. Second, two legitimate 2026-08-11 treatment events stored and shown in the UI as **Therapy** and **Physical Therapy** share the same description, but the clinician PDF labels both as **Therapy**.

### Decisions

- Classify the missing per-item scores as an information-presentation regression, not data loss or a scoring-formula defect.
- Plan a compact current 14-day symptom profile that shows each PHQ-9 and GAD-7 item, symptom-present days and coverage as appropriate, and its resulting 0-3 frequency score.
- Preserve the conversation-focused report design and normalized workbook model rather than restoring redundant raw-response tables.
- Classify the treatment-event issue as a clinician-PDF presentation/mapping defect. Preserve the stored event type closely enough to distinguish Physical Therapy from counseling Therapy.
- Keep both valid 2026-08-11 records unchanged and add regression coverage for distinct same-day event types with the same description.
- Group these closely related clinician-output fidelity corrections into planned Iteration 008.2. No application code changes are part of this documentation update.

## August 30, 2026: Iteration 008.1 Source-GUI Validation and Iteration 008.2 Implementation

### 008.1 walkthrough outcome

Daniel completed the interactive source-GUI walkthrough after several days of ordinary use. Chart dates and scores appeared correctly correlated; keyboard chart navigation worked; date changes worked; the unsaved-change warning worked; the overall look and feel was acceptable; and no general-use issues were noticed. This closes Iteration 008.1's source-GUI gate, but it does not establish packaged validation.

Daniel recorded one non-blocking cosmetic observation: the up/down arrows within each PHQ-9 and GAD-7 Spinbox had an awkward internal gap. He preferred each arrow pair to read as one compact control, with spacing between questionnaire items instead.

### 008.2 implementation decisions

- Restore one compact current 14-day item profile in the PDF and add one normalized **14-Day Item Profile** workbook sheet. One record per assessment item is cleaner than repeating current-window derived values across daily item-response rows.
- Reuse the existing explicit 14-calendar-day scoring function. Do not change formulas, schema, stored responses, migrations, or missing-day guidance.
- Match Physical Therapy before the broader Therapy display category. Preserve stored event types and never infer type from a shared description.
- Use `reports` as the one generated-output folder for both canonical outputs. Source runs use the repository `reports` folder; portable runs use a `reports` folder beside the executable.
- Generate collision-safe filenames automatically, offer to open each successfully saved file, and add **Open Reports Folder** as the approved fifth Review action. An external-open failure must not undo or obscure generation success.
- Defer user-defined output destinations. Persistent paths, permissions, removable drives, and settings behavior would add a separate configuration and release-validation problem immediately before Alpha.
- Reduce Spinbox internal padding and retain inter-item spacing. Do not replace widgets or redesign the questionnaire.

### Validation and consequences

Focused tests cover PHQ-9/GAD-7 item counts, complete and incomplete coverage, established frequency thresholds, PDF/workbook presence, distinct same-day Therapy/Physical Therapy events with the same description, common-folder routing and creation, portable containment, non-overwriting filenames, optional open behavior, graceful failures, the fifth Review action, and compact Spinbox padding. The full suite, compilation, and representative fictional PDF/workbook validation are recorded in the Iteration 008.2 document and build notes. No production database or real user output was used.

## August 29, 2026: Closed Alpha Program Planning and Development Provenance

### Context

With the Windows portable workflow validated and the application approaching a small external test, the project needed a deliberate closed-alpha process rather than an informal file handoff. The program must test usability, reliability, data integrity, and report usefulness without weakening the local-first boundary or turning Daniel into the custodian of participant health information.

Daniel also asked that the project record how the work is actually produced. He defines what the application should accomplish and evaluates whether it meets the need. He relies on the assistant to handle software-development and process implementation because trying to learn software development concurrently with the project's other demands would add enough friction that he would likely stop the project. This is project provenance and a practical division of labor, not a deficiency. Daniel remains the final reviewer for product direction, privacy, clinical framing, and release decisions.

### Decisions

- Draft a versioned Closed Alpha Test Plan before preparing invitations or distributing a build.
- Target Friday, September 4, 2026 for the start of a two-week Windows-only test using a portable ZIP and an initial cohort of approximately 5-8 deliberately recruited testers.
- Focus the first cycle on usability, reliability, data integrity, and report usefulness; use structured issue intake plus short first-use, midpoint, and final surveys.
- Preserve local ownership of databases, reports, and exports. Do not collect participant health data by default, and direct testers not to place assessment responses, journal text, treatment details, or identifiable reports in feedback.
- Use tester IDs such as `MHT-A001`, keep any contact mapping separate, and provide direct support limited to software use and defect reporting.
- State that the alpha is pre-release, not diagnostic or treatment software, does not provide monitoring or emergency response, and should not be the only repository for important health information.
- Let participants stop at any time and delete their extracted local files, with clear warning that deletion is permanent without their own backup.
- Recruit the first cohort deliberately before broader LinkedIn outreach.
- Keep clinician review separate and use fictional/sample reports rather than participant reports.
- Mark eligibility, pseudonymity, real-versus-fictional entry policy, support-channel expectations, compensation, and clinician-track timing as provisional decisions requiring Daniel's approval.

### Documentation and consequences

Alpha Test Plan v0.1 now records the working baseline, privacy and safety boundaries, release controls, schedule, test scenarios, feedback fields, triage levels, evaluation criteria, provisional decisions, and records to retain. This planning step changes documentation only; it does not change application code, authorize distribution, or resolve the separately planned Iteration 008.2 implementation.

## August 29, 2026: Closed Alpha Governance Decisions Finalized

### Context

Daniel reviewed every provisional item in Alpha Test Plan v0.1 and chose a deliberately narrow product-testing model. The program must produce candid evidence about software behavior without asking testers to explain mental-health familiarity, disclose diagnoses, or send anything entered into the tracker. The decision process also examined Maryland's incorporation of the federal human-subject framework and the Common Rule definition of research.

Daniel explicitly understands that assistant discussion is not legal advice and does not interpret it as legal advice. Because paid legal review is not financially practical, he chose to proceed with a documented risk posture: Closed Alpha 1 is designed solely to improve the software and its immediate distribution, documentation, usability, reliability, data integrity, workflows, and generated-output usability. It is not designed to develop knowledge about participants, health, behavior, treatment, assessment results, outcomes, or effects on health.

### Decisions

- Run Closed Alpha 1 from September 4-18, 2026 with 5-8 adults and no financial or material compensation.
- Recruit for varied software-use perspectives without asking for diagnosis, health history, or an explanation of why a person fits a category. Do not rely entirely on close family; defer broader LinkedIn outreach until the first cohort and process are reviewed.
- Assign IDs such as `MHT-A001`. Daniel may know identities for communication and support, but GitHub and ordinary project records use IDs. Keep a Daniel-only roster segregated from GitHub and target destruction 30 days after closeout unless a documented administrative need requires otherwise.
- Let participants enter real, fictional, random, or mixed data locally without asking which. Entered data remains controlled by the participant.
- Establish a categorical health-data firewall. Feedback is about the software only. Do not request or accept assessment responses, journal entries, treatment or clinician information, generated reports, Analysis Workbooks, databases, screenshots containing entered data, or other medical or health information, even if fictional or created for testing.
- If prohibited material is received, do not use, analyze, or intentionally retain it, regardless of whether it was sent accidentally or intentionally; delete or destroy it as soon as reasonably practicable after identification and request only non-medical troubleshooting details. Prefer project-created fictional reproduction data.
- Use Google Forms without file uploads for structured intake and milestone surveys. Put the warning immediately before every free-text field. Use a secured dedicated Google account and Drive with conservative sharing and folder separation; do not store participant health data there.
- Use `projectmentalhealthtracker@gmail.com` for best-effort software and administrative support, generally targeted within 24-48 hours. It is not continuously monitored or available for clinical, crisis, or emergency support. A tester who encounters a blocker or suspects data loss should stop the affected activity rather than repeatedly retry it.
- Require a versioned, plain-language Closed Alpha Participation Acknowledgment before software distribution. Do not call it informed consent. Record the version and date accepted for every tester.
- End the active feedback and support cycle on September 18. Testers may retain or delete the installed alpha and their local data, but later feedback is outside Closed Alpha 1 and fixes or support for an obsolete build are not promised.
- Defer clinician review until Closed Alpha 1 feedback has been incorporated into a stable candidate report; do not run it concurrently.

### Compliance posture and references

Maryland Health-General § 13-2001 incorporates the federal human-subject framework's definition of research, and § 13-2002 applies federal protections when an activity is research using a human subject. Under 45 C.F.R. § 46.102(l), research is a systematic investigation, including testing and evaluation, designed to develop or contribute to generalizable knowledge. The project documents its software-testing design against that framework while recognizing that this is a project decision and risk posture, not a binding legal determination.

Authoritative references reviewed:

- [Maryland Health-General § 13-2001](https://mgaleg.maryland.gov/2026RS/Statute_Web/ghg/13-2001.pdf)
- [Maryland Health-General § 13-2002](https://mgaleg.maryland.gov/2026RS/Statute_Web/ghg/13-2002.pdf)
- [45 C.F.R. § 46.102 (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.102)
- [HHS OHRP: What Is Human Subjects Research?](https://www.hhs.gov/ohrp/education-and-outreach/online-education/human-research-protection-training/lesson-2-what-is-human-subjects-research/index.html)

### Documentation and consequences

Alpha Test Plan v0.2 resolves every provisional decision from v0.1. Closed Alpha Participation Acknowledgment v0.1 establishes the pre-distribution participant-facing gate. ADR 0007 records the durable governance and health-data-firewall decision. README, Roadmap, and Privacy and Data Handling now point to or implement the approved model.

Tester names, the exact application build and hash, and the supporting invitation, Tester Guide, Forms, surveys, issue log, release record, Drive configuration, replacement-build procedure, and closeout message remain operational work. No application code, database, personal data, report, export, or generated health artifact changed in this documentation iteration.

## August 29, 2026: Closed Alpha Tester Guide v0.1 Drafted

### Context

The approved test plan and participation acknowledgment established the program rules, but a participant still needed a short, practical guide from distribution through closeout. The guide had to support safe use without teaching every interface path, because Closed Alpha 1 is intended to reveal whether the application and its own wording are understandable.

Repository inspection confirmed the current portable behavior: the supplied batch launcher enables portable mode; first launch creates `phq9_tracker.sqlite` beside the executable in the extracted folder; the application does not intentionally upload entered content; and PDF/workbook actions use Windows save dialogs, so generated outputs remain at locations chosen by the tester rather than a guaranteed portable subfolder.

### Decisions

- Keep the participant journey concise: safe extraction and launch, local-data understanding, one persisted first-use check-in, natural use, midpoint feedback, later Review/output exploration, and final closeout.
- Repeat the intent-neutral health-data firewall and make all problem reporting software-only. Do not accept files or entered content, and use no screenshot by default.
- Explain tester IDs only as needed for feedback and support; do not expose private-roster operating details beyond the already approved participant acknowledgment.
- Use a closed-application copy of the entire extracted folder as the simplest participant backup instruction. Generated outputs saved elsewhere require separate backup.
- Describe deletion according to portable behavior: close the application, delete the extracted folder, and separately delete locally generated outputs saved elsewhere.
- Leave the final application version/source revision, ZIP filename/size/hash, supported Windows versions/architecture, download URL, Google Form URLs, clean-Windows launcher/security-prompt check, and frozen-package backup/deletion/replacement instructions as visible release-readiness placeholders rather than guessing.
- Add a small alpha-document index and link the guide from the README, roadmap, approved plan, and governance ADR.

### Validation and consequences

The guide was checked against Alpha Test Plan v0.2, Closed Alpha Participation Acknowledgment v0.1, the portable build script, database-path selection, Review action labels, and PDF/workbook save behavior. A text audit checked required dates, safety boundaries, support expectations, milestones, reporting fields, placeholders, and prohibited terminology. No application code, test code, database, report, export, personal data, or health information changed.

Closed Alpha Tester Guide v0.1 remains a draft and must not be distributed until every release-readiness placeholder is replaced and the complete instructions are exercised against the frozen ZIP on a clean Windows environment.

## August 30, 2026: Closed Alpha Tester Guide Participant-Facing Cleanup

### Context

Daniel approved removing internal and nice-to-have release-control details from the participant-facing Tester Guide. The guide should contain only information necessary for safe participation and useful software testing. Internal build identification, integrity, clean-environment validation, and replacement-readiness controls remain required, but they belong in the Alpha Test Plan and release-readiness records rather than in tester instructions.

### Decisions

- Limit the guide's Release Information section to the individually supplied tester ID; application version/build identifier; approved ZIP filename and download URL; tester-relevant Windows compatibility; and first-use, routine feedback, midpoint, and final Form URLs.
- Remove participant-facing source-revision, ZIP-size, SHA-256, clean-Windows verification, and internal backup/deletion/replacement-readiness placeholders. Testers are not asked to verify a hash.
- Preserve the statement that Forms do not accept uploads and the routing distinction between Forms for routine feedback or milestones and email for access, administrative questions, blockers, or suspected data loss.
- Remove internal checklist status language from the launch and backup passages while preserving the verified launcher name, database-handling warning, and instruction to contact support before moving data into another build.
- Keep the internal release gates in Alpha Test Plan v0.2 unchanged and clarify there that the participant guide's substantive content is ready to freeze after its remaining tester-facing values are supplied and confirmed.

### Validation and consequences

A focused text review confirmed that the removed terms no longer appear in the Tester Guide, that all nine approved tester-facing Release Information fields remain, and that the privacy, local-data, backup, support, testing, reporting, safety, and closeout guidance is unchanged except for the removal of internal status wording. Markdown whitespace and the exact changed-file inventory were also checked. No application code, test code, database, report, export, personal data, or health information changed.

## September 12, 2026: Iteration 010 Extensible Questionnaire Framework

Iteration 010 promotes the existing reusable assessment model to a questionnaire-oriented extension contract while retaining database, package, executable, and environment-variable compatibility. PHQ-9 and GAD-7 remain the only registered built-ins. Their source and redistribution status now travel with the definition metadata, and PHQ-9 item 9 behavior is explicitly instrument-specific.

Today's Check-In now lets the user choose either or both questionnaires and derives an independent Complete or Not completed state from saved records. An unselected questionnaire is not silently stored as an all-zero response. The universal safety message appears before the first question and in every PDF footer. PDF and Analysis Workbook generation allow questionnaire selection and filter the derived 14-day profiles accordingly.

Custom questionnaire authoring, external definitions, configurable scoring rules, and release packaging are deliberately deferred. Existing records require no destructive migration because the additive generic `assessment_entries` path introduced in Iteration 004 remains authoritative for shared questionnaire behavior, while `phq9_entries` stays synchronized for compatibility.

Daniel's GUI review found that the optional-details submission controls extended below the available Today-page viewport. The form now uses a vertical scrollbar, supports mouse-wheel scrolling while the pointer is inside the Today page, automatically brings the optional controls into view after the core check-in is saved, and returns to the top when optional entry closes. A live 1180 x 780 Tk geometry check confirmed that the Save Optional Details button was fully visible after the automatic scroll.

## Ongoing Journal Practice

Future iteration entries should capture the context that prompted the work, the decisions made, meaningful alternatives that were rejected or deferred, validation performed, consequences, and lessons learned. Significant product or architectural decisions should also be recorded or amended in `docs/decisions/`.

## August 31, 2026: Closed Alpha 1 Candidate Packaging

Daniel's August 30 source-GUI walkthrough closed Iteration 008.2: both output types passed repeat-generation/open-prompt checks, the common reports folder and real outputs were acceptable, Spinboxes were improved, and the 008.1 sanity check remained good. He separately deferred a future Treatment Cycles chart that overlays the current ketamine cycle and two prior cycles in three colors; no such feature was added to this release.

Candidate `0.3.0-alpha.1` was built from the approved uncommitted worktree based on `4f4afa7eb2046b882325b8ada6df4690d9d4a854`. Compilation and 59/59 tests passed. The first package was rejected when it exposed broken automatic Tcl/Tk discovery. The release build was corrected to bundle the required Tkinter/Tcl/Tk runtime explicitly, then rebuilt as `PHQ9Tracker-Portable-0.3.0-alpha.1.zip`.

The rebuilt archive was database-free. Portable-mode startup created a blank database beside the executable; the exact packaged executable passed fictional persistence, Review/chart/keyboard, guarded-date, unsaved-change, History/manage, double PDF/workbook generation, collision-safe naming, and output inspection. PDF and workbook content passed structural and rendered visual checks. The full desktop GUI pass used installed-mode LocalAppData because the desktop-control path could not directly invoke the batch launcher; portable containment was verified separately by startup behavior and automated coverage. The candidate remained undistributed.

Daniel then independently checked the actual candidate ZIP on August 31 from his Windows development workstation. The previously reported `%LOCALAPPDATA%\PHQ9Tracker` validation folder was already absent. He manually extracted `PHQ9Tracker-Portable-0.3.0-alpha.1.zip`, launched `PHQ9Tracker.exe` directly from the extracted folder, and launched `Launch Portable Mental Health Tracker.bat`; both opened successfully with a blank database. This owner validation closes the earlier local cleanup uncertainty and supplies direct evidence for both extracted launch paths. It remains distinct from a separate clean-Windows validation, so the clean-environment and Windows security-prompt gate stays open.

Later on August 31, Daniel transferred the exact candidate ZIP to a volunteer's separate Windows computer. The volunteer received and extracted the ZIP on that machine, launched and used the packaged application, and reported through Daniel that all exercised behavior worked. No Python, Tkinter, or other development runtime preparation was performed. This closes the identified separate-Windows extraction-and-launch gate to the extent observed. It does not claim a pristine VM or freshly installed Windows image, specific SmartScreen or other security-prompt behavior, or exact persistence/output subtests. Work's installed-mode desktop-control pass, Daniel's development-workstation EXE/batch test, and the volunteer's separate-machine test remain three distinct bodies of evidence.

The end-of-night Alpha infrastructure was privately editor-ready: five unpublished Forms were linked to five response Sheets and had zero responses at audit; Routine Problem / Feedback was complete for build `0.3.0-alpha.1`; `MHT-TEST-001` remained the sole fictional validation ID; and the private administration record held the build and ZIP filename with a blank download URL. No Form was published, no real tester was enrolled, and no ZIP upload, sharing, or distribution occurred. Remaining gates are final tester selection and pseudonymous IDs, explicit publication authorization and signed-out/private-browser Form validation, the fictional end-to-end administrative dry run, any final security-prompt risk decision, and Daniel's final go/no-go and distribution authorization.

## September 7, 2026: Public Repository Readiness Documentation

Daniel abandoned the formal Closed Alpha before enrollment or distribution and chose to evaluate a public-repository soft launch instead. This iteration did not change repository visibility, publish Forms, create a release or tag, upload the portable ZIP, or modify application behavior.

The repository was audited as a first-time public visitor would encounter it. Public-facing guidance now identifies `0.3.0-alpha.1` as unsigned alpha/pre-release software, uses a future GitHub pre-release as the recommended nontechnical download path, distinguishes portable-batch storage from direct-EXE and installed-mode LocalAppData storage, and provides backup/update/reset guidance. Privacy and security documentation now prohibits users from sending databases, reports, workbooks, tracker-entered content, or private screenshots and asks for version, reproduction steps, expected/actual behavior, and exact non-health error or security-warning text.

The former Closed Alpha materials remain as historical provenance but are explicitly superseded. Their tester-ID, acknowledgment, cohort, milestone, and private-Form workflow is not active. The volunteer's name was removed from the current tree because the validation fact does not require identifying the person.

That identity work was later completed through an audited history rewrite, leaving `main` at `156cf2e331cdf9224275ca6de9a286dbad012f19` with Daniel's confirmed GitHub noreply address. Daniel then selected GNU GPL version 3.

## September 7, 2026: Iteration 009 Public Redistribution and Licensing Readiness

The dependency audit found no GPLv3-incompatible runtime component, but it retired the previously validated `PHQ9Tracker-Portable-0.3.0-alpha.1.zip` (`76DE3678...`) from public redistribution because its third-party notices were incomplete. The project added the canonical unmodified GPLv3 text, Daniel's copyright identification in project documentation, a committed notice tree sourced from exact upstream distributions, a hash/version manifest, a fail-closed verifier, pinned release requirements, and packaging automation that places `LICENSE` and `THIRD_PARTY_NOTICES` in distributable folders and ZIPs.

The first attempted full rebuild used the available Python 3.14.5 environment after the preserved Python 3.12 build executable proved inaccessible to the sandbox. That runtime's Tcl/Tk installation could not initialize its own `init.tcl`; the resulting package failed the same way and was rejected. The narrower correction then verified the old ZIP's exact hash and 1,836-entry privacy-clean inventory, retained its executable byte-for-byte, added the notice set, and produced `PHQ9Tracker-Portable-0.3.0-alpha.1-redistribution.1.zip` (43,790,609 bytes; 1,916 entries; SHA-256 `CC1EDC4E9F2A0977C13E931308B7DC3C7B32FD4C2345A6D6221AA75F9B690249`).

The notice-complete archive passed integrity, privacy, exact-license matching, packaged command-line persistence, repeated PDF/workbook generation, PDF extraction and five-page rendering, and eight-sheet workbook structure/content/rendering checks. All 59 source tests and compilation also passed. Current GUI startup nevertheless failed with `_tkinter.TclError: Can't find a usable init.tcl`, including when the unchanged historical executable was extracted to a short path. This is a mandatory release blocker. The artifact was not promoted, the old separate-machine evidence was not applied to its new hash, and no commit, push, tag, release, upload, visibility change, Form change, or distribution was made.

## September 8, 2026: Iteration 009 Tcl/Tk Packaging Repair

The failed package already contained `init.tcl`, `tk.tcl`, `_tkinter.pyd`, and the intended Tcl/Tk DLLs. A project-local environment assembled from the official signed CPython 3.12.10 Windows MSI components reproduced the same initialization failure with Tcl/Tk 8.6.15, ruling out the active Python 3.14 installation and missing bundle content as the root causes. Low-level Tcl diagnostics showed that canonicalization under the sandboxed Windows user profile removed or doubled path components. The same libraries initialized when addressed through Windows extended paths.

The repair is confined to packaging. The PyInstaller runtime hook now supplies extended bundle-relative Tcl/Tk paths, a new pre-import entry point reasserts them immediately before application import, the source-runtime verifier applies the same normalization, and the release script fails on PyInstaller errors or missing Tcl/Tk bundle content. It also defaults to the distinct `redistribution.2` artifact revision. No application source, data model, feature, or visible behavior changed; no global Python, registry, or Windows environment change was made.

The pinned Python 3.12.10/Tcl/Tk 8.6.15/PyInstaller 6.22.1 rebuild produced `PHQ9Tracker-Portable-0.3.0-alpha.1-redistribution.2.zip` (43,745,615 bytes; 1,910 entries; 96,483,945 uncompressed bytes; SHA-256 `5A43D176103FCEDBA1FBD36F01C78FDD88237FB27F369C859A9B37C8F497D1DA`; executable SHA-256 `D914BDB42E89093959467717A427F6238AD5B99629A635E0E1BE31EDC44E2E59`). The exact archive passed integrity, privacy, GPL/notice, normal/short extraction, direct/batch startup-liveness, portable blank-database and fictional persistence, repeated collision-safe PDF/workbook generation, rendered output inspection, file-level reset/relaunch, compilation, and all 61 tests.

The startup crash was resolved, and Daniel then completed the required hands-on GUI walkthrough against the exact quarantined `.2` ZIP on his development workstation. He reported that fresh extraction and batch launch, fictional PHQ-9/GAD-7 entry with a note and treatment event, close/reopen persistence, Review/chart interaction, exercised keyboard/date behavior, unsaved-change handling, two collision-safe GUI PDF generations, two collision-safe GUI Analysis Workbook generations, Open Reports Folder, in-app delete/reset, and close/reopen after reset all worked. No Windows Defender or SmartScreen prompt appeared. This records only Daniel's reported results; it does not claim separate-machine validation of the `.2` hash or transfer the old artifact's evidence. The `.2` folder and ZIP remain quarantined under ignored `work/pending_iteration_009_candidate/`. No push, tag, release, upload, visibility change, Form change, or distribution occurred.

## September 13, 2026: Iteration 011 Community and Security Intake

After the first Len-branded public prerelease was published and its documentation reconciled, the next repository-readiness gap was the absence of structured, privacy-conscious community intake. GitHub Issues accepted only blank submissions, private vulnerability reporting was disabled, and the repository had no contributing guide, support guide, code of conduct, issue forms, or pull-request template.

Iteration 011 separates ordinary support, suspected vulnerabilities, and conduct concerns. The new guides preserve Len's software-only, non-clinical boundary and require project-created fictional data. Public bug and feature forms warn against PHI, PII, assessment content, generated Len files, credentials, and identifying paths before accepting details. Blank issues are disabled by configuration, and the pull-request checklist carries the same privacy, compatibility, testing, documentation, licensing, and AI-review expectations into proposed code changes.

GitHub private vulnerability reporting is the preferred security route, with the public project email retained only as a fallback. After Daniel's explicit action-time confirmation, the setting was enabled in the live public repository and GitHub confirmed that the repository settings were saved. Discussions remain disabled until the project has an approved moderation model for likely health or clinical disclosures.

This work changes repository participation and documentation only. It adds no application feature, dependency, schema change, user-data migration, package, release artifact, or clinical claim. Validation covers the structured YAML, local Markdown links, required privacy/safety language, forbidden tracked artifacts, whitespace, compilation, and the full automated test suite.

## September 13, 2026: Iteration 012 Repository Automation and Discovery

Iteration 012 adds the repository's first application test workflow. Pull requests targeting `main`, pushes to `main`, and owner-requested manual runs use a GitHub-hosted Windows runner with Python 3.12 to install the existing source dependencies, run the complete automated test suite, and compile the source, tests, and packaging modules. The repository description and topics now foreground Len's privacy-first, local-first Windows scope, and a focused label taxonomy covers data storage, reporting, workbooks, Windows packaging, accessibility, privacy and safety, triage status, and genuinely high-priority work.

The workflow has read-only repository permissions, a bounded timeout, and concurrency cancellation for superseded runs. Its external GitHub Actions are pinned to verified full release commit hashes rather than mutable branch references. It deliberately does not build or publish packages, create releases, access secrets, test with real data, or make GUI and exact-artifact claims that its source-level checks cannot support.

Dependabot vulnerability alerts and GitHub secret-scanning alerts are enabled as read-only detection signals. Automatic dependency-update pull requests, secret push protection, and CodeQL remain deferred until the CI signal is proven and their operational effects are reviewed. The workflow must produce a successful live run before its job is made a required `main` status check or a passing badge is added to the README. Branch and tag rules remain separate repository-governance decisions.

The first live Windows CI run parsed and started the workflow successfully, installed the dependency set, and ran all 68 tests. Two portable-path assertions failed because the GitHub runner represented its temporary directory once with the long Windows username and once with the equivalent DOS 8.3 alias. The application already resolves the executable path by design. The tests now derive their expected portable database and reports paths from that same resolved executable location, preserving the intended beside-the-executable contract while avoiding a spelling-sensitive comparison of equivalent Windows paths.

Enabling Dependabot surfaced 23 alerts in the pinned release-build requirements: 13 for Pillow 12.2.0 and 10 for pypdf 6.13.3. Pillow is part of the documented distributed runtime; pypdf is used for test and release preflight and is not listed in the distributed-runtime notice manifest. The published prerelease remains byte-for-byte frozen. Dependency upgrades, updated third-party notices and manifest evidence, rebuilding, and exact-artifact validation belong in a separate future release iteration rather than this repository-automation correction.
