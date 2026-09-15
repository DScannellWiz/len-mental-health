Current as of: 2026-09-14

# Iteration 013 - Dependency Security Remediation

## Operational Checkpoint

- Current gate: Gate E dependency and CI closeout passed. Gate D passed against the exact candidate on an authorized separate Windows environment, all 23 Dependabot alerts were solved after GitHub's documented manual refresh, and the narrowly scoped final closeout documentation change must merge through the protected-main pull-request path before tagging or release.
- Repository state: remediation commit `a7eeec3bb5c6720bf58eca2163ec050994b98f65` is on remote `main`. Windows CI run `34907622120` completed successfully for that exact commit: Python 3.12 tests passed in 59 seconds and the overall workflow completed in 1 minute 3 seconds.
- Frozen history: public `v0.4.0-alpha.1`, tag `b9b4aaaa3c8339183c32ca7dda7c18ea83150ec8`, and `release/Len-Portable-0.4.0-alpha.1.zip` remain unchanged.
- Versions before remediation: Pillow 12.2.0 and pypdf 6.13.3 in `packaging/requirements-release.txt`.
- Selected and installed versions: Pillow 12.3.0 and pypdf 6.16.1. These are the minimum versions that address all 23 inventoried alerts.
- Files changed: `packaging/requirements-release.txt`; `packaging/third_party_notice_manifest.json`; Pillow notice directory/version and installed license text; this Iteration 013 record; `BUILD_AND_RELEASE.md`; `ROADMAP.md`; and the unpublished `docs/releases/v0.4.1-alpha.1.md` candidate record. A new uncommitted candidate was created at `release/Len-Portable-0.4.1-alpha.1.zip`. No application source, tests, user data, future-planning document, or frozen release file was changed.
- Validation completed: all Gate A-C checks; one controlled Python 3.12.10/PyInstaller 6.22.1 candidate build; exact-ZIP layout, safe-path, privacy/generated-artifact, runtime, launcher, canonical-license, updated Pillow-notice, and pypdf-exclusion checks; Microsoft Defender custom scans of the ZIP and extracted executable; Authenticode inspection (unsigned, as expected for this project); and exact-candidate Gate D validation on an authorized separate Windows environment, including direct and portable startup/storage, two-run fictional-data persistence, PDF/XLSX generation, and rendered-output inspection.
- Candidate provenance: `Len-Portable-0.4.1-alpha.1.zip`; 43,806,172 bytes; SHA-256 `41C9F5DACB1523FE15730FDA21B014825B7D55141D1C754A31C951DF5AE5DE18`; built from uncommitted repository baseline `0532cfc736a373f0b3542da98747e8d077b493f1` plus the recorded Iteration 013 working-tree changes.
- Dependabot closeout: after `a7eeec3` reached `main`, GitHub initially retained stale Pillow 12.2.0 and pypdf 6.13.3 dependency-graph records alongside the new pins and continued to show all 23 alerts. GitHub's support workflow instructed the owner to use **Security > Dependabot alerts > Refresh Dependabot alerts**. The owner performed that manual refresh, after which all 23 alerts were solved without dismissing any alert or changing either pin again. The remediation was correct; GitHub required a manual graph/alert reconciliation. No GitHub Support ticket is required.
- Unresolved work: merge this final closeout documentation update through the normal protected-main pull-request path and allow required status checks to pass; then confirm the merged commit as the tag target, create the `v0.4.1-alpha.1` prerelease, upload only the exact preserved candidate, and independently verify the public asset. Public announcement or broader promotion remains a separate decision.
- Exact next action: create and merge a one-file documentation PR containing only this closeout update. Do not rebuild, sign, rename, substitute, or publish the candidate before that merge and its required checks are complete.

## Objectives

- Account for the 23 Dependabot alerts reported against Pillow 12.2.0 and pypdf 6.13.3.
- Distinguish vulnerable dependency presence from vulnerable code-path reachability in Len.
- Apply the smallest defensible dependency remediation without unrelated updates or feature work.
- Preserve application behavior, local-first privacy, existing data compatibility, licensing evidence, and frozen release history.
- Build and validate a new exact Windows candidate only after source remediation is stable.

