# Security Policy

## Supported Version

| Version | Supported | Status |
| --- | --- | --- |
| `0.5.0-alpha.1` | Yes | Current public prerelease |
| `0.4.1-alpha.1` | No | Frozen historical prerelease |
| `0.4.0-alpha.1` | No | Frozen historical prerelease |
| `0.3.0-alpha.1` | No | Frozen historical release |

Only the latest published alpha is supported. When a newer alpha is published, earlier prereleases remain downloadable as frozen historical records but are not maintained as supported current versions.

The public `0.5.0-alpha.1` portable artifact is 43,700,470 bytes with SHA-256 `F5B4DD956481294BD136345F5C6F02D708943A37851DD80B191A1A987CC0717D`; its tag targets `1fe8af87fe2fb22e73de474a70708f25119e491a`. The artifact is not code-signed and has not received a formal third-party security audit. It passed exact-candidate validation, including the owner's hands-on UI review, but should not be treated as a clinically validated or regulated product.

## Reporting a Software Security Issue

Report a suspected software security issue through [GitHub private vulnerability reporting](https://github.com/DScannellWiz/len-mental-health/security/advisories/new). Do not open a public issue when disclosure could put users or their data at risk.

If GitHub private vulnerability reporting is unavailable, use `projectmentalhealthtracker@gmail.com` as a fallback and include only the minimum non-health information needed to understand the suspected vulnerability.

Include only:

- the application version and Windows version;
- a concise description of the suspected software vulnerability;
- reproduction steps using project-created fictional data;
- the exact non-health error, antivirus, Defender, or SmartScreen message;
- the affected filename and the official release source.

Do not attach or send a tracker database, generated PDF, spreadsheet, export, log containing entered data, assessment response, score, journal entry, treatment or clinician information, credential, or screenshot containing health or other private information. Redact usernames and identifying file paths. If a minimal proof of concept is necessary, create it with new fictional data that does not describe a real person.

Neither private vulnerability reporting nor the project address is continuously monitored or an emergency, crisis, clinical, or medical-support channel.

## Windows Security Warnings

Allow Windows Security and other antivirus products to perform normal scanning. Do not disable protection, suppress an actual threat detection, or override a warning you do not understand. Because the current public prerelease is unsigned and unfamiliar, Windows may display reputation or publisher warnings. Report the exact warning text and release source so it can be distinguished from an actual detection.

## Data Protection Limitations

The application keeps data local by design, but its SQLite database, generated reports, workbooks, and backups are not encrypted by the application. Security also depends on the Windows account, device, storage media, backup destination, and any sharing action the user chooses. Local-first design is not a guarantee of confidentiality or security.
