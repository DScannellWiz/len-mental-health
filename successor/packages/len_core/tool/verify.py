"""Independent fixture/oracle comparison; stdlib only, fictional inputs only."""
import ast
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from types import MappingProxyType, ModuleType

from fixture_identity import check_historical_identities

PACKAGE = Path(__file__).resolve().parents[1]
REPOSITORY = PACKAGE.parents[2]
REVISION = 'ea9802b91eee001c6c0e22103f3e13446103bb9e'
SOURCE_HASH = '4181c26a10288ef749cd88621a922507338512235462ce8a3022dd1f11778e9a'
SYMBOLS = frozenset('''
PHQ9_ITEM_LABELS GAD7_ITEM_LABELS DEFINITION_ID_PATTERN INTERPRETATION_POLICIES
DEFINITION_ORIGINS QUESTIONNAIRE_BEHAVIORS QUESTION_BEHAVIORS ResponseOption
QuestionDefinition ScoringStrategyDescriptor ProfileStrategyDescriptor
SCORING_STRATEGY_DESCRIPTORS PROFILE_STRATEGY_DESCRIPTORS SCORING_RULES PROFILE_RULES
QuestionnaireDefinition _validate_identifier validate_questionnaire_definition
LEGACY_FREQUENCY_RESPONSE_OPTIONS DAILY_SEVERITY_RESPONSE_OPTIONS
DAILY_SEVERITY_INSTRUCTION _builtin_questions PHQ_SCREENER_SOURCE_URL
_builtin_definition LEGACY_BUILTIN_DEFINITIONS ASSESSMENTS
resolve_scoring_strategy calculate_questionnaire_total
'''.split())


def load_oracle():
    content = subprocess.check_output(['git', '-C', str(REPOSITORY), 'show',
        f'{REVISION}:src/phq9_tracker/app.py'])
    if hashlib.sha256(content).hexdigest() != SOURCE_HASH:
        raise RuntimeError('Pinned source identity differs; stop for review.')
    tree = ast.parse(content.decode('utf-8'))
    selected = []
    for node in tree.body:
        name = getattr(node, 'name', None)
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            name = getattr(node.targets[0], 'id', None)
        if name in SYMBOLS:
            selected.append(node)
    if len(selected) != len(SYMBOLS):
        raise RuntimeError('Oracle allowlist drift')
    module = ModuleType('len_daily_pinned_oracle')
    sys.modules[module.__name__] = module
    module.__dict__.update(dataclass=dataclass, MappingProxyType=MappingProxyType,
        re=re, math=math, json=json, datetime=datetime, timedelta=timedelta)
    future = ast.ImportFrom(module='__future__', names=[ast.alias(name='annotations')], level=0)
    compiled = ast.fix_missing_locations(ast.Module(body=[future, *selected], type_ignores=[]))
    exec(compile(compiled, 'pinned_daily_oracle', 'exec'), module.__dict__)
    return module


def classify(input):
    """Independently apply owner contract, never read fixture expectations."""
    if input['origin'] != 'builtin' or input['id'] not in ('phq9', 'gad7'):
        return {'kind': 'invalid', 'errors': [{'code':'unsupportedQuestionnaire','item':None}]}
    count = 9 if input['id'] == 'phq9' else 7
    ids = [f"{input['id']}.item{i}" for i in range(1, count+1)]
    seen, values, errors = set(), {}, []
    for answer in input['answers']:
        item, value = answer['item'], answer.get('value')
        if item not in ids: errors.append({'code':'unknownItem','item':item})
        if item in seen: errors.append({'code':'duplicateItem','item':item})
        seen.add(item)
        values[item] = value
        if value is not None:
            if type(value) is not int: errors.append({'code':'invalidSeverityType','item':item})
            elif not 0 <= value <= 3: errors.append({'code':'severityOutOfRange','item':item})
    if errors: return {'kind':'invalid','errors':errors}
    missing = [item for item in ids if values.get(item) is None]
    if missing: return {'kind':'incomplete','missing':missing}
    return {'kind':'complete','total':sum(values[item] for item in ids)}


def strict_equal(actual, expected):
    # JSON canonical equality distinguishes booleans, integers and floats.
    return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)


def main():
    dart = sys.argv[1]
    path = PACKAGE / 'fixtures/daily.json'
    content = path.read_bytes()
    fixture = json.loads(content)
    if fixture['schema'] != 'len.daily-conformance/1' or fixture['fictional'] is not True:
        raise RuntimeError('Fixture contract drift')
    cases = fixture['cases']
    historical_count = check_historical_identities(cases)
    if len({case['id'] for case in cases}) != len(cases): raise RuntimeError('Duplicate fixture IDs')
    dart_outputs = json.loads(subprocess.check_output([dart, str(PACKAGE/'tool/conformance.dart'), str(path)], cwd=PACKAGE))
    if set(dart_outputs) != {case['id'] for case in cases}: raise RuntimeError('Dart case-set mismatch')
    oracle = load_oracle()
    complete, incomplete, invalid = 0, 0, 0
    raw_observations = []
    for case in cases:
        expected = case['expected']
        independently_classified = classify(case['input'])
        if not strict_equal(independently_classified, expected): raise AssertionError(f"Independent mismatch {case['id']}")
        if not strict_equal(dart_outputs[case['id']], expected): raise AssertionError(f"Dart mismatch {case['id']}")
        kind = expected['kind']
        if kind == 'invalid':
            invalid += 1
            continue  # No invented keyed/type admission equivalence in legacy helper.
        data = case['input']
        answers = {answer['item']: answer.get('value') for answer in data['answers']}
        definition = oracle.ASSESSMENTS[data['id']]
        # Omitted entries stay omitted; null stays null. Never zero fill.
        values = [answers[item.question_id] for item in definition.items if item.question_id in answers]
        try:
            total = oracle.calculate_questionnaire_total(definition, values)
            raw = {'outcome':'returned','total':total}
        except ValueError as error:
            raw = {'outcome':'rejected','reason':str(error)}
        raw_observations.append({'id':case['id'],'python':raw,'approved_kind':kind})
        if kind == 'complete':
            complete += 1
            if raw != {'outcome':'returned','total':expected['total']}: raise AssertionError('Python total differs')
        else:
            incomplete += 1
            if raw['outcome'] != 'rejected': raise AssertionError('Expected raw Python missing-input rejection changed')
    # Observe strict-type discrepancy directly without mapping it to agreement.
    permissive = oracle.calculate_questionnaire_total(oracle.ASSESSMENTS['gad7'], [True, 1.0, 0,0,0,0,0])
    if permissive != 2: raise AssertionError('Pinned permissiveness observation changed')
    controls = [({'kind':'complete','total':999}, cases[0]['expected']),
        ({'kind':'complete','total':0}, {'kind':'incomplete','missing':['gad7.item1']}),
        ({'kind':'incomplete','missing':['gad7.item1']}, {'kind':'invalid','errors':[]}),
        ({'kind':'complete','total':True}, {'kind':'complete','total':1})]
    if any(strict_equal(wrong, expected) for wrong, expected in controls): raise AssertionError('Fault control ineffective')
    report = {'cases_passed':len(cases),'historical_identities_preserved':historical_count,'complete_python_dart_expected':complete,
        'incomplete_approved_contract_with_python_rejection':incomplete,
        'invalid_independent_contract':invalid,'fault_controls':len(controls),
        'python_bool_float_observation':permissive,'python_source_sha256':SOURCE_HASH,
        'fixtures_sha256':hashlib.sha256(content).hexdigest(),'raw_python':raw_observations}
    print(json.dumps(report, indent=2))


if __name__ == '__main__': main()
