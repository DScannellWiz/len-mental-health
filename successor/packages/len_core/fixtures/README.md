# Daily conformance fixture contract

`len.daily-conformance/1` is this iteration's test envelope, not a persisted user-data schema or product version. Fictional inputs only. It is a new daily slice; the Iteration 016 archive remains unchanged.

Top level: `schema`, `fictional: true`, unique `cases`. Each case has a stable `id`, independent `rationale`, `input` and `expected`. Input contains `origin` (`builtin` or `custom`), questionnaire `id`, and ordered keyed `answers`. An answer contains a string `item` and optional `value`. Absent or null value means unanswered; absent required item is also missing. A malformed envelope/identity representation fails the test harness explicitly. Supplied scalar type/range failures become domain invalid errors. Unknown/duplicate/foreign string item IDs reach domain validation, including unanswered unknown items.

Expected output is exactly one test-boundary tag:

- `{"kind":"complete","total":<integer>}`.
- `{"kind":"incomplete","missing":[<canonical IDs>]}`. No total key.
- `{"kind":"invalid","errors":[{"code":<typed code name>,"item":<string or null>}]}`. No total key.

These JSON tags serialize typed results for cross-language comparison. They are not public Dart status strings. Expected outputs are never passed into the evaluator or computed by it. Detailed code names/order document the implementation of the owner-approved contract; review them before making them a durable external protocol.

Eight legacy daily case IDs retain their historical inputs and independently specified arithmetic/missingness. Seven complete cases preserve their totals. `daily-unanswered-distinct` now explicitly expects the approved incomplete variant; the oracle still records its raw rejection. Other cases add mixed severity, reordering, custom/unknown identities, omitted/null fields, invalid-plus-missing precedence, duplicate/foreign/extra IDs and hostile scalar types. This does not extend the prior twenty-case claim into unimplemented custom scoring, period analysis or safety behavior.

Pinned reference: `ea9802b91eee001c6c0e22103f3e13446103bb9e`, `src/phq9_tracker/app.py`, SHA-256 `4181c26a10288ef749cd88621a922507338512235462ce8a3022dd1f11778e9a`. The verifier does not edit either reference or original fixture archive.

## Historical identity guard

`daily-severity-0123` is PHQ-9 with `[0,1,2,3,0,0,0,0,0]`, total 6. `daily-unanswered-distinct` has PHQ item 1 unanswered and the other eight explicitly zero; its approved typed result is incomplete with `phq9.item1` missing and no total. The newer GAD vector and PHQ item 9 unanswered variants remain under `daily-gad-severity-0123` and `daily-phq-item9-unanswered`. All 36 IDs are unique.

[historical_daily.json](historical_daily.json) is an exact eight-case extraction from the independently verified Iteration 016 archive, not from current fixtures. It preserves original rationales and raw expected results. Archive SHA-256: `c59d0f32ab5d4198007b8b873de96752c8f9dec473c8117a6dc563fd039efe36`. Its canonical-JSON SHA-256 is pinned in [fixture_identity.py](../tool/fixture_identity.py): `11897d95bebfaff01c6af96394066e3f3b1ec7bd2f4192745bea71d3ffa45875`. Canonicalization ignores checkout line endings and key order while retaining numeric types and array order. The guard verifies presence, uniqueness, input and expected-output identity before conformance execution. The only outcome conversion is the documented historical-to-typed projection. Updating either baseline or pin requires historical-source review; never generate them from `daily.json`.
