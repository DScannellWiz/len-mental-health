Current as of: 2026-09-17
Last substantive update: 2026-09-17

# Privacy and Data Handling

Len is designed for local use. It does not intentionally upload PHQ-9 or GAD-7 responses, notes, treatment events, databases, reports, or workbooks. Local-first behavior reduces routine external exposure, but it is not a guarantee of privacy or security.

## Sensitive Local Files

The application does not encrypt its SQLite database, generated PDFs, generated workbooks, or backups. The database includes immutable questionnaire-definition snapshots plus versioned normalized submissions/responses alongside compatibility records; all of those records are part of the same sensitive file. Anyone or any software with access to these files may be able to read sensitive content.

Storage depends on how the application is started:

| Mode | Database | Reports |
| --- | --- | --- |
| Portable batch launcher | `phq9_tracker.sqlite` in the extracted application folder | `reports` in the extracted application folder |
| Packaged EXE launched directly or future installed build | `%LOCALAPPDATA%\PHQ9Tracker\phq9_tracker.sqlite` | `%LOCALAPPDATA%\PHQ9Tracker\reports` |
| Source launcher | `data\phq9_tracker.sqlite` in the repository | `reports` in the repository |

Starting the packaged EXE directly does not activate portable mode. Users who alternate between the EXE and **Launch Portable Len.bat** can create two separate databases and may mistakenly believe data was lost.

## Backup, Update, and Deletion

Close the application before copying or replacing a database. Back up the entire database and any reports that must be retained before an update, reset, or deletion; do not copy or restore individual SQLite tables. Backups are sensitive files too and should be stored only in a location the user controls.

For a portable update, extract the new version into a new folder. Copy the backed-up database into that folder before using the portable batch launcher, confirm that expected records appear, and retain the old folder or backup until verification is complete. Do not overwrite the only working portable folder in place.

Deleting an assessment, note, or treatment event in the application is permanent without a backup. Deleting `phq9_tracker.sqlite` while the app is closed resets that storage location; the next launch creates a blank database. Generated reports are independent files and are not automatically removed when database records are deleted.

Len's questionnaire framework does not send definitions or responses to an external service. Only clearly redistributable instruments may be included as built-ins. Future custom instruments may explicitly select user-defined deterministic scoring through an allowlisted application-owned strategy, but Len will not automatically generate clinical interpretation, severity bands, risk flags, diagnosis, or treatment narrative for them.

## Repository Boundary

Private runtime data belongs in:

- `data/` for source-run SQLite databases;
- `reports/` for source-run clinician PDFs and normalized XLSX Analysis Workbooks;
- the extracted portable folder for portable-mode databases and reports;
- `%LOCALAPPDATA%\PHQ9Tracker` for packaged direct-EXE and installed-mode data.

Do not commit real user databases, spreadsheets, reports, exports, screenshots, logs, PHI, PII, credentials, private support correspondence, or identifying issue details. Sample data may be committed only under `sample_data/`, must be project-created, and must be clearly fictional.

Portable release archives must not contain a user database or generated private artifact. Release validation must use project-created fictional data and confirm that the distributable ZIP itself remains blank.

## Public Support Boundary

The project accepts software and repository feedback only. Users must not submit assessment responses, scores, journal entries, treatment or clinician information, generated reports, Analysis Workbooks, databases, exports, logs containing entered data, or screenshots containing health or private information.

Useful reports include:

- the application version and Windows version;
- steps to reproduce the software behavior;
- expected and actual behavior;
- the exact error or Windows security-warning text;
- a screenshot only when it has been checked to contain no health information, identity details, account information, or identifying file paths.

Problems should be reproduced with newly created fictional data whenever possible. If prohibited health or private information is received, do not use or analyze it; delete it as soon as reasonably practicable and request only the minimum non-health troubleshooting details.

`projectmentalhealthtracker@gmail.com` is the intentionally public project support address. It is for software and repository administration only. It is not continuously monitored and must not receive databases, reports, workbooks, screenshots with entered data, personal health information, requests for medical interpretation, or crisis messages.

## Historical Closed Alpha Materials

The abandoned Closed Alpha plan is retained under `docs/alpha/` as project provenance. Its tester-ID, acknowledgment, private Form, and cohort workflow is superseded and is not an active release or support process. The strict health-data firewall developed for that plan remains useful and is carried forward in the public support rules above.

## Medical and Emergency Boundary

The application, repository, issue tracker, and support address are not monitoring, diagnostic, treatment, crisis, or emergency services. Users should not rely on them as the sole record of important health information or as a substitute for professional care.

Future Travel Mode and LAN-sharing concepts do not weaken the local-first boundary. Travel import must be validated and append-only against an authoritative home database; LAN clients must use an authoritative local host or service rather than opening SQLite directly over a network share.
