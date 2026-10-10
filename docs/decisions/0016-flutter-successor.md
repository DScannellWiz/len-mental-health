# ADR: Flutter for Len's Windows-first successor

Status: **ACCEPTED by Dan, project owner, October 10, 2026**. This records his explicit architecture decision and acceptance of the sequencing below. It does **not** authorize successor implementation. The filename is a local documentation identifier; canonical repository preservation/numbering is not performed here.

## Context

Len remains one privacy-first product/repository. Python/Tkinter is the supported alpha/reference. Five fictional isolated proof areas report PASS WITH RESOLVABLE RISKS: Windows feasibility, conformance, owned SQLite worker/recovery, reusable accessibility and local reporting. The reporting CR defect is resolved with independent/native validation, not model normalization. See [decision review](../Iterations/016_architecture_decision_review.md) for evidence and risk IDs.

## Accepted decision

Dan selects Flutter presentation plus a pure-Dart application/domain core as Len's **Windows-first successor architecture**. Use typed ports, one owned serialized SQLite worker, transactional receipts/revisions, validated generation promotion through a control catalog, immutable report contracts and replaceable local output/platform adapters. Centralize accessibility. Do not require Python at runtime, a browser frontend, local HTTP server, account, cloud, telemetry or remote rendering. Python/Tkinter remains the **supported alpha/reference implementation** through transition.

Use the reviewed modular boundaries; introduce packages incrementally rather than copying all experiments into production. Experimental SQLite/report/SDK pins require separate production dependency review. Retain GPLv3 project licensing basis; no relicensing or library adoption follows automatically.

Hard requirements: severity 0–3 and daily sums; recorded-day analytics excluding missing days; separate 14-day presence mapping 0→0, 1–6→1, 7–11→2, 12–14→3 with coverage; appropriate built-in Item 9 exclusivity; no invented custom clinical interpretation; offline operation and no mandatory external processing; source-preserving migration and no only-copy mutation; no arbitrary UI SQL/filesystem/shell access; no weakened OS security. Module/isolate boundaries do not claim OS containment.

## Alternatives and rationale

Continue Python/Tkinter as supported product regardless of this decision. Keeping Python as a mandatory successor sidecar is not proposed: extra runtime/IPC/mobile burdens are not needed by the demonstrated pure-Dart design. Tauri 2 remains a credible fallback; no equivalent Tauri proof is available here, so do not claim comparative performance or accessibility superiority. Flutter's selection is justified by demonstrated Len-specific reusable fit, not popularity or sunk proof effort. Reopen selection if mandatory quality/privacy/correctness requires unsustainable workarounds or no viable adapter remains.

## Consequences and gates

Positive: one portable product core, one semantic source for reports, no required remote runtime, centralized accessibility and independently testable adapters. Costs: maintained Windows settings bridge, a Dart reimplementation guarded by conformance, native SQLite supply-chain/IO responsibility, strict report encoding/reader policy and dependency maintenance.

No observed architecture blocker remains. Conditional B1/B2 triggers in the review reopen selection. P1–P10 gate production features: semantic/safety parity, actual migration, IO recovery, untrusted-file defenses, complex accessibility, complete reports/OOXML fidelity, private storage/residue and integration/scale. R1–R5 gate release/distribution and each additional platform: signing/trust, legal/provenance/reproducibility, security/network evidence, independent Windows acceptance and platform-specific validation. Deferred enhancements cannot relax a hard requirement.

Dan explicitly accepts the change from earlier preselection sequencing: **signing and clean-machine trust remain mandatory release gates**; **additional platforms require native validation before support commitments**. These checks remain unpassed. Their sequencing has changed; their mandatory status has not. The architecture is accepted without certifying a releasable successor or any additional platform.

PDF tagging/Unicode, encrypted-storage/key-recovery policy, legacy source-format range, performance budgets and distribution form require decisions before their relevant features. No claim of PDF/UA, complete safety parity, arbitrary import security, power-loss durability or mobile readiness is made.

## Implementation and transition

This decision selects direction only; authorize Iteration 017 implementation separately after reviewing the [bounded implementation plan](../Iterations/017_daily_severity_core_plan.md). The planned first capability is an SDK-only daily-severity core/calculation service with independent conformance and no UI/storage/export. No implementation begins under this ADR-finalization task.

Python remains supported until complete approved parity, safe source-preserving migrations, opt-in pilot acceptance, usable accessible releases, recovery/export continuity, trusted distribution and a communicated support/retention policy. No shared database or dual-write contract. Retain source/oracle/release history and pre-cutover copies; later successor writes are not automatically readable/reverse-synced into Python. Retirement requires a separate Dan decision.

## Decision record

Owner outcome: **APPROVED by Dan**. Approval date: **2026-10-10**, supplied directly in this conversation. Accepted scope: Flutter as Windows-first successor; Python/Tkinter remains supported alpha/reference; mandatory signing/clean-machine release gates; native validation before additional-platform support commitments.

Successor implementation: **not authorized**. Python retirement: **not authorized**. Production dependency selection, migration, release/distribution, canonical synchronization and Git/public-state operations: **not authorized here**. Documentation and planning only; stop for Dan and Bob's review of Iteration 017.

## Subsequent bounded implementation authorization

Dan separately authorized Iteration 017 on 2026-10-10, limited to the daily core and fictional conformance. This does not expand the architecture decision into UI/storage/safety/release or retirement authorization. See the [017 checkpoint](../Iterations/017_implementation_checkpoint.md). No Git/public-state action is authorized by this note.
