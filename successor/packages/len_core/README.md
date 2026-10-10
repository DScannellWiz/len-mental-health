# Len daily-severity domain core

Iteration 017, owner-authorized 2026-10-10. SDK-only domain component, not a usable successor application. Python/Tkinter remains supported. GPL-3.0 license: the repository's [LICENSE](../../../LICENSE). No external runtime or development dependencies; Python stdlib/Git are oracle tooling only. Not published to a package registry.

## Interface and invariants

`QuestionnaireIdentity` preserves builtin/custom origin. `BuiltinCatalog` owns immutable PHQ-9/GAD-7 definitions and canonical item identities; all catalog items are required. Neither labels, position nor a custom claim to `phq9` can resolve a trusted built-in definition. No questionnaire wording, clinical interpretation or safety action is included.

`SeverityValue.fromInt` validates 0â€“3. `ResponseValue.fromRaw` snapshots scalar admission: null is unanswered, actual integers 0â€“3 are severity, everything else becomes a typed invalid value. It never retains mutable rejected payloads, parses strings, converts floats/booleans, clamps or supplies zero. Adapters must preserve absent/null input rather than normalize invalid values.

`ItemResponse` pairs identity with an immutable response value. `DailySeverityRequest` copies the caller's keyed response collection. `DailySeverityService.evaluate` is synchronous and pure:

- `CompleteDailySeverity`: every required answer valid; canonical immutable responses and integer total (PHQ 0â€“27, GAD 0â€“21).
- `IncompleteDailySeverity`: missing required answers, including omitted entries; canonical immutable missing IDs, no total member.
- `InvalidDailySeverity`: explicit immutable typed errors, no total member. Invalid supplied values, duplicate/unknown/foreign IDs or unsupported questionnaire admission override incompleteness.

Results form a sealed family and have no public constructors. Consumers use exhaustive Dart pattern matching. Arithmetic occurs only after validation and completeness succeed. Errors follow input order (membership, duplicate, then value); missing/complete responses follow catalog order. Errors contain codes and item IDs, not raw supplied values. Item IDs are untrusted at admission: downstream adapters must not log them indiscriminately.

Item 9 contributes severity normally; this package does not implement or certify safety prompts, events or timing. Custom identities are rejected, never given clinical interpretation. Validation is not permission to persist partial check-ins. Collections and fields are immutable, not an OS security boundary.

## Tests and conformance

Tests are executable Dart programs with explicit throwing assertions, not a `package:test` suite. This avoids third-party dev dependencies; **`dart test` is not the entry point**. Any failure exits nonzero. No VM `--enable-asserts` requirement.

With the existing Dart SDK (verified 3.13.5), from this package directory:

```powershell
# Replace only this path with the existing SDK location; install nothing.
$dartPath = 'C:\path\to\dart-sdk\bin\dart.exe'
& $dartPath --suppress-analytics pub get --offline
& $dartPath test/core_test.dart
& $dartPath test/boundary_test.dart
python -B tool/verification_test.py
python -B tool/verify.py $dartPath
python -B tool/architecture_checks.py $dartPath
python -B -O tool/architecture_checks.py $dartPath
& $dartPath --suppress-analytics analyze --fatal-infos
& $dartPath --suppress-analytics format --output=none --set-exit-if-changed lib test tool/conformance.dart
```

The Dart CLI's analytics flag is used for CLI commands. Direct script execution uses the VM; passing that CLI flag directly to the VM is invalid. Offline pub resolves zero packages and does not download dependencies. Do not install missing routine prerequisites automatically.

The fictional [fixtures](fixtures/daily.json) have handwritten expected outcomes, separate from both engines. [Fixture contract](fixtures/README.md). The conformance tool reads only input when invoking the core. Python verification reads exact committed source via Git, checks its SHA-256, extracts an explicit allowlist in memory and executes no original module imports/startup/GUI/DB functions. No real database is accessed or source snapshot generated.

Complete inputs compare fixture expectations, independently computed Python admission/sums, unchanged pinned Python totals and Dart output. Incomplete inputs preserve raw Python rejection separately from Dan's approved typed result. Invalid cases are independently validated and compared with Dart; they do not claim legacy keyed/type parity. Python bool/float permissiveness is explicitly observed, never adopted. Fault controls catch wrong totals, zero-filled missing answers, invalid downgraded to incomplete and JSON boolean/integer confusion.

`lib/` has no imports or dependencies. File/JSON/process operations are confined to `test/`/`tool/`. The tests cover immutable state, strict admission, keyed order, all 16,384 GAD vectors and 36 PHQ single-item contributions. Architecture checks include failed external construction/subclass compilation and remove their temporary source directories in `finally`-equivalent context-manager cleanup. No persisted evidence output or user data is required.

## Deferred boundaries

No Flutter widgets, storage/files, dates, period analytics, presence scoring, rounding, reporting, platform adapter, network, telemetry, interpretation or Item 9 workflow. Missing-day exclusion/coverage and the derived 14-day mapping remain requirements for later implementation, not functionality claimed here. Incomplete persistence, partial period records and date/rounding policies require future decisions.

The minimum SDK constraint records the verified toolchain; older SDK compatibility is not claimed. No new licensing obligations from package dependencies were introduced. Source license inheritance is not a release/legal audit or distribution authorization.

## Verification remediation and CI

The 36 current cases include eight historical identities guarded by a pinned [archive-derived baseline](fixtures/historical_daily.json). The two newer variants have distinct IDs. The baseline retains historical inputs/results; the guard explicitly maps historical unanswered output into the approved incomplete result without a total. Never regenerate this baseline from current fixtures. Regression tests reject identity/input/expectation drift, duplicate IDs and baseline tampering. Architecture enforcement uses explicit failures and a fixed seven-check count; disposable forbidden-import/dependency controls fail under ordinary Python, `-O` and `PYTHONOPTIMIZE` without a success summary.

The repository's [Windows CI](../../../.github/workflows/windows-ci.yml) adds a separate Dart job with pinned Dart 3.13.5, offline dependency resolution, formatting, analysis, both Dart runners, verification controls, conformance and ordinary/optimized architecture checks. Full Git history makes the exact Python oracle commit available. Python CI is unchanged. Workflow configuration is locally validated; a GitHub-hosted run and any owner-controlled required-check policy remain separate gates. No settings changes are needed to propose this workflow file.
