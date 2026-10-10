import '../lib/len_core.dart';
import 'support.dart';

int passed = 0;
void test(String name, void Function() action) {
  action();
  passed++;
  print('PASS $name');
}

DailySeverityRequest request(String id, List<Object?> values) =>
    DailySeverityRequest(QuestionnaireIdentity(DefinitionOrigin.builtin, id), [
      for (var i = 0; i < values.length; i++)
        ItemResponse('$id.item${i + 1}', ResponseValue.fromRaw(values[i])),
    ]);

void main() {
  const service = DailySeverityService();
  test('all severity factories and strict bounds', () {
    for (var i = 0; i <= 3; i++)
      equal(SeverityValue.fromInt(i).value, i, 'severity');
    throws(() => SeverityValue.fromInt(-1), 'negative rejected');
    throws(() => SeverityValue.fromInt(4), 'four rejected');
  });
  test('explicit zeros complete both questionnaires', () {
    for (final id in ['phq9', 'gad7']) {
      final result = service.evaluate(
        request(id, List.filled(id == 'phq9' ? 9 : 7, 0)),
      );
      check(
        result is CompleteDailySeverity && result.total == 0,
        'zero is answered',
      );
    }
  });
  test('omitted and null answers incomplete without total', () {
    final omitted =
        service.evaluate(request('gad7', [0])) as IncompleteDailySeverity;
    equal(omitted.missingItemIds.length, 6, 'omitted');
    final unanswered = service.evaluate(
      request('gad7', [null, 0, 0, 0, 0, 0, 0]),
    ) as IncompleteDailySeverity;
    equal(unanswered.missingItemIds, ['gad7.item1'], 'null');
    final dynamic dynamicResult = unanswered;
    throws(() {
      dynamicResult.total;
    }, 'no incomplete total member');
  });
  test('invalid plus missing in either order and all errors', () {
    for (final values in [
      [null, 4, true],
      [4, null, true],
    ]) {
      final result =
          service.evaluate(request('gad7', values)) as InvalidDailySeverity;
      equal(result.errors.length, 2, 'all invalid answers reported');
      final dynamic dynamicResult = result;
      throws(() {
        dynamicResult.total;
      }, 'no invalid total member');
    }
  });
  test('no coercion or invalid mutable payload retention', () {
    for (final raw in [true, false, 0.0, 1.0, '0', '', [], {}]) {
      final result =
          service.evaluate(request('gad7', [raw])) as InvalidDailySeverity;
      equal(
        result.errors.single.code.name,
        'invalidSeverityType',
        'strict type',
      );
    }
    final payload = <Object?>[];
    final admitted = ResponseValue.fromRaw(payload);
    payload.add(0);
    check(
      admitted is InvalidResponseValue,
      'mutable object cannot become valid',
    );
  });
  test('identity duplicates unknown and foreign items', () {
    final result = service.evaluate(
      DailySeverityRequest(
        const QuestionnaireIdentity(DefinitionOrigin.builtin, 'gad7'),
        [
          ItemResponse('gad7.item1', SeverityValue.fromInt(0)),
          ItemResponse('gad7.item1', SeverityValue.fromInt(0)),
          ItemResponse('phq9.item9', SeverityValue.fromInt(3)),
        ],
      ),
    ) as InvalidDailySeverity;
    equal(result.errors.map((error) => error.code.name).toList(), [
      'duplicateItem',
      'unknownItem',
    ], 'identities');
  });
  test('custom and unsupported cannot acquire builtin identity', () {
    for (final identity in [
      const QuestionnaireIdentity(DefinitionOrigin.custom, 'phq9'),
      const QuestionnaireIdentity(DefinitionOrigin.custom, 'fictional.nine'),
      const QuestionnaireIdentity(DefinitionOrigin.builtin, 'unknown'),
    ]) {
      check(
        BuiltinCatalog.resolve(identity) == null,
        'untrusted catalog claim',
      );
      check(
        service.evaluate(DailySeverityRequest(identity, []))
            is InvalidDailySeverity,
        'unsupported',
      );
    }
    equal(
      BuiltinCatalog.phq9.items[8].id,
      'phq9.item9',
      'trusted item identity',
    );
  });
  test('keyed order canonicalized', () {
    final original = request('gad7', [0, 1, 2, 3, 0, 1, 2]);
    final reversed = DailySeverityRequest(
      original.identity,
      original.responses.reversed,
    );
    final result = service.evaluate(reversed) as CompleteDailySeverity;
    equal(result.total, 9, 'mixed total');
    equal(
      result.responses.map((answer) => answer.itemId).toList(),
      original.responses.map((answer) => answer.itemId).toList(),
      'canonical order',
    );
  });
  test('input snapshot and all output collections immutable', () {
    final caller = request('gad7', List.filled(7, 0)).responses.toList();
    final input = DailySeverityRequest(
      const QuestionnaireIdentity(DefinitionOrigin.builtin, 'gad7'),
      caller,
    );
    caller.clear();
    equal(input.responses.length, 7, 'snapshot');
    throws(() => input.responses.clear(), 'request list immutable');
    throws(() => BuiltinCatalog.gad7.items.clear(), 'catalog immutable');
    final complete = service.evaluate(input) as CompleteDailySeverity;
    throws(() => complete.responses.clear(), 'complete immutable');
    final incomplete =
        service.evaluate(request('gad7', [])) as IncompleteDailySeverity;
    throws(() => incomplete.missingItemIds.clear(), 'missing immutable');
    final invalid =
        service.evaluate(request('gad7', [4])) as InvalidDailySeverity;
    throws(() => invalid.errors.clear(), 'errors immutable');
    final dynamic dynamicResult = complete;
    throws(() {
      dynamicResult.total = 123;
    }, 'total final');
  });
  test('exhaustive GAD 16384 vectors independent arithmetic', () {
    for (var vector = 0; vector < 16384; vector++) {
      var remainder = vector;
      var expected = 0;
      final values = <int>[];
      for (var item = 0; item < 7; item++) {
        final value = remainder % 4;
        remainder ~/= 4;
        expected += value;
        values.add(value);
      }
      final result =
          service.evaluate(request('gad7', values)) as CompleteDailySeverity;
      equal(result.total, expected, 'vector $vector');
      check(result.total >= 0 && result.total <= 21, 'range');
    }
  });
  test('PHQ single item contributions including Item9 no side effect', () {
    for (var item = 0; item < 9; item++) {
      for (var severity = 0; severity < 4; severity++) {
        final values = List<int>.filled(9, 0)..[item] = severity;
        final result =
            service.evaluate(request('phq9', values)) as CompleteDailySeverity;
        equal(result.total, severity, 'item contribution');
      }
    }
  });
  test('all missing exact canonical identities', () {
    final result =
        service.evaluate(request('phq9', [])) as IncompleteDailySeverity;
    equal(
      result.missingItemIds,
      BuiltinCatalog.phq9.items.map((item) => item.id).toList(),
      'missing set',
    );
  });
  print(
    'RESULT $passed/$passed core tests passed; 16384 GAD vectors and 36 PHQ contributions',
  );
}
