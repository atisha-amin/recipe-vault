"""
recipes.py — All CRUD operations, search, and stats for Recipe Vault.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.database import get_connection


# ── Read ──────────────────────────────────────────────────────────────────────

def get_all_recipes(order_by: str = "title") -> list:
    allowed = {"title", "date_added", "category"}
    col = order_by if order_by in allowed else "title"
    conn = get_connection()
    return conn.execute(
        f"SELECT * FROM recipes ORDER BY {col} COLLATE NOCASE"
    ).fetchall()


def get_recipe_by_id(recipe_id: int) -> Optional[object]:
    conn = get_connection()
    conn.execute(
        "UPDATE recipes SET last_viewed = ? WHERE recipe_id = ?",
        (datetime.now().isoformat(timespec="seconds"), recipe_id),
    )
    conn.commit()
    return conn.execute(
        "SELECT * FROM recipes WHERE recipe_id = ?", (recipe_id,)
    ).fetchone()


def get_favorites() -> list:
    conn = get_connection()
    return conn.execute(
        "SELECT * FROM recipes WHERE is_favorite = 1 ORDER BY title COLLATE NOCASE"
    ).fetchall()


def get_recently_viewed(limit: int = 10) -> list:
    conn = get_connection()
    return conn.execute(
        "SELECT * FROM recipes WHERE last_viewed IS NOT NULL "
        "ORDER BY last_viewed DESC LIMIT ?",
        (limit,),
    ).fetchall()


def get_categories() -> list[str]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT DISTINCT category FROM recipes WHERE category != '' ORDER BY category"
    ).fetchall()
    return [r["category"] for r in rows]


def get_stats() -> dict:
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM recipes").fetchone()[0]
    favorites = conn.execute(
        "SELECT COUNT(*) FROM recipes WHERE is_favorite = 1"
    ).fetchone()[0]
    by_category = conn.execute(
        "SELECT category, COUNT(*) as cnt FROM recipes "
        "WHERE category != '' GROUP BY category ORDER BY cnt DESC"
    ).fetchall()
    top_tags = conn.execute(
        "SELECT t.name, COUNT(rt.recipe_id) as cnt "
        "FROM tags t JOIN recipe_tags rt ON t.tag_id = rt.tag_id "
        "GROUP BY t.name ORDER BY cnt DESC LIMIT 10"
    ).fetchall()
    return {
        "total": total,
        "favorites": favorites,
        "by_category": [dict(r) for r in by_category],
        "top_tags": [dict(r) for r in top_tags],
    }


# ── Search ────────────────────────────────────────────────────────────────────

def search_recipes(query: str = "", category: str = "", tag: str = "") -> list:
    conn = get_connection()
    joins: list[str] = []
    where: list[str] = []
    params: list = []

    if query.strip():
        safe_q = query.strip().replace('"', '""')
        joins.append("JOIN recipes_fts ON recipes.recipe_id = recipes_fts.recipe_id")
        where.append("recipes_fts MATCH ?")
        params.append(f'"{safe_q}"*')

    if category:
        where.append("recipes.category = ?")
        params.append(category)

    if tag:
        joins.append(
            "JOIN recipe_tags ON recipes.recipe_id = recipe_tags.recipe_id "
            "JOIN tags ON recipe_tags.tag_id = tags.tag_id"
        )
        where.append("tags.name = ?")
        params.append(tag)

    join_sql = " ".join(joins)
    where_sql = ("WHERE " + " AND ".join(where)) if where else ""
    sql = f"""
        SELECT DISTINCT recipes.*
        FROM recipes {join_sql}
        {where_sql}
        ORDER BY recipes.title COLLATE NOCASE
    """
    try:
        return conn.execute(sql, params).fetchall()
    except Exception:
        return []


# ── Write ─────────────────────────────────────────────────────────────────────

def add_recipe(
    title: str,
    category: str = "",
    ingredients: str = "",
    instructions: str = "",
    notes: str = "",
    source: str = "",
    tags: list[str] | None = None,
    date_added: str = "",
) -> int:
    if not date_added:
        date_added = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO recipes (title, category, ingredients, instructions, notes, source, date_added) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (title, category, ingredients, instructions, notes, source, date_added),
    )
    recipe_id = cursor.lastrowid
    conn.commit()
    if tags:
        _set_tags(conn, recipe_id, tags)
        conn.commit()
    return recipe_id  # type: ignore[return-value]


def update_recipe(
    recipe_id: int,
    title: str,
    category: str = "",
    ingredients: str = "",
    instructions: str = "",
    notes: str = "",
    source: str = "",
    tags: list[str] | None = None,
) -> None:
    now = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    conn.execute(
        "UPDATE recipes SET title=?, category=?, ingredients=?, instructions=?, "
        "notes=?, source=?, last_updated=? WHERE recipe_id=?",
        (title, category, ingredients, instructions, notes, source, now, recipe_id),
    )
    conn.commit()
    if tags is not None:
        _set_tags(conn, recipe_id, tags)
        conn.commit()


def delete_recipe(recipe_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM recipes WHERE recipe_id = ?", (recipe_id,))
    conn.commit()


def toggle_favorite(recipe_id: int) -> bool:
    conn = get_connection()
    current = conn.execute(
        "SELECT is_favorite FROM recipes WHERE recipe_id = ?", (recipe_id,)
    ).fetchone()["is_favorite"]
    new_val = 0 if current else 1
    conn.execute(
        "UPDATE recipes SET is_favorite = ? WHERE recipe_id = ?",
        (new_val, recipe_id),
    )
    conn.commit()
    return bool(new_val)


# ── Tags ──────────────────────────────────────────────────────────────────────

def get_all_tags() -> list[str]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT name FROM tags ORDER BY name COLLATE NOCASE"
    ).fetchall()
    return [r["name"] for r in rows]


def get_tags_for_recipe(recipe_id: int) -> list[str]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT t.name FROM tags t "
        "JOIN recipe_tags rt ON t.tag_id = rt.tag_id "
        "WHERE rt.recipe_id = ? ORDER BY t.name",
        (recipe_id,),
    ).fetchall()
    return [r["name"] for r in rows]


def _set_tags(conn: sqlite3.Connection, recipe_id: int, tags: list[str]) -> None:
    conn.execute("DELETE FROM recipe_tags WHERE recipe_id = ?", (recipe_id,))
    for raw in tags:
        tag = raw.strip()
        if not tag:
            continue
        conn.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
        tag_id = conn.execute(
            "SELECT tag_id FROM tags WHERE name = ?", (tag,)
        ).fetchone()["tag_id"]
        conn.execute(
            "INSERT OR IGNORE INTO recipe_tags (recipe_id, tag_id) VALUES (?, ?)",
            (recipe_id, tag_id),
        )


# Fix missing import
import sqlite3
