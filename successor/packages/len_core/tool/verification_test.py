"""Regression and deliberate-failure controls for the verification gates."""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from fixture_identity import BASELINE, check_historical_identities

ROOT = Path(__file__).resolve().parents[1]


class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads((ROOT / 'fixtures/daily.json').read_text())['cases']

    def test_preserved_archive_cases(self):
        self.assertEqual(check_historical_identities(self.cases), 8)

    def test_changed_historical_input_rejected(self):
        for case_id in ('daily-severity-0123', 'daily-unanswered-distinct'):
            with self.subTest(case=case_id):
                cases = copy.deepcopy(self.cases)
                case = next(c for c in cases if c['id'] == case_id)
                case['input']['answers'][0]['value'] = 3
                with self.assertRaisesRegex(RuntimeError, 'Historical fixture changed'):
                    check_historical_identities(cases)

    def test_changed_historical_expectation_rejected(self):
        for value in (999, True, 7.0):
            with self.subTest(value=value):
                cases = copy.deepcopy(self.cases)
                cases[0]['expected']['total'] = value
                with self.assertRaisesRegex(RuntimeError, 'Historical fixture changed'):
                    check_historical_identities(cases)

    def test_missing_or_renamed_identity_rejected(self):
        for rename in (False, True):
            with self.subTest(rename=rename):
                cases = copy.deepcopy(self.cases)
                if rename:
                    cases[0]['id'] = 'renamed'
                else:
                    cases.pop(0)
                with self.assertRaisesRegex(RuntimeError, 'Historical fixture changed'):
                    check_historical_identities(cases)

    def test_duplicate_identity_rejected(self):
        self.cases.append(copy.deepcopy(self.cases[0]))
        with self.assertRaisesRegex(RuntimeError, 'Duplicate fixture IDs'):
            check_historical_identities(self.cases)

    def test_baseline_tampering_rejected(self):
        baseline = json.loads(BASELINE.read_text())
        baseline['cases'][0]['expected']['total'] = 999
        with tempfile.TemporaryDirectory(prefix='len-fixture-control-') as folder:
            path = Path(folder) / 'baseline.json'
            path.write_text(json.dumps(baseline))
            with self.assertRaisesRegex(RuntimeError, 'baseline identity mismatch'):
                check_historical_identities(self.cases, path)

    def test_new_variants_retain_distinct_coverage(self):
        cases = {c['id']: c for c in self.cases}
        gad = cases['daily-gad-severity-0123']
        self.assertEqual(gad['input'], {
            'origin': 'builtin', 'id': 'gad7', 'answers': [
                {'item': f'gad7.item{i + 1}', 'value': value}
                for i, value in enumerate([0, 1, 2, 3, 0, 0, 0])
            ],
        })
        self.assertEqual(gad['expected'], {'kind': 'complete', 'total': 6})
        phq = cases['daily-phq-item9-unanswered']
        self.assertEqual(phq['input'], {
            'origin': 'builtin', 'id': 'phq9', 'answers': [
                {'item': f'phq9.item{i + 1}', 'value': value}
                for i, value in enumerate([0] * 8 + [None])
            ],
        })
        self.assertEqual(phq['expected'], {'kind': 'incomplete', 'missing': ['phq9.item9']})

    def test_architecture_failure_in_all_python_modes(self):
        # Mutate a disposable copy only. Failure occurs before invoking Dart.
        # Passing a nonexistent executable ensures this cannot pass by accident
        # due to a later compilation failure instead of the intended invariant.
        for violation, message in (
            ('import', 'Forbidden runtime import'),
            ('dependency', 'External dependencies are forbidden'),
        ):
            with tempfile.TemporaryDirectory(prefix='len-architecture-control-') as folder:
                package = Path(folder)
                for relative in ('tool/architecture_checks.py', 'lib/len_core.dart', 'pubspec.yaml'):
                    target = package / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / relative, target)
                if violation == 'import':
                    target = package / 'lib/len_core.dart'
                    target.write_text("import 'dart:io';\n" + target.read_text())
                else:
                    target = package / 'pubspec.yaml'
                    target.write_text(target.read_text() + '\ndependencies:\n  forbidden: any\n')
                for mode in ('ordinary', '-O', 'PYTHONOPTIMIZE'):
                    with self.subTest(violation=violation, mode=mode):
                        env = os.environ.copy()
                        env.pop('PYTHONOPTIMIZE', None)
                        if mode == 'PYTHONOPTIMIZE':
                            env['PYTHONOPTIMIZE'] = '1'
                        command = [sys.executable, '-B']
                        if mode == '-O':
                            command.append('-O')
                        run = subprocess.run(
                            [*command, str(package / 'tool/architecture_checks.py'), 'not-a-dart-executable'],
                            capture_output=True, text=True, env=env,
                        )
                        self.assertNotEqual(run.returncode, 0)
                        self.assertIn(message, run.stderr)
                        self.assertNotIn('RESULT', run.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
