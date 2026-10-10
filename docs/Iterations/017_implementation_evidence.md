# Iteration 017 implementation evidence

**Current status: verification remediation complete locally; STOP for Dan and Bob.** The final remediation section below supersedes initial counts, fixture hash, inventory and CI limitations. GitHub-hosted CI has not run.

## Initial implementation record (historical)

2026-10-10. **Implemented and verified; STOP for Dan/Bob review before commit, push or PR.** Dan's attached authorization enabled only the pure-Dart daily core and independent fictional fixtures. No Iteration 018 authorization.

## Identity and isolation

- Repository: `DScannellWiz/len-mental-health`.
- GitHub main verified read-only with `git ls-remote`: `ea9802b91eee001c6c0e22103f3e13446103bb9e`.
- Dedicated local branch: `feature/iteration-017-daily-severity-core`; HEAD remains that same SHA, no new commit.
- Checkout: the current isolated Work project, `work/iteration017-source/`. It is a separate local clone, not a change to either existing developer checkout. Its origin is the local canonical checkout; no remote configuration/public state was changed.
- Canonical checkout was on `fix/single-builtin-severity` at `f87f2508c6f80de420657a71ba03ce1b65b97507`, with unrelated documentation changes. The prior Active Len checkout was at `c98c258c60f672f99a769a58a260de92484a4515`, `main` ahead one local commit. Both remain untouched.
- Finalized plan, accepted ADR, architecture review/checkpoint were reconciled into this repository checkout before implementation. Historical proof files remain external, identified by [provenance](016_evidence_provenance.md).

## Implemented boundary

One package at `successor/packages/len_core/`: immutable definitions, closed built-in catalog identity, strict 0–3 severity values, copied keyed inputs, sealed immutable complete/incomplete/invalid results, structured errors and pure daily calculation. Invalid takes precedence; missing never becomes zero; incomplete/invalid have no total member. Catalog/item origin cannot be acquired by custom identities. Item 9 contributes to the sum with no safety action.

No Flutter, SQLite, files, platform, network, PDF/XLSX, dates, period/presence analytics, interpretation or safety workflows in the runtime. No real user data, production Python changes, original module imports or tool/dependency installation. No external runtime/dev package dependency. Dart 3.13.5 Windows x64; Python 3.12 reference tooling; SDK-only manifest supports `>=3.13.0 <4.0.0`, not a claim of older SDK validation.

## Exact verification

| Final check | Result |
|---|---|
| Core executable tests | 12/12 pass; includes all 16,384 GAD vectors and 36 PHQ single-item contributions |
| Conformance-edge executable tests | 6/6 pass |
| Independent fixture cases | 34/34 pass: 10 complete arithmetic comparisons, 5 approved incomplete cases with raw Python rejection, 19 invalid admission cases |
| Comparator fault controls | 4/4 detect wrong outcomes/type confusion |
| Architecture/API checks | 7/7 pass, including 2 negative external-construction/subclass compilation checks |
| Dart analyzer | No issues found |
| Format verification | 5 files checked, 0 changes required |
| Offline dependency resolution | Success; lockfile `packages: {}`; no downloaded dependency |
| Git diff whitespace | Clean; no staged changes |
| Documentation link verification | 57/57 final links pass, including case-sensitive paths |

Focused tests preceded final whole-package verification. Python repository suite/native Flutter builds/Iteration 016 experiments were not rerun: no interaction requiring them is introduced. Counts describe distinct suites, not a sum of independent test claims. No release/platform/packaging or runtime network trace is claimed.

Reference source: `src/phq9_tracker/app.py` at pinned SHA above, SHA-256 `4181c26a10288ef749cd88621a922507338512235462ce8a3022dd1f11778e9a`. Fixture SHA-256: `e194e73945d9e6fb11918d7f412b8b9dc067f80336dba6f7776ec4df49cae255`.

Raw Python count/None rejection is retained as evidence rather than silently projected into agreement. Approved Dart missing-only outcomes are incomplete. A targeted probe also confirms Python accepts `[True, 1.0, 0, 0, 0, 0, 0]` as total 2; strict Dart rejects both types. This is documented legacy-helper permissiveness, not a reason to change Python or weaken the approved contract. Invalid keyed/admission cases do not claim direct Python parity.

## Failures and limitations

Initial SDK CLI formatting/resolution/analysis failed because the sandbox blocked normal local SDK settings initialization; rerun was separately approved with explicit `--suppress-analytics`, offline resolution and zero dependencies. A CLI-only analytics flag passed to direct VM script execution was rejected; invocation was corrected. Final runs pass. No OS protection was disabled/bypassed; no missing prerequisite was installed. Existing repository access also required approved read-only escalation.

No core test failure or unresolved daily semantic blocker remains. Standalone throwing test programs intentionally avoid a third-party test runner; `dart test` is not supported here. CI integration and package versioning need review before wider use. The fixture tag/error vocabulary is an explicit test boundary, not an approved persisted data format. Unknown item IDs can contain untrusted text: do not put them into unrestricted logs.

