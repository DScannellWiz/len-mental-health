import importlib
import json
import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from unittest.mock import patch


project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))
app = importlib.import_module("phq9_tracker.app")


class Iteration014QuestionnaireContractTests(unittest.TestCase):
    def custom_definition(self, **changes):
        definition = app.QuestionnaireDefinition(
            questionnaire_id="custom-example",
            definition_version=1,
            display_name="Custom Example",
            short_name="Example",
            description="A fictional contract test questionnaire.",
            timeframe_text="Choose one response.",
            source_citation="Fictional test definition",
            source_url="",
            rights_status="User-authored fictional test content",
            rights_source_url="",
            required_notice="",
            origin="custom",
            items=(
                app.QuestionDefinition(
                    question_id="custom-example.item1",
                    prompt="Fictional prompt",
                    options=(
                        app.ResponseOption("never", "Never"),
                        app.ResponseOption("sometimes", "Sometimes"),
                    ),
                ),
            ),
            scoring_rule="none",
            score_min=None,
            score_max=None,
            profile_rule="none",
            interpretation_policy="raw_only",
        )
        return replace(definition, **changes)

    def test_builtin_definitions_are_immutable_exact_compatibility_contracts(self):
        self.assertIs(app.AssessmentDefinition, app.QuestionnaireDefinition)
        self.assertIs(app.ASSESSMENTS, app.QUESTIONNAIRES)
        self.assertEqual(app.ASSESSMENT_ORDER, app.QUESTIONNAIRE_ORDER)
        expected = {
            "phq9": (app.PHQ9_ITEM_LABELS, 27),
            "gad7": (app.GAD7_ITEM_LABELS, 21),
        }
        for questionnaire_id, (labels, maximum) in expected.items():
            definition = app.validate_questionnaire_definition(app.QUESTIONNAIRES[questionnaire_id])
            self.assertEqual(definition.assessment_id, questionnaire_id)
            self.assertEqual(definition.definition_version, 2)
            self.assertEqual(definition.item_labels, labels)
            self.assertEqual(definition.item_count, len(labels))
            self.assertEqual(definition.max_score, maximum)
            self.assertEqual(definition.score_min, 0)
            self.assertEqual(definition.scoring_rule, "sum")
            self.assertEqual(definition.profile_rule, "symptom_presence_14d")
            self.assertEqual(definition.interpretation_policy, "validated_builtin")
            self.assertEqual(definition.origin, "builtin")
            self.assertTrue(definition.source_url)
            self.assertTrue(definition.rights_source_url)
            for item in definition.items:
                self.assertEqual([option.value for option in item.options], [0, 1, 2, 3])
                self.assertEqual([option.score for option in item.options], [0, 1, 2, 3])
                self.assertEqual(
                    [option.label for option in item.options],
                    ["Not present", "Mild", "Moderate", "High"],
                )
            self.assertEqual(definition.timeframe_text, app.DAILY_SEVERITY_INSTRUCTION)
        with self.assertRaises(FrozenInstanceError):
            app.QUESTIONNAIRES["phq9"].display_name = "Changed"

    def test_v1_snapshots_remain_exact_immutable_provenance_but_labels_are_not_user_interpretation(self):
        expected_regressed_labels = [
            "Not at all",
            "Several days",
            "More than half the days",
            "Nearly every day",
        ]
        for questionnaire_id in ("phq9", "gad7"):
            definition = app.LEGACY_BUILTIN_DEFINITIONS[questionnaire_id]
            self.assertEqual(definition.definition_version, 1)
            self.assertEqual([option.label for option in definition.items[0].options], expected_regressed_labels)
            self.assertEqual(
                [app.user_facing_response_label(definition, option) for option in definition.items[0].options],
                ["0", "1", "2", "3"],
            )

    def test_phq9_item9_behavior_is_attached_only_to_stable_phq9_item_id(self):
        phq9 = app.QUESTIONNAIRES["phq9"]
        behavior_items = [item.question_id for item in phq9.items if "phq9_item9_context" in item.behavior_ids]
        self.assertEqual(behavior_items, ["phq9.item9"])
        self.assertTrue(phq9.has_item9_safety_context)
        self.assertFalse(app.QUESTIONNAIRES["gad7"].has_item9_safety_context)

        invalid_item = replace(
            self.custom_definition().items[0],
            behavior_ids=("phq9_item9_context",),
        )
        with self.assertRaisesRegex(ValueError, "restricted to phq9.item9"):
            app.validate_questionnaire_definition(self.custom_definition(items=(invalid_item,)))

    def test_canonical_serialization_preserves_nonnumeric_nonscored_options(self):
        definition = self.custom_definition()
        first = app.serialize_questionnaire_definition(definition)
        second = app.serialize_questionnaire_definition(definition)
        self.assertEqual(first, second)
        data = json.loads(first)
        self.assertEqual(data["items"][0]["options"][0], {"label": "Never", "score": None, "value": "never"})
        self.assertEqual(data["scoring_rule"], "none")
        self.assertIsNone(data["score_max"])
        restored = app.deserialize_questionnaire_definition(first)
        self.assertEqual(restored, definition)
        self.assertEqual(app.serialize_questionnaire_definition(restored), first)

    def test_deserialization_rejects_incomplete_and_unsafe_definitions(self):
        with self.assertRaisesRegex(ValueError, "Invalid questionnaire definition JSON"):
            app.deserialize_questionnaire_definition("[]")
        data = app.questionnaire_definition_data(self.custom_definition())
        data["behavior_ids"] = ["run_code"]
        with self.assertRaisesRegex(ValueError, "Unknown questionnaire behavior"):
            app.deserialize_questionnaire_definition(json.dumps(data))

    def test_invalid_identifiers_versions_duplicates_and_scores_fail_closed(self):
        definition = self.custom_definition()
        with self.assertRaisesRegex(ValueError, "stable lowercase identifier"):
            app.validate_questionnaire_definition(replace(definition, questionnaire_id="Not Valid"))
        with self.assertRaisesRegex(ValueError, "positive integer"):
            app.validate_questionnaire_definition(replace(definition, definition_version=0))

        duplicate_question = replace(definition, items=(definition.items[0], definition.items[0]))
        with self.assertRaisesRegex(ValueError, "Duplicate question_id"):
            app.validate_questionnaire_definition(duplicate_question)

        duplicate_options = (
            app.ResponseOption("same", "First"),
            app.ResponseOption("same", "Second"),
        )
        with self.assertRaisesRegex(ValueError, "duplicate option values"):
            app.validate_questionnaire_definition(
                replace(definition, items=(replace(definition.items[0], options=duplicate_options),))
            )

        invalid_score_options = (app.ResponseOption("bad", "Bad", float("nan")),)
        with self.assertRaisesRegex(ValueError, "invalid option score"):
            app.validate_questionnaire_definition(
                replace(definition, items=(replace(definition.items[0], options=invalid_score_options),))
            )

    def test_unknown_strategies_behaviors_and_custom_clinical_claims_fail_closed(self):
        definition = self.custom_definition()
        with self.assertRaisesRegex(ValueError, "Unknown scoring rule"):
            app.validate_questionnaire_definition(replace(definition, scoring_rule="execute_formula"))
        with self.assertRaisesRegex(ValueError, "Unknown profile rule"):
            app.validate_questionnaire_definition(replace(definition, profile_rule="infer_clinical_risk"))
        with self.assertRaisesRegex(ValueError, "Unknown questionnaire behavior"):
            app.validate_questionnaire_definition(replace(definition, behavior_ids=("run_code",)))
        with self.assertRaisesRegex(ValueError, "Unknown question behavior"):
            app.validate_questionnaire_definition(
                replace(definition, items=(replace(definition.items[0], behavior_ids=("run_code",)),))
            )
        with self.assertRaisesRegex(ValueError, "cannot use validated_builtin"):
            app.validate_questionnaire_definition(replace(definition, interpretation_policy="validated_builtin"))

    def test_builtins_require_source_and_rights_evidence(self):
        definition = app.QUESTIONNAIRES["gad7"]
        for field_name in ("source_url", "rights_status", "rights_source_url"):
            with self.subTest(field_name=field_name), self.assertRaisesRegex(ValueError, field_name):
                app.validate_questionnaire_definition(replace(definition, **{field_name: ""}))

    def test_sum_scoring_requires_complete_numeric_options_and_exact_bounds(self):
        definition = app.QUESTIONNAIRES["gad7"]
        first_item = definition.items[0]
        incomplete_scores = tuple(
            replace(option, score=None if option.value == 3 else option.score)
            for option in first_item.options
        )
        with self.assertRaisesRegex(ValueError, "numeric score for every option"):
            app.validate_questionnaire_definition(
                replace(definition, items=(replace(first_item, options=incomplete_scores), *definition.items[1:]))
            )
        with self.assertRaisesRegex(ValueError, "Score bounds do not match"):
            app.validate_questionnaire_definition(replace(definition, score_max=99))

    def test_current_totals_resolve_through_application_owned_sum_strategy(self):
        expected_cases = {
            "phq9": ([0, 1, 2, 3, 0, 1, 2, 3, 0], 12),
            "gad7": ([3, 2, 1, 0, 3, 2, 1], 12),
        }
        for questionnaire_id, (responses, expected_total) in expected_cases.items():
            with self.subTest(questionnaire_id=questionnaire_id):
                definition = app.QUESTIONNAIRES[questionnaire_id]
                descriptor = app.resolve_scoring_strategy(definition)
                self.assertEqual(descriptor.strategy_id, "sum")
                self.assertEqual(descriptor.implementation_id, "sum_option_scores_v1")
                self.assertTrue(descriptor.deterministic)
                self.assertEqual(app.calculate_questionnaire_total(definition, responses), expected_total)

    def test_today_response_choices_distinguish_unanswered_from_explicit_zero(self):
        question = app.QUESTIONNAIRES["phq9"].items[0]
        choices = app.questionnaire_response_choices(question)
        self.assertEqual(choices[0], app.UNANSWERED_RESPONSE)
        zero_display = app.display_questionnaire_response(question, 0)
        self.assertNotEqual(zero_display, app.UNANSWERED_RESPONSE)
        self.assertEqual(app.parse_questionnaire_response(question, app.UNANSWERED_RESPONSE), None)
        self.assertEqual(app.parse_questionnaire_response(question, zero_display), 0)
        with self.assertRaisesRegex(ValueError, "Unknown response"):
            app.parse_questionnaire_response(question, "not a declared option")

    def test_sum_strategy_rejects_missing_and_unknown_responses(self):
        definition = app.QUESTIONNAIRES["phq9"]
        with self.assertRaisesRegex(ValueError, "Unsupported response for phq9.item9"):
            app.calculate_questionnaire_total(definition, [0] * 8 + [None])
        with self.assertRaisesRegex(ValueError, "Unsupported response for phq9.item1"):
            app.calculate_questionnaire_total(definition, [4] + [0] * 8)
        with self.assertRaisesRegex(ValueError, "requires 9 responses"):
            app.calculate_questionnaire_total(definition, [0] * 8)

    def test_custom_deterministic_sum_does_not_add_clinical_interpretation(self):
        definition = self.custom_definition(
            items=(
                replace(
                    self.custom_definition().items[0],
                    options=(
                        app.ResponseOption("never", "Never", 0),
                        app.ResponseOption("sometimes", "Sometimes", 1),
                    ),
                ),
            ),
            scoring_rule="sum",
            score_min=0,
            score_max=1,
            interpretation_policy="raw_only",
        )
        self.assertEqual(app.calculate_questionnaire_total(definition, ["sometimes"]), 1)
        self.assertEqual(definition.interpretation_policy, "raw_only")

    def test_known_but_unimplemented_strategy_descriptors_fail_closed(self):
        scoring_definition = self.custom_definition(scoring_rule="subscale_sum")
        with self.assertRaisesRegex(ValueError, "Scoring strategy is not implemented: subscale_sum"):
            app.calculate_questionnaire_total(scoring_definition, ["never"])

        profile_definition = self.custom_definition(profile_rule="item_history")
        with self.assertRaisesRegex(ValueError, "Profile strategy is not implemented for 14-day scoring: item_history"):
            app.calculate_questionnaire_profile_for_window(
                profile_definition,
                [],
                "2026-01-01",
                "2026-01-14",
            )

    def test_current_profiles_resolve_through_exact_14_day_strategy(self):
        cases = {
            "phq9": (12, 9, [12, 0, 0, 0, 0, 0, 0, 0, 1], [3, 0, 0, 0, 0, 0, 0, 0, 1]),
            "gad7": (7, 7, [7, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0]),
        }
        for questionnaire_id, (presence_days, item_count, expected_counts, expected_scores) in cases.items():
            with self.subTest(questionnaire_id=questionnaire_id):
                definition = app.QUESTIONNAIRES[questionnaire_id]
                entries = []
                for day in range(1, 15):
                    items = [1 if day <= presence_days else 0, *([0] * (item_count - 1))]
                    if questionnaire_id == "phq9" and day == 14:
                        items[8] = 3
                    entries.append(
                        app.AssessmentEntryRow(
                            id=day,
                            assessment_id=questionnaire_id,
                            entry_date=f"2026-01-{day:02d}",
                            items=items,
                            total=sum(items),
                            severity="",
                            notes="",
                        )
                    )

                descriptor = app.resolve_profile_strategy(definition)
                self.assertEqual(descriptor.strategy_id, "symptom_presence_14d")
                self.assertEqual(descriptor.implementation_id, "symptom_presence_thresholds_14d_v1")
                result = app.calculate_questionnaire_profile_for_window(
                    definition,
                    entries,
                    "2026-01-01",
                    "2026-01-14",
                )
                self.assertEqual(result.item_counts, expected_counts)
                self.assertEqual(result.item_scores, expected_scores)
                self.assertEqual(result.entries_included, 14)
                self.assertEqual(result.calendar_days, 14)

    def test_raw_only_custom_profile_computes_without_clinical_interpretation(self):
        definition = self.custom_definition(
            items=(
                replace(
                    self.custom_definition().items[0],
                    options=(
                        app.ResponseOption("never", "Never", 0),
                        app.ResponseOption("sometimes", "Sometimes", 1),
                    ),
                ),
            ),
            scoring_rule="sum",
            score_min=0,
            score_max=1,
            profile_rule="symptom_presence_14d",
        )
        entry = app.AssessmentEntryRow(1, "custom-example", "2026-01-14", ["sometimes"], 1, "", "")

        result = app.calculate_questionnaire_profile_for_window(
            definition, [entry], "2026-01-01", "2026-01-14"
        )

        self.assertEqual(result.item_scores, [1])
        self.assertEqual(result.severity, "")
        self.assertIsNone(app.questionnaire_total_trend_omission_reason(definition))

    def test_unsupported_analytics_capabilities_have_neutral_omission_reasons(self):
        definition = self.custom_definition()

        self.assertIn("does not define a total score", app.questionnaire_total_trend_omission_reason(definition))
        self.assertIn("does not define a 14-day item profile", app.questionnaire_profile_omission_reason(definition))

    def test_approved_v1_v2_score_series_are_chronological_for_both_builtins(self):
        for questionnaire_id, item_count in (("phq9", 9), ("gad7", 7)):
            entries = [
                app.AssessmentEntryRow(2, questionnaire_id, "2026-01-02", [1] * item_count, item_count, "Mild", "", definition_version=2),
                app.AssessmentEntryRow(1, questionnaire_id, "2026-01-01", [0] * item_count, 0, "Minimal", "", definition_version=1),
            ]
            with patch.object(app, "load_questionnaire_definition_snapshot", return_value=app.LEGACY_BUILTIN_DEFINITIONS[questionnaire_id]):
                series = app.build_questionnaire_trend_series(questionnaire_id, entries)
            self.assertEqual(len(series), 1)
            self.assertEqual(series[0].definition_versions, (1, 2))
            self.assertEqual([row.entry_date for row in series[0].entries], ["2026-01-01", "2026-01-02"])
            self.assertEqual([row.definition_version for row in series[0].entries], [1, 2])
            self.assertEqual(series[0].label, app.QUESTIONNAIRES[questionnaire_id].display_name)

    def test_unapproved_future_version_remains_a_separate_score_series(self):
        current = app.QUESTIONNAIRES["phq9"]
        future_items = tuple(replace(item, options=tuple(replace(option, score=option.score * 2)
                                                           for option in item.options)) for item in current.items)
        future = replace(current, definition_version=3, items=future_items, score_max=54)
        entries = [
            app.AssessmentEntryRow(1, "phq9", "2026-01-01", [1] * 9, 9, "Mild", "", definition_version=1),
            app.AssessmentEntryRow(2, "phq9", "2026-01-02", [1] * 9, 9, "Mild", "", definition_version=2),
            app.AssessmentEntryRow(3, "phq9", "2026-01-03", [1] * 9, 18, "", "", definition_version=3),
        ]
        with patch.object(app, "load_questionnaire_definition_snapshot", side_effect=lambda _, version: app.LEGACY_BUILTIN_DEFINITIONS["phq9"] if version == 1 else future):
            series = app.build_questionnaire_trend_series("phq9", entries)
        self.assertEqual([part.definition_versions for part in series], [(1, 2), (3,)])

    def test_profile_comparison_crosses_approved_v1_v2_boundary(self):
        version_two = app.QUESTIONNAIRES["phq9"]
        entries = [
            app.AssessmentEntryRow(1, "phq9", "2026-01-14", [1] + [0] * 8, 1, "Minimal", "", definition_version=1),
            app.AssessmentEntryRow(2, "phq9", "2026-01-28", [1] + [0] * 8, 1, "Minimal", "", definition_version=2),
        ]

        with patch.object(app, "load_questionnaire_definition_snapshot", return_value=version_two):
            highlights = app.symptom_highlights("phq9", entries, "2026-01-28", limit=1)

        self.assertIn("PHQ-9", highlights[0])
        self.assertNotIn("PHQ-9 v2", highlights[0])
        self.assertIn("two periods", highlights[0])

    def test_treatment_cycle_uses_both_approved_versions(self):
        entries = [
            app.AssessmentEntryRow(1, "phq9", "2026-01-14", [1] + [0] * 8, 1, "Minimal", "", definition_version=1),
            app.AssessmentEntryRow(2, "phq9", "2026-01-15", [2] + [0] * 8, 2, "Minimal", "", definition_version=2),
        ]
        with patch.object(app, "load_questionnaire_definition_snapshot", return_value=app.LEGACY_BUILTIN_DEFINITIONS["phq9"]):
            _, cycle_entries, other_series = app._latest_definition_group("phq9", entries, "2026-01-15")
        cycles = app.treatment_cycles(cycle_entries, [(1, "2026-01-14", "Ketamine infusion", "fictional")], "2026-01-15")
        self.assertFalse(other_series)
        self.assertEqual([row.definition_version for row in cycles[0].entries], [1, 2])


if __name__ == "__main__":
    unittest.main()
