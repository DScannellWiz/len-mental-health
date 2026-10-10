# Iteration 017 compact checkpoint

2026-10-10. **VERIFICATION REMEDIATION COMPLETE LOCALLY — STOP for Dan and Bob.** Both review P2 findings are resolved; Dart CI configuration added. Hosted CI has not run. No commit, push, PR, merge, release or Iteration 018 authorization.

Checkout: `work/iteration017-source/`. Branch: `feature/iteration-017-daily-severity-core`. HEAD/base: `ea9802b91eee001c6c0e22103f3e13446103bb9e`. No new commit; nothing staged. No current remote-main verification is claimed by this pass.

The pure-Dart daily core is unchanged: immutable typed complete/incomplete/invalid results; strict integer 0–3 severity; invalid precedence; no partial total, coercion or zero fill; custom/foreign identity rejection. No UI, storage, analytics, safety workflow or Python product change.

Historical archive verified unchanged: SHA-256 `c59d0f32ab5d4198007b8b873de96752c8f9dec473c8117a6dc563fd039efe36`. Restored `daily-severity-0123` to PHQ-9 and `daily-unanswered-distinct` to PHQ item 1 missing. New variants retained as `daily-gad-severity-0123` and `daily-phq-item9-unanswered`. An archive-derived eight-case baseline is pinned independently; no baseline generated from current fixtures. Historical raw outcomes are preserved, with explicit approved typed incomplete projection.

Architecture checks use explicit failures and a fixed seven-check completion gate. Six deliberate forbidden-import/dependency controls fail with the intended diagnostic and no success summary under ordinary Python, `-O` and `PYTHONOPTIMIZE=1`.

Current verification: **8/8 verification regression tests; 12/12 core and 6/6 boundary Dart tests; 36/36 conformance cases (11 complete, 6 incomplete, 19 invalid); 8/8 historical identities; 4/4 comparator controls; 7/7 architecture checks under ordinary and optimized Python**. GAD 16,384 vectors and PHQ 36 contributions pass. Offline resolution has zero packages; analyzer with fatal infos clean; five Dart files format-clean.

CI: separate Windows Dart job, pinned SDK 3.13.5/actions, full oracle history and all nine validation commands. Existing Python job/triggers/permissions/concurrency unchanged. YAML and targeted structural checks pass. GitHub-hosted execution/owner required-check policy remain pending; no settings touched.

Current fixture SHA-256: `da014dd29388bf7b24a767e2bbb8b0903a0f384338c8d4a313a01703396c4588`. Baseline canonical SHA-256: `11897d95bebfaff01c6af96394066e3f3b1ec7bd2f4192745bea71d3ffa45875`. Python oracle source SHA-256 unchanged: `4181c26a10288ef749cd88621a922507338512235462ce8a3022dd1f11778e9a`. Toolchain: Dart 3.13.5 / Python 3.12.

This pass changes 11 existing files and adds 3; no deletions. Total pending iteration: 5 modified tracked files and 23 new files. Original domain/Dart tests, Python source/tests and prior unrelated modifications preserved. See [full evidence and inventory](017_implementation_evidence.md), [package verification commands](../../successor/packages/len_core/README.md) and [fixture contract](../../successor/packages/len_core/fixtures/README.md).

Ready for bounded Dan/Bob review, with hosted CI pending. No source synchronization over the dirty canonical checkout. Suggested eventual commit: `Add pure-Dart daily core with guarded conformance and CI`. Any Git/transfer action requires separate approval. Python remains supported; future safety, migration, accessibility and release-trust gates remain mandatory.