Incomplete persistence, partial period records, date/rounding policy, safety workflows, clinical/custom interpretation, integration scale, native accessibility, migration/recovery, release signing/trust and other platforms remain outside this component's acceptance. Python stays supported; no replacement, shared data path or retirement is enabled.

## Changed-file inventory

Modified: `README.md`, `ROADMAP.md`, `BUILD_AND_RELEASE.md` (bounded domain-component/status/verification sections only).

New preserved/planning/evidence documents:

- `docs/decisions/0016-flutter-successor.md`
- `docs/Iterations/016_architecture_decision_review.md`
- `docs/Iterations/016_decision_checkpoint.md`
- `docs/Iterations/016_evidence_provenance.md`
- `docs/Iterations/017_daily_severity_core_plan.md`
- `docs/Iterations/017_implementation_checkpoint.md`
- `docs/Iterations/017_implementation_evidence.md`

New package files under `successor/packages/len_core/`:

- `.gitignore`, `pubspec.yaml`, `pubspec.lock`, `README.md`
- `lib/len_core.dart`
- `fixtures/README.md`, `fixtures/daily.json`
- `test/support.dart`, `test/core_test.dart`, `test/boundary_test.dart`
- `tool/conformance.dart`, `tool/verify.py`, `tool/architecture_checks.py`

No deleted files. SDK package metadata/cache and temporary negative-compilation sources are ignored; no database/report/log/source snapshot is included. Working tree: 3 modified tracked documents, 20 new source/documentation files, nothing staged; HEAD unchanged.

## Review and synchronization boundary

Proposed PR: **Iteration 017: pure-Dart daily-severity core and independent conformance**. Technical acceptance passes for this component; owner API/fixture/documentation review remains required. No signing/release-readiness claim. Suggested eventual commit title: `Add pure-Dart daily severity core with independent conformance`.

Implementation already resides in a dedicated repository feature checkout; there is no need to copy source over the dirty canonical checkout. Review this checkout directly, using `git status --short --untracked-files=all` and `git diff --check`. Any canonical transfer should use a separately approved clean feature checkout based on the verified main SHA, preserving its unrelated changes. Do not run blanket copy/stage commands against the existing canonical tree. Local commit, origin adjustment, push, PR and merge are still unapproved; no synchronization performed. Owner approval must identify the intended Git action.

The approved retirement safeguards remain: Python supported; no user database changed; complete future semantic/safety parity, source-preserving migration/reconciliation/recovery, accessible trusted release and separate owner retirement decision are mandatory before replacement.


## Final verification remediation — 2026-10-10

### Scope and findings resolved

Owner-authorized only: restore historical fixture identities, enforce architecture checks under optimized Python, add bounded Dart CI and update evidence. No scoring, domain API, UI, persistence, analytics, Python product, user data or Iteration 018 changes.

The original historical archive `experiments/iteration_016_conformance_proof/fixtures/core.json` was verified before extraction against SHA-256 `c59d0f32ab5d4198007b8b873de96752c8f9dec473c8117a6dc563fd039efe36`; it remains unchanged. `fixtures/historical_daily.json` contains eight exact original case records, including original rationales and raw expectations, plus provenance. It was extracted from that archive, never from current fixtures. Its canonical-JSON hash is `11897d95bebfaff01c6af96394066e3f3b1ec7bd2f4192745bea71d3ffa45875`, independently pinned in `tool/fixture_identity.py`. JSON canonicalization avoids checkout line-ending drift while retaining scalar types and array order. Changing the baseline/pin requires historical-source review.

- `daily-severity-0123`: restored PHQ-9 `[0,1,2,3,0,0,0,0,0]`, total 6. New GAD equivalent retained as `daily-gad-severity-0123`.
- `daily-unanswered-distinct`: restored PHQ item 1 unanswered, other eight zero. Approved domain projection is incomplete with only `phq9.item1` missing and no total; the historical raw unanswered result remains intact in the baseline. New item 9 variant retained as `daily-phq-item9-unanswered`.
- Conformance now invokes the historical guard before Dart/oracle comparison. Missing/renamed/duplicate identities, changed inputs/expectations (including boolean/float type confusion), and baseline tampering fail deterministic controls.
- All architecture enforcement assertions became explicit conditional failures. Counters advance only after successful checks; success additionally requires the fixed seven-check count. Regression tests use disposable copies to introduce forbidden imports and dependencies, require the intended diagnostic and nonzero exit, and reject a success summary.

### Current verification results

Focused verification controls ran first, followed by package checks. Exact results:

| Check | Current result |
|---|---|
| Verification regression suite | 8/8 unittest methods pass; includes six deliberate architecture failures: two violations in ordinary, `-O`, and `PYTHONOPTIMIZE=1` modes |
| Core Dart tests | 12/12 pass; 16,384 GAD vectors and 36 PHQ single-item contributions |
| Boundary Dart tests | 6/6 pass |
| Historical case identity | 8/8 preserved against independently pinned archive extract |
| Current conformance | 36/36 unique cases pass: 11 complete Python/Dart/expected, 6 incomplete with raw Python rejection, 19 invalid independent admission cases |
| Comparator fault controls | 4/4 pass; comparator checks, not end-to-end engine mutation claims |
| Architecture checks, ordinary Python | 7/7 pass, including two external API negative compilation checks |
| Architecture checks, `python -O` | 7/7 pass, including the same two negative compilation checks |
| Offline dependency resolution | Pass; zero packages in lockfile; no dependency installation |
| Static analysis | Pass with `--fatal-infos`; no issues |
| Dart format check | Five files checked; zero changes |
| Workflow validation | YAML parser and structural checks pass; existing Python job and workflow triggers/permissions/concurrency compare equal to HEAD |

