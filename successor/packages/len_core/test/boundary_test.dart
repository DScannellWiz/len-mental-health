import '../lib/len_core.dart';
import 'support.dart';

void main() {
  var passed = 0;
  void test(String name, void Function() action) {
    action();
    passed++;
    print('PASS $name');
  }

  test('malformed origin cannot become builtin', () {
    for (final origin in [null, true, 'Builtin', 'other']) {
      throws(
        () => decodeRequest({'origin': origin, 'id': 'phq9', 'answers': []}),
        'origin rejected',
      );
    }
  });
  test('malformed envelopes rejected at harness boundary', () {
    for (final input in [
      {'origin': 'builtin', 'id': 9, 'answers': []},
      {'origin': 'builtin', 'id': 'gad7', 'answers': {}},
      {
        'origin': 'builtin',
        'id': 'gad7',
        'answers': [null],
      },
      {
        'origin': 'builtin',
        'id': 'gad7',
        'answers': [
          {'item': 9, 'value': 0},
        ],
      },
    ]) {
      throws(() => decodeRequest(input), 'malformed input rejected');
    }
  });
  test('null, omitted value and omitted item preserve missingness', () {
    final omittedValue = const DailySeverityService().evaluate(
      decodeRequest({
        'origin': 'builtin',
        'id': 'gad7',
        'answers': [
          {'item': 'gad7.item1'},
        ],
      }),
    );
    check(
      omittedValue is IncompleteDailySeverity &&
          omittedValue.missingItemIds.length == 7,
      'omitted value is missing',
    );
    final result = const DailySeverityService().evaluate(
      decodeRequest({
        'origin': 'builtin',
        'id': 'gad7',
        'answers': [
          {'item': 'gad7.item1', 'value': null},
        ],
      }),
    );
    equal(encodeResult(result), {
      'kind': 'incomplete',
      'missing': [
        'gad7.item1',
        'gad7.item2',
        'gad7.item3',
        'gad7.item4',
        'gad7.item5',
        'gad7.item6',
        'gad7.item7',
      ],
    }, 'exact missing result');
  });
  test('supplied malformed scalar cannot become missing', () {
    final result = const DailySeverityService().evaluate(
      decodeRequest({
        'origin': 'builtin',
        'id': 'gad7',
        'answers': [
          {'item': 'gad7.item1', 'value': []},
        ],
      }),
    );
    equal(encodeResult(result), {
      'kind': 'invalid',
      'errors': [
        {'code': 'invalidSeverityType', 'item': 'gad7.item1'},
      ],
    }, 'invalid precedence');
  });
  test('error ordering stable and item-only metadata', () {
    final request = decodeRequest({
      'origin': 'builtin',
      'id': 'gad7',
      'answers': [
        {'item': 'gad7.item1', 'value': 4},
        {'item': 'gad7.item1', 'value': 'hostile fictional value'},
      ],
    });
    final actual = encodeResult(const DailySeverityService().evaluate(request));
    equal(actual, {
      'kind': 'invalid',
      'errors': [
        {'code': 'severityOutOfRange', 'item': 'gad7.item1'},
        {'code': 'duplicateItem', 'item': 'gad7.item1'},
        {'code': 'invalidSeverityType', 'item': 'gad7.item1'},
      ],
    }, 'stable errors with no raw value');
  });
  test('request snapshots caller and parsed collections', () {
    final answers = [
      {'item': 'gad7.item1', 'value': 0},
    ];
    final request = decodeRequest({
      'origin': 'builtin',
      'id': 'gad7',
      'answers': answers,
    });
    answers[0]['value'] = 4;
    answers.clear();
    check(request.responses.single.value is SeverityValue, 'adapter snapshot');
  });
  print('RESULT $passed/$passed boundary tests passed');
}
