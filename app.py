"""
app.py — Recipe Vault: a personal recipe library.
Run locally:  streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import pandas as pd

from app.database import init_db
from app.recipes import (
    get_all_recipes,
    get_recipe_by_id,
    get_favorites,
    get_recently_viewed,
    get_categories,
    get_stats,
    get_all_tags,
    get_tags_for_recipe,
    search_recipes,
    add_recipe,
    update_recipe,
    delete_recipe,
    toggle_favorite,
)
from app.export import recipe_to_markdown

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Recipe Vault",
    page_icon="🍰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
/* Sidebar */
[data-testid="stSidebar"] { background: #1a1a2e; }
[data-testid="stSidebar"] * { color: #e8e8f0 !important; }

/* Recipe cards */
.recipe-card {
    background: var(--background-color);
    border: 1px solid rgba(128,128,128,0.2);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.6rem;
    cursor: pointer;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.recipe-card:hover {
    border-color: #e07b54;
    box-shadow: 0 2px 8px rgba(224,123,84,0.15);
}

/* Recipe detail */
.recipe-title { font-size: 2rem; font-weight: 700; margin-bottom: 0.25rem; }
.recipe-meta  { color: #888; font-size: 0.85rem; margin-bottom: 1rem; }

/* Tag pills */
.tag-pill {
    display: inline-block;
    background: rgba(224,123,84,0.15);
    color: #e07b54;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.78rem;
    margin: 2px;
}

/* Section headers in recipe detail */
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    border-bottom: 2px solid #e07b54;
    padding-bottom: 4px;
    margin: 1.25rem 0 0.75rem 0;
    color: #e07b54;
}

/* Ingredient sub-section label */
.ingredient-sublabel {
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #888;
    margin: 0.75rem 0 0.25rem 0;
}

/* Ingredient line */
.ingredient-line { padding: 3px 0; border-bottom: 1px solid rgba(128,128,128,0.1); }

/* Instruction step */
.instruction-step { display: flex; gap: 12px; margin-bottom: 12px; }
.step-num {
    background: #e07b54;
    color: white;
    border-radius: 50%;
    width: 26px; height: 26px; min-width: 26px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem; font-weight: 700; margin-top: 2px;
}

/* Stat cards */
.stat-card { background: rgba(224,123,84,0.08); border-radius: 10px; padding: 1rem; text-align: center; }
.stat-number { font-size: 2.5rem; font-weight: 700; color: #e07b54; }
.stat-label  { font-size: 0.85rem; color: #888; }

/* Mobile: stack columns */
@media (max-width: 640px) {
    .recipe-title { font-size: 1.4rem; }
    .stat-number  { font-size: 1.8rem; }
}

hr { border-color: rgba(128,128,128,0.2) !important; }
</style>
""", unsafe_allow_html=True)

# ── Initialise DB & seed ──────────────────────────────────────────────────────

init_db()

if not get_all_recipes():
    from app.seed import seed_database
    seed_database()

# ── Session state ─────────────────────────────────────────────────────────────

