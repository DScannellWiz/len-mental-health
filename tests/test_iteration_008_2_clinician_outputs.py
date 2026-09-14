import importlib
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))
app = importlib.import_module("phq9_tracker.app")


class Iteration0082ClinicianOutputTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.previous_db_path = app.DB_PATH
        self.db_path = Path(self.tmp.name) / "fictional.sqlite"
        app.DB_PATH = self.db_path
        app.init_db()

    def tearDown(self):
        app.DB_PATH = self.previous_db_path
        self.tmp.cleanup()

    def populate_profile_and_events(self):
        for day in range(1, 15):
            phq_items = [
                int(day <= 12),
                int(day <= 7),
                int(day == 1),
                0,
                0,
                0,
                0,
                0,
                0,
            ]
            app.upsert_entry(f"2026-08-{day:02d}", phq_items)
        for day in (1, 7, 14):
            app.upsert_assessment_entry("gad7", f"2026-08-{day:02d}", [1, 0, 0, 0, 0, 0, 0])
        shared_description = "Shared fictional rehabilitation visit"
        app.add_event("2026-08-11", "Therapy", shared_description, dedupe=False)
        app.add_event("2026-08-11", "Physical Therapy", shared_description, dedupe=False)

    def test_item_profile_reuses_counts_coverage_and_frequency_thresholds(self):
        self.populate_profile_and_events()

        rows = app.build_14_day_item_profile("2026-08-14")
        phq = [row for row in rows if row["assessment_id"] == "phq9"]
        gad = [row for row in rows if row["assessment_id"] == "gad7"]

        self.assertEqual(len(rows), 16)
        self.assertEqual(
            [(row["symptom_present_days"], row["recorded_day_coverage"], row["frequency_score"]) for row in phq[:3]],
            [(12, 14, 3), (7, 14, 2), (1, 14, 1)],
        )
        self.assertEqual(
            (gad[0]["symptom_present_days"], gad[0]["recorded_day_coverage"], gad[0]["frequency_score"]),
            (3, 3, 1),
        )
        self.assertTrue(all(row["calendar_days"] == 14 for row in rows))

    def test_pdf_and_workbook_render_profiles_and_distinct_same_day_event_types(self):
        if app.colors is None or app.PILImage is None or app.load_workbook is None:
            self.skipTest("PDF and workbook validation dependencies are required.")
        try:
            from pypdf import PdfReader
        except ImportError:
            self.skipTest("PDF text validation requires pypdf.")
        self.populate_profile_and_events()
        pdf_path = Path(self.tmp.name) / "fictional-report.pdf"
        workbook_path = Path(self.tmp.name) / "fictional-analysis.xlsx"

        app.generate_report("2026-08-01", "2026-08-14", str(pdf_path))
        app.export_analysis_workbook(str(workbook_path))

        text = " ".join(
            " ".join(page.extract_text() or "" for page in PdfReader(str(pdf_path)).pages).split()
        )
        self.assertIn("Len Clinician Discussion Report", text)
        self.assertIn("Current 14-Day Item Profile", text)
        self.assertIn("Present days", text)
        self.assertIn("14 of 14", text)
        self.assertIn("3 of 14", text)
        self.assertIn("Physical Therapy", text)
        self.assertIn("Therapy", text)
        self.assertEqual(text.count("Shared fictional rehabilitation visit"), 2)

        workbook = app.load_workbook(workbook_path, read_only=True, data_only=True)
        self.assertIn("14-Day Item Profile", workbook.sheetnames)
        profile_sheet = workbook["14-Day Item Profile"]
        profile_headers = [cell.value for cell in profile_sheet[1]]
        profile_rows = [dict(zip(profile_headers, values)) for values in profile_sheet.iter_rows(min_row=2, values_only=True)]
        self.assertEqual(len(profile_rows), 16)
        self.assertEqual(profile_rows[0]["recorded_day_coverage"], 14)
        events_sheet = workbook["Treatment Events"]
        event_headers = [cell.value for cell in events_sheet[1]]
        event_rows = [dict(zip(event_headers, values)) for values in events_sheet.iter_rows(min_row=2, values_only=True)]
        matching = [row for row in event_rows if row["description"] == "Shared fictional rehabilitation visit"]
        self.assertEqual({row["event_type"] for row in matching}, {"Therapy", "Physical Therapy"})
        self.assertEqual({row["normalized_event_type"] for row in matching}, {"Therapy", "Physical Therapy"})
        workbook.close()
        self.assertFalse(pdf_path.with_suffix(".csv").exists())
        self.assertFalse(workbook_path.with_suffix(".csv").exists())


