"""Boundary checks and negative public-API compilation tests; no third parties."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    dart = sys.argv[1]
    checks = 0
    files = list((ROOT / 'lib').rglob('*.dart'))
    require(bool(files), 'No domain source files')
    for file in files:
        for uri in re.findall(r"(?:import|export)\s+['\"]([^'\"]+)", file.read_text()):
            require(not uri.startswith(('dart:io','dart:ffi','dart:isolate','package:')), f'Forbidden runtime import: {uri}')
            if not uri.startswith('dart:'):
                require((file.parent / uri).resolve().is_relative_to((ROOT/'lib').resolve()), f'Import leaves domain: {uri}')
    checks += 1
    manifest = (ROOT/'pubspec.yaml').read_text()
    require(not re.search(r'^(?:dependencies|dev_dependencies|dependency_overrides):', manifest, re.M), 'External dependencies are forbidden')
    require('packages: {}' in (ROOT/'pubspec.lock').read_text(), 'Lockfile must contain zero packages')
    checks += 1
    source = '\n'.join(file.read_text() for file in files)
    require('expected' not in source or 'expected = definition.items' in source, 'Unexpected expectation access')
    require(not any(term in source for term in ('jsonDecode','DateTime','calculate_questionnaire_total')), 'Forbidden runtime operation')
    checks += 1
    require(all('total' not in block for block in [
        source.split('final class IncompleteDailySeverity')[1].split('final class InvalidDailySeverity')[0],
        source.split('final class InvalidDailySeverity')[1].split('/// Invalid wins')[0],
    ]), 'Failure result exposes total')
    checks += 1
    fixture = json.loads((ROOT/'fixtures/daily.json').read_text())
    require(fixture['fictional'] is True and len({case['id'] for case in fixture['cases']}) == len(fixture['cases']), 'Fixture provenance or unique IDs invalid')
    checks += 1
    negatives = [
        ("void main() { CompleteDailySeverity(); }", 'CompleteDailySeverity'),
        ("class Fake extends DailySeverityResult {}\nvoid main() {}", 'DailySeverityResult'),
    ]
    for code, diagnostic in negatives:
        with tempfile.TemporaryDirectory(prefix='api-negative-', dir=ROOT/'.dart_tool') as temporary:
            file = Path(temporary)/'negative.dart'
            file.write_text("import '../../lib/len_core.dart';\n"+code)
            run = subprocess.run([dart,str(file)],capture_output=True,text=True)
            require(run.returncode != 0 and diagnostic in run.stderr and "Couldn't resolve" not in run.stderr, f'Negative API compilation check failed: {run.stderr}')
        checks += 1
    require(checks == 7, 'Architecture check count differs from required seven')
    print(f'RESULT {checks}/7 architecture checks passed (including 2 negative API compilation checks)')


if __name__ == '__main__': main()
