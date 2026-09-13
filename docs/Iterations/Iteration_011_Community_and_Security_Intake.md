Current as of: 2026-09-13

# Iteration 011 - Community and Security Intake

## Objectives

- Give public contributors a maintainable Windows development and validation workflow.
- Route ordinary software support, suspected vulnerabilities, and conduct concerns to distinct channels.
- Prevent public issue forms from soliciting health, identity, credential, or generated Len data.
- Establish clear participation and pull-request expectations without changing Len's application behavior.

## Design Decisions

- GitHub private vulnerability reporting is the preferred security channel; the public project email remains a fallback.
- Blank issues are disabled so contributors encounter the privacy and medical-boundary warnings before submitting a public report.
- Bug reports require fictional-data reproduction or confirmation that the defect occurs before data entry.
- Feature requests ask about general data and compatibility effects without requesting a personal use case.
- Discussions remain disabled because an open-ended forum would require an approved moderation model for likely health or clinical disclosures.
- The code of conduct uses project-specific, plain-language expectations rather than importing a broader governance framework that the sole maintainer may not be prepared to administer.
- This iteration adds no application feature, dependency, schema change, migration, packaging change, or release artifact.

## Files Added

- `CONTRIBUTING.md`
- `SUPPORT.md`
- `CODE_OF_CONDUCT.md`
- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/feature_request.yml`
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/pull_request_template.md`
- `docs/Iterations/Iteration_011_Community_and_Security_Intake.md`

## Files Modified

- `README.md`
- `SECURITY.md`
- `ROADMAP.md`
- `DEVELOPMENT_JOURNAL.md`

## Validation Performed

- GitHub private vulnerability reporting was enabled in the live public repository after explicit owner confirmation; GitHub displayed `Repository settings saved` and changed the control to `Disable private vulnerability reporting`.
- All 68 automated tests passed with the dependency-complete bundled Python 3.12 runtime.
- Source, test, and packaging compilation passed.
- Repository-specific structural checks passed for both issue forms and the issue-template configuration.
- Twenty-three local Markdown links across the changed and added documentation resolved successfully.
- The tracked/unignored file inventory contained no database, report, workbook, export, log, screenshot, executable, or release-archive artifact.
- `git diff --check` passed; Git emitted only informational LF-to-CRLF working-copy warnings.
- An initial run with the unprovisioned system Python 3.14 environment produced one environment-dependent error and six dependency skips because the reporting dependencies and usable Tcl/Tk runtime were absent. No application source was changed; the complete rerun used the dependency-complete Python 3.12 validation runtime and passed 68 of 68 tests.

## Privacy and Security Impact

The repository now warns contributors before public issue submission and routes suspected vulnerabilities to a private GitHub channel. The guidance consistently rejects real assessment data, databases, generated outputs, logs containing entered data, credentials, identifying paths, and other private information. These repository controls reduce accidental solicitation but cannot prevent a person from disregarding the warnings.

## Migration

No user-data or developer migration is required. These files affect repository participation only.

## Remaining Work

- Verify the rendered GitHub issue-form chooser and private-reporting route after publication.
- Add a Windows continuous-integration workflow in a separate approved iteration.
- Define moderation capacity before enabling GitHub Discussions.
