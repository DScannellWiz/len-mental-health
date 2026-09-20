import importlib
import io
import sqlite3
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))
app = importlib.import_module("phq9_tracker.app")


class Iteration014ReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.previous_db_path = app.DB_PATH
        self.db_path = Path(self.tmp.name) / "iteration014-reports.sqlite"
        app.DB_PATH = self.db_path
        app.init_db()

    def tearDown(self):
        app.DB_PATH = self.previous_db_path
        self.tmp.cleanup()

    def add_fictional_records(self):
        app.upsert_entry("2026-09-01", [1, 0, 0, 0, 0, 0, 0, 0, 0], notes="Fictional note")
        app.upsert_assessment_entry("gad7", "2026-09-09", [0, 1, 0, 0, 0, 0, 0])
        app.upsert_assessment_entry("gad7", "2026-09-10", [1, 1, 0, 0, 0, 0, 0])

    def move_gad7_record_to_version_one(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                UPDATE questionnaire_submissions
                SET definition_version = 1
                WHERE questionnaire_id = 'gad7' AND entry_date = '2026-09-10'
                """
            )

    def test_date_range_is_validated_before_registry_eligibility(self):
        self.add_fictional_records()

        self.assertEqual(app.normalize_report_date_range("2026-09-01", "2026-09-10"), ("2026-09-01", "2026-09-10"))
        self.assertEqual(app.eligible_report_questionnaires("2026-09-01", "2026-09-05"), ["phq9"])
        self.assertEqual(app.eligible_report_questionnaires("2026-09-06", "2026-09-10"), ["gad7"])
        self.assertEqual(app.eligible_report_questionnaires("2026-09-01", "2026-09-10"), ["phq9", "gad7"])
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            app.normalize_report_date_range("09/01/2026", "2026-09-10")
        with self.assertRaisesRegex(ValueError, "start date"):
            app.normalize_report_date_range("2026-09-11", "2026-09-10")

    def test_workbook_has_one_public_identity_and_separate_severity_average(self):
        self.add_fictional_records()
        self.move_gad7_record_to_version_one()

        workbook = app._analysis_workbook_data()
        self.assertEqual(len(workbook["Daily Assessments"]), 3)
        self.assertTrue(all("definition_version" not in row for row in workbook["Daily Assessments"]))
        self.assertEqual(
            {row["question_id"] for row in workbook["Item Responses"] if row["assessment_id"] == "gad7"},
            {f"gad7.item{number}" for number in range(1, 8)},
        )
        metadata = {row["metadata_key"]: row["metadata_value"] for row in workbook["Metadata"]}
        self.assertNotIn("questionnaire_definition_versions", metadata)
        labels = {row["response_label"] for row in workbook["Item Responses"] if row["assessment_id"] == "gad7"}
        self.assertEqual(labels, {"Not present", "Mild"})
        self.assertEqual(metadata["safety_message"], app.UNIVERSAL_SAFETY_MESSAGE)
        self.assertEqual(metadata["non_diagnostic_notice"], app.NON_DIAGNOSTIC_OUTPUT_NOTICE)
        gad_profile = [row for row in workbook["14-Day Item Profile"] if row["assessment_id"] == "gad7"]
        self.assertEqual(len(gad_profile), 7)
        self.assertEqual({row["recorded_day_coverage"] for row in gad_profile}, {2})
        self.assertTrue(all("definition_version" not in row for row in gad_profile))
        gad_average = [row for row in workbook["Item Severity Averages"] if row["assessment_id"] == "gad7"]
        self.assertEqual(len(gad_average), 7)
        self.assertEqual(gad_average[0]["average_severity"], 0.5)
        self.assertEqual(gad_average[0]["recorded_checkins"], 2)
        gad_total = [row for row in workbook["14-Day Frequency Totals"] if row["assessment_id"] == "gad7"]
        self.assertEqual(len(gad_total), 1)
        self.assertEqual(gad_total[0]["frequency_total_score"], 2)
        self.assertEqual(app.ANALYSIS_WORKBOOK_SCHEMA_VERSION, "1.4")

    def test_pdf_hides_storage_versions_and_keeps_required_safety_copy(self):
        if app.colors is None or app.PILImage is None:
            self.skipTest("PDF report generation requires reportlab and Pillow.")
        try:
            from pypdf import PdfReader
        except ImportError:
            self.skipTest("PDF text validation requires pypdf.")
        self.add_fictional_records()
        self.move_gad7_record_to_version_one()
        target = Path(self.tmp.name) / "fictional-gate-f.pdf"

        app.upsert_entry("2026-09-10", [1, 0, 0, 0, 0, 0, 0, 0, 1])
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE questionnaire_submissions SET definition_version = 1 WHERE questionnaire_id = 'phq9' AND entry_date = '2026-09-01'")

        app.generate_report("2026-09-01", "2026-09-10", str(target))

        text = " ".join(
            " ".join(page.extract_text() or "" for page in PdfReader(str(target)).pages).split()
        )
        self.assertIn("Questionnaire Definitions", text)
        self.assertNotIn("GAD-7 v1", text)
        self.assertNotIn("GAD-7 v2", text)
        self.assertNotIn("PHQ-9 v1", text)
        self.assertNotIn("PHQ-9 v2", text)
        self.assertIn("Selected Period Average Item Severity", text)
        self.assertIn("GAD-7 scores across the selected period", text)
        self.assertIn("PHQ-9 scores across the selected period", text)
        self.assertNotIn("GAD-7 v1 scores across the selected period", text)
        self.assertNotIn("GAD-7 v2 scores across the selected period", text)
        self.assertNotIn("PHQ-9 v1 scores across the selected period", text)
        self.assertNotIn("PHQ-9 v2 scores across the selected period", text)
        self.assertIn("PHQ-9 item 9 context", text)
        self.assertIn(app.NON_DIAGNOSTIC_OUTPUT_NOTICE, text)
        self.assertIn("If you feel unsafe or may act on thoughts of self-harm", text)
        self.assertIn("Len does not monitor responses or provide emergency help", text)
        self.assertNotIn(str(self.db_path), text)

    def test_mixed_stored_versions_share_severity_and_frequency_without_data_loss(self):
        for day in range(1, 14):
            values = [0, 1 if day == 1 else 0, 2 if day <= 6 else 0,
                      3 if day <= 7 else 0, 1 if day <= 11 else 0,
                      2 if day <= 12 else 0, 3]
            app.upsert_assessment_entry("gad7", f"2026-09-{day:02d}", values, notes=f"fictional {day}")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE questionnaire_submissions SET definition_version = 1 WHERE questionnaire_id = 'gad7' AND entry_date <= '2026-09-06'")
            before = conn.execute("SELECT id, entry_date, total_score, notes FROM questionnaire_submissions ORDER BY entry_date").fetchall()
        app.init_db()
        with sqlite3.connect(self.db_path) as conn:
            after = conn.execute("SELECT id, entry_date, total_score, notes FROM questionnaire_submissions ORDER BY entry_date").fetchall()
            versions = {row[0] for row in conn.execute("SELECT DISTINCT definition_version FROM questionnaire_submissions")}
        self.assertEqual(before, after)
        self.assertEqual(versions, {1, 2})  # Storage metadata remains stable.
        entries = app.fetch_assessment_entries("gad7")
        self.assertEqual(len(app.build_questionnaire_trend_series("gad7", entries)), 1)
        averages = app.build_item_severity_averages("gad7", entries)
        self.assertEqual([row["average_severity"] for row in averages], [0, 0.1, 0.9, 1.6, 0.8, 1.8, 3.0])
        profile = app.build_14_day_item_profile("2026-09-14", ["gad7"])
        self.assertEqual([row["symptom_present_days"] for row in profile], [0, 1, 6, 7, 11, 12, 13])
        self.assertEqual([row["frequency_score"] for row in profile], [0, 1, 1, 2, 2, 3, 3])
        self.assertEqual({row["recorded_day_coverage"] for row in profile}, {13})
        self.assertEqual(sum(row["frequency_score"] for row in profile), 12)
        self.assertEqual(app.build_14_day_frequency_totals("2026-09-14", ["gad7"])[0]["frequency_total_score"], 12)
        self.assertEqual([app.convert_14_day_count_to_item_score(n) for n in (0, 1, 6, 7, 11, 12, 14)], [0, 1, 1, 2, 2, 3, 3])

    def test_cli_passes_explicit_date_range_and_registry_selection_to_pdf(self):
        self.add_fictional_records()
        target = Path(self.tmp.name) / "cli-report.pdf"
        argv = [
            "len",
            "--report-pdf",
            str(target),
            "--report-start",
            "2026-09-10",
            "--report-end",
            "2026-09-10",
            "--questionnaires",
            "gad7",
        ]
        output = io.StringIO()
        with patch.object(sys, "argv", argv), patch.object(app, "generate_report") as generate, redirect_stdout(output):
            app.main()

        generate.assert_called_once_with("2026-09-10", "2026-09-10", str(target), ["gad7"])
        self.assertIn("GAD-7", output.getvalue())
        self.assertNotIn("GAD-7 v2", output.getvalue())


if __name__ == "__main__":
    unittest.main()
