"""Guard historical case identities using an archive-derived, pinned baseline."""
import hashlib
import json
from pathlib import Path

BASELINE = Path(__file__).resolve().parents[1] / 'fixtures/historical_daily.json'
# Canonical JSON hash, independent of checkout line endings. Never regenerate
# this baseline/pin from daily.json; changes require historical-source review.
BASELINE_SHA256 = '11897d95bebfaff01c6af96394066e3f3b1ec7bd2f4192745bea71d3ffa45875'


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def check_historical_identities(cases, baseline_path=BASELINE):
    baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
    digest = hashlib.sha256(canonical(baseline).encode('utf-8')).hexdigest()
    if digest != BASELINE_SHA256:
        raise RuntimeError('Historical baseline identity mismatch')
    actual = {case['id']: case for case in cases}
    if len(actual) != len(cases):
        raise RuntimeError('Duplicate fixture IDs')
    for historical in baseline['cases']:
        case_id = historical['id']
        questionnaire = {'phq': 'phq9', 'gad': 'gad7'}[historical['input']['definition']]
        values = historical['input']['responses']
        original_input = {
            'origin': 'builtin', 'id': questionnaire,
            'answers': [
                {'item': f'{questionnaire}.item{i + 1}', 'value': value}
                for i, value in enumerate(values)
            ],
        }
        raw_expected = historical['expected']
        if raw_expected['status'] == 'ok':
            expected = {'kind': 'complete', 'total': raw_expected['total']}
        elif raw_expected['status'] == 'unanswered':
            # Explicit owner-approved projection, not Python rejection coercion.
            expected = {'kind': 'incomplete', 'missing': [
                f'{questionnaire}.item{i + 1}'
                for i, value in enumerate(values) if value is None
            ]}
        else:
            raise RuntimeError('Unsupported historical result projection')
        case = actual.get(case_id)
        if case is None or canonical(case['input']) != canonical(original_input) or canonical(case['expected']) != canonical(expected):
            raise RuntimeError(f'Historical fixture changed: {case_id}')
    return len(baseline['cases'])
