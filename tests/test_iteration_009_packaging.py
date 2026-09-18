import importlib.util
import os
import runpy
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_hygiene_module():
    module_path = ROOT / "packaging" / "verify_release_hygiene.py"
    spec = importlib.util.spec_from_file_location("verify_release_hygiene", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _assert_extended_tcl_paths(runtime_root: Path) -> None:
    expected_root = str(runtime_root.resolve()).replace("\\", "/")
    if sys.platform == "win32":
        expected_root = f"//?/{expected_root}"
    assert os.environ["TCL_LIBRARY"] == f"{expected_root}/_tcl_data"
    assert os.environ["TK_LIBRARY"] == f"{expected_root}/_tk_data"


def test_runtime_hook_uses_tcl_safe_bundle_paths(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path), raising=False)

    runpy.run_path(str(ROOT / "packaging" / "pyi_rth_tkinter_portable.py"))

    _assert_extended_tcl_paths(tmp_path)


def test_portable_entry_reasserts_tcl_paths_before_app_import(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path), raising=False)

    runpy.run_path(
        str(ROOT / "packaging" / "portable_entry.py"),
        run_name="iteration_009_packaging_test",
    )

    _assert_extended_tcl_paths(tmp_path)


class ReleaseHygieneTests(unittest.TestCase):
    def test_rejects_cache_files_and_embedded_build_roots(self):
        verifier = _load_hygiene_module()
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "PHQ9Tracker"
            tkinter_cache = bundle / "_internal" / "tkinter" / "__pycache__"
            tkinter_cache.mkdir(parents=True)
            (tkinter_cache / "constants.cpython-312.pyc").write_bytes(b"compiled")
            (bundle / "PHQ9Tracker.exe").write_bytes(
                b"prefix C:\\Users\\Builder\\release-python-3.12.10 suffix"
            )

            issues = verifier.find_hygiene_issues(
                bundle,
                [r"C:\Users\Builder\release-python-3.12.10"],
            )

        self.assertTrue(any(issue.startswith("Python cache directory:") for issue in issues))
        self.assertTrue(any(issue.startswith("Python bytecode cache:") for issue in issues))
        self.assertTrue(any(issue.startswith("Embedded local build root:") for issue in issues))

    def test_preserves_required_tcl_tk_content(self):
        verifier = _load_hygiene_module()
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "PHQ9Tracker"
            required_files = (
                bundle / "_internal" / "_tcl_data" / "init.tcl",
                bundle / "_internal" / "_tk_data" / "tk.tcl",
                bundle / "_internal" / "_tkinter.pyd",
                bundle / "_internal" / "tcl86t.dll",
                bundle / "_internal" / "tk86t.dll",
            )
            for required_file in required_files:
                required_file.parent.mkdir(parents=True, exist_ok=True)
                required_file.write_bytes(b"required runtime content")

            issues = verifier.find_hygiene_issues(bundle, [])

        self.assertEqual(issues, [])
