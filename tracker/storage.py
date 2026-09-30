"""SQLite storage for job applications."""
import sqlite3
from contextlib import contextmanager

from .models import JobApplication

DEFAULT_DB = "jobs.db"


@contextmanager
def _conn(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(db_path: str = DEFAULT_DB) -> None:
    with _conn(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                company      TEXT    NOT NULL,
                role         TEXT    NOT NULL,
                status       TEXT    NOT NULL DEFAULT 'applied',
                applied_date TEXT    NOT NULL,
                url          TEXT    DEFAULT '',
                notes        TEXT    DEFAULT ''
            )
        """)


def add(app: JobApplication, db_path: str = DEFAULT_DB) -> int:
    init_db(db_path)
    with _conn(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO applications (company, role, status, applied_date, url, notes) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (app.company, app.role, app.status, app.applied_date, app.url, app.notes),
        )
        return cur.lastrowid


def update_status(app_id: int, status: str, db_path: str = DEFAULT_DB) -> bool:
    init_db(db_path)
    with _conn(db_path) as conn:
        cur = conn.execute(
            "UPDATE applications SET status = ? WHERE id = ?", (status, app_id)
        )
        return cur.rowcount > 0


def update_notes(app_id: int, notes: str, db_path: str = DEFAULT_DB) -> bool:
    init_db(db_path)
    with _conn(db_path) as conn:
        cur = conn.execute(
            "UPDATE applications SET notes = ? WHERE id = ?", (notes, app_id)
        )
        return cur.rowcount > 0


def delete(app_id: int, db_path: str = DEFAULT_DB) -> bool:
    init_db(db_path)
    with _conn(db_path) as conn:
        cur = conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
        return cur.rowcount > 0


def list_all(status_filter: str | None = None, db_path: str = DEFAULT_DB) -> list[JobApplication]:
    init_db(db_path)
    with _conn(db_path) as conn:
        if status_filter:
            rows = conn.execute(
                "SELECT * FROM applications WHERE status = ? ORDER BY applied_date DESC", (status_filter,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM applications ORDER BY applied_date DESC"
            ).fetchall()
    return [
        JobApplication(
            id=r["id"], company=r["company"], role=r["role"],
            status=r["status"], applied_date=r["applied_date"],
            url=r["url"], notes=r["notes"],
        )
        for r in rows
    ]