## Gate A - Advisory Triage and Reachability

Gate A is complete. GitHub's reviewed advisory severities account for the reported total: Pillow contributes 10 High and 3 Moderate alerts; pypdf contributes 2 High and 8 Moderate alerts.

### Len usage evidence

- Production code imports only `PIL.Image`, `PIL.ImageDraw`, and `PIL.ImageFont` in `src/phq9_tracker/app.py`.
- Len creates fixed-size RGB chart canvases, draws text/shapes with fixed application logic, loads Pillow's built-in default font, and saves internally generated `.png` files for embedding in Len-generated reports.
- Len does not open user-supplied images or PDFs, parse Pillow PDF/GD/EPS/JPEG2000/McIdas/TGA inputs, load BDF/PCF fonts, call `ImageShow`, use `ImageCms`, invoke rank filters, or accept externally controlled crop/paste/filter coordinates.
- pypdf is imported only by three test modules. Those tests use `PdfReader`, page iteration, and `extract_text()` on PDFs generated moments earlier by Len from fictional test data.
- The release preflight imports pypdf to confirm the build environment is complete, but the application does not import it. The audited PyInstaller runtime manifest and prior exact-bundle inspection confirm pypdf is not a distributed runtime component.

### Pillow remediation matrix

All rows affect Pillow 12.2.0 and are fixed by 12.3.0. Because Pillow is a shipped runtime component, every row is relevant to dependency hygiene even where the vulnerable function is not reachable through Len's current UI or report flow.

