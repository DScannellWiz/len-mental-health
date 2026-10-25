# Dependency-security checkpoint — 2026-10-24

**Ready for Dan/Bob review.** The three isolated dependency updates pass local compatibility and Windows packaging checks. This is not publication approval or validation of the existing public executable.

- Root: `C:/Users/Acer/.codex/.chatgpt-projects/g-p-6ab95345f1b081919030f9d68b48dba4/work/security-dependabot-20261024`
- Branch: `security/dependabot-20261024`
- Base: `16de8212f76b7dd9dba65e9dd6fadd656c75b512`; changes remain uncommitted.

## Reachability and design decision

A harmless generated workbook with fictional data and an ordinary 8×8 PNG confirms:

`Len import → OpenPyXL read_chartsheet → find_images → Image(BytesIO) → real Pillow Image.open`.

The chart-sheet case calls the parser once; an ordinary worksheet-image control calls it zero times. Both save the same fictional date, total 9 and note correctly. The same two characterization tests pass before and after updates. The fixture adds a normal DrawingML picture during serialization because OpenPyXL has no chart-sheet add_image convenience method; application loading is unchanged.

This proves header-parser reachability, not native memory corruption, code execution, full decoding, multiframe iteration or TIFF encoding. No exploit payload was created or executed. [XBM](https://github.com/python-pillow/Pillow/security/advisories/GHSA-xgh8-jp6q-p5x8) and [GIF](https://github.com/python-pillow/Pillow/security/advisories/GHSA-74r2-7ff9-mjj2) advisories demonstrate why image opening itself matters.

Use upstream dependency fixes at the shared parser boundary. Do not change accepted inputs or application behavior.

## Updates and advisory coverage

| Package | Old → candidate | Prior public affected-version records covered |
| --- | --- | --- |
| Pillow | 12.3.0 → 13.0.0 | 41 |
| pypdf | 6.16.1 → 6.21.2 | 19 |
| setuptools | 84.0.0 → 84.1.0 | 1 |

Official wheels exist and support Python 3.12. Installer wheel hashes match PyPI metadata. Before/after inventories show only these three version changes, no new packages, and no unrelated upgrades. Optional extras were not requested; `pip check` passes.

A deterministic comparison excludes the candidates from all 61 prior advisory ranges. Fresh public GitHub advisory queries return zero records for the candidates, including both Pillow spellings. This is not an authenticated repository alert inventory: the earlier alert API returned 401, so current alert numbers/count/state remain unresolved. Nothing was dismissed.

OpenJPEG still reports 2.5.4, but [Pillow 13's Windows recipe](https://github.com/python-pillow/Pillow/blob/13.0.0/winbuild/build_prepare.py) carries the patch for [GHSA-78g4-xqwv-q3g8](https://github.com/python-pillow/Pillow/security/advisories/GHSA-78g4-xqwv-q3g8). That is official-wheel/build-recipe evidence; no disassembly or hostile decoder execution was performed.

## Validation

| Check | Result |
| --- | --- |
| Baseline focused import/report/packaging checks | 10 passed |
| Candidate focused checks | 10 passed |
| Reporting/output/portable subsystem | 35 passed |
| Full unittest suite | 120 passed, zero skipped |
| Existing pytest-style runtime-hook functions | 2 additional checks passed using standard-library patching |
| Compilation and dependency consistency | Passed |
| Full license preflight | 34 notice files, 11 package versions passed |
| Windows PyInstaller build and bundle hygiene | Passed |
| Representative source PDF | Seven pages; required text and every rendered page inspected |
| Packaged CLI | Help, harmless import, PDF generation and XLSX export passed |
| Packaged output content | Fictional saved row, six-page PDF and ten-sheet workbook verified |

Initial full-suite failure was a missing unchanged launcher in the disposable copy (119/120 passed). Restoring that staging file and checking its import path produced the final full pass. New probe development also corrected a test SQL column and PDF line-wrap assertion. These were harness corrections, not application fixes. The PDF renderer emitted two font-configuration warnings; all seven page images rendered and were inspected.

## Packaging and notices

Assessment artifact, retained in the isolated root's ignored `release/`:
`Len-Portable-security-assessment-20261024.zip`

- ZIP: **43,865,163 bytes**; SHA-256 `3C5F42A116BC9126CA881F2045740C8404DFBC12CE6993DFC235EEC32C955411`.
- Executable: **10,146,938 bytes**; SHA-256 `0A1A5E0CD714C7184338F76815C0B0E99E282CF6ACE07FDF4EAD01F4A0174885`.
- Python 3.12.10, Tcl/Tk 8.6.15, PyInstaller 6.22.1, hooks 2026.7 unchanged.
- Archive inspection: 1,043 Python modules, including 80 PIL, 176 OpenPyXL and 97 ReportLab; zero pypdf/setuptools/pkg_resources/olefile modules and no Ghostscript-named binaries.
- Six bundled PIL native modules match installed wheel bytes. Format handlers remain bundled; their presence alone does not prove exploitable input flow.
- ZIP integrity, all exact license hashes, executable identity and absence of databases/reports/workbooks/logs passed.

This filename is an assessment label, not a new application version. The build predates final source-document reconciliation, so its embedded README lacks the final checkpoint paragraph. Application, packaging-code, dependency and notice inputs were unchanged afterward. Preserve this exact identity; future rebuilds need their own validation.

The complete Pillow 13 wheel license inventory replaces the old notice. SHA-256:
`988FFE8AB3480B0F4E9A0AB2702BFFD73D9FB6B47198043FB3BA101A62FAC236`.
The new notice retains its upstream CRLF bytes; a single-path `.gitattributes` rule prevents Git normalization. The notices README's stale 12.2.0 row is corrected. pypdf/setuptools runtime notices are unnecessary for this inspected bundle because their code is absent.

Process-local TEMP/TMP to a dedicated writable assessment directory resolved temporary-file permissions. Existing `core.autocrlf=true` checkout conversion initially broke license hashes. Canonical Git-blob bytes were verified and restored for 34 existing files only in the disposable build copy. The verifier, Git settings and unrelated source notices were unchanged. Direct verification of the source checkout's untouched CRLF notices still fails; use byte-preserving build staging, such as `git -c core.autocrlf=false archive HEAD` output. No Windows security controls were weakened.

## Exact file inventory

Modified:
- `packaging/requirements-release.txt`
- `packaging/third_party_notice_manifest.json`
- `THIRD_PARTY_NOTICES/README.md`
- `README.md`
- `ROADMAP.md`
- `BugList.md`
- `BUILD_AND_RELEASE.md`

Added:
- `.gitattributes` (exact-byte rule for the new Pillow notice only)
- `THIRD_PARTY_NOTICES/Pillow-13.0.0/licenses/LICENSE`
- `tests/test_dependency_security_reachability.py`
- `docs/Iterations/security_dependency_20261024_checkpoint.md`

Deleted:
- `THIRD_PARTY_NOTICES/Pillow-12.3.0/licenses/LICENSE`

Application source, clinical scoring, persistence, network behavior and Iteration 018 remain untouched. Its before/after status lists matched. Tests used only new fictional data. A fresh read-only investigation and one fresh patch review found no concrete regression.

## Residual risk and next gate

Parser reachability remains intentional. Critical exploit prerequisites are not proven in Len. FPX needs olefile, absent here; Ghostscript may exist on an end user's machine even though this bundle omits it. Updated pypdf and setuptools still matter to test/build environments.

Published v0.5.0-alpha.1 is unchanged and was not re-inspected here. This assessment cannot repair that executable or close its risk. Authenticated alert reconciliation, hosted CI, full packaged GUI/portable persistence acceptance, separate-machine testing, malware scanning and signing/trust remain separate gates.

**Stop for Dan/Bob review.** No staging, commit, push, PR, merge, release or GitHub administration occurred. No product-policy change is proposed in this patch.

Retained managed evidence under `artifacts/phase2/` includes raw metadata/advisory queries, exact wheel/package inventories, test/license/build logs, bundle inventory, harmless fixtures, fictional outputs/rendered pages, a detailed remediation record, `source-changes.patch` and SHA-256 file inventory.

Synchronize only the reviewed source patch into a clean canonical checkout at the recorded base; never copy environments, generated artifacts or user-data folders:

```powershell
git -C <canonical-repository> status --short
git -C <canonical-repository> rev-parse HEAD
git -c core.autocrlf=false -C <canonical-repository> apply --check <source-changes.patch>
git -c core.autocrlf=false -C <canonical-repository> apply <source-changes.patch>
git -C <canonical-repository> diff --check
git -C <canonical-repository> status --short
```

Stop on base/cleanliness/patch mismatch; preserve unrelated work. Suggested eventual commit after explicit approval: `Update release dependencies for October 2026 security advisories`.

Lesson: read-only workbook access is not a universal parser boundary; library version strings may omit vendor security backports. Source, dependency, runtime and exact-release evidence have distinct limits.
