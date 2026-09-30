import tempfile
import unittest

from tracker.models import JobApplication
from tracker.storage import add, delete, list_all, update_notes, update_status


def _db():
    return tempfile.mktemp(suffix=".db")


def _app(**kwargs):
    defaults = {"company": "Acme", "role": "Engineer", "applied_date": "2024-01-01"}
    defaults.update(kwargs)
    return JobApplication(**defaults)


class TestStorage(unittest.TestCase):
    def test_add_and_list(self):
        db = _db()
        new_id = add(_app(), db)
        self.assertIsInstance(new_id, int)
        apps = list_all(db_path=db)
        self.assertEqual(len(apps), 1)
        self.assertEqual(apps[0].company, "Acme")
        self.assertEqual(apps[0].id, new_id)

    def test_update_status(self):
        db = _db()
        app_id = add(_app(), db)
        ok = update_status(app_id, "interview", db)
        self.assertTrue(ok)
        apps = list_all(db_path=db)
        self.assertEqual(apps[0].status, "interview")

    def test_update_status_nonexistent(self):
        db = _db()
        ok = update_status(999, "interview", db)
        self.assertFalse(ok)

    def test_update_notes(self):
        db = _db()
        app_id = add(_app(), db)
        ok = update_notes(app_id, "Great team!", db)
        self.assertTrue(ok)
        apps = list_all(db_path=db)
        self.assertEqual(apps[0].notes, "Great team!")

    def test_delete(self):
        db = _db()
        app_id = add(_app(), db)
        ok = delete(app_id, db)
        self.assertTrue(ok)
        self.assertEqual(len(list_all(db_path=db)), 0)

    def test_delete_nonexistent(self):
        db = _db()
        self.assertFalse(delete(999, db))

    def test_list_with_status_filter(self):
        db = _db()
        add(_app(status="applied"), db)
        add(_app(status="rejected"), db)
        active = list_all(status_filter="applied", db_path=db)
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].status, "applied")

    def test_multiple_apps_ordered_desc(self):
        db = _db()
        add(_app(applied_date="2024-01-01"), db)
        add(_app(applied_date="2024-03-01"), db)
        apps = list_all(db_path=db)
        self.assertGreater(apps[0].applied_date, apps[1].applied_date)


class TestModel(unittest.TestCase):
    def test_is_active(self):
        self.assertTrue(JobApplication("A", "B", status="applied").is_active())
        self.assertTrue(JobApplication("A", "B", status="interview").is_active())
        self.assertFalse(JobApplication("A", "B", status="rejected").is_active())
        self.assertFalse(JobApplication("A", "B", status="withdrawn").is_active())


if __name__ == "__main__":
    unittest.main()
