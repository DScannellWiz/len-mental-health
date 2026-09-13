# Security Policy

## Supported Version

| Version | Supported | Status |
| --- | --- | --- |
| `0.4.0-alpha.1` | Yes | Current public prerelease |
| `0.3.0-alpha.1` | No | Frozen historical release |

The public `0.4.0-alpha.1` portable artifact was built from commit `c98c258c60f672f99a769a58a260de92484a4515`; the later release/tag commit is `b9b4aaaa3c8339183c32ca7dda7c18ea83150ec8`. The artifact is not code-signed, has not received a formal third-party security audit or separate-machine validation, and should not be treated as a clinically validated or regulated product. A separate owner-performed hands-on exact-hash GUI walkthrough is not recorded for this artifact and is not claimed.

## Reporting a Software Security Issue

Report a suspected software security issue privately to `projectmentalhealthtracker@gmail.com` before opening a public issue when disclosure could put users or their data at risk.

Include only:

- the application version and Windows version;
- a concise description of the suspected software vulnerability;
- reproduction steps using project-created fictional data;
- the exact non-health error, antivirus, Defender, or SmartScreen message;
- the affected filename and the official release source.

Do not attach or send a tracker database, generated PDF, spreadsheet, export, log containing entered data, assessment response, score, journal entry, treatment or clinician information, credential, or screenshot containing health or other private information. Redact usernames and identifying file paths. If a minimal proof of concept is necessary, create it with new fictional data that does not describe a real person.

The project address is not continuously monitored and is not an emergency, crisis, clinical, or medical-support channel.

## Windows Security Warnings

Allow Windows Security and other antivirus products to perform normal scanning. Do not disable protection, suppress an actual threat detection, or override a warning you do not understand. Because the current public prerelease is unsigned and unfamiliar, Windows may display reputation or publisher warnings. Report the exact warning text and release source so it can be distinguished from an actual detection.

## Data Protection Limitations

The application keeps data local by design, but its SQLite database, generated reports, workbooks, and backups are not encrypted by the application. Security also depends on the Windows account, device, storage media, backup destination, and any sharing action the user chooses. Local-first design is not a guarantee of confidentiality or security.
