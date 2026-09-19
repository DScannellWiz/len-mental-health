Current as of: 2026-09-18
Last substantive update: 2026-09-18

# Len

[![Windows CI](https://github.com/DScannellWiz/len-mental-health/actions/workflows/windows-ci.yml/badge.svg?branch=main)](https://github.com/DScannellWiz/len-mental-health/actions/workflows/windows-ci.yml)

Len is a privacy-first, local-first Windows desktop application for recording PHQ-9 and GAD-7 check-ins over time. It combines daily assessment responses with optional notes and treatment events, then creates a readable PDF conversation aid and a normalized XLSX Analysis Workbook.

Canonical repository: [github.com/DScannellWiz/len-mental-health](https://github.com/DScannellWiz/len-mental-health)

The project began as a personal response to the **Tyranny of Temporal Distance**: the difficulty of accurately describing weeks or months of symptoms during a short appointment when the most recent day can overshadow the broader pattern. See [Project Origins](PROJECT_ORIGINS.md) for the motivation and design history.

## Maturity and Availability

The current public prerelease, [`v0.5.0-alpha.1`](https://github.com/DScannellWiz/len-mental-health/releases/tag/v0.5.0-alpha.1), is available for Windows 11 64-bit. It is alpha/pre-release software, not a finished or clinically validated product. Its exact candidate passed the 109-test full source and clean-release suites, exact-archive privacy and licensing checks, Windows Defender scans, direct and portable launch/storage/persistence checks, migration and reset checks, PDF/workbook/CLI validation, rendered-output inspection, and the owner's hands-on exact-candidate UI review. The executable remains unsigned. This evidence does not guarantee that the software will work on every computer or be useful for every person.

The official public binary is [`Len-Portable-0.5.0-alpha.1.zip`](https://github.com/DScannellWiz/len-mental-health/releases/download/v0.5.0-alpha.1/Len-Portable-0.5.0-alpha.1.zip), 43,700,470 bytes, with SHA-256 `F5B4DD956481294BD136345F5C6F02D708943A37851DD80B191A1A987CC0717D`. Only the latest published alpha is supported. `v0.4.1-alpha.1`, `v0.4.0-alpha.1`, `v0.3.0-alpha.1`, and earlier prereleases remain downloadable as frozen historical records; they are not rebuilt, overwritten, relabeled, or maintained as current versions. Do not download executables or ZIP files from reposts or unofficial mirrors.

Known issue in the published `v0.5.0-alpha.1` binary: its Review and PDF score trends split historical definition v1 observations from new v2 observations even though those scores have the same daily-severity meaning. The current source corrects the analytical grouping; a corrected binary has not yet been released. Stored check-ins and their definition versions are preserved.

## Current Features

- A definition-driven Today's Check-In with a compact questionnaire roster, one active form at a time, explicit daily-severity guidance, and `Not present / Mild / Moderate / High` choices for both PHQ-9 and GAD-7.
- Explicit unanswered choices, with one saved submission per questionnaire per calendar date and deliberate same-day saves updating that submission.
- A universal safety message before the first question and in every PDF footer; PHQ-9 item 9 context remains PHQ-9-only.
- Previous Day and Next Day navigation, existing-date loading, future-date prevention, and unsaved-change protection.
- History / Manage Entries tools for editing and confirmed deletion of assessments, notes, and treatment events.
- Clearly labeled Daily Severity Scores and 14-Day Symptom Frequency Scores with recorded-day coverage.
- Review summaries, recent charts, treatment-cycle views, and long-term trends.
- Chart point values available by hover, click, and keyboard.
- A compact full-history PDF designed to support—not replace—a conversation with a licensed clinician.
- Date-range-first PDF and normalized XLSX selection, limited to questionnaires with records in that range, with definition-version-aware trends and current 14-day item-profile records.
- One local `reports` folder for both generated outputs.

## Running from Source

Source use is intended for developers and requires Python 3.12 or later on Windows.

```powershell
python -m pip install -r requirements.txt
& ".\Launch Len.bat"
```

Run those commands from the project root. The launcher adds the repository's `src` folder to Python's import path and uses a project-local `.venv` or `venv` when available.

## Using a Portable Build

To use the official portable ZIP:

1. Allow Windows Security or your antivirus product to scan the downloaded ZIP.
2. Extract the entire ZIP into a normal user-writable folder. Do not run the app from inside the ZIP.
3. Keep all extracted files together.
4. Start it with **Launch Portable Len.bat** whenever you want portable-mode storage.

Starting `PHQ9Tracker.exe` directly does not enable portable mode. A direct EXE launch uses the installed-mode data location under `%LOCALAPPDATA%\PHQ9Tracker` instead of the extracted folder. Switching launch methods can therefore make an existing history appear missing even though it remains in the other location.

## Data, Reports, Backups, and Updates

The application does not include cloud synchronization or an automatic backup service.

| How the app is started | Database | Generated PDF/XLSX files |
| --- | --- | --- |
| Official portable batch launcher | `phq9_tracker.sqlite` beside the launcher | `reports` beside the launcher |
| Packaged EXE started directly, or a future installed build | `%LOCALAPPDATA%\PHQ9Tracker\phq9_tracker.sqlite` | `%LOCALAPPDATA%\PHQ9Tracker\reports` |
| Source launcher | `data\phq9_tracker.sqlite` in the repository | `reports` in the repository |

The SQLite database, PDFs, and workbooks can contain highly sensitive information and are not encrypted by the application. Store backups somewhere you control and protect them like other private health records.

Before replacing or updating the application:

1. Close Len.
2. Identify the storage mode you actually used from the table above.
3. Copy the database and any reports you want to retain to a separate backup location.
4. For a portable update, extract the new release into a new folder rather than overwriting the old folder. Copy the backed-up `phq9_tracker.sqlite` into the new extracted folder before launching it with the portable batch launcher.
5. Confirm that History shows the expected records before deleting the old folder or backup.

Current migrations add immutable questionnaire-definition snapshots and normalized submission/response records while preserving the existing PHQ-9 and reusable assessment tables. They are designed to preserve older PHQ-9/GAD-7 records, but backup and verification are still required. A complete database backup made while Len is closed contains both the legacy compatibility records and the versioned normalized records; restore the whole database file rather than copying individual tables. Reports are separate files, so deleting records from the app or deleting/restoring the database does not automatically delete previously generated reports. In-app record deletion and manual database deletion are permanent without a backup. Deleting the database while the app is closed resets that storage location; the next launch creates a new blank database.

## Privacy and Support Boundary

This app is local-first. It does not intentionally upload assessment responses, notes, treatment events, databases, reports, or workbooks. Local-first design reduces exposure, but it is not a guarantee of privacy or security; the computer, backup location, email client, and any files the user chooses to share remain outside the application's control.

Never submit or email:

- a tracker database;
- a generated PDF, spreadsheet, export, or log containing entered data;
- assessment answers, scores, journal entries, treatment or clinician information;
- screenshots containing health information, names, account details, file paths that identify a person, or other private data.

For software support, provide the application version, Windows version, steps to reproduce the behavior, what you expected, what happened, and the exact non-health error or security-warning text. Screenshots are acceptable only after confirming that they contain no health information or other private data. Reproduce problems with newly created fictional data whenever possible.

Use the [Support Guide](SUPPORT.md) for ordinary software-reporting instructions. Suspected vulnerabilities must be submitted through [GitHub private vulnerability reporting](https://github.com/DScannellWiz/len-mental-health/security/advisories/new), not a public issue. The intentionally public project address, `projectmentalhealthtracker@gmail.com`, remains a best-effort fallback for software and repository administration and is not continuously monitored. Do not send personal health information or generated health-data artifacts to any project channel.

See [Privacy and Data Handling](docs/PRIVACY_AND_DATA_HANDLING.md), the [Security Policy](SECURITY.md), and the [Support Guide](SUPPORT.md) for the full boundaries.

## Windows Security Notice

The current public portable build is not code-signed. Windows Defender, Microsoft SmartScreen, or another security product may scan it or warn that an unfamiliar pre-release application has limited reputation. Allow normal scanning. Do not disable antivirus protection, suppress an actual threat detection, or override a warning you do not understand.

If a warning appears, stop and report the exact product name, warning text, detected file, release filename, and release source without including private health data. Code signing would improve publisher identity and reputation signals, but it is not currently available and is not a substitute for clean build and release practices.

## Medical and Safety Disclaimer

Len is not medical advice, a diagnostic tool, a treatment recommendation, a medical device claim, an emergency service, or crisis support. It is not a substitute for a qualified healthcare professional. Scores, summaries, charts, and reports can be incomplete or misleading when data is missing and must be interpreted in context.

If you may be in immediate danger or need urgent help, contact local emergency services or an appropriate crisis resource. Do not use this repository, its issue tracker, or the project support email for emergency or clinical support.

## Project Documentation

- [Project Origins](PROJECT_ORIGINS.md) explains the human problem that started the project and its intended division of labor.
- [Development Journal](DEVELOPMENT_JOURNAL.md) records the reconstructed prehistory and significant iterations.
- [Product Principles](docs/product-principles.md) defines the stable philosophical core and adaptable implementation layers.
- [Architecture Decision Records](docs/decisions/) document significant product and architectural decisions.
- [Build and Release Notes](BUILD_AND_RELEASE.md) covers developer packaging, validation, and release controls.
- [Contributing Guide](CONTRIBUTING.md) defines the development workflow, validation expectations, and fictional-data-only rule.
- [Support Guide](SUPPORT.md) routes ordinary software questions and protects the project's medical and privacy boundaries.
- [Community Code of Conduct](CODE_OF_CONDUCT.md) defines participation and enforcement expectations.
- [v0.5.0-alpha.1 Release Record and GitHub Release Notes](docs/releases/v0.5.0-alpha.1.md) records the exact current public artifact evidence, publication state, validation boundaries, rejected-candidate history, and post-publication download verification.
- [Historical Closed Alpha Documentation](docs/alpha/README.md) preserves an abandoned private testing plan as provenance. It is not an active enrollment, support, or release workflow.

## License

Copyright © 2026 Daniel Scannell.

Len is licensed under the [GNU General Public License version 3](LICENSE) (`GPL-3.0-only`). Users may use, study, modify, redistribute, and commercially use the software subject to GPLv3's terms, including the source-availability and same-license requirements that apply when covered modified versions are distributed. The license does not prohibit commercial use or add medical-data restrictions.

Windows binary distributions also contain third-party software under compatible licenses. Their required verbatim notices are preserved in [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES/README.md); those notices do not replace or narrow GPLv3.

## AI-Assisted Development

This project is developed with AI-assisted software engineering under the direction of the repository owner. Daniel defines the outcomes the product should achieve and remains the final reviewer for architecture, privacy, clinical framing, and release decisions. The assistant translates those outcomes into implementation, validation, and documentation work. This division of labor is an intentional development method and part of the project's provenance.
