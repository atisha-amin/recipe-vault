"""
tests/test_recipes.py — Unit tests for Recipe Vault.

Run with: pytest tests/
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure the project root is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

# Point the DB at a temp file for every test session
os.environ.setdefault("RECIPE_VAULT_TEST", "1")
_TMP_DB = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_TMP_DB.close()

import app.database as _db_module
_db_module._DB_PATH = Path(_TMP_DB.name)

from app.database import init_db
from app.recipes import (
    add_recipe,
    get_all_recipes,
    get_recipe_by_id,
    get_favorites,
    get_categories,
    get_all_tags,
    get_tags_for_recipe,
    search_recipes,
    update_recipe,
    delete_recipe,
    toggle_favorite,
)


@pytest.fixture(autouse=True)
def fresh_db():
    """Re-initialise the DB before every test."""
    # Drop and recreate by wiping the file
    open(_TMP_DB.name, "w").close()
    init_db()
    yield


# ── add / read ────────────────────────────────────────────────────────────────

def test_add_and_retrieve():
    rid = add_recipe(
        title="Test Cake",
        category="Cakes",
        ingredients="flour\nsugar",
        instructions="Mix. Bake.",
        notes="Good warm.",
        source="Grandma",
        tags=["chocolate", "easy"],
    )
    assert rid > 0
    recipe = get_recipe_by_id(rid)
    assert recipe["title"] == "Test Cake"
    assert recipe["category"] == "Cakes"
    assert recipe["source"] == "Grandma"


def test_get_all_recipes_empty():
    assert get_all_recipes() == []


def test_get_all_recipes_multiple():
    add_recipe(title="Alpha")
    add_recipe(title="Beta")
    recipes = get_all_recipes()
    assert len(recipes) == 2
    titles = [r["title"] for r in recipes]
    assert "Alpha" in titles and "Beta" in titles


# ── tags ──────────────────────────────────────────────────────────────────────

def test_tags_stored_and_retrieved():
    rid = add_recipe(title="Taggy", tags=["chocolate", "lemon"])
    tags = get_tags_for_recipe(rid)
    assert set(tags) == {"chocolate", "lemon"}


def test_tags_case_insensitive_dedup():
    rid = add_recipe(title="CaseyTag", tags=["Chocolate", "chocolate"])
    tags = get_tags_for_recipe(rid)
    assert len(tags) == 1


def test_get_all_tags():
    add_recipe(title="R1", tags=["vanilla", "lemon"])
    add_recipe(title="R2", tags=["lemon", "caramel"])
    all_tags = get_all_tags()
    assert "vanilla" in all_tags
    assert "lemon" in all_tags
    assert "caramel" in all_tags


# ── update ────────────────────────────────────────────────────────────────────

def test_update_recipe():
    rid = add_recipe(title="Old Title", category="Cookies")
    update_recipe(rid, title="New Title", category="Cakes", tags=["new-tag"])
    recipe = get_recipe_by_id(rid)
    assert recipe["title"] == "New Title"
    assert recipe["category"] == "Cakes"
    tags = get_tags_for_recipe(rid)
    assert "new-tag" in tags


def test_update_clears_old_tags():
    rid = add_recipe(title="TagSwap", tags=["old"])
    update_recipe(rid, title="TagSwap", tags=["new"])
    tags = get_tags_for_recipe(rid)
    assert "old" not in tags
    assert "new" in tags


# ── delete ────────────────────────────────────────────────────────────────────

def test_delete_recipe():
    rid = add_recipe(title="Delete Me")
    delete_recipe(rid)
    assert get_recipe_by_id(rid) is None


def test_delete_cascades_tags():
    rid = add_recipe(title="Gone", tags=["removeme"])
    delete_recipe(rid)
    all_tags = get_tags_for_recipe(rid)
    assert all_tags == []


# ── favorites ─────────────────────────────────────────────────────────────────

def test_toggle_favorite():
    rid = add_recipe(title="Fav Test")
    recipe = get_recipe_by_id(rid)
    assert recipe["is_favorite"] == 0
    new_state = toggle_favorite(rid)
    assert new_state is True
    recipe = get_recipe_by_id(rid)
    assert recipe["is_favorite"] == 1
    toggle_favorite(rid)
    recipe = get_recipe_by_id(rid)
    assert recipe["is_favorite"] == 0


def test_get_favorites():
    rid1 = add_recipe(title="A")
    rid2 = add_recipe(title="B")
    toggle_favorite(rid1)
    favs = get_favorites()
    assert len(favs) == 1
    assert favs[0]["recipe_id"] == rid1


# ── search ────────────────────────────────────────────────────────────────────

def test_search_by_title():
    add_recipe(title="Chocolate Brownies", ingredients="cocoa butter flour")
    add_recipe(title="Lemon Cake", ingredients="lemon flour butter")
    results = search_recipes(query="Chocolate")
    assert any("Brownie" in r["title"] for r in results)


def test_search_by_ingredient():
    add_recipe(title="Almond Tart", ingredients="almond flour butter sugar")
    add_recipe(title="Vanilla Cake", ingredients="vanilla flour butter milk")
    results = search_recipes(query="almond")
    assert len(results) == 1
    assert results[0]["title"] == "Almond Tart"


def test_search_by_category():
    add_recipe(title="Cookie1", category="Cookies")
    add_recipe(title="Cake1", category="Cakes")
    results = search_recipes(category="Cookies")
    assert all(r["category"] == "Cookies" for r in results)


def test_search_by_tag():
    rid = add_recipe(title="Chai Cake", tags=["chai"])
    add_recipe(title="Plain Cake")
    results = search_recipes(tag="chai")
    assert len(results) == 1
    assert results[0]["recipe_id"] == rid


def test_search_empty_query_returns_empty():
    add_recipe(title="Something")
    results = search_recipes()
    assert results == []


def test_search_no_results():
    add_recipe(title="Vanilla Cake")
    results = search_recipes(query="xyzzy_nonexistent")
    assert results == []


# ── categories ────────────────────────────────────────────────────────────────

def test_get_categories():
    add_recipe(title="A", category="Cookies")
    add_recipe(title="B", category="Cakes")
    add_recipe(title="C", category="Cookies")
    cats = get_categories()
    assert set(cats) == {"Cookies", "Cakes"}