defaults = {
    "page": "browse",
    "selected_recipe_id": None,
    "edit_mode": False,
    "confirm_delete": False,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


def nav(page: str, recipe_id: int | None = None) -> None:
    st.session_state.page = page
    st.session_state.selected_recipe_id = recipe_id
    st.session_state.edit_mode = False
    st.session_state.confirm_delete = False
    st.rerun()


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🍰 Recipe Vault")
    st.markdown("---")

    if st.button("📖  Browse All", use_container_width=True):
        nav("browse")
    if st.button("🔍  Search", use_container_width=True):
        nav("search")
    if st.button("❤️  Favorites", use_container_width=True):
        nav("favorites")
    if st.button("🕐  Recently Viewed", use_container_width=True):
        nav("recent")
    if st.button("➕  Add Recipe", use_container_width=True):
        nav("add")
    if st.button("📊  Dashboard", use_container_width=True):
        nav("dashboard")

    st.markdown("---")

    # ── docx import ───────────────────────────────────────────────────────
    st.markdown("**Import Recipes**")
    uploaded = st.file_uploader(
        "Upload .docx", type=["docx"], label_visibility="collapsed"
    )
    if uploaded:
        import os, tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name
        with st.spinner("Parsing…"):
            try:
                from app.parser import import_docx_to_db
                imported, skipped = import_docx_to_db(tmp_path)
                st.success(f"✅ {imported} imported, {skipped} skipped")
            except Exception as exc:
                st.error(f"Import failed: {exc}")
            finally:
                os.unlink(tmp_path)

    stats = get_stats()
    st.markdown("---")
    st.markdown(f"**{stats['total']}** recipes · **{stats['favorites']}** ❤️")


# ── Shared helpers ────────────────────────────────────────────────────────────

def _tag_pills(tags: list[str]) -> str:
    return " ".join(f'<span class="tag-pill">{t}</span>' for t in tags)


def _render_card(recipe, tags: list[str]) -> None:
    fav = " ❤️" if recipe["is_favorite"] else ""
    tag_html = _tag_pills(tags[:4])
    st.markdown(
        f'<div class="recipe-card">'
        f'<strong>{recipe["title"]}</strong>{fav}<br>'
        f'<small style="color:#888">{recipe["category"]}</small>'
        f'<div style="margin-top:6px">{tag_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if st.button("Open →", key=f"open_{recipe['recipe_id']}"):
        nav("detail", recipe["recipe_id"])


def _two_col_cards(recipes: list) -> None:
    col_a, col_b = st.columns(2)
    for i, r in enumerate(recipes):
        tags = get_tags_for_recipe(r["recipe_id"])
        with (col_a if i % 2 == 0 else col_b):
            _render_card(r, tags)


# ── Page: Browse ──────────────────────────────────────────────────────────────

def render_browse() -> None:
    st.title("📖 All Recipes")
    recipes = get_all_recipes()

    cats = ["All"] + sorted({r["category"] for r in recipes if r["category"]})
    col_f, col_s, col_fav = st.columns([2, 1, 1])
    with col_f:
        sel_cat = st.selectbox("Category", cats, label_visibility="collapsed")
    with col_s:
        sort_by = st.selectbox("Sort", ["Title", "Date Added"], label_visibility="collapsed")
    with col_fav:
        only_favs = st.checkbox("❤️ Favorites only")

    if sel_cat != "All":
        recipes = [r for r in recipes if r["category"] == sel_cat]
    if only_favs:
        recipes = [r for r in recipes if r["is_favorite"]]

    sort_col = "title" if sort_by == "Title" else "date_added"
    recipes = sorted(recipes, key=lambda r: r[sort_col] or "", reverse=(sort_col == "date_added"))

    if not recipes:
        st.info("No recipes found. Try clearing filters or adding some!")
        return

    st.markdown(f"*{len(recipes)} recipe{'s' if len(recipes) != 1 else ''}*")
    _two_col_cards(recipes)


# ── Page: Search ──────────────────────────────────────────────────────────────

def render_search() -> None:
    st.title("🔍 Search Recipes")

    col1, col2, col3 = st.columns([3, 1.5, 1.5])
    with col1:
        query = st.text_input(
            "Search", placeholder="e.g. chocolate, lemon, cream cheese",
            label_visibility="collapsed",
        )
    with col2:
        cats = ["All"] + get_categories()
        cat_filter = st.selectbox("Category", cats, label_visibility="collapsed")
    with col3:
        all_tags = ["All"] + get_all_tags()
        tag_filter = st.selectbox("Tag", all_tags, label_visibility="collapsed")

    if query or cat_filter != "All" or tag_filter != "All":
        results = search_recipes(
            query=query,
            category=cat_filter if cat_filter != "All" else "",
            tag=tag_filter if tag_filter != "All" else "",
        )
        st.markdown(f"*{len(results)} result{'s' if len(results) != 1 else ''} found*")
        if results:
            _two_col_cards(results)
        else:
            st.info("No recipes matched. Try different keywords.")
    else:
        st.info("Enter a search term or choose a filter above.")


# ── Page: Favorites ───────────────────────────────────────────────────────────

def render_favorites() -> None:
    st.title("❤️ Favorites")
    recipes = get_favorites()
    if not recipes:
        st.info("No favorites yet. Open a recipe and click the heart!")
        return
    st.markdown(f"*{len(recipes)} favorite recipe{'s' if len(recipes) != 1 else ''}*")
    _two_col_cards(list(recipes))


# ── Page: Recently Viewed ─────────────────────────────────────────────────────

def render_recent() -> None:
    st.title("🕐 Recently Viewed")
    recipes = get_recently_viewed()
    if not recipes:
        st.info("No recently viewed recipes yet.")
        return
    for r in recipes:
        tags = get_tags_for_recipe(r["recipe_id"])
        col_card, col_meta = st.columns([3, 1])
        with col_card:
            _render_card(r, tags)
        with col_meta:
            if r["last_viewed"]:
                ts = r["last_viewed"][:16].replace("T", " ")
                st.markdown(
                    f"<small style='color:#888'>Viewed<br>{ts}</small>",
                    unsafe_allow_html=True,
                )


# ── Page: Recipe Detail ───────────────────────────────────────────────────────

def render_detail(recipe_id: int) -> None:
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        st.error("Recipe not found.")
        return

    tags = get_tags_for_recipe(recipe_id)
    fav_icon = "❤️" if recipe["is_favorite"] else "🤍"

    # ── Header row ────────────────────────────────────────────────────────
    col_title, col_actions = st.columns([4, 1])

    with col_title:
        st.markdown(
            f'<div class="recipe-title">{recipe["title"]}</div>',
            unsafe_allow_html=True,
        )
        meta_parts: list[str] = []
        if recipe["category"]:
            meta_parts.append(f"📂 {recipe['category']}")
        if recipe["date_added"]:
            meta_parts.append(f"📅 {recipe['date_added']}")
        if recipe["source"]:
            src = recipe["source"]
            if src.startswith("http"):
                meta_parts.append(f'🔗 <a href="{src}" target="_blank">{src}</a>')
            else:
                meta_parts.append(f"🔗 {src}")
        if meta_parts:
            st.markdown(
                f'<div class="recipe-meta">{" · ".join(meta_parts)}</div>',
                unsafe_allow_html=True,
            )
        if tags:
            st.markdown(_tag_pills(tags), unsafe_allow_html=True)

    with col_actions:
        if st.button(
            f"{fav_icon} {'Unfavorite' if recipe['is_favorite'] else 'Favorite'}",
            use_container_width=True,
        ):
            toggle_favorite(recipe_id)
            st.rerun()

        if st.button("✏️ Edit", use_container_width=True):
            st.session_state.edit_mode = True
            st.rerun()

        md = recipe_to_markdown(recipe, tags)
        st.download_button(
            "⬇️ Export .md",
            data=md,
            file_name=f"{recipe['title'].lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

        if not st.session_state.confirm_delete:
            if st.button("🗑️ Delete", use_container_width=True):
                st.session_state.confirm_delete = True
                st.rerun()
        else:
            st.warning("Delete this recipe?")
            if st.button("Yes, delete", use_container_width=True):
                delete_recipe(recipe_id)
                nav("browse")
            if st.button("Cancel", use_container_width=True):
                st.session_state.confirm_delete = False
                st.rerun()

    st.markdown("---")

    # ── Body: ingredients + instructions ──────────────────────────────────
    col_left, col_right = st.columns([1, 1.6])

    with col_left:
        if recipe["ingredients"]:
            st.markdown(
                '<div class="section-header">🥣 Ingredients</div>',
                unsafe_allow_html=True,
            )
            for line in recipe["ingredients"].splitlines():
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped.startswith("---") and stripped.endswith("---"):
                    label = stripped.strip("- ").strip()
                    st.markdown(
                        f'<div class="ingredient-sublabel">{label}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="ingredient-line">• {stripped}</div>',
                        unsafe_allow_html=True,
                    )

    with col_right:
        if recipe["instructions"]:
            st.markdown(
                '<div class="section-header">📋 Instructions</div>',
                unsafe_allow_html=True,
            )
            steps = [l for l in recipe["instructions"].splitlines() if l.strip()]
            for i, step in enumerate(steps, 1):
                st.markdown(
                    f'<div class="instruction-step">'
                    f'<div class="step-num">{i}</div>'
                    f'<div>{step.strip()}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    if recipe["notes"]:
        st.markdown(
            '<div class="section-header">📝 Notes</div>',
            unsafe_allow_html=True,
        )
        st.info(recipe["notes"])


# ── Page: Edit ────────────────────────────────────────────────────────────────

def render_edit(recipe_id: int) -> None:
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        st.error("Recipe not found.")
        return
    tags = get_tags_for_recipe(recipe_id)

    st.subheader(f"✏️ Editing: {recipe['title']}")

    with st.form("edit_form"):
        title = st.text_input("Title", value=recipe["title"])
        category = st.text_input("Category", value=recipe["category"])
        ingredients = st.text_area(
            "Ingredients (one per line)", value=recipe["ingredients"], height=220
        )
        instructions = st.text_area(
            "Instructions (one step per line)", value=recipe["instructions"], height=260
        )
        notes = st.text_area("Notes", value=recipe["notes"], height=120)
        source = st.text_input("Source / Inspiration", value=recipe["source"])
        tags_str = st.text_input(
            "Tags (comma-separated)", value=", ".join(tags)
        )

        col1, col2 = st.columns(2)
        with col1:
            saved = st.form_submit_button("💾 Save Changes", use_container_width=True)
        with col2:
            cancelled = st.form_submit_button("Cancel", use_container_width=True)

        if saved:
            new_tags = [t.strip() for t in tags_str.split(",") if t.strip()]
            update_recipe(
                recipe_id=recipe_id,
                title=title,
                category=category,
                ingredients=ingredients,
                instructions=instructions,
                notes=notes,
                source=source,
                tags=new_tags,
            )
            st.success("Saved!")
            st.session_state.edit_mode = False
            st.rerun()

        if cancelled:
            st.session_state.edit_mode = False
            st.rerun()


# ── Page: Add ─────────────────────────────────────────────────────────────────

def render_add() -> None:
    st.subheader("➕ Add New Recipe")

    with st.form("add_form", clear_on_submit=True):
        title = st.text_input("Recipe Title *")
        category = st.text_input("Category (e.g. Cookies, Cakes)")
        ingredients = st.text_area("Ingredients (one per line)", height=180)
        instructions = st.text_area("Instructions (one step per line)", height=220)
        notes = st.text_area("Notes / Tips", height=100)
        source = st.text_input("Source / Inspiration")
        tags_str = st.text_input(
            "Tags (comma-separated)", placeholder="e.g. chocolate, holiday, easy"
        )

        submitted = st.form_submit_button("💾 Save Recipe", use_container_width=True)

        if submitted:
            if not title.strip():
                st.error("Title is required.")
            else:
                new_tags = [t.strip() for t in tags_str.split(",") if t.strip()]
                new_id = add_recipe(
                    title=title.strip(),
                    category=category.strip(),
                    ingredients=ingredients.strip(),
                    instructions=instructions.strip(),
                    notes=notes.strip(),
                    source=source.strip(),
                    tags=new_tags,
                )
                st.success(f"✅ '{title}' added!")
                nav("detail", new_id)


# ── Page: Dashboard ───────────────────────────────────────────────────────────

def render_dashboard() -> None:
    st.title("📊 Dashboard")
    stats = get_stats()

    col1, col2, col3, col4 = st.columns(4)
    for col, num, label in [
        (col1, stats["total"], "Total Recipes"),
        (col2, stats["favorites"], "Favorites"),
        (col3, len(stats["by_category"]), "Categories"),
        (col4, len(get_all_tags()), "Unique Tags"),
    ]:
        with col:
            st.markdown(
                f'<div class="stat-card">'
                f'<div class="stat-number">{num}</div>'
                f'<div class="stat-label">{label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("")
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Recipes by Category")
        if stats["by_category"]:
            df_cat = (
                pd.DataFrame(stats["by_category"])
                .rename(columns={"category": "Category", "cnt": "Recipes"})
            )
            st.bar_chart(df_cat.set_index("Category"), color="#e07b54")
        else:
            st.info("No category data yet.")

    with col_r:
        st.subheader("Top Tags")
        if stats["top_tags"]:
            df_tags = (
                pd.DataFrame(stats["top_tags"])
                .rename(columns={"name": "Tag", "cnt": "Recipes"})
            )
            st.dataframe(df_tags, use_container_width=True, hide_index=True)
        else:
            st.info("No tags yet.")

    st.markdown("---")
    st.subheader("All Recipes")
    all_recipes = get_all_recipes()
    if all_recipes:
        df = pd.DataFrame([dict(r) for r in all_recipes])[
            ["recipe_id", "title", "category", "date_added", "is_favorite"]
        ]
        df.columns = ["ID", "Title", "Category", "Date Added", "Favorite"]
        df["Favorite"] = df["Favorite"].apply(lambda x: "❤️" if x else "")
        st.dataframe(df, use_container_width=True, hide_index=True)


# ── Router ────────────────────────────────────────────────────────────────────

page = st.session_state.page

if page == "browse":
    render_browse()

elif page == "search":
    render_search()

elif page == "favorites":
    render_favorites()

elif page == "recent":
    render_recent()

elif page == "add":
    render_add()

elif page == "dashboard":
    render_dashboard()

elif page == "detail":
    rid = st.session_state.selected_recipe_id
    if rid:
        if st.button("← Back"):
            nav("browse")
        if st.session_state.edit_mode:
            render_edit(rid)
        else:
            render_detail(rid)
    else:
        nav("browse")