class Iteration0082OutputDiscoveryTests(unittest.TestCase):
    def test_common_source_folder_is_created_and_collisions_do_not_overwrite(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp, patch.object(app, "REPORTS_DIR", Path(tmp) / "reports"):
            output_dir = app.generated_output_dir(create=True)
            self.assertTrue(output_dir.is_dir())
            first = app.next_available_output_path("report.pdf")
            first.touch()
            second = app.next_available_output_path("report.pdf")
            self.assertEqual(second, output_dir / "report_2.pdf")

    def test_portable_output_folder_stays_beside_executable(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            executable = Path(tmp) / "PHQ9Tracker.exe"
            with patch.object(sys, "frozen", True, create=True), patch.object(sys, "executable", str(executable)), patch.dict(
                os.environ, {"PHQ9_TRACKER_PORTABLE": "1"}
            ):
                self.assertEqual(app.generated_output_dir(), executable.resolve().parent / "reports")

    def test_open_choice_is_optional_and_open_failure_preserves_saved_path(self):
        saved_path = Path("C:/fictional/reports/report.pdf")
        with patch.object(app.messagebox, "askyesno", return_value=False), patch.object(app, "open_in_default_application") as opener:
            app.offer_to_open_generated_file(saved_path, "PDF report")
            opener.assert_not_called()

        with patch.object(app.messagebox, "askyesno", return_value=True), patch.object(
            app, "open_in_default_application", side_effect=OSError("No association")
        ), patch.object(app.messagebox, "showwarning") as warning:
            app.offer_to_open_generated_file(saved_path, "PDF report")
            self.assertIn(str(saved_path), warning.call_args.args[1])
            self.assertIn("saved successfully", warning.call_args.args[1])

    def test_review_generators_use_common_paths_and_offer_open_without_launching(self):
        pdf_path = Path("C:/fictional/reports/report.pdf")
        workbook_path = Path("C:/fictional/reports/analysis.xlsx")
        target = object()
        with patch.object(app, "available_report_date_range", return_value=("2026-08-01", "2026-08-14")), patch.object(
            app, "next_available_output_path", return_value=pdf_path
        ) as next_path, patch.object(app, "generate_report") as generate, patch.object(app, "offer_to_open_generated_file") as offer:
            app.PHQ9App.create_report(target)
            next_path.assert_called_once_with("Len_Report_2026-08-01_to_2026-08-14.pdf")
            generate.assert_called_once_with("2026-08-01", "2026-08-14", str(pdf_path))
            offer.assert_called_once_with(pdf_path, "PDF report")

        with patch.object(app, "next_available_output_path", return_value=workbook_path), patch.object(
            app, "export_analysis_workbook"
        ) as export, patch.object(app, "offer_to_open_generated_file") as offer, patch.object(app, "date") as current_date:
            current_date.today.return_value.isoformat.return_value = "2026-09-10"
            app.PHQ9App.export_analysis_file(target)
            app.next_available_output_path.assert_called_once_with("Len_Analysis_2026-09-10.xlsx")
            export.assert_called_once_with(str(workbook_path))
            offer.assert_called_once_with(workbook_path, "Analysis workbook")

    def test_reports_folder_action_creates_folder_and_handles_open_error(self):
        folder = Path("C:/fictional/reports")
        with patch.object(app, "generated_output_dir", return_value=folder) as directory, patch.object(
            app, "open_in_default_application", side_effect=OSError("Explorer unavailable")
        ), patch.object(app.messagebox, "showwarning") as warning:
            app.PHQ9App.open_reports_folder(object())
            directory.assert_called_once_with(create=True)
            self.assertIn(str(folder), warning.call_args.args[1])

    def test_output_folder_creation_failure_is_reported_calmly(self):
        with patch.object(app, "next_available_output_path", side_effect=OSError("Folder unavailable")), patch.object(
            app.messagebox, "showerror"
        ) as error:
            app.PHQ9App.export_analysis_file(object())
            error.assert_called_once_with("Analysis export failed", "Folder unavailable")

        with patch.object(app, "generated_output_dir", side_effect=OSError("Folder unavailable")), patch.object(
            app.messagebox, "showwarning"
        ) as warning:
            app.PHQ9App.open_reports_folder(object())
            self.assertIn("Folder unavailable", warning.call_args.args[1])

    def test_spinbox_style_uses_compact_internal_padding(self):
        target = Mock()
        style = Mock()
        with patch.object(app.ttk, "Style", return_value=style):
            app.PHQ9App.configure_ui_styles(target)
        style.configure.assert_any_call("TSpinbox", padding=(2, 0), arrowsize=14)


if __name__ == "__main__":
    unittest.main()
