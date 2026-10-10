import 'dart:convert';
import 'dart:io';

import '../lib/len_core.dart';
import '../test/support.dart';

void main(List<String> arguments) {
  final document = jsonDecode(
    File(arguments.single).readAsStringSync(),
  ) as Map<String, dynamic>;
  if (document['schema'] != 'len.daily-conformance/1' ||
      document['fictional'] != true) {
    throw FormatException('Unsupported or non-fictional fixture contract');
  }
  final outputs = <String, Object?>{};
  for (final raw in document['cases'] as List) {
    final input = raw['input'] as Map<String, dynamic>;
    // Expected outputs are deliberately never passed to the engine.
    outputs[raw['id'] as String] = encodeResult(
      const DailySeverityService().evaluate(decodeRequest(input)),
    );
  }
  stdout.write(jsonEncode(outputs));
}
