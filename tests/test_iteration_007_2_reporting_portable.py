import importlib
import os
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch


project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))
app = importlib.import_module("phq9_tracker.app")


class NormalizedAnalysisWorkbookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.db_path = Path(self.tmp.name) / "synthetic.sqlite"
        os.environ["PHQ9_TRACKER_DB_PATH"] = str(self.db_path)
        app.DB_PATH = self.db_path
        app.init_db()

    def tearDown(self):
        self.tmp.cleanup()

    def test_normalized_workbook_has_stable_relationships_and_atomic_event_rows(self):
        if app.pd is None or app.load_workbook is None:
            self.skipTest("Analysis workbook validation requires pandas and openpyxl.")

        note_text = "Synthetic journal text retained exactly, including commas, line two, and <context> & meaning."
        app.upsert_entry("2026-08-01", [0, 1, 2, 1, 0, 1, 2, 1, 0], notes=note_text, note_tag="Other")
        app.upsert_assessment_entry("gad7", "2026-08-01", [1, 1, 0, 0, 1, 0, 0], notes=note_text, note_tag="Other")
        app.add_event("2026-08-01", "Therapy", "Synthetic morning session", dedupe=False)
        app.add_event("2026-08-01", "Therapy", "Synthetic evening session", dedupe=False)
        app.add_event("2026-08-01", "Physical Therapy", "Shared synthetic description", dedupe=False)
        app.add_event("2026-08-02", "Ketamine infusion", "Synthetic cycle anchor", dedupe=False)
        app.upsert_entry("2026-08-03", [1] * 9)

        output = Path(self.tmp.name) / "analysis.xlsx"
        app.export_analysis_workbook(str(output))

        workbook = app.load_workbook(output, read_only=False, data_only=True)
        expected_sheets = [
            "Daily Assessments",
            "Item Responses",
            "Notes",
            "Treatment Events",
            "Treatment Cycles",
            "Metadata",
            "Daily Summary",
            "14-Day Item Profile",
        ]
        self.assertEqual(workbook.sheetnames, expected_sheets)
        for worksheet in workbook.worksheets:
            self.assertEqual(list(worksheet.merged_cells.ranges), [])
            self.assertEqual(worksheet.freeze_panes, "A2")
            self.assertEqual(worksheet.auto_filter.ref, worksheet.dimensions)
            headers = [cell.value for cell in worksheet[1]]
            self.assertTrue(all(header and " " not in header for header in headers))

        assessment_ws = workbook["Daily Assessments"]
        assessment_headers = [cell.value for cell in assessment_ws[1]]
        assessment_rows = [dict(zip(assessment_headers, values)) for values in assessment_ws.iter_rows(min_row=2, values_only=True)]
        item_ws = workbook["Item Responses"]
        item_headers = [cell.value for cell in item_ws[1]]
        item_rows = [dict(zip(item_headers, values)) for values in item_ws.iter_rows(min_row=2, values_only=True)]
        assessment_ids = {row["assessment_record_id"] for row in assessment_rows}
        self.assertEqual(len(assessment_rows), 3)
        self.assertEqual(len(item_rows), 25)
        self.assertTrue(all(row["assessment_record_id"] in assessment_ids for row in item_rows))
        self.assertTrue(all(str(row["entry_date"]).startswith("2026-") for row in assessment_rows))

        notes_ws = workbook["Notes"]
        notes_headers = [cell.value for cell in notes_ws[1]]
        notes_rows = [dict(zip(notes_headers, values)) for values in notes_ws.iter_rows(min_row=2, values_only=True)]
        self.assertEqual(notes_rows[0]["note_text"], note_text)
        self.assertEqual(notes_rows[0]["daily_record_id"], "day:2026-08-01")

        events_ws = workbook["Treatment Events"]
        event_headers = [cell.value for cell in events_ws[1]]
        event_rows = [dict(zip(event_headers, values)) for values in events_ws.iter_rows(min_row=2, values_only=True)]
        therapy_rows = [row for row in event_rows if row["normalized_event_type"] == "Therapy"]
        self.assertEqual(len(therapy_rows), 2)
        physical_therapy_rows = [row for row in event_rows if row["normalized_event_type"] == "Physical Therapy"]
        self.assertEqual(len(physical_therapy_rows), 1)
        self.assertEqual(len({row["treatment_event_record_id"] for row in event_rows}), 4)

        metadata = {
            key: value
            for key, value, _description in workbook["Metadata"].iter_rows(min_row=2, values_only=True)
        }
        self.assertEqual(metadata["workbook_schema_version"], app.ANALYSIS_WORKBOOK_SCHEMA_VERSION)
        self.assertEqual(metadata["application"], "Len")
        self.assertEqual(metadata["daily_summary_authority"], "derived")
        self.assertGreater(workbook["14-Day Item Profile"].column_dimensions["G"].width, 30)
        workbook.close()

    def test_analysis_workbook_rejects_non_xlsx_target(self):
        with self.assertRaisesRegex(ValueError, "must be saved as an .xlsx"):
            app.export_analysis_workbook(str(Path(self.tmp.name) / "analysis.csv"))


class PortableDatabaseRoutingTests(unittest.TestCase):
    def test_portable_database_is_local_persistent_and_resettable(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            portable_dir = Path(tmp) / "PHQ9Tracker-Portable-test"
            portable_dir.mkdir()
            executable = portable_dir / "PHQ9Tracker.exe"
            executable.touch()
            prior_portable = os.environ.get("PHQ9_TRACKER_PORTABLE")
            prior_explicit = os.environ.pop("PHQ9_TRACKER_DB_PATH", None)
            try:
                os.environ["PHQ9_TRACKER_PORTABLE"] = "1"
                with patch.object(sys, "frozen", True, create=True), patch.object(sys, "executable", str(executable)):
                    portable_db = app.default_db_path()
                self.assertEqual(portable_db, executable.resolve().parent / "phq9_tracker.sqlite")

                app.DB_PATH = portable_db
                app.init_db()
                app.upsert_entry("2026-08-15", [1] * 9, notes="Synthetic portable persistence test")
                with closing(sqlite3.connect(portable_db)) as conn:
                    self.assertEqual(conn.execute("SELECT COUNT(*) FROM assessment_entries").fetchone()[0], 1)

                portable_db.unlink()
                app.init_db()
                with closing(sqlite3.connect(portable_db)) as conn:
                    self.assertEqual(conn.execute("SELECT COUNT(*) FROM assessment_entries").fetchone()[0], 0)
                    self.assertEqual(conn.execute("SELECT COUNT(*) FROM treatment_events").fetchone()[0], 0)
            finally:
                if prior_portable is None:
                    os.environ.pop("PHQ9_TRACKER_PORTABLE", None)
                else:
                    os.environ["PHQ9_TRACKER_PORTABLE"] = prior_portable
                if prior_explicit is not None:
                    os.environ["PHQ9_TRACKER_DB_PATH"] = prior_explicit


if __name__ == "__main__":
    unittest.main()
