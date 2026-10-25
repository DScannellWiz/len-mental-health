"""Harmless characterization of workbook image parsing, not an exploit test."""

import importlib
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chartsheet.chartsheet import Chartsheet
from openpyxl.drawing.image import Image as WorkbookImage
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
app = importlib.import_module("phq9_tracker.app")


class SpreadsheetImageReachabilityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.db_patch = patch.object(app, "DB_PATH", self.root / "fictional.sqlite")
        self.db_patch.start()
        self.addCleanup(self.db_patch.stop)
        app.init_db()

    def make_workbook(self, image_location):
        """Generate ordinary PNG bytes and fictional rows; never external input."""
        image_path = self.root / "ordinary.png"
        Image.new("RGB", (8, 8), "blue").save(image_path, "PNG")
        workbook = Workbook()
        self.addCleanup(workbook.close)
        sheet = workbook.active
        sheet.title = "Fictional check-ins"
        sheet.append(["Date", *(f"Item {i}" for i in range(1, 10)), "Notes"])
        sheet.append(["2026-10-01", *([1] * 9), "Fictional probe only"])
        destination = self.root / f"{image_location}.xlsx"
        if image_location == "worksheet":
            sheet.add_image(WorkbookImage(str(image_path)), "L1")
            workbook.save(destination)
        else:
            chartsheet = workbook.create_chartsheet("Ordinary chart")
            chart = BarChart()
            chart.add_data(Reference(sheet, min_col=2, max_col=2, min_row=1, max_row=2), titles_from_data=True)
            chartsheet.add_chart(chart)
            original = Chartsheet.to_tree

            def include_ordinary_picture(instance, *args, **kwargs):
                tree = original(instance, *args, **kwargs)
                # Chartsheet has no add_image convenience API. Add an ordinary
                # DrawingML picture to its serializer-created drawing instead.
                instance._drawing.images.append(WorkbookImage(str(image_path)))
                return tree

            with patch.object(Chartsheet, "to_tree", include_ordinary_picture):
                workbook.save(destination)
        return destination

    def assert_import_preserves_fictional_values(self, destination, expected_opens):
        # The spy delegates to the real parser; it neither supplies fake images
        # nor changes the application's loading flags or accepted formats.
        with patch.object(Image, "open", wraps=Image.open) as opened:
            self.assertEqual(app.import_spreadsheet(str(destination)), 1)
        self.assertEqual(opened.call_count, expected_opens)
        for call in opened.call_args_list:
            stream = call.args[0]
            self.assertEqual(stream.getvalue()[:8], b"\x89PNG\r\n\x1a\n")
        with sqlite3.connect(app.DB_PATH) as connection:
            row = connection.execute(
                "SELECT entry_date, total, notes FROM phq9_entries"
            ).fetchone()
        self.assertEqual(row, ("2026-10-01", 9, "Fictional probe only"))

    def test_ordinary_read_only_worksheet_skips_embedded_image(self):
        self.assert_import_preserves_fictional_values(self.make_workbook("worksheet"), 0)

    def test_chartsheet_image_reaches_real_pillow_open_during_import(self):
        self.assert_import_preserves_fictional_values(self.make_workbook("chartsheet"), 1)


if __name__ == "__main__":
    unittest.main()