Current `daily.json` raw SHA-256: `da014dd29388bf7b24a767e2bbb8b0903a0f384338c8d4a313a01703396c4588`. Python oracle source hash remains `4181c26a10288ef749cd88621a922507338512235462ce8a3022dd1f11778e9a`, verified by conformance from commit `ea9802b91eee001c6c0e22103f3e13446103bb9e`. Dart 3.13.5 and Python 3.12 remain the tested tools.

The first focused run encountered Windows sandbox denial creating/writing disposable system-temp folders (six methods passed, two errored before their controls could execute). The explicitly approved unsandboxed rerun passed all eight methods. No protection was disabled, dependency installed or product file mutated by failure controls. An initial documentation patch failed before changes; a later documentation write hit an encoding read error and was completed using explicit UTF-8. Neither affected implementation/test results.

### CI configuration and limits

`.github/workflows/windows-ci.yml` adds only `dart-core`, a separate Windows job with a 20-minute timeout and package working directory. Twelve steps comprise checkout, Python setup, Dart setup and nine validation commands. Every external action is pinned to a full SHA; checkout/Python reuse existing pins. Dart setup uses `dart-lang/setup-dart@6afc89df92d6eb3834022f73cd65adc8cdfcb92d`, verified against its public v1 ref and action manifest. Exact SDK 3.13.5 availability was checked against the official archive VERSION endpoint. See [setup-dart documentation](https://github.com/dart-lang/setup-dart) for version input behavior.

Checkout uses `fetch-depth: 0` so conformance can read the pinned historical Python commit on a fresh runner. Separate steps enforce offline resolution, formatting, analysis, core/boundary tests, verification regression controls, independent conformance and normal/optimized architecture checks. No continue-on-error, conditional skip, secret, write permission or new repository setting is introduced. The existing Python job is unchanged.

Workflow parsing used the already available Dart YAML parser; targeted structural checks verified all 12 steps, exact nine commands, full action pins, SDK/history requirements and unchanged existing workflow policy. No actionlint/schema tool was installed. This is local YAML/structural validation plus successful local execution of the configured checks, not a GitHub-hosted run or complete runner simulation. Hosted CI remains pending an authorized commit/push/PR. If organization action allowlists or required-check configuration need changes, stop for owner action; none was inspected or modified here.

### File inventory for this remediation pass

Modified relative to the reviewed checkout:

- `.github/workflows/windows-ci.yml`
- `BUILD_AND_RELEASE.md`, `BugList.md`
- `docs/Iterations/017_implementation_checkpoint.md`, `docs/Iterations/017_implementation_evidence.md`
- `successor/packages/len_core/.gitignore`, `successor/packages/len_core/README.md`
- `successor/packages/len_core/fixtures/README.md`, `successor/packages/len_core/fixtures/daily.json`
- `successor/packages/len_core/tool/architecture_checks.py`, `successor/packages/len_core/tool/verify.py`

Added:

- `successor/packages/len_core/fixtures/historical_daily.json`
- `successor/packages/len_core/tool/fixture_identity.py`
- `successor/packages/len_core/tool/verification_test.py`

Final hygiene: tracked diff and all changed/new text files have no whitespace errors; 19 local documentation links resolve. Hash comparison against the pre-remediation inventory confirms exactly the 11 modifications and three additions above, with no other existing file changed. The historical archive hash and all eight extracted case records were rechecked successfully.

No deletions. Package Python bytecode caches are now ignored. Earlier root README/ROADMAP modifications and decision/planning documents are preserved. The domain source and existing Dart tests are unchanged. No generated reports, user data, toolchains or external proof archives are added to the repository.

### Review, synchronization and stop

Both P2 findings are remediated locally. The bounded Dart CI job is ready for review; hosted CI acceptance is still pending. No successor release claim. The updated implementation remains at `work/iteration017-source/`, branch `feature/iteration-017-daily-severity-core`, HEAD `ea9802b91eee001c6c0e22103f3e13446103bb9e`. Nothing staged, committed, pushed, merged or opened as a PR; no remote/admin state changed.

Review commands: `git status --short --untracked-files=all` and `git diff --check` from that isolated checkout; explicitly inspect untracked package files as well. No copy into the dirty canonical repository is needed or authorized. Preserve the isolated checkout for the later owner-approved protected-branch workflow; any source transfer must target a separately approved clean checkout, never blanket-copy over unrelated modifications. Suggested eventual commit title: `Add pure-Dart daily core with guarded conformance and CI`. Stop for Dan and Bob; no further implementation authorized.
