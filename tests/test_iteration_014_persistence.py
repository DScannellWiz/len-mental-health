import hashlib
import importlib
import shutil
import sqlite3
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))
app = importlib.import_module("phq9_tracker.app")


class Iteration014PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.db_path = Path(self.tmp.name) / "iteration014.sqlite"

    def tearDown(self):
        self.tmp.cleanup()

    def test_c1_migration_is_idempotent_and_stores_exact_builtin_snapshots(self):
        app.init_db(self.db_path)
        app.init_db(self.db_path)

        with sqlite3.connect(self.db_path) as conn:
            ledger = conn.execute(
                "SELECT migration_id, application_id, checksum_sha256 FROM schema_migrations"
            ).fetchall()
            snapshots = conn.execute(
                """
                SELECT questionnaire_id, definition_version, definition_json, definition_sha256
                FROM questionnaire_definition_snapshots
                ORDER BY questionnaire_id, definition_version
                """
            ).fetchall()

        self.assertEqual(
            ledger,
            [
                (
                    app.QUESTIONNAIRE_SNAPSHOT_MIGRATION.migration_id,
                    "len",
                    app.QUESTIONNAIRE_SNAPSHOT_MIGRATION.checksum,
                ),
                (
                    app.NORMALIZED_QUESTIONNAIRE_STORAGE_MIGRATION.migration_id,
                    "len",
                    app.NORMALIZED_QUESTIONNAIRE_STORAGE_MIGRATION.checksum,
                ),
            ],
        )
        self.assertEqual(
            [(row[0], row[1]) for row in snapshots],
            [("gad7", 1), ("gad7", 2), ("phq9", 1), ("phq9", 2)],
        )
        for questionnaire_id, definition_version, payload, recorded_hash in snapshots:
            expected = (
                app.QUESTIONNAIRES[questionnaire_id]
                if definition_version == 2
                else app.LEGACY_BUILTIN_DEFINITIONS[questionnaire_id]
            )
            self.assertEqual(recorded_hash, hashlib.sha256(payload.encode("utf-8")).hexdigest())
            self.assertEqual(payload, app.serialize_questionnaire_definition(expected))
            self.assertEqual(
                app.load_questionnaire_definition_snapshot(questionnaire_id, definition_version, self.db_path),
                expected,
            )

    def test_snapshot_and_migration_records_are_database_immutable(self):
        app.init_db(self.db_path)
        with sqlite3.connect(self.db_path) as conn:
            with self.assertRaisesRegex(sqlite3.IntegrityError, "snapshots are immutable"):
                conn.execute(
                    "UPDATE questionnaire_definition_snapshots SET definition_json = '{}' WHERE questionnaire_id = 'phq9'"
                )
            with self.assertRaisesRegex(sqlite3.IntegrityError, "snapshots are immutable"):
                conn.execute("DELETE FROM questionnaire_definition_snapshots WHERE questionnaire_id = 'phq9'")
            with self.assertRaisesRegex(sqlite3.IntegrityError, "migration records are immutable"):
                conn.execute("DELETE FROM schema_migrations")

    def test_reusing_definition_version_with_different_bytes_fails_and_rolls_back(self):
        app.init_db(self.db_path)
        conflicting = replace(app.QUESTIONNAIRES["phq9"], display_name="Changed meaning")
        with sqlite3.connect(self.db_path) as conn:
            with self.assertRaisesRegex(RuntimeError, "definition version conflict"):
                app.apply_schema_migrations(
                    conn,
                    definitions=(conflicting, app.QUESTIONNAIRES["gad7"]),
                )
        self.assertEqual(
            app.load_questionnaire_definition_snapshot("phq9", 2, self.db_path),
            app.QUESTIONNAIRES["phq9"],
        )

    def test_forced_migration_failure_rolls_back_schema_and_ledger(self):
        failing = app.SchemaMigration(
            migration_id="len.test.forced_failure",
            statements=(
                "CREATE TABLE should_not_survive (id INTEGER PRIMARY KEY)",
                "INSERT INTO missing_table VALUES (1)",
            ),
        )
        with sqlite3.connect(self.db_path) as conn:
            with self.assertRaises(sqlite3.OperationalError):
                app.apply_schema_migrations(conn, migrations=(failing,), definitions=())
            tables = {
                row[0]
                for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
            }
        self.assertNotIn("should_not_survive", tables)
        self.assertNotIn("schema_migrations", tables)

    def test_checksum_drift_and_unknown_newer_migrations_fail_closed(self):
        app.init_db(self.db_path)
        changed = app.SchemaMigration(
            migration_id=app.QUESTIONNAIRE_SNAPSHOT_MIGRATION.migration_id,
            statements=(*app.QUESTIONNAIRE_SNAPSHOT_MIGRATION.statements, "SELECT 1"),
        )
        with sqlite3.connect(self.db_path) as conn:
            with self.assertRaisesRegex(RuntimeError, "checksum mismatch"):
                app.apply_schema_migrations(
                    conn,
                    migrations=(changed, app.NORMALIZED_QUESTIONNAIRE_STORAGE_MIGRATION),
                    definitions=(),
                )

        future_path = Path(self.tmp.name) / "future.sqlite"
        app.init_db(future_path)
        with sqlite3.connect(future_path) as conn:
            conn.execute("DROP TRIGGER schema_migrations_no_delete")
            conn.execute(
                """
                INSERT INTO schema_migrations (migration_id, application_id, checksum_sha256)
                VALUES ('len.999.future', 'len', ?)
                """,
                ("f" * 64,),
            )
            conn.commit()
        with sqlite3.connect(future_path) as conn:
            with self.assertRaisesRegex(RuntimeError, "unsupported schema migration"):
                app.apply_schema_migrations(conn)

    def test_existing_legacy_database_remains_readable_and_rows_are_preserved(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE phq9_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_date TEXT NOT NULL UNIQUE,
                    item1 INTEGER NOT NULL, item2 INTEGER NOT NULL, item3 INTEGER NOT NULL,
                    item4 INTEGER NOT NULL, item5 INTEGER NOT NULL, item6 INTEGER NOT NULL,
                    item7 INTEGER NOT NULL, item8 INTEGER NOT NULL, item9 INTEGER NOT NULL,
                    total INTEGER NOT NULL, severity TEXT NOT NULL, notes TEXT DEFAULT '',
                    source TEXT DEFAULT 'manual', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                INSERT INTO phq9_entries (
                    entry_date, item1, item2, item3, item4, item5, item6, item7, item8, item9,
                    total, severity, notes, source
                ) VALUES ('2026-01-02', 0, 1, 2, 3, 0, 1, 2, 3, 0, 12, 'Moderate', 'keep me', 'import')
                """
            )
            conn.commit()

        app.init_db(self.db_path)
        with sqlite3.connect(self.db_path) as conn:
            legacy = conn.execute(
                "SELECT entry_date, item1, item2, item3, total, severity, notes, source FROM phq9_entries"
            ).fetchone()
            compatibility = conn.execute(
                "SELECT assessment_id, entry_date, item1, item2, item3, total, severity, notes, source FROM assessment_entries"
            ).fetchone()
            normalized = conn.execute(
                """
                SELECT questionnaire_id, definition_version, entry_date, total_score, severity, notes, source
                FROM questionnaire_submissions
                """
            ).fetchone()
        self.assertEqual(legacy, ("2026-01-02", 0, 1, 2, 12, "Moderate", "keep me", "import"))
        self.assertEqual(compatibility, ("phq9", "2026-01-02", 0, 1, 2, 12, "Moderate", "keep me", "import"))
        self.assertEqual(normalized, ("phq9", 1, "2026-01-02", 12, "Moderate", "keep me", "import"))

    def test_closed_database_backup_can_be_restored_and_migrated_again(self):
        backup_path = Path(self.tmp.name) / "pre_iteration_014_backup.sqlite"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE phq9_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_date TEXT NOT NULL UNIQUE,
                    item1 INTEGER NOT NULL, item2 INTEGER NOT NULL, item3 INTEGER NOT NULL,
                    item4 INTEGER NOT NULL, item5 INTEGER NOT NULL, item6 INTEGER NOT NULL,
                    item7 INTEGER NOT NULL, item8 INTEGER NOT NULL, item9 INTEGER NOT NULL,
                    total INTEGER NOT NULL, severity TEXT NOT NULL, notes TEXT DEFAULT '',
                    source TEXT DEFAULT 'manual', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                INSERT INTO phq9_entries (
                    entry_date, item1, item2, item3, item4, item5, item6, item7, item8, item9,
                    total, severity, notes, source, created_at, updated_at
                ) VALUES (
                    '2026-01-03', 1, 0, 1, 0, 1, 0, 1, 0, 1,
                    5, 'Mild', 'fictional restore fixture', 'import',
                    '2026-01-03 08:00:00', '2026-01-03 09:00:00'
                )
                """
            )
            conn.commit()

        shutil.copy2(self.db_path, backup_path)
        app.init_db(self.db_path)

        shutil.copy2(backup_path, self.db_path)
        app.init_db(self.db_path)

        with sqlite3.connect(self.db_path) as conn:
            legacy = conn.execute(
                "SELECT entry_date, item1, item9, total, severity, notes, source, created_at, updated_at "
                "FROM phq9_entries"
            ).fetchall()
            compatibility = conn.execute(
                "SELECT assessment_id, entry_date, item1, item9, total, severity, notes, source, "
                "created_at, updated_at FROM assessment_entries"
            ).fetchall()
            normalized = conn.execute(
                "SELECT questionnaire_id, definition_version, entry_date, total_score, severity, notes, "
                "source, created_at, updated_at FROM questionnaire_submissions"
            ).fetchall()
            response_count = conn.execute("SELECT COUNT(*) FROM questionnaire_responses").fetchone()[0]
            migration_ids = [row[0] for row in conn.execute("SELECT migration_id FROM schema_migrations")]

        self.assertEqual(
            legacy,
            [("2026-01-03", 1, 1, 5, "Mild", "fictional restore fixture", "import", "2026-01-03 08:00:00", "2026-01-03 09:00:00")],
        )
        self.assertEqual(
            compatibility,
            [("phq9", "2026-01-03", 1, 1, 5, "Mild", "fictional restore fixture", "import", "2026-01-03 08:00:00", "2026-01-03 09:00:00")],
        )
        self.assertEqual(
            normalized,
            [("phq9", 1, "2026-01-03", 5, "Mild", "fictional restore fixture", "import", "2026-01-03 08:00:00", "2026-01-03 09:00:00")],
        )
        self.assertEqual(response_count, 9)
        self.assertEqual(
            migration_ids,
            [
                app.QUESTIONNAIRE_SNAPSHOT_MIGRATION.migration_id,
                app.NORMALIZED_QUESTIONNAIRE_STORAGE_MIGRATION.migration_id,
            ],
        )

    def test_c2_backfill_is_idempotent_and_preserves_zero_as_a_response(self):
        app.init_db(self.db_path)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO assessment_entries (
                    assessment_id, entry_date, item1, item2, item3, item4, item5, item6, item7,
                    item8, item9, total, severity, notes, note_tag, source, created_at, updated_at
                ) VALUES (
                    'gad7', '2026-02-03', 0, 1, 2, 3, 0, 1, 2,
                    NULL, NULL, 9, 'Mild', 'exact note', 'Work', 'import',
                    '2026-02-03 08:00:00', '2026-02-03 09:00:00'
                )
                """
            )
            conn.commit()

        app.init_db(self.db_path)
        app.init_db(self.db_path)
        with sqlite3.connect(self.db_path) as conn:
            submission = conn.execute(
                """
                SELECT id, questionnaire_id, definition_version, entry_date, total_score, severity,
                       notes, note_tag, source, created_at, updated_at
                FROM questionnaire_submissions
                """
            ).fetchone()
            responses = conn.execute(
                """
                SELECT question_id, response_order, response_value_json, response_score
                FROM questionnaire_responses
                WHERE submission_id = ? ORDER BY response_order
                """,
                (submission[0],),
            ).fetchall()
        self.assertEqual(
            submission[1:],
            (
                "gad7", 1, "2026-02-03", 9, "Mild", "exact note", "Work", "import",
                "2026-02-03 08:00:00", "2026-02-03 09:00:00",
            ),
        )
        self.assertEqual(len(responses), 7)
        self.assertEqual(responses[0], ("gad7.item1", 1, "0", 0))
        self.assertNotIn(None, [response[2] for response in responses])

    def test_c2_forced_reconciliation_failure_rolls_back_tables_and_ledger_record(self):
        with sqlite3.connect(self.db_path) as conn:
            app.apply_schema_migrations(
                conn,
                migrations=(app.QUESTIONNAIRE_SNAPSHOT_MIGRATION,),
            )
            conn.execute(
                """
                CREATE TABLE assessment_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assessment_id TEXT NOT NULL, entry_date TEXT NOT NULL,
                    item1 INTEGER NOT NULL, item2 INTEGER NOT NULL, item3 INTEGER NOT NULL,
                    item4 INTEGER NOT NULL, item5 INTEGER NOT NULL, item6 INTEGER NOT NULL,
                    item7 INTEGER NOT NULL, item8 INTEGER, item9 INTEGER,
                    total INTEGER NOT NULL, severity TEXT NOT NULL, notes TEXT, note_tag TEXT,
                    source TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
                    UNIQUE (assessment_id, entry_date)
                )
                """
            )
            conn.execute(
                """
                INSERT INTO assessment_entries (
                    assessment_id, entry_date, item1, item2, item3, item4, item5, item6, item7,
                    item8, item9, total, severity, notes, note_tag, source, created_at, updated_at
                ) VALUES (
                    'gad7', '2026-03-04', 0, 0, 0, 0, 0, 0, 0,
                    NULL, NULL, 99, 'Minimal', '', '', 'manual',
                    '2026-03-04 08:00:00', '2026-03-04 08:00:00'
                )
                """
            )
            conn.commit()
            with self.assertRaisesRegex(RuntimeError, "Legacy total does not reconcile"):
                app.apply_schema_migrations(conn)
            tables = {
                row[0]
                for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
            }
            ledger_ids = [row[0] for row in conn.execute("SELECT migration_id FROM schema_migrations")]
        self.assertNotIn("questionnaire_submissions", tables)
        self.assertNotIn("questionnaire_responses", tables)
        self.assertEqual(ledger_ids, [app.QUESTIONNAIRE_SNAPSHOT_MIGRATION.migration_id])

    def test_c2_constraints_enforce_one_submission_per_questionnaire_date(self):
        app.init_db(self.db_path)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            values = ("phq9", 1, "2026-04-05", 0, "Minimal", "", "", "manual", "now", "now")
            conn.execute(
                """
                INSERT INTO questionnaire_submissions (
                    questionnaire_id, definition_version, entry_date, total_score, severity,
                    notes, note_tag, source, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                values,
            )
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute(
                    """
                    INSERT INTO questionnaire_submissions (
                        questionnaire_id, definition_version, entry_date, total_score, severity,
                        notes, note_tag, source, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    values,
                )
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute(
                    """
                    INSERT INTO questionnaire_submissions (
                        questionnaire_id, definition_version, entry_date, total_score, severity,
                        notes, note_tag, source, created_at, updated_at
                    ) VALUES ('missing', 1, '2026-04-06', 0, '', '', '', 'manual', 'now', 'now')
                    """
                )

    def test_c3_reads_verified_normalized_rows_before_legacy_compatibility_rows(self):
        app.init_db(self.db_path)
        previous_db_path = app.DB_PATH
        app.DB_PATH = self.db_path
        try:
            app.upsert_assessment_entry("gad7", "2026-05-06", [0, 1, 2, 3, 0, 1, 2], notes="original")
            app.init_db(self.db_path)
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "UPDATE assessment_entries SET notes = 'legacy changed after backfill' WHERE assessment_id = 'gad7'"
                )
                conn.commit()
            rows = app.fetch_assessment_entries("gad7")
            profile = app.build_14_day_item_profile("2026-05-06", ["gad7"])
        finally:
            app.DB_PATH = previous_db_path
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].items, [0, 1, 2, 3, 0, 1, 2])
        self.assertEqual(rows[0].notes, "original")
        self.assertEqual(rows[0].definition_version, 2)
        self.assertEqual({record["definition_version"] for record in profile}, {2})

    def test_c3_falls_back_for_an_unmigrated_legacy_database(self):
        app.init_db(self.db_path)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DROP TABLE questionnaire_responses")
            conn.execute("DROP TABLE questionnaire_submissions")
            conn.execute("DELETE FROM assessment_entries")
            conn.execute(
                """
                INSERT INTO assessment_entries (
                    assessment_id, entry_date, item1, item2, item3, item4, item5, item6, item7,
                    item8, item9, total, severity, notes, note_tag, source
                ) VALUES ('gad7', '2026-06-07', 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 'Minimal', 'legacy', '', 'manual')
                """
            )
            conn.commit()
        previous_db_path = app.DB_PATH
        app.DB_PATH = self.db_path
        try:
            rows = app.fetch_assessment_entries("gad7")
        finally:
            app.DB_PATH = previous_db_path
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].entry_date, "2026-06-07")
        self.assertEqual(rows[0].items, [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(rows[0].notes, "legacy")
        self.assertIsNone(rows[0].definition_version)

    def test_c4_phq9_save_updates_all_compatibility_stores_atomically(self):
        app.init_db(self.db_path)
        previous_db_path = app.DB_PATH
        app.DB_PATH = self.db_path
        try:
            app.upsert_entry("2026-07-08", [0, 1, 2, 3, 0, 1, 2, 3, 0], notes="kept", note_tag="Work")
            rows = app.fetch_assessment_entries("phq9")
        finally:
            app.DB_PATH = previous_db_path
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].total, 12)
        with sqlite3.connect(self.db_path) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM phq9_entries").fetchone()[0], 1)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM assessment_entries").fetchone()[0], 1)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM questionnaire_submissions").fetchone()[0], 1)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM questionnaire_responses").fetchone()[0], 9)

    def test_c4_normalized_failure_rolls_back_legacy_and_normalized_updates(self):
        app.init_db(self.db_path)
        previous_db_path = app.DB_PATH
        app.DB_PATH = self.db_path
        try:
            app.upsert_entry("2026-08-09", [1] * 9, notes="original")
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    CREATE TRIGGER force_normalized_response_failure
                    BEFORE INSERT ON questionnaire_responses
                    BEGIN
                        SELECT RAISE(ABORT, 'forced normalized failure');
                    END
                    """
                )
                conn.commit()
            with self.assertRaisesRegex(sqlite3.IntegrityError, "forced normalized failure"):
                app.upsert_entry("2026-08-09", [2] * 9, notes="must roll back")
        finally:
            app.DB_PATH = previous_db_path

        with sqlite3.connect(self.db_path) as conn:
            phq9 = conn.execute("SELECT item1, total, notes FROM phq9_entries").fetchone()
            compatibility = conn.execute("SELECT item1, total, notes FROM assessment_entries").fetchone()
            normalized = conn.execute(
                "SELECT total_score, notes FROM questionnaire_submissions"
            ).fetchone()
            responses = conn.execute(
                "SELECT response_value_json FROM questionnaire_responses ORDER BY response_order"
            ).fetchall()
        self.assertEqual(phq9, (1, 9, "original"))
        self.assertEqual(compatibility, (1, 9, "original"))
        self.assertEqual(normalized, (9, "original"))
        self.assertEqual(responses, [("1",)] * 9)

    def test_d1_multi_questionnaire_save_is_one_transaction(self):
        app.init_db(self.db_path)
        previous_db_path = app.DB_PATH
        app.DB_PATH = self.db_path
        try:
            app.upsert_questionnaire_entries(
                "2026-09-10",
                {"phq9": [1] * 9, "gad7": [2] * 7},
                notes="both",
                note_tag="Health",
            )
        finally:
            app.DB_PATH = previous_db_path
        with sqlite3.connect(self.db_path) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM phq9_entries").fetchone()[0], 1)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM assessment_entries").fetchone()[0], 2)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM questionnaire_submissions").fetchone()[0], 2)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM questionnaire_responses").fetchone()[0], 16)

    def test_d1_second_questionnaire_failure_rolls_back_entire_batch(self):
        app.init_db(self.db_path)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TRIGGER fail_gad7_submission
                BEFORE INSERT ON questionnaire_submissions
                WHEN NEW.questionnaire_id = 'gad7'
                BEGIN
                    SELECT RAISE(ABORT, 'forced gad7 failure');
                END
                """
            )
            conn.commit()
        previous_db_path = app.DB_PATH
        app.DB_PATH = self.db_path
        try:
            with self.assertRaisesRegex(sqlite3.IntegrityError, "forced gad7 failure"):
                app.upsert_questionnaire_entries(
                    "2026-09-11",
                    {"phq9": [1] * 9, "gad7": [2] * 7},
                )
        finally:
            app.DB_PATH = previous_db_path
        with sqlite3.connect(self.db_path) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM phq9_entries").fetchone()[0], 0)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM assessment_entries").fetchone()[0], 0)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM questionnaire_submissions").fetchone()[0], 0)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM questionnaire_responses").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
