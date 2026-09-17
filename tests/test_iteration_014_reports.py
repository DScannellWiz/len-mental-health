import hashlib
import importlib
import io
import sqlite3
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from dataclasses import replace
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

    def move_gad7_record_to_version_two(self):
        definition = replace(app.QUESTIONNAIRES["gad7"], definition_version=2)
        payload = app.serialize_questionnaire_definition(definition)
        payload_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO questionnaire_definition_snapshots (
                    questionnaire_id, definition_version, definition_json, definition_sha256
                ) VALUES (?, ?, ?, ?)
                """,
                ("gad7", 2, payload, payload_hash),
            )
            conn.execute(
                """
                UPDATE questionnaire_submissions
                SET definition_version = 2
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

    def test_workbook_rows_and_metadata_preserve_exact_definition_versions(self):
        self.add_fictional_records()
        self.move_gad7_record_to_version_two()

        workbook = app._analysis_workbook_data()
        daily_versions = {
            (row["assessment_id"], row["entry_date"]): row["definition_version"]
            for row in workbook["Daily Assessments"]
        }
        self.assertEqual(daily_versions[("phq9", "2026-09-01")], 1)
        self.assertEqual(daily_versions[("gad7", "2026-09-10")], 2)
        self.assertEqual(
            {row["question_id"] for row in workbook["Item Responses"] if row["assessment_id"] == "gad7"},
            {f"gad7.item{number}" for number in range(1, 8)},
        )
        metadata = {row["metadata_key"]: row["metadata_value"] for row in workbook["Metadata"]}
        self.assertEqual(metadata["questionnaire_definition_versions"], "phq9:v1|gad7:v1|gad7:v2")
        self.assertEqual(metadata["safety_message"], app.UNIVERSAL_SAFETY_MESSAGE)
        self.assertEqual(metadata["non_diagnostic_notice"], app.NON_DIAGNOSTIC_OUTPUT_NOTICE)
        self.assertEqual(app.ANALYSIS_WORKBOOK_SCHEMA_VERSION, "1.2")

    def test_pdf_identifies_versions_and_keeps_required_safety_copy(self):
        if app.colors is None or app.PILImage is None:
            self.skipTest("PDF report generation requires reportlab and Pillow.")
        try:
            from pypdf import PdfReader
        except ImportError:
            self.skipTest("PDF text validation requires pypdf.")
        self.add_fictional_records()
        self.move_gad7_record_to_version_two()
        target = Path(self.tmp.name) / "fictional-gate-f.pdf"

        app.generate_report("2026-09-01", "2026-09-10", str(target))

        text = " ".join(
            " ".join(page.extract_text() or "" for page in PdfReader(str(target)).pages).split()
        )
        self.assertIn("Questionnaire Definitions", text)
        self.assertIn("GAD-7 v1", text)
        self.assertIn("GAD-7 v2", text)
        self.assertIn(app.NON_DIAGNOSTIC_OUTPUT_NOTICE, text)
        self.assertIn("If you feel unsafe or may act on thoughts of self-harm", text)
        self.assertIn("Len does not monitor responses or provide emergency help", text)
        self.assertNotIn(str(self.db_path), text)

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
        self.assertIn("GAD-7 v1", output.getvalue())


if __name__ == "__main__":
    unittest.main()