| Advisory | Severity | Affected range | Vulnerable function | Len reachability classification |
|---|---|---|---|---|
| [GHSA-jjj6-mw9f-p565](https://github.com/advisories/GHSA-jjj6-mw9f-p565) / CVE-2026-59200 | High | `>=5.1.0,<12.3.0` | `PdfParser.PdfStream.decode()` decompression bomb | Probably not reachable: Len never uses Pillow's PDF parser or accepts PDFs as input. |
| [GHSA-4x4j-2g7c-83w6](https://github.com/advisories/GHSA-4x4j-2g7c-83w6) / CVE-2026-55798 | Moderate | `<12.3.0` | `ImageShow.WindowsViewer.get_command()` command injection | Probably not reachable: Len never calls `Image.show()` or `ImageShow`; report paths are application-created temporary PNG paths. |
| [GHSA-pg7v-jwj7-p798](https://github.com/advisories/GHSA-pg7v-jwj7-p798) / CVE-2026-59203 | Moderate | `>=12.0.0,<12.3.0` | EPS `%%BeginBinary` infinite loop | Probably not reachable: Len neither opens nor parses EPS files. |
| [GHSA-vjc4-5qp5-m44j](https://github.com/advisories/GHSA-vjc4-5qp5-m44j) / CVE-2026-59204 | High | `>=8.2.0,<12.3.0` | tiled JPEG2000 decode memory exhaustion | Probably not reachable: Len does not open JPEG2000 or any user-supplied image. |
| [GHSA-62p4-gmf7-7g93](https://github.com/advisories/GHSA-62p4-gmf7-7g93) / CVE-2026-54058 | High | `<12.3.0` | McIdas AREA mmap stride out-of-bounds read | Probably not reachable: Len does not open McIdas images or call `Image.open()`. |
| [GHSA-fj7v-r99m-22gq](https://github.com/advisories/GHSA-fj7v-r99m-22gq) / CVE-2026-59198 | Moderate | `>=5.2.0,<12.3.0` | mode-1 TGA RLE encode heap disclosure | Probably not reachable: Len creates RGB PNGs only and never saves TGA/RLE data. |
| [GHSA-xj96-63gp-2gmr](https://github.com/advisories/GHSA-xj96-63gp-2gmr) / CVE-2026-59197 | High | `<12.3.0` | `ImageFilter.RankFilter` size overflow/out-of-bounds write | Probably not reachable: Len imports no filter module and supplies no filter sizes. |
| [GHSA-6r8x-57c9-28j4](https://github.com/advisories/GHSA-6r8x-57c9-28j4) / CVE-2026-59199 | High | `<12.3.0` | `Image.paste()`, `crop()`, or `alpha_composite()` coordinate overflow | Probably not reachable: Len calls none of these APIs; drawing coordinates are used only with `ImageDraw` on fixed-size canvases. |
| [GHSA-9hw9-ch79-4vh6](https://github.com/advisories/GHSA-9hw9-ch79-4vh6) / CVE-2026-59205 | High | `<12.3.0` | `ImageCmsTransform.apply()` mode mismatch/out-of-bounds write | Probably not reachable: Len imports and uses no color-management API. |
| [GHSA-8v84-f9pq-wr9x](https://github.com/advisories/GHSA-8v84-f9pq-wr9x) / CVE-2026-54059 | High | `<12.3.0` | PCF bitmap decompression-bomb bypass | Probably not reachable: Len uses only `ImageFont.load_default()` and accepts no font files. |
| [GHSA-5x94-69rx-g8h2](https://github.com/advisories/GHSA-5x94-69rx-g8h2) / CVE-2026-54060 | High | `<12.3.0` | `FontFile.compile()` decompression-bomb bypass | Probably not reachable: Len does not load or compile BDF/PCF fonts. |
| [GHSA-45hq-cxwh-f6vc](https://github.com/advisories/GHSA-45hq-cxwh-f6vc) / CVE-2026-55379 | High | `<12.3.0` | BDF glyph decompression-bomb bypass | Probably not reachable: Len accepts no BDF fonts and loads only the built-in default font. |
| [GHSA-phj9-mv4w-65pm](https://github.com/advisories/GHSA-phj9-mv4w-65pm) / CVE-2026-55380 | High | `<12.3.0` | `GdImageFile.open()` decompression-bomb bypass | Probably not reachable: Len neither imports `GdImageFile` nor accepts GD images. |

### pypdf remediation matrix

All rows affect pypdf 6.13.3. None is reachable in the shipped Len application because pypdf is not imported by production code or bundled by PyInstaller. The dependency is nevertheless present in the controlled release/test environment, and several findings affect the exact `PdfReader`/`extract_text()` APIs used by validation tests if those tests were ever pointed at attacker-controlled input.

| Advisory | Severity | Fixed version | Vulnerable function | Len reachability classification |
|---|---|---:|---|---|
| [GHSA-5qjq-93h5-hrgp](https://github.com/advisories/GHSA-5qjq-93h5-hrgp) / CVE-2026-59938 | Moderate | 6.14.0 | oversized declared image dimensions during image loading | Probably not reachable in current tests: they do not extract images and read only Len-generated PDFs. Not present in shipped runtime. |
| [GHSA-55h5-xmcq-c37v](https://github.com/advisories/GHSA-55h5-xmcq-c37v) / CVE-2026-59937 | Moderate | 6.14.0 | repeated malformed cross-reference recovery | Probably not reachable: current tests parse only freshly generated, well-formed Len PDFs. Not present in shipped runtime. |
| [GHSA-5xf7-4p34-54qr](https://github.com/advisories/GHSA-5xf7-4p34-54qr) / CVE-2026-59936 | High | 6.14.1 | unterminated inline-image infinite loop | Probably not reachable: current tests do not consume external PDFs. Not present in shipped runtime. |
| [GHSA-g867-7843-wf8q](https://github.com/advisories/GHSA-g867-7843-wf8q) / CVE-2026-59935 | High | 6.14.2 | unterminated ASCII85/ASCIIHex inline-image infinite loop | Probably not reachable: current tests do not consume external PDFs. Not present in shipped runtime. |
| [GHSA-fc8x-2rww-xw9m](https://github.com/advisories/GHSA-fc8x-2rww-xw9m) / CVE-2026-82398 | Moderate | 6.15.0 | inefficient `read_until_whitespace()` on long non-whitespace input | Probably not reachable with Len-generated PDFs; parser primitive can be used by `PdfReader`, so dependency remediation remains warranted. |
| [GHSA-fwg2-594c-jp42](https://github.com/advisories/GHSA-fwg2-594c-jp42) / CVE-2026-71852 | Moderate | 6.15.0 | excessive CID font width ranges during text extraction | Probably not reachable with Len's standard report fonts; `extract_text()` is used in tests, so the function family is relevant to the test environment. |
| [GHSA-fp3f-mc75-235c](https://github.com/advisories/GHSA-fp3f-mc75-235c) / CVE-2026-71870 | Moderate | 6.15.0 | oversized `/ToUnicode` values during text extraction | Probably not reachable with Len-generated PDFs; `extract_text()` is used in tests, so the function family is relevant to the test environment. |
| [GHSA-jp53-mhqp-8xcg](https://github.com/advisories/GHSA-jp53-mhqp-8xcg) / CVE-2026-84309 | Moderate | 6.16.0 | cycle in `TreeObject.insert_child()` | Probably not reachable: Len tests read rather than modify PDF trees. Not present in shipped runtime. |
| [GHSA-23w6-3w8w-8484](https://github.com/advisories/GHSA-23w6-3w8w-8484) / CVE-2026-84310 | Moderate | 6.16.1 | excessive outline traversal | Probably not reachable: Len-generated reports contain no application-created outline and tests do not access `reader.outline`. Not present in shipped runtime. |
| [GHSA-763m-79hh-57f2](https://github.com/advisories/GHSA-763m-79hh-57f2) / CVE-2026-84311 | Moderate | 6.16.1 | excessive reused XForm traversal during text extraction | Probably not reachable with Len-generated reports, but `extract_text()` is used in tests; dependency remediation is warranted. Not present in shipped runtime. |

### Gate A conclusion

No alert is currently classified as directly reachable from Len's user-facing inputs. That conclusion is bounded to the inspected `0532cfc` source and the existing package composition; it is not a claim that Pillow 12.2.0 or pypdf 6.13.3 is safe in general. Because Pillow is distributed and pypdf is part of the validation environment, version remediation is still required.

## Gate B - Remediation Selection

Gate B is complete. The proposed changes are documented here before implementation:

| Dependency | Existing | Minimum safe for inventoried alerts | Proposed | Rationale |
|---|---:|---:|---:|---|
| Pillow | 12.2.0 | 12.3.0 | 12.3.0 | One targeted patch/minor update fixes all 13 Pillow alerts. Upstream supports Python 3.12 and publishes a CPython 3.12 Windows x86-64 wheel. The MIT-CMU license expression is unchanged. Len does not use the 12.3.0 removal of non-image `ImageCms` modes. |
| pypdf | 6.13.3 | 6.16.1 | 6.16.1 | This is the first version containing all fixes for the 10 inventoried pypdf alerts. It is a pure-Python wheel supporting Python 3.9 and later, retains the BSD-3-Clause license, and documents the same `PdfReader`, page iteration, and `extract_text()` APIs used by Len's tests. |

No other dependency update is proposed. Neither selected release adds a required transitive runtime dependency. The existing PyInstaller version remains unchanged; actual hook/bundle compatibility and the exact Pillow notice inventory remain Gate C/D validation items rather than assumptions.

## Gate C - Implementation and Source Validation

Gate C updated only the two pinned dependencies and the corresponding distributed Pillow license evidence:

- `Pillow==12.2.0` became `Pillow==12.3.0`.
- `pypdf==6.13.3` became `pypdf==6.16.1`.
- The installed Pillow 12.3.0 `LICENSE` replaced the 12.2.0 notice under `THIRD_PARTY_NOTICES`; its exact SHA-256 is `4F7866A74802C6326F81FAFF59A56546B6AEC2B10B91973E0E9308DE95E79857`.
- The notice manifest now identifies Pillow 12.3.0 and that exact license hash. pypdf remains absent from the distributed-runtime notice manifest because it is a test/release-environment dependency and is not bundled in Len.
- No source or test change was necessary: current APIs remained compatible and existing tests already exercise Len's Pillow report generation and pypdf parsing/text extraction of Len-generated PDFs.

Validation performed on Windows with the controlled Python 3.12.10 release environment:

| Validation | Result |
|---|---|
| Installed/imported dependency versions | Passed: Pillow 12.3.0; pypdf 6.16.1 |
| Iteration 007 UX/report tests | Passed: 6 tests |
| Iteration 008.1 accessibility/report tests | Passed: 9 tests |
| Iteration 008.2 clinician-output tests | Passed: 9 tests |
| Iteration 010 questionnaire/report tests | Passed: 6 tests |
| Multi-assessment report tests | Passed: 3 tests |
| Full suite | Passed: 68 tests |
| `compileall` over `src`, `tests`, and `packaging` | Passed |
| `git diff --check` | Passed; Git emitted only its existing LF-to-CRLF working-copy warning for `packaging/requirements-release.txt` |

The release-license verifier passed after the notice refresh: 34 exact notice files and all 11 distributed package versions matched the manifest. Gate C is complete.

## Gate D - Windows Candidate

### Version recommendation

`v0.4.1-alpha.1` is recommended for the candidate. The change is a backward-compatible security-maintenance update to two dependencies, with no application feature, data-schema, or accepted-input change. A patch-level increment from `v0.4.0-alpha.1` communicates that scope while preserving the alpha prerelease designation. This recommendation does not authorize or create a tag or GitHub release.

The candidate was built once with controlled Python 3.12.10 and PyInstaller 6.22.1. Its exact identity is:

- Filename: `Len-Portable-0.4.1-alpha.1.zip`
- Size: 43,806,172 bytes
- SHA-256: `41C9F5DACB1523FE15730FDA21B014825B7D55141D1C754A31C951DF5AE5DE18`
- Source provenance: committed baseline `0532cfc736a373f0b3542da98747e8d077b493f1` plus the uncommitted Iteration 013 dependency, notice, manifest, and iteration-record changes.

Exact-ZIP static validation passed with 1,856 files and 96,687,018 uncompressed bytes. Required Tcl/Tk runtime files, the portable launcher, canonical GPL license, 35 third-party notice entries, and the exact Pillow 12.3.0 notice were present. No unsafe archive paths, root-level generated/private artifacts, Pillow 12.2.0 notice, or pypdf runtime entries were found; Pillow runtime entries were present. Microsoft Defender custom scans reported no threats for both the ZIP and extracted executable. The executable is not Authenticode-signed.

Sandbox Application Control blocked the extracted executable before it launched. Owner-side normal PowerShell then produced the same result: the portable window never appeared, and direct packaged CLI execution was blocked. Windows Code Integrity Operational events 3033 and 3077 identify enforced policy `{0283AC0F-FFF1-49AE-ADA1-8A933130CAD6}` and state that `PHQ9Tracker.exe` did not meet the Enterprise signing-level requirements. Authenticode inspection independently reports `NotSigned`. There is no Mark-of-the-Web alternate data stream on the extracted executable, so removing an Internet-zone marker is not a supported explanation or remedy.

The fictional-data seeding step completed before the owner-side launch attempt: the validation database contains 14 PHQ-9 records, 14 GAD-7 records, 14 fictional notes, and 2 fictional events. Those counts validate only the source-side test fixture, not packaged persistence, because the packaged executable never ran. No PDF or workbook was generated. The later missing-file validation failures are downstream consequences of the blocked executable. PDF rendering also reported that `pypdfium2` is absent from the controlled release environment; that validation-tool dependency can be supplied from the established validation environment if and when an exact packaged PDF exists, without changing the release candidate.

No bypass, policy change, signing operation, alternate-location workaround, or rebuild was attempted on the primary workstation. Direct/portable launch and generated-output validation were incomplete there because the executable never launched; those checks were subsequently completed against the same candidate on an authorized separate Windows environment. The frozen `v0.4.0-alpha.1` ZIP and tag remain unchanged and out of scope.

### Separate-device validation package

Preparation is complete. This outer bundle is a validation aid and is not a release asset:

- Filename: `Len-Portable-0.4.1-alpha.1-Separate-Device-Validation.zip`
- Size: 43,482,519 bytes
- SHA-256: `518DACF4A626D865FD9B5760E1747902A5570BFA237967F7B098400372C23AA5`
- Location: `release/Len-Portable-0.4.1-alpha.1-Separate-Device-Validation.zip`
- Contents: the unchanged candidate ZIP; a PowerShell validation runner; instructions and safety boundaries; a SHA-256 manifest; and a fictional SQLite fixture containing 14 PHQ-9 records, 14 GAD-7 records, 14 fictional notes, and 2 fictional events.
- Fixture SHA-256: `A9747ABC29E94DB918473C5589FACD48B75EF2B910B38A80EBCA365C715828AA`.

The outer bundle contains five safe relative-path entries. Its embedded candidate is still exactly 43,806,172 bytes with SHA-256 `41C9F5DACB1523FE15730FDA21B014825B7D55141D1C754A31C951DF5AE5DE18`. The four-file internal manifest was verified before compression, and the nested candidate hash and size were independently read back from the completed outer ZIP. The validation runner passed a PowerShell syntax-only parse and was not executed on this machine. It explicitly refuses stale results, candidate identity mismatches, security-policy bypasses, and overwrites; it records static, Defender, signature, direct/portable launch, isolated/portable storage, two-run persistence, packaged PDF/XLSX generation, manual rendered-output checks, and final candidate identity.

### Separate-device validation result

Gate D passed on September 14, 2026 in normal, non-administrator Windows PowerShell 5.1 on the authorized separate Windows environment identified in the transcript as `HOID`. The exact candidate matched 43,806,172 bytes and SHA-256 `41C9F5DACB1523FE15730FDA21B014825B7D55141D1C754A31C951DF5AE5DE18` before extraction and again after all validation steps. No candidate rebuild, edit, rename, signing operation, or substitution occurred.

The runner confirmed 1,856 file entries and 96,687,018 uncompressed bytes; all required launcher, license, notice, and Tcl/Tk files were present; no unsafe paths, private/generated root artifacts, Pillow 12.2.0 notice, or pypdf runtime entry was found. Authenticode status remained `NotSigned`. The runner completed its Microsoft Defender checks without a nonzero result.

Direct launch reached a responsive window titled **Len**, created the database only under isolated LocalAppData, and did not create a portable database. The portable launcher then used the exact fictional fixture beside the executable, reached a responsive **Len** window twice, and preserved the fictional PHQ-9/GAD-7 history across the second run. The operator confirmed the expected window, history, and normal behavior at each prompt.

The packaged executable generated both required outputs:

- `Len_Report_2026-08-30_to_2026-09-12.pdf`: 31,664 bytes; SHA-256 `69372561F835F1DB067701FCE83968692C8149F031DC86A94DEAF19EFAEDD891`.
- `Len_Analysis_2026-09-12.xlsx`: 26,584 bytes; SHA-256 `6D683348D87492B2063D3D432D9F013C8A7567AFFC29B7AB427BE6E7BDD91D64`.

The PDF passed its header check and the workbook contained the expected eight sheets. The operator confirmed every PDF page and all workbook sheets were readable, unclipped, and free of visible errors. A separate post-return inspection rendered all five PDF pages and all eight workbook sheets successfully and found no visible clipping, overlap, unreadable content, or formula-error markers.

The results archive is validation evidence and not a release asset: `Len-v0.4.1-alpha.1-Separate-Device-Results.zip`; 48,250 bytes; SHA-256 `6538B9ECA2A2407AED0B40C1D48256B7E3907AEBADB208EFFCA73722EF72BD2B`. Its transcript SHA-256 is `11B4706BED9421B5EFDB02F494C3436522B0FFF62363DD84766EBEBDF4B9B085`. Generated validation outputs, transcripts, and the results archive must not be committed or included in the release ZIP.

Trusted code signing is future release-infrastructure work outside Iteration 013. It is not a remaining task or proposed mutation for this iteration.

## Gate E - GitHub Remediation Closeout and Release Status

The remediation was committed as `a7eeec3bb5c6720bf58eca2163ec050994b98f65` and published to remote `main`. Its `packaging/requirements-release.txt` pins Pillow exactly to 12.3.0 and pypdf exactly to 6.16.1. Pillow 12.3.0 is outside every inventoried Pillow affected range, all of which end before 12.3.0. pypdf 6.16.1 contains the fixes through the highest inventoried fixed version, 6.16.1. No dependency pin changed after this remediation commit.

Windows CI run `34907622120` targeted exact head SHA `a7eeec3bb5c6720bf58eca2163ec050994b98f65` and completed successfully. Its Python 3.12 test step passed in 59 seconds, and the full workflow completed in 1 minute 3 seconds.

Immediately after the push and successful CI run, GitHub's dependency graph showed stale superseded records for Pillow 12.2.0 and pypdf 6.13.3 alongside Pillow 12.3.0 and pypdf 6.16.1, and Dependabot continued to report all 23 alerts as open. This was not evidence that the patched manifest still selected the vulnerable versions: the local and remote `packaging/requirements-release.txt` files had already matched byte-for-byte at `a7eeec3`.

GitHub's support workflow instructed the owner to run **Security > Dependabot alerts > Refresh Dependabot alerts**. The owner performed that documented manual refresh. GitHub then reconciled the stale dependency-graph and alert records, and all 23 remediation alerts were solved. No alerts were manually dismissed, no dependency pins were changed again, and no GitHub Support ticket is required. The corrected diagnosis is that the dependency remediation was valid and GitHub required the manual refresh/rebuild to reconcile stale superseded records.

Gate E is complete for dependency remediation, CI, and Dependabot alert resolution. Release publication is not complete at this checkpoint. This final documentation update must first merge through the protected-main pull-request path with required checks green. Only the resulting approved merged commit may become the `v0.4.1-alpha.1` tag target. The prerelease must then contain only the unchanged `Len-Portable-0.4.1-alpha.1.zip` candidate (43,806,172 bytes; SHA-256 `41C9F5DACB1523FE15730FDA21B014825B7D55141D1C754A31C951DF5AE5DE18`), followed by an independent public-download verification. The executable remains unsigned, and trusted signing remains outside Iteration 013.

## Privacy and Security Impact

The remediation changes public third-party code used for report generation and validation. It does not change Len's storage locations, database schema, assessment data, report contents, network behavior, or local-first privacy model. Testing must use only repository-created fictional data. The dependency updates reduce risk from known malformed image/PDF inputs without expanding Len's accepted-input surface.

## Migration

No database or user-data migration is expected. Existing Len data must still be opened and preserved during packaged validation.

## Remaining Work

- Create a branch for this one-file closeout update, review its exact diff, and open a pull request without staging the two future-planning documents or any candidate, validation bundle, generated output, transcript, results archive, database, report, export, log, screenshot, secret, or other generated/private artifact.
- Merge the closeout pull request only after required CI/status checks pass, then verify the resulting merged `main` commit before creating tag `v0.4.1-alpha.1`.
- Create the GitHub release as a prerelease and upload only the exact existing `Len-Portable-0.4.1-alpha.1.zip`; do not rebuild or substitute it.
- Independently download the published asset and verify its filename, 43,806,172-byte size, and SHA-256 `41C9F5DACB1523FE15730FDA21B014825B7D55141D1C754A31C951DF5AE5DE18` before declaring release completion.
- Treat public promotion as a separate owner-authorized milestone.
- Treat trusted code signing as future release-infrastructure work outside Iteration 013.
- Do not modify, replace, retag, or otherwise change `v0.4.0-alpha.1`.
