Current as of: 2026-09-18
Last substantive update: 2026-09-18

# Build and Release Notes

## Current Public-Release Posture

`v0.4.1-alpha.1` is the current public prerelease. The published artifact is `Len-Portable-0.4.1-alpha.1.zip` (43,806,172 bytes; 1,856 file entries; 96,687,018 uncompressed file bytes; SHA-256 `41C9F5DACB1523FE15730FDA21B014825B7D55141D1C754A31C951DF5AE5DE18`). The release/tag commit is `6c199cc166ac4e107924f0134249c369f0c233dc`; its separate build-source provenance is preserved in the [release record](docs/releases/v0.4.1-alpha.1.md). The public prerelease and asset are available from [the official GitHub release](https://github.com/DScannellWiz/len-mental-health/releases/tag/v0.4.1-alpha.1). The local release ZIP remains ignored and must not be committed to Git.

Only the latest published alpha is supported. `v0.4.0-alpha.1`, `v0.3.0-alpha.1`, and earlier prereleases remain downloadable as frozen historical records; do not rebuild, overwrite, relabel, or transfer their validation evidence to a newer candidate.

Release preparation for `v0.5.0-alpha.1` is authorized, but it is not public. Its planned portable asset is `Len-Portable-0.5.0-alpha.1.zip`; build-source commit, byte size, ZIP entry count, uncompressed size, SHA-256, signature inspection, Defender results, and exact-candidate validation evidence remain pending until the candidate is built once and frozen. See the [candidate record and draft release notes](docs/releases/v0.5.0-alpha.1.md). Do not advertise `v0.5.0-alpha.1` as available before separate publication approval.

Do not create a tag, GitHub Release, upload, or public announcement merely because the source and candidate tests pass. Repository visibility, source publication, binary distribution, and social-media promotion are separate owner decisions.

## Packaging Choice

Use a folder-based PyInstaller build (`--onedir`) rather than a single-file executable. This keeps startup faster, makes troubleshooting easier, reduces antivirus false positives, and supports bundled assets and future report templates more cleanly.

The visible application name is **Len**. The executable remains `PHQ9Tracker.exe`, and the Python package, environment variables, database filename, LocalAppData folder, and icon asset retain their PHQ9-oriented names for backward compatibility and existing-data continuity.

## Dependencies

Recommended build environment:

- Python 3.12.10 from python.org with Tcl/Tk 8.6.15 installed for reproduction of the audited `0.3.0-alpha.1` runtime
- `pandas`
- `openpyxl`
- `Pillow`
- `reportlab`
- `pypdfium2` for screenshot/PDF verification
- `pyinstaller`
- Inno Setup 6 for the Windows installer

Install the exact release dependency set in an isolated environment:

```powershell
python -m pip install -r .\packaging\requirements-release.txt
```

The source launcher prefers a project-local `.venv` or `venv` when present. Report generation also checks `PHQ9_TRACKER_BUNDLED_PYTHON`, then those project-local environments, before reporting exactly which packages are unavailable.

The release script performs dependency and licensing preflights before invoking PyInstaller. It fails early when the selected Python/runtime versions, package versions, project license, or third-party notice hashes differ from `packaging\third_party_notice_manifest.json`.

## Build Executable and Portable Version

```powershell
cd <project-root>
.\packaging\build_release.ps1 -Version <next-version>
```

This creates:

- `dist\PHQ9Tracker\` folder-based application build
- `release\Len-Portable-<next-version>\` portable folder
- `release\Len-Portable-<next-version>.zip` portable archive

The current build script requires an explicit version and rejects the frozen `0.3.0-alpha.1` value. Use `-ArtifactRevision` only when packaging content changes without an application-version change. Every folder, ZIP, and future installer produced from the folder build includes the project `LICENSE` at its root and the complete `THIRD_PARTY_NOTICES` directory.

The release verifier must initialize the exact Python 3.12.10/Tcl/Tk 8.6.15 runtime and match all package versions before PyInstaller runs. The build explicitly bundles the Tkinter package, Tcl/Tk libraries, extension, and DLLs, then fails if any required bundle file is absent. After PyInstaller copies the Tkinter sources, the build removes only the redundant bundled `tkinter\__pycache__` directory and fails if any `__pycache__`, `.pyc`, or selected local build-root string remains anywhere in the bundle. The controlled Python installation is not modified. On Windows, the runtime hook and `packaging\portable_entry.py` set `TCL_LIBRARY` and `TK_LIBRARY` to extended (`//?/`) bundle paths before application import. This prevents Tcl path canonicalization from dropping sandboxed user-profile path components; it is not a machine-wide environment change.

The original `PHQ9Tracker-Portable-0.3.0-alpha.1.zip` may be used only as an audited packaging input by the narrow notice-repackaging command:

```powershell
.\packaging\repackage_release_with_notices.ps1 -Version 0.3.0-alpha.1 -ArtifactRevision redistribution.1
```

That command refuses any base archive whose SHA-256 is not `76DE3678AF9BF5C61CC0C0A318347E0F5E1C7F471A6112FE9431DA9A304F4C47`, verifies its 1,836-entry privacy-clean inventory, verifies every committed notice hash, and creates a distinct output without changing the validated executable bytes. It exists to make this administrative correction reproducible; a normal future release should use the full build script in the pinned, Tcl/Tk-capable environment.

## Licensing and Notices

Project source is `GPL-3.0-only`; the canonical unmodified text is `LICENSE`. Daniel's copyright identification belongs in project documentation, not inside the GPL text. `THIRD_PARTY_NOTICES\README.md` inventories the distributed runtime, and the adjacent verbatim files preserve CPython's complete license/incorporated-software appendix, Tcl/Tk terms, the PyInstaller bootloader exception, NumPy and Pillow embedded-component inventories, ReportLab/font notices, and the applicable pandas, OpenPyXL, et_xmlfile, python-dateutil, six, charset-normalizer, and tzdata/IANA terms.

Do not delete notices merely because a third-party license is GPL-compatible. Compatibility and notice-preservation are separate requirements.

The portable launcher sets `PHQ9_TRACKER_PORTABLE=1`, which keeps `phq9_tracker.sqlite` and the `reports` folder inside the portable folder. Starting `PHQ9Tracker.exe` directly does not set portable mode and instead uses `%LOCALAPPDATA%\PHQ9Tracker`. Public instructions must tell portable users to use the batch launcher consistently.

Future Len-branded portable builds retain the executable icon and create no system shortcuts. The launcher is named `Launch Portable Len.bat`. Historical `0.3.0-alpha.1` artifacts keep their original launcher names and bytes.

## Application Icon

The build uses the existing icon asset:

```text
packaging\assets\PHQ9_Tracker.ico
```

This icon was copied from the user's shared application icon template folder and should remain a checked-in packaging asset unless replaced intentionally in a future branding iteration.

## Build Installer

Install Inno Setup, then compile:

```powershell
iscc /DMyAppVersion=<next-version> .\packaging\PHQ9Tracker.iss
```

The installer deploys the folder-based app under a **Len** Program Files folder, creates a Start Menu shortcut under **Len**, selects desktop-shortcut creation by default, and registers an uninstaller in Windows Apps & Features. Both shortcuts explicitly use the executable's embedded Len icon.

Installed builds store user data in:

```text
%LOCALAPPDATA%\PHQ9Tracker\phq9_tracker.sqlite
```

This preserves user data during upgrades because installer file replacement does not overwrite LocalAppData.

## Database Migration

Iteration 004 keeps the legacy `phq9_entries` table and adds `assessment_entries`.

On startup, existing PHQ-9 rows are copied into `assessment_entries` using `INSERT OR IGNORE`. GAD-7 entries are stored only in `assessment_entries`. This keeps older PHQ-9 behavior intact while giving future assessments a reusable storage path.

Iteration 006 requires no schema migration. It adds stable-ID update/delete operations over the existing tables, keeps legacy PHQ-9 rows synchronized, and prevents deleted PHQ-9 assessments from being recreated by the startup migration.

Iteration 007 also requires no schema migration. Date navigation, Review summaries, treatment-cycle windows, and the compact clinician report operate on the existing assessment, note, and treatment-event records.

Iteration 007.2 requires no schema migration. Its normalized analysis workbook derives stable relationships from existing assessment IDs, treatment-event IDs, and deterministic date/item identifiers.

Iteration 008 requires no schema migration. It removes legacy report/export interfaces and code while continuing to read the same assessment, note, and treatment-event records.

Iteration 008.1 requires no schema migration. Chart callouts, guarded date loading, interface wording/style changes, keyboard bindings, and recency-aware report language operate on the existing records and report pipeline.

Iteration 008.2 requires no schema migration. It derives current 14-day item-profile records from existing assessment entries, corrects event-type display mapping, and changes only generated-output routing and Review conveniences.

Iteration 014 adds two transactional, idempotent migrations: an append-only migration ledger with immutable questionnaire-definition snapshots, followed by normalized versioned questionnaire submissions/responses. Startup preserves exact PHQ-9/GAD-7 v1 snapshots, adds active v2 daily-severity definitions, backfills previously unnormalized compatibility rows against v1, and verifies identity, response shape/order/value/score, totals, severity, source, timestamps, and uniqueness before commit. Existing normalized v1/v2 rows reconcile against their stored definition version. Reads prefer verified normalized rows with an explicit legacy fallback. Writes keep normalized storage and `assessment_entries` atomic, and PHQ-9 writes also keep `phq9_entries` synchronized. The migration does not drop, rename, repurpose, or destructively rewrite either compatibility table.

## User Data During Backup and Updates

Before an update, close the application and back up the database plus any reports the user wants to retain. For a portable update, extract the new version to a new folder; do not overwrite the only working copy in place. Copy the backed-up `phq9_tracker.sqlite` into the new folder before starting the portable batch launcher, verify the expected History records, and retain the old folder or backup until verification succeeds.

Installed-mode or direct-EXE data under `%LOCALAPPDATA%\PHQ9Tracker` is separate from portable-mode data. Changing launch methods can make a valid database appear missing. Installer replacement is designed not to overwrite LocalAppData, but installer behavior remains less validated than the portable path and should not be the initial public binary offering.

Current startup migration preserves legacy PHQ-9/GAD-7 records, applies schema changes in a transaction, and fails closed when a migration checksum, immutable definition snapshot, or backfilled record does not reconcile. There is no automatic backup, restore wizard, or encryption. Transaction rollback protects a failed migration attempt, but it is not a substitute for a closed-application backup. Back up and restore the complete database file, then verify expected History records before deleting the previous copy.

## Windows Security and Code Signing

The candidate is not code-signed. Windows Defender, Microsoft SmartScreen, or another security product may scan it or warn that it is an unfamiliar pre-release application with limited reputation. Users should allow normal scanning and must not be told to disable antivirus, suppress an actual detection, or override a warning they do not understand.

Capture the exact security product, warning text, detected file, release filename, release source, and hash when investigating. Do not collect screenshots containing private health data or identifying paths. Code signing would improve publisher identity and reputation signals, but it is a future release-engineering improvement rather than evidence that a binary is safe.

## Size Reduction

Current build script excludes common development-only modules such as test tooling, notebooks, and IPython. Inno Setup uses LZMA2 solid compression. Additional opportunities:

- Build inside a clean virtual environment.
- Avoid installing large unused scientific packages.
- Inspect `dist\PHQ9Tracker` and remove unused sample data, caches, or tests before installer compilation.
- Keep report screenshots, generated PDFs/workbooks, databases, and other private artifacts out of release source/build inputs. A running portable copy creates its private `reports` folder beside the executable.

## Versioning

Update these together for each release:

- `packaging\build_release.ps1` `-Version`
- `packaging\build_release.ps1` `-ArtifactRevision` when packaging content changes without an application-version change
- `packaging\PHQ9Tracker.iss` `MyAppVersion`
- Release zip and installer filenames
- `packaging\requirements-release.txt`, `packaging\third_party_notice_manifest.json`, and `THIRD_PARTY_NOTICES` when runtime components change

## Validation Checklist

- Launch installed app.
- Launch portable app.
- Confirm existing PHQ-9 database rows migrate into `assessment_entries`.
- Restore a closed-application pre-Iteration-014 database backup, launch again, and confirm the same historical rows migrate into the compatibility and normalized stores without duplication or loss.
- Save a Today's Check-In with PHQ-9, GAD-7, notes, and optional treatment event.
- Confirm both active questionnaires are definition v2, show `Not present / Mild / Moderate / High`, and place the single-day severity instruction immediately above the questions.
- At a reduced supported window size, use the keyboard to move through the questionnaire roster and active definition-driven form; confirm unanswered required items are blocked, a selected zero is accepted, switching forms preserves unsaved answers, and one/both questionnaire saves retain independent completion state.
- Navigate across month and year boundaries, confirm an existing date auto-loads, verify future dates are blocked, and confirm unsaved-change protection.
- Open Review and inspect recent, treatment-cycle, and long-term views using synthetic data.
- Hover and click representative chart points at the left edge, center, right edge, highest score, and lowest score; confirm every callout shows the exact date, series, and score without clipping. Tab to a chart and verify Left/Right, Enter, and Escape.
- Change Today and History date fields with and without unsaved edits. Confirm safe changes auto-load, unsafe changes remain guarded, Enter loads explicitly, and no save can apply visible responses to a date that is not loaded.
- Confirm Review shows **Refresh**, **Import Spreadsheet**, **Generate PDF**, **Analysis Workbook**, and **Open Reports Folder**, with no separate Clinician Report tab.
- For reports, choose the date range first; confirm only questionnaires with records in that range are eligible and that incompatible definition versions are identified rather than blended.
- Generate the full-history clinician PDF when `reportlab` and `Pillow` are available and confirm that no companion CSV is created.
- Confirm the clinician PDF has no clipped content, preserves every included journal entry in full, and omits duplicate raw PHQ-9 tables. Typical reports remain compact, but narrative-heavy reports may exceed four pages rather than truncate user text.
- Confirm the PDF's current 14-day item profile shows PHQ-9 and GAD-7 symptom-present day counts, recorded-day coverage, and 0-3 frequency scores with missing days described as missing information.
- Create same-day Therapy and Physical Therapy events with the same fictional description and confirm both event types remain distinct in the PDF and workbook.
- With fictional data, confirm recent above-zero PHQ-9 item 9 responses are described within the latest 14-day window with coverage; older-only responses are labeled historical and do not imply current risk; and no item 9 prompt appears when every selected response is zero.
- Generate the normalized Analysis Workbook and confirm its eight logical worksheets contain no merged cells, one logical record per row, and valid identifier relationships. Confirm **14-Day Item Profile** contains 16 derived item records.
- Confirm historical v1 workbook item responses retain `definition_version=1` but expose only numeric daily-severity `response_label` values, never the known-regressed frequency wording; confirm v1 and v2 analytics remain separate.
- Confirm PDF and workbook files both land under the common `reports` folder, repeated generation does not overwrite an existing file, optional open prompts work, open failures preserve the saved path, and **Open Reports Folder** opens the same location.
- Inspect the portable folder and ZIP before launch; confirm they contain no database, report, export, log, screenshot, PHI, or PII.
- Launch the portable package, confirm it creates `phq9_tracker.sqlite` beside the executable, save synthetic data, restart and confirm persistence, then delete/reset the synthetic database and verify a fresh launch contains zero records.
- Confirm installed app data remains under LocalAppData after reinstall/upgrade.
- Confirm no real databases, reports, exports, logs, screenshots, PHI, or PII are staged for Git.
- Confirm the running window and taskbar representation use `packaging\assets\PHQ9_Tracker.ico` where Windows supports it.
- Confirm Start Menu and default desktop shortcuts launch `PHQ9Tracker.exe` and display its icon.
- Confirm portable builds create no system shortcuts.

## Current Validation Status

Iteration 014 passes 106 tests in the controlled project environment, including a closed-database backup/restore/re-migration regression, plus application/test compilation and Git whitespace validation. Focused persistence (16) and report/privacy (4) runs also pass. Dan completed and reported **PASS** for the required isolated Windows keyboard/reduced-window source walkthrough with fictional data. Iteration 014 is complete, but the versioned questionnaire framework remains unreleased; no package, release, or public artifact inherits this source validation.

### Len public prerelease - 0.4.1-alpha.1

Iteration 013 updates Pillow to 12.3.0 and pypdf to 6.16.1, refreshes the exact Pillow license evidence, and leaves application source, data schema, storage, accepted inputs, and features unchanged. The controlled environment passed 68 automated tests, compilation, release-license verification, and exact-candidate static checks. The candidate was built from committed baseline `0532cfc736a373f0b3542da98747e8d077b493f1` plus the recorded uncommitted Iteration 013 changes.

The primary workstation's enforced App Control policy rejected the unsigned executable before launch. No bypass or policy change was attempted. The exact same 43,806,172-byte candidate subsequently passed normal non-administrator validation on an authorized separate Windows environment: direct launch used isolated LocalAppData, two portable launches preserved the fictional PHQ-9/GAD-7 fixture, and the packaged executable generated a five-page PDF and eight-sheet workbook. The operator confirmed the application and rendered outputs, and post-return inspection found no visible PDF/workbook defect or formula-error marker. The candidate's final SHA-256 remained `41C9F5DACB1523FE15730FDA21B014825B7D55141D1C754A31C951DF5AE5DE18`.

The executable is unsigned and may be warned about or blocked by Windows or organizational application-control policy. Documentation must not advise weakening security controls. The ZIP is ignored and must not be committed. Validation packages, transcripts, databases, reports, workbooks, and result archives are evidence only and must not be staged or shipped.

The exact candidate was published unchanged as a GitHub prerelease on September 14, 2026. Tag `v0.4.1-alpha.1` targets release commit `6c199cc166ac4e107924f0134249c369f0c233dc`; post-publication verification confirmed the public asset's filename, byte count, and SHA-256. Broader promotion remains a separate owner decision.

### Len public prerelease - 0.4.0-alpha.1

On September 12, 2026, the exact artifact was built from a clean local `main` checkout at `c98c258c60f672f99a769a58a260de92484a4515`; the cached `origin/main` matched at build time, but that observation was not a live authenticated GitHub audit. The controlled Python 3.12.10 environment passed the release-license verifier with 34 notice files and 11 pinned package versions, and the full source suite passed 68 tests. Release-specific documentation was then committed as `b9b4aaaa3c8339183c32ca7dda7c18ea83150ec8`, and the `v0.4.0-alpha.1` tag and GitHub prerelease reference that later commit. The artifact was not rebuilt or changed between validation and publication.

The exact ZIP has a flat portable layout and includes `PHQ9Tracker.exe`, `Launch Portable Len.bat`, the canonical GPLv3 `LICENSE`, 35 third-party-notice file entries, and the required Tcl/Tk runtime files. Its pre-launch inventory contains no database, report, export, log, or other generated user-data file. Both direct execution and the portable launcher reached a responsive window titled **Len**. Direct execution wrote to an isolated LocalAppData path; the portable launcher wrote beside the executable. A 14-day fictional PHQ-9/GAD-7 dataset with 14 notes and two distinct same-day treatment-event types persisted across a portable restart. Deleting the isolated fictional database and relaunching produced zero assessment and treatment-event records.

The packaged executable generated a five-page Len clinician PDF and an eight-sheet normalized workbook from the fictional data. PDF text and rendered-page inspection confirmed PHQ-9 and GAD-7 content, complete fictional notes, distinct Therapy and Physical Therapy events, item-9 context, safety text, readable charts/tables, and no clipping or overlap. Workbook checks confirmed 28 assessment rows, 224 item-response rows, 14 note rows, two treatment-event rows, 16 current-profile rows, valid Len/questionnaire metadata, no merged cells, and no formula-error markers. These generated files are validation evidence only and are not distributable release contents.

Microsoft Defender command-line custom scans of the exact ZIP and extracted executable returned no threats. `PHQ9Tracker.exe` is not Authenticode-signed. Defender results are point-in-time evidence, not a guarantee of safety or future reputation behavior.

The public asset was independently downloaded again on September 13, 2026 and matched the recorded 43,804,004-byte size and SHA-256 exactly; the detailed timestamp, source URL, and result are in the [release record](docs/releases/v0.4.0-alpha.1.md). Publication does not add validation that was not performed: a separate owner-performed hands-on exact-hash GUI walkthrough is not recorded for this artifact, separate-machine validation was not performed, and installer compilation and validation remain outside this portable-only release. Public announcement or broader promotion remains a separate owner decision.

Iteration 007.2 passed 40 automated tests using isolated synthetic databases. A normalized workbook passed worksheet, relationship, no-merge, full-text, ISO-date, and same-day-event checks. A four-page synthetic clinician report was structurally checked, rendered to PNG, and visually inspected with complete long-form notes.

Iteration 008 passes 41 automated tests using isolated synthetic databases. The focused tests confirm the four-action Review workflow, removal of the Clinician Report tab and legacy combined exporter, fresh full-history report bounds, and PDF-only report generation. Source compilation also passes. A four-page fictional full-history PDF passed text extraction and page-by-page rendered inspection with all required sections, all six long-form fictional notes, the correct date range, and no companion CSV. Interactive source-GUI and packaged-release validation remain separate gates.

Iteration 008.1 passes all 50 automated tests in the dependency-complete project environment using isolated fictional databases. Focused tests cover exact chart callout content and hit targets, recent/older/absent item 9 cases, guarded date auto-loading, and extracted historical-item-9 PDF wording. The full suite also exercises PDF generation and the normalized seven-sheet workbook, and source/test compilation passes. Daniel completed the source-GUI walkthrough on August 30, 2026; packaged-release validation remains a separate gate.

Iteration 008.2 passes all 59 automated tests in the dependency-complete environment using isolated fictional databases. Focused coverage verifies PHQ-9/GAD-7 item counts, complete and incomplete coverage, established 0-3 thresholds, PDF/workbook presence, same-day Therapy/Physical Therapy fidelity, the common output folder, portable containment, collision-safe names, optional-open behavior, open-folder behavior, graceful failures, the fifth Review action, and compact Spinbox padding. Source and test compilation pass. A representative fictional PDF/workbook pair was generated together under `reports`; text, structure, relationships, treatment-event types, 16 profile rows, and absence of companion CSV files were checked. Daniel completed and passed the seven-part source-GUI walkthrough on August 30, 2026.

### Closed Alpha 1 candidate - 0.3.0-alpha.1

The previously validated candidate is `PHQ9Tracker-Portable-0.3.0-alpha.1.zip` (43,654,431 bytes; 1,836 entries; SHA-256 `76DE3678AF9BF5C61CC0C0A318347E0F5E1C7F471A6112FE9431DA9A304F4C47`). It was packaged on August 31, 2026 from an uncommitted but validated worktree based on commit `4f4afa7eb2046b882325b8ada6df4690d9d4a854`; it must not be represented as a commit containing Iterations 008.1/008.2 or the Alpha documentation. It is retired from public redistribution because it lacks the project GPL and required third-party notices.

The first PyInstaller attempt exposed a real release defect: automatic Tcl/Tk discovery excluded Tk. The build now validates and explicitly bundles the Python runtime's Tkinter package, Tcl/Tk libraries, and a portable runtime hook. The rebuilt candidate's ZIP contains no database or generated user output. A clean extraction created a blank database in the portable folder before GUI initialization; automated portable-routing coverage also passes. The exact packaged executable completed fictional GUI persistence, Review/chart/keyboard, guarded-date, unsaved-change, History/manage, PDF, workbook, collision-safe output, and output-content checks in a normal desktop launch. The desktop control path could not invoke the batch launcher directly, so that full GUI pass used installed-mode LocalAppData while portable containment was verified separately. This is a locally validated candidate, not distribution authorization.

The five-page packaged PDF passed text extraction and page-by-page visual inspection, including the 16-item current profile and distinct Therapy/Physical Therapy labels. The packaged workbook contained all eight expected sheets, 16 profile records, correct distinct events, complete fictional text, readable rendered sheets, and no formula-error markers. No companion CSV was created.

On August 31, Daniel independently checked the actual ZIP on his Windows development workstation. The previously reported `%LOCALAPPDATA%\PHQ9Tracker` validation folder was already absent. He manually extracted the archive, launched `PHQ9Tracker.exe` directly, and launched `Launch Portable Mental Health Tracker.bat`; both launch paths succeeded with a blank database. This owner validation is separate from the earlier Work desktop-control installed-mode pass. It verifies the extracted candidate and both launcher paths on the development workstation, not on a separate clean machine.

Later that day, Daniel transferred the exact candidate ZIP to a volunteer's separate Windows computer. The volunteer received and extracted it there, launched and used the packaged application, and reported through Daniel that all behavior exercised worked. No Python, Tkinter, or other development runtime was installed or prepared. This closes the identified separate-Windows extraction-and-launch gate to the extent observed, while not claiming a pristine VM or fresh Windows image, specific security-prompt behavior, or exact persistence/output subtests. It is separate from both earlier validation paths.

The formal Closed Alpha distribution gates are historical and superseded. The rewritten public history is now at `156cf2e331cdf9224275ca6de9a286dbad012f19`, and Daniel selected GPLv3. Public repository and binary-release gates still require a notice-complete exact ZIP that passes current GUI launch validation, final privacy/status audits, review and commit of the pending changes, accurate unsigned-binary warnings, and Daniel's separate authorization for each visibility or distribution action.

### Iteration 009 notice-complete packaging attempt

On September 7, 2026, the exact retired ZIP was verified and repackaged without changing `PHQ9Tracker.exe` (executable SHA-256 `0C8D26741BF00DC53E3533F6E8580993BB2B52A20E968FD1134F2ED22D91CE74`). The resulting `PHQ9Tracker-Portable-0.3.0-alpha.1-redistribution.1.zip` was 43,790,609 bytes with 1,916 entries and SHA-256 `CC1EDC4E9F2A0977C13E931308B7DC3C7B32FD4C2345A6D6221AA75F9B690249`. Its root GPL and all 35 repository notice/index files matched byte-for-byte, and it contained no database, report, workbook, CSV, log, screenshot, or validation data.

Two separate packaged command-line processes read a persistent fictional database containing 14 PHQ-9 records, 14 GAD-7 records, two notes, and three treatment events, then generated two PDFs and two eight-sheet workbooks without overwriting the earlier outputs. The five-page PDF passed extraction and page-by-page rendered inspection. The workbook passed relationship, no-merge, filter/freeze, content, formula-error, and eight-sheet rendered inspection.

The required GUI launch did not pass. A clean extraction created the expected blank portable database, but both the batch launcher and the unchanged historical executable terminated with `_tkinter.TclError: Can't find a usable init.tcl`. The active Python 3.14.5 installation also failed its own Tcl initialization, and a fresh Python 3.14 package build reproduced the same error; that build was rejected. Because a current exact-artifact launch is mandatory, the notice-complete ZIP is a rejected validation artifact, not a redistribution-ready candidate. Its folder and ZIP were moved out of `release/` into ignored validation work so they cannot be mistaken for publishable output. No separate-machine evidence applies to its hash, and no commit, upload, tag, release, or distribution is authorized from this result.

### Iteration 009 Tcl/Tk repair candidate

On September 8, 2026, the failure was reproduced in both Python 3.14.5 and an isolated official CPython 3.12.10/Tcl/Tk 8.6.15 environment. All required Tcl/Tk files existed and matched the intended versions. Direct Tcl diagnostics showed that path normalization under the sandboxed Windows profile dropped or doubled path components; the same libraries initialized successfully when addressed through Windows extended paths. The packaging runtime hook and new pre-import entry point now establish those paths explicitly. Application source and behavior were not changed.

The full pinned rebuild produced `PHQ9Tracker-Portable-0.3.0-alpha.1-redistribution.2.zip` (43,745,615 bytes; 1,910 entries; 96,483,945 uncompressed bytes; SHA-256 `5A43D176103FCEDBA1FBD36F01C78FDD88237FB27F369C859A9B37C8F497D1DA`). Its executable SHA-256 is `D914BDB42E89093959467717A427F6238AD5B99629A635E0E1BE31EDC44E2E59`. The exact ZIP passed integrity, privacy, GPL/notice, normal/short extraction, direct/batch startup-liveness, portable blank-database, fictional persistence, repeated PDF/workbook, collision, rendered-output, reset/relaunch, compilation, and all 61 automated tests.

Daniel subsequently completed the required hands-on GUI walkthrough against that exact `.2` ZIP on his development workstation. He reported successful fresh extraction and batch launch; fictional PHQ-9/GAD-7 entry with a note and treatment event; close/reopen persistence; normal Review/chart and exercised keyboard/date behavior; sensible unsaved-change handling; two collision-safe GUI PDF generations; two collision-safe GUI Analysis Workbook generations; Open Reports Folder opening the correct folder; and in-app delete/reset followed by close/reopen confirmation that the data was gone and the application relaunched normally. He observed no Windows Defender or SmartScreen prompt. This record does not add detail beyond Daniel's report and is not separate-machine validation of the `.2` hash. The artifact remains quarantined, and no upload, tag, release, distribution, or visibility change is authorized without Daniel's separate approval.

On August 15, 2026, PyInstaller 6.22.1 successfully created the folder-based application, `release\PHQ9Tracker-Portable-0.2.0\`, and `release\PHQ9Tracker-Portable-0.2.0.zip`. Inspection before first launch confirmed that neither the portable folder nor the ZIP contained `.sqlite`, `.db`, or `.sqlite3` files. The first packaged launch created `phq9_tracker.sqlite` inside the portable folder as designed. Review, History / Manage Entries, Treatment Events, Clinician Report, and How Scoring Works opened cleanly with no prior data.

Synthetic entries persisted across a full close and reopen. The packaged clinician PDF generated successfully and passed manual review. The packaged Analysis Workbook generated successfully and passed structural/data-integrity inspection: all seven expected worksheets were present, relationships and calculations reconciled, narrative and event text was complete, and no merged cells were present. Deleting the portable database and relaunching recreated a pristine blank state. The portable ZIP is therefore validated for the Florida use case.

PyInstaller embedded the intended application icon, but the running window/taskbar representation still showed the generic Tk feather. This is a deferred cosmetic packaging issue rather than a portable-release blocker. Inno Setup remains unavailable, so installer compilation, installed-mode behavior, shortcuts, and installer icon presentation are still pending validation.
