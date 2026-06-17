"""
parser.py — Parse a .docx recipe file and load recipes into the database.

Parsing assumptions (specific to this document's format)
---------------------------------------------------------
1.  Recipe titles  → Word "Heading 1" style.
2.  Sub-sections   → Word "Heading 2" style.
3.  Source line    → first italic (or "Inspired by…") Normal paragraph
                     that appears immediately after the title, before any H2.
4.  Ingredient sub-sections:
        H2 starting with an en-dash (–) e.g. "– For the Frosting"
        H2 containing "ingredient" keyword
    These become labelled dividers: "--- For the Frosting ---"
5.  Instruction section switches:
        H2 starting with a hyphen-dash (-) e.g. "-FOr the cake"
    These switch the active section to instructions without emitting text.
6.  Instruction-step H2s:
        H2 whose text begins with a cooking verb (Preheat, Bake, Mix, …)
    These are added directly as instruction steps.
7.  "Finished product" and "Dips" H2s → skipped entirely.
8.  "Tips" / "Tip" H2s → switch active section to notes.
9.  Brownies-style recipes with no H2 at all are handled by:
        - source detected from partially-italic Normal paragraph
        - ingredients from Normal style
        - instructions from "Normal (Web)" style
10. Eggless Cookies-style recipes where ingredients are formatted as H2
    lines are detected by a leading digit or fraction character.
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document  # python-docx

from app.database import init_db
from app.recipes import add_recipe, get_all_recipes


# ── Section classification helpers ───────────────────────────────────────────

_SKIP_SECTIONS = {"finished product", "dips"}
_NOTES_PREFIXES = ("tips", "tip")

# H2 text that begins with a cooking verb → treat as an instruction step
_INSTRUCTION_VERB_PREFIXES = (
    "preheat", "bake ", "lay ", "mix ", "prepare ", "make ", "cream ",
    "fold ", "whisk ", "beat ", "stir ", "split ", "assemble", "zest ",
    "cut ", "add ", "take ", "decorate",
)

# Category inference from title/text
_CATEGORY_MAP: dict[str, str] = {
    "cookie": "Cookies",
    "brownie": "Brownies",
    "bar": "Bars",
    "cake": "Cakes",
    "cupcake": "Cupcakes",
    "muffin": "Muffins",
    "bread": "Bread",
    "babka": "Bread",
    "bagel": "Bread",
    "cobbler": "Cobblers & Crisps",
    "cheesecake": "Cheesecake",
    "mousse": "Mousse & Cups",
    "tiramisu": "Mousse & Cups",
    "truffle": "Candy & Truffles",
    "roll": "Bread",
    "cinnamon roll": "Bread",
    "spaghetti": "Savory",
    "eggplant": "Savory",
    "kati": "Savory",
    "chutney": "Savory",
    "breadstick": "Savory",
}

# Auto-tag keywords
_TAG_KEYWORDS: list[str] = [
    "chocolate", "vanilla", "lemon", "orange", "chai", "mango",
    "blueberry", "cranberry", "pear", "blackberry", "carrot",
    "cinnamon", "cardamom", "banana", "funfetti", "gulab jamun",
    "cream cheese", "cheesecake", "no-bake", "eggless", "vegan",
    "indian", "savory", "holiday", "easy", "one-bowl",
    "espresso", "coffee", "caramel", "almond", "coconut",
]


def _classify_h2(text: str) -> tuple[str, str | None]:
    """
    Classify a Heading 2 paragraph.

    Returns (kind, label) where kind is one of:
        'skip'               → ignore this section entirely
        'notes'              → switch to notes section
        'instructions_step'  → add text as an instruction step
        'instructions_switch'→ switch to instructions section (no text emitted)
        'ingredient_line'    → add text as a raw ingredient line
        'ingredients'        → start/label an ingredient sub-section
    """
    t = text.strip()
    t_lower = t.lower().lstrip("-– \u2013")

    # Skip
    if any(t_lower.startswith(s) for s in _SKIP_SECTIONS) or t_lower in _SKIP_SECTIONS:
        return "skip", None

    # Notes / tips
    if t_lower.startswith(_NOTES_PREFIXES):
        return "notes", None

    # Cooking-verb H2 → instruction step
    for prefix in _INSTRUCTION_VERB_PREFIXES:
        if t_lower.startswith(prefix):
            return "instructions_step", t

    # En-dash (–) prefix → ingredient sub-section label
    if t.startswith("–") or t.startswith("\u2013"):
        label = t.lstrip("–\u2013 ").strip()
        return "ingredients", label

    # Hyphen prefix → instruction section switch
    if t.startswith("-"):
        return "instructions_switch", None

    # "INGREDIENTS" keyword in any form → ingredient sub-section label
    if "ingredient" in t_lower:
        label = t.strip()
        return "ingredients", label

    # Looks like an actual ingredient line mis-formatted as H2
    # (Eggless Cookies: each ingredient is a separate H2)
    if re.match(r"^[\d½¼⅓⅔¾]", t) or ("zest of" in t_lower):
        return "ingredient_line", t

    # Default: ingredient sub-section label
    return "ingredients", t.lstrip("-– ").strip()


def _is_source_line(p) -> bool:
    """True if the paragraph looks like a source/inspiration attribution."""
    text = p.text.strip()
    if not text:
        return False
    has_italic = any(r.italic for r in p.runs if r.text.strip())
    starts_inspired = text.lower().startswith("inspired")
    return has_italic or starts_inspired


def _infer_category(title: str, combined_text: str) -> str:
    """Infer the recipe category from its title and content."""
    haystack = (title + " " + combined_text).lower()
    for kw, cat in _CATEGORY_MAP.items():
        if kw in haystack:
            return cat
    return "Other"


def _infer_tags(title: str, combined_text: str) -> list[str]:
    """Auto-detect tags from title and ingredient/instruction text."""
    haystack = (title + " " + combined_text).lower()
    return [tag for tag in _TAG_KEYWORDS if tag in haystack]


# ── Main parser ───────────────────────────────────────────────────────────────

def parse_docx(filepath: str | Path) -> list[dict]:
    """
    Parse a .docx file and return a list of recipe dicts.

    Each dict contains: title, category, ingredients, instructions,
    notes, source, tags.
    """
    doc = Document(str(filepath))
    recipes: list[dict] = []
    current: dict | None = None
    current_section: str | None = None

    def _new_recipe(title: str) -> dict:
        return {
            "title": title,
            "source": "",
            "category": "",
            "ingredients": [],
            "instructions": [],
            "notes": [],
            "tags": [],
        }

    def _save():
        if current and current.get("title"):
            recipes.append(current)

    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue
        style = p.style.name

        # ── New recipe ────────────────────────────────────────────────────
        if style == "Heading 1":
            _save()
            current = _new_recipe(text)
            current_section = None
            continue

        if current is None:
            continue

        # ── Section header ────────────────────────────────────────────────
        if style == "Heading 2":
            kind, label = _classify_h2(text)
            if kind == "skip":
                current_section = "skip"
            elif kind == "notes":
                current_section = "notes"
            elif kind == "instructions_step":
                current_section = "instructions"
                current["instructions"].append(text)
            elif kind == "instructions_switch":
                current_section = "instructions"
            elif kind == "ingredient_line":
                if current_section != "instructions":
                    current_section = "ingredients"
                current["ingredients"].append(text)
            else:  # kind == "ingredients"
                current_section = "ingredients"
                if label:
                    current["ingredients"].append(f"--- {label} ---")
            continue

        if current_section == "skip":
            continue

        # ── Source detection (before first section is set) ────────────────
        if current_section is None:
            if _is_source_line(p):
                current["source"] = text
                continue
            # First non-source content: default to ingredients
            current_section = "ingredients"

        # ── Brownies: "Normal (Web)" style signals instructions ───────────
        if "web" in style.lower() and current_section == "ingredients":
            current_section = "instructions"

        # ── Append to current section ─────────────────────────────────────
        if current_section == "ingredients":
            current["ingredients"].append(text)
        elif current_section == "instructions":
            current["instructions"].append(text)
        elif current_section == "notes":
            current["notes"].append(text)

    _save()

    # ── Post-process: join lists, infer category + tags ───────────────────
    result: list[dict] = []
    for r in recipes:
        combined = " ".join(r["ingredients"] + r["instructions"])
        category = r["category"] or _infer_category(r["title"], combined)
        auto_tags = _infer_tags(r["title"], combined)
        all_tags = list(dict.fromkeys(r["tags"] + auto_tags))

        result.append({
            "title": r["title"],
            "category": category,
            "ingredients": "\n".join(r["ingredients"]),
            "instructions": "\n".join(r["instructions"]),
            "notes": "\n".join(r["notes"]),
            "source": r["source"],
            "tags": all_tags,
        })

    return result


# ── DB import ─────────────────────────────────────────────────────────────────

def import_docx_to_db(
    filepath: str | Path,
    skip_duplicates: bool = True,
) -> tuple[int, int]:
    """
    Parse a .docx file and insert recipes into the database.
    Returns (imported_count, skipped_count).
    """
    init_db()
    existing_titles = {r["title"].lower() for r in get_all_recipes()}
    recipes = parse_docx(filepath)

    imported = skipped = 0
    for r in recipes:
        if skip_duplicates and r["title"].lower() in existing_titles:
            skipped += 1
            continue
        add_recipe(
            title=r["title"],
            category=r["category"],
            ingredients=r["ingredients"],
            instructions=r["instructions"],
            notes=r["notes"],
            source=r["source"],
            tags=r["tags"],
        )
        imported += 1

    return imported, skipped
