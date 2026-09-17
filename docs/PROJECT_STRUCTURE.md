Current as of: 2026-09-17
Last substantive update: 2026-09-17

# Project Structure

```text
src/phq9_tracker/     Application source code
data/                 Private local SQLite databases
exports/              Retired output location; retained as ignored legacy scaffolding
reports/              Generated clinician PDFs and normalized XLSX workbooks
docs/                 Documentation
packaging/            Build and installer scripts
tests/                Tests that use fake temporary data
sample_data/          Fake/sample data only
```

Real user data should stay out of GitHub. The repository keeps placeholder files so the intended folders are visible without committing private contents.

The active SQLite database remains one file. Iteration 014 adds the migration ledger, immutable questionnaire-definition snapshots, and normalized versioned submissions/responses inside that file while retaining the existing compatibility tables. Application source, questionnaire definitions, and migration statements remain under `src/phq9_tracker/`; private database content remains under the appropriate runtime data location.

The `reports/` directory is the one active generated-output location for clinician PDFs and normalized Analysis Workbooks. The `exports/` directory remains ignored as legacy scaffolding, but the application no longer writes new workbooks there.
