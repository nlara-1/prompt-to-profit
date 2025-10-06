# db.py
import sqlite3
import threading
from typing import List, Dict, Any, Optional
from utils import hash_code

_DB_PATH = "data.db"
_lock = threading.Lock()

def _connect():
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    return conn

def _columns(conn, table: str):
    rows = conn.execute(f"PRAGMA table_info({table});").fetchall()
    return {r["name"] for r in rows}

def _ensure_row(conn):
    conn.execute("""
        INSERT OR IGNORE INTO game_state (id, admin_code_hash, start_now, end_now, updatedAt)
        VALUES (1, NULL, 0, 0, datetime('now'))
    """)

def migrate_db():
    """Create tables if missing and add missing columns safely."""
    with _lock, _connect() as conn:
        # leaderboard
        conn.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          playerName TEXT NOT NULL,
          totalScore INTEGER NOT NULL,
          createdAt TEXT NOT NULL
        );
        """)

        # game_state (create minimal, then add columns as needed)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS game_state (
          id INTEGER PRIMARY KEY CHECK (id=1)
        );
        """)

        cols = _columns(conn, "game_state")
        if "admin_code_hash" not in cols:
            conn.execute("ALTER TABLE game_state ADD COLUMN admin_code_hash TEXT;")
        if "start_now" not in cols:
            conn.execute("ALTER TABLE game_state ADD COLUMN start_now INTEGER DEFAULT 0;")
        if "end_now" not in cols:
            conn.execute("ALTER TABLE game_state ADD COLUMN end_now INTEGER DEFAULT 0;")
        if "updatedAt" not in cols:
            conn.execute("ALTER TABLE game_state ADD COLUMN updatedAt TEXT;")

        _ensure_row(conn)

        # Set default admin code if empty
        row = conn.execute("SELECT admin_code_hash FROM game_state WHERE id=1").fetchone()
        if row and (row["admin_code_hash"] is None):
            conn.execute(
                "UPDATE game_state SET admin_code_hash=?, updatedAt=datetime('now') WHERE id=1",
                (hash_code("BSCATUTSA"),)
            )

def init_db():
    migrate_db()
    return True

def set_admin_code_hash(h: str):
    with _lock, _connect() as conn:
        conn.execute("UPDATE game_state SET admin_code_hash=?, updatedAt=datetime('now') WHERE id=1", (h,))

def get_admin_code_hash() -> Optional[str]:
    with _lock, _connect() as conn:
        row = conn.execute("SELECT admin_code_hash FROM game_state WHERE id=1").fetchone()
        return row["admin_code_hash"] if row else None

def set_end_now(flag: int):
    with _lock, _connect() as conn:
        conn.execute("UPDATE game_state SET end_now=?, updatedAt=datetime('now') WHERE id=1", (flag,))

def get_end_now() -> int:
    with _lock, _connect() as conn:
        row = conn.execute("SELECT end_now FROM game_state WHERE id=1").fetchone()
        return int(row["end_now"]) if row else 0

def set_start_now(flag: int):
    with _lock, _connect() as conn:
        conn.execute("UPDATE game_state SET start_now=?, updatedAt=datetime('now') WHERE id=1", (flag,))

def get_start_now() -> int:
    with _lock, _connect() as conn:
        row = conn.execute("SELECT start_now FROM game_state WHERE id=1").fetchone()
        return int(row["start_now"]) if row else 0

def add_leaderboard(player: str, score: int):
    with _lock, _connect() as conn:
        conn.execute(
            "INSERT INTO leaderboard (playerName, totalScore, createdAt) VALUES (?, ?, datetime('now'))",
            (player, score)
        )

def top10() -> List[Dict[str, Any]]:
    with _lock, _connect() as conn:
        rows = conn.execute(
            "SELECT playerName, totalScore, createdAt FROM leaderboard ORDER BY totalScore DESC, createdAt ASC LIMIT 10"
        ).fetchall()
        return [dict(r) for r in rows]

def standings(limit: int = 200) -> List[Dict[str, Any]]:
    with _lock, _connect() as conn:
        rows = conn.execute(
            "SELECT playerName, totalScore, createdAt FROM leaderboard ORDER BY totalScore DESC, createdAt ASC LIMIT ?",
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
