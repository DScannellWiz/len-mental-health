import 'dart:convert';

import '../lib/len_core.dart';

// Strict language-neutral fixture boundary. Malformed envelopes fail the harness;
// supplied scalar type errors reach the domain as typed invalid responses.
DailySeverityRequest decodeRequest(Map<String, dynamic> input) {
  final origin = switch (input['origin']) {
    'builtin' => DefinitionOrigin.builtin,
    'custom' => DefinitionOrigin.custom,
    _ => throw FormatException('Unknown definition origin'),
  };
  final id = input['id'];
  final answers = input['answers'];
  if (id is! String || answers is! List)
    throw FormatException('Invalid envelope');
  final responses = <ItemResponse>[];
  for (final raw in answers) {
    if (raw is! Map || raw['item'] is! String) {
      throw FormatException('Invalid keyed answer');
    }
    responses.add(
      ItemResponse(raw['item'] as String, ResponseValue.fromRaw(raw['value'])),
    );
  }
  return DailySeverityRequest(QuestionnaireIdentity(origin, id), responses);
}

Map<String, Object?> encodeResult(DailySeverityResult result) =>
    switch (result) {
      CompleteDailySeverity(:final total) => {
        'kind': 'complete',
        'total': total,
      },
      IncompleteDailySeverity(:final missingItemIds) => {
        'kind': 'incomplete',
        'missing': missingItemIds,
      },
      InvalidDailySeverity(:final errors) => {
        'kind': 'invalid',
        'errors': errors
            .map((error) => {'code': error.code.name, 'item': error.itemId})
            .toList(),
      },
    };

void check(bool condition, String message) {
  if (!condition) throw StateError(message);
}

void equal(Object? actual, Object? expected, String message) {
  check(
    jsonEncode(actual) == jsonEncode(expected),
    '$message: actual=$actual expected=$expected',
  );
}

void throws(void Function() action, String message) {
  var rejected = false;
  try {
    action();
  } catch (_) {
    rejected = true;
  }
  check(rejected, message);
}
