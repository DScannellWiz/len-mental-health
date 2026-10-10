/// Pure domain API. No UI, persistence, clinical interpretation or safety action.
library;

enum DefinitionOrigin { builtin, custom }

enum BuiltinQuestionnaireId { phq9, gad7 }

final class QuestionnaireIdentity {
  const QuestionnaireIdentity(this.origin, this.id);
  final DefinitionOrigin origin;
  final String id;
}

final class ItemDefinition {
  const ItemDefinition._(this.id, this.questionnaire);
  final String id;
  final BuiltinQuestionnaireId questionnaire;
}

final class QuestionnaireDefinition {
  QuestionnaireDefinition._(this.id, int itemCount)
    : items = List.unmodifiable(
        List.generate(
          itemCount,
          (index) => ItemDefinition._('${id.name}.item${index + 1}', id),
        ),
      );
  final BuiltinQuestionnaireId id;
  final List<ItemDefinition> items;
}

/// Only this catalog constructs trusted built-in definitions/item identities.
abstract final class BuiltinCatalog {
  static final phq9 = QuestionnaireDefinition._(BuiltinQuestionnaireId.phq9, 9);
  static final gad7 = QuestionnaireDefinition._(BuiltinQuestionnaireId.gad7, 7);

  static QuestionnaireDefinition? resolve(QuestionnaireIdentity identity) {
    if (identity.origin != DefinitionOrigin.builtin) return null;
    return switch (identity.id) {
      'phq9' => phq9,
      'gad7' => gad7,
      _ => null,
    };
  }
}

enum ValidationCode {
  unsupportedQuestionnaire,
  unknownItem,
  duplicateItem,
  severityOutOfRange,
  invalidSeverityType,
}

sealed class ResponseValue {
  const ResponseValue();

  /// Snapshots admission of a scalar. Invalid mutable objects are not retained.
  factory ResponseValue.fromRaw(Object? raw) {
    if (raw == null) return const UnansweredValue();
    if (raw is! int)
      return const InvalidResponseValue._(ValidationCode.invalidSeverityType);
    if (raw < 0 || raw > 3)
      return const InvalidResponseValue._(ValidationCode.severityOutOfRange);
    return SeverityValue.fromInt(raw);
  }
}

final class SeverityValue extends ResponseValue {
  const SeverityValue._(this.value);
  factory SeverityValue.fromInt(int value) {
    if (value < 0 || value > 3) throw RangeError.range(value, 0, 3, 'severity');
    return SeverityValue._(value);
  }
  final int value;
}

final class UnansweredValue extends ResponseValue {
  const UnansweredValue();
}

final class InvalidResponseValue extends ResponseValue {
  const InvalidResponseValue._(this.code);
  final ValidationCode code;
}

final class ItemResponse {
  const ItemResponse(this.itemId, this.value);
  final String itemId;
  final ResponseValue value;
}

final class DailySeverityRequest {
  DailySeverityRequest(this.identity, Iterable<ItemResponse> responses)
    : responses = List.unmodifiable(responses);
  final QuestionnaireIdentity identity;
  final List<ItemResponse> responses;
}

final class ValidationError {
  const ValidationError._(this.code, this.itemId);
  final ValidationCode code;
  final String? itemId;
}

sealed class DailySeverityResult {
  const DailySeverityResult._();
}

final class CompleteDailySeverity extends DailySeverityResult {
  CompleteDailySeverity._(
    this.definition,
    Iterable<ItemResponse> responses,
    this.total,
  ) : responses = List.unmodifiable(responses),
      super._();
  final QuestionnaireDefinition definition;
  final List<ItemResponse> responses;
  final int total;
}

final class IncompleteDailySeverity extends DailySeverityResult {
  IncompleteDailySeverity._(this.definition, Iterable<String> missingItemIds)
    : missingItemIds = List.unmodifiable(missingItemIds),
      super._();
  final QuestionnaireDefinition definition;
  final List<String> missingItemIds;
}

final class InvalidDailySeverity extends DailySeverityResult {
  InvalidDailySeverity._(Iterable<ValidationError> errors)
    : errors = List.unmodifiable(errors),
      super._();
  final List<ValidationError> errors;
}

/// Invalid wins over incomplete. Errors follow input order; missing IDs and
/// complete responses use catalog order. Arithmetic begins only after admission.
final class DailySeverityService {
  const DailySeverityService();

  DailySeverityResult evaluate(DailySeverityRequest request) {
    final definition = BuiltinCatalog.resolve(request.identity);
    if (definition == null) {
      return InvalidDailySeverity._([
        const ValidationError._(ValidationCode.unsupportedQuestionnaire, null),
      ]);
    }
    final expected = definition.items.map((item) => item.id).toSet();
    final seen = <String>{};
    final answers = <String, ItemResponse>{};
    final errors = <ValidationError>[];
    for (final response in request.responses) {
      if (!expected.contains(response.itemId)) {
        errors.add(
          ValidationError._(ValidationCode.unknownItem, response.itemId),
        );
      }
      if (!seen.add(response.itemId)) {
        errors.add(
          ValidationError._(ValidationCode.duplicateItem, response.itemId),
        );
      }
      if (response.value case InvalidResponseValue(:final code)) {
        errors.add(ValidationError._(code, response.itemId));
      }
      answers[response.itemId] = response;
    }
    if (errors.isNotEmpty) return InvalidDailySeverity._(errors);
    final missing = definition.items
        .where((item) => answers[item.id]?.value is! SeverityValue)
        .map((item) => item.id)
        .toList();
    if (missing.isNotEmpty)
      return IncompleteDailySeverity._(definition, missing);
    final ordered = definition.items.map((item) => answers[item.id]!).toList();
    final total = ordered.fold<int>(
      0,
      (sum, answer) => sum + (answer.value as SeverityValue).value,
    );
    return CompleteDailySeverity._(definition, ordered, total);
  }
}
