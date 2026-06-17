"""
database.py — Database connection and schema initialisation for Recipe Vault.

Connection strategy
-------------------
* Turso (libsql-client) is used when TURSO_DATABASE_URL and TURSO_AUTH_TOKEN
  are present in the environment (or Streamlit secrets).
* Falls back to a local SQLite file at data/recipes.db for local development.

To switch from local → Turso:
  1. Create a free database at https://turso.tech
  2. Add TURSO_DATABASE_URL and TURSO_AUTH_TOKEN to .streamlit/secrets.toml
     (locally) or Streamlit Cloud > App Settings > Secrets (in production).
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Optional

# ── Optional Turso import ────────────────────────────────────────────────────
try:
    import libsql_client  # type: ignore
    _LIBSQL_AVAILABLE = True
except ImportError:
    _LIBSQL_AVAILABLE = False


def _get_secret(key: str) -> str:
    """Read from Streamlit secrets first, then environment variables."""
    try:
        import streamlit as st
        return st.secrets.get(key, "")  # type: ignore[attr-defined]
    except Exception:
        return os.environ.get(key, "")


def _use_turso() -> bool:
    return (
        _LIBSQL_AVAILABLE
        and bool(_get_secret("TURSO_DATABASE_URL"))
        and bool(_get_secret("TURSO_AUTH_TOKEN"))
    )


# ── Local SQLite path ─────────────────────────────────────────────────────────
_DB_PATH = Path(__file__).parent.parent / "data" / "recipes.db"

# Module-level connection (shared, thread-safe with check_same_thread=False)
_conn: Optional[sqlite3.Connection] = None


def get_connection() -> sqlite3.Connection:
    """
    Return the shared SQLite connection, creating it if needed.
    Using a single persistent connection avoids FTS consistency issues
    that arise when multiple short-lived connections interleave in WAL mode.
    """
    global _conn
    if _conn is None:
        _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        _conn = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.execute("PRAGMA journal_mode=WAL")
        _conn.execute("PRAGMA foreign_keys=ON")
    return _conn


# ── Schema DDL ────────────────────────────────────────────────────────────────
_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS recipes (
    recipe_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT    NOT NULL,
    category     TEXT    DEFAULT '',
    ingredients  TEXT    DEFAULT '',
    instructions TEXT    DEFAULT '',
    notes        TEXT    DEFAULT '',
    source       TEXT    DEFAULT '',
    date_added   TEXT    DEFAULT (date('now')),
    last_updated TEXT    DEFAULT NULL,
    is_favorite  INTEGER DEFAULT 0,
    last_viewed  TEXT    DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS tags (
    tag_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL UNIQUE COLLATE NOCASE
);

CREATE TABLE IF NOT EXISTS recipe_tags (
    recipe_id INTEGER NOT NULL REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    tag_id    INTEGER NOT NULL REFERENCES tags(tag_id)       ON DELETE CASCADE,
    PRIMARY KEY (recipe_id, tag_id)
);

CREATE VIRTUAL TABLE IF NOT EXISTS recipes_fts USING fts5(
    recipe_id UNINDEXED,
    title,
    ingredients,
    instructions,
    notes,
    content='recipes',
    content_rowid='recipe_id'
);

CREATE TRIGGER IF NOT EXISTS recipes_ai AFTER INSERT ON recipes BEGIN
    INSERT INTO recipes_fts(recipe_id, title, ingredients, instructions, notes)
    VALUES (new.recipe_id, new.title, new.ingredients, new.instructions, new.notes);
END;

CREATE TRIGGER IF NOT EXISTS recipes_ad AFTER DELETE ON recipes BEGIN
    INSERT INTO recipes_fts(recipes_fts, recipe_id, title, ingredients, instructions, notes)
    VALUES ('delete', old.recipe_id, old.title, old.ingredients, old.instructions, old.notes);
END;

CREATE TRIGGER IF NOT EXISTS recipes_au AFTER UPDATE OF title, ingredients, instructions, notes ON recipes BEGIN
    INSERT INTO recipes_fts(recipes_fts, recipe_id, title, ingredients, instructions, notes)
    VALUES ('delete', old.recipe_id, old.title, old.ingredients, old.instructions, old.notes);
    INSERT INTO recipes_fts(recipe_id, title, ingredients, instructions, notes)
    VALUES (new.recipe_id, new.title, new.ingredients, new.instructions, new.notes);
END;
"""


def init_db() -> None:
    """Create all tables and triggers if they don't already exist."""
    conn = get_connection()
    conn.executescript(_SCHEMA_SQL)
    conn.commit()
    # Migration: add last_updated if missing (older databases)
    cols = {row[1] for row in conn.execute("PRAGMA table_info(recipes)").fetchall()}
    if "last_updated" not in cols:
        conn.execute("ALTER TABLE recipes ADD COLUMN last_updated TEXT DEFAULT NULL")
        conn.commit()
