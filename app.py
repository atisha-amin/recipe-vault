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
/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #1a1a2e; }
[data-testid="stSidebar"] * { color: #e8e8f0 !important; }

/* ── Browse hero ── */
.rv-hero { padding: 2rem 0 1rem 0; }
.rv-hero h1 { font-size: 2.6rem; font-weight: 800; letter-spacing: -0.5px; margin: 0 0 0.3rem 0; }
.rv-hero p  { color: #888; font-size: 1rem; margin: 0; }

/* ── Recipe cards grid ── */
.rv-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 14px;
    margin-top: 1rem;
}
.rv-card {
    border: 1.5px solid rgba(128,128,128,0.18);
    border-radius: 14px;
    padding: 1.1rem 1.2rem 1rem;
    cursor: pointer;
    transition: border-color 0.18s, box-shadow 0.18s, transform 0.12s;
    position: relative;
}
.rv-card:hover {
    border-color: #e07b54;
    box-shadow: 0 4px 16px rgba(224,123,84,0.13);
    transform: translateY(-2px);
}
.rv-card-emoji  { font-size: 1.9rem; margin-bottom: 0.45rem; display: block; }
.rv-card-title  { font-size: 1rem; font-weight: 700; margin: 0 0 3px 0; line-height: 1.3; }
.rv-card-cat    { font-size: 0.77rem; color: #888; margin-bottom: 7px; }
.rv-card-fav    { position: absolute; top: 10px; right: 12px; font-size: 0.85rem; }
.rv-card-tags   { margin-top: 5px; }

/* ── Tag pills ── */
.tag-pill {
    display: inline-block;
    background: rgba(224,123,84,0.12);
    color: #e07b54;
    border-radius: 20px;
    padding: 2px 9px;
    font-size: 0.73rem;
    margin: 2px 2px 0 0;
}

/* ── Recipe detail ── */
.recipe-title { font-size: 2rem; font-weight: 700; margin-bottom: 0.25rem; }
.recipe-meta  { color: #888; font-size: 0.85rem; margin-bottom: 1rem; }
.section-header {
    font-size: 1.05rem; font-weight: 700;
    border-bottom: 2px solid #e07b54;
    padding-bottom: 4px; margin: 1.25rem 0 0.75rem 0;
    color: #e07b54; text-transform: uppercase; letter-spacing: 0.04em;
}
.ingredient-sublabel {
    font-size: 0.8rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.05em; color: #888; margin: 0.75rem 0 0.3rem 0;
}
.ingredient-line { padding: 4px 0; border-bottom: 1px solid rgba(128,128,128,0.1); font-size: 0.95rem; }
.instruction-step { display: flex; gap: 12px; margin-bottom: 14px; align-items: flex-start; }
.step-num {
    background: #e07b54; color: white; border-radius: 50%;
    width: 26px; height: 26px; min-width: 26px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.78rem; font-weight: 700; margin-top: 2px;
}

/* ── Stat cards ── */
.stat-card { background: rgba(224,123,84,0.07); border-radius: 12px; padding: 1.1rem; text-align: center; border: 1px solid rgba(224,123,84,0.15); }
.stat-number { font-size: 2.4rem; font-weight: 800; color: #e07b54; }
.stat-label  { font-size: 0.82rem; color: #888; margin-top: 2px; }

/* ── Card-style buttons (browse grid only) ── */
[data-testid="stMainBlockContainer"] [data-testid="stButton"] > button {
    text-align: left !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 90px !important;
    padding: 0.9rem 1rem !important;
    border-radius: 14px !important;
    border: 1.5px solid rgba(128,128,128,0.2) !important;
    background: transparent !important;
    font-weight: normal !important;
    line-height: 1.55 !important;
    transition: border-color 0.18s, box-shadow 0.18s, transform 0.12s !important;
}
[data-testid="stMainBlockContainer"] [data-testid="stButton"] > button:hover {
    border-color: #e07b54 !important;
    box-shadow: 0 4px 16px rgba(224,123,84,0.15) !important;
    transform: translateY(-1px) !important;
    color: inherit !important;
}

/* ── Mobile ── */
@media (max-width: 640px) {
    .rv-hero h1 { font-size: 1.8rem; }
    .rv-grid    { grid-template-columns: 1fr; }
    .recipe-title { font-size: 1.4rem; }
    .stat-number  { font-size: 1.8rem; }
}
hr { border-color: rgba(128,128,128,0.18) !important; }
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

_CAT_EMOJI: dict[str, str] = {
    "Cakes": "🎂", "Cookies": "🍪", "Brownies": "🍫", "Bread": "🍞",
    "Muffins": "🧁", "Cheesecake": "🍰", "Savory": "🍝",
    "Mousse & Cups": "🥛", "Candy & Truffles": "🍬", "Cobblers & Crisps": "🍑",
}


def _tag_pills(tags: list[str]) -> str:
    return " ".join(f'<span class="tag-pill">{t}</span>' for t in tags)


def _render_card(recipe, tags: list[str]) -> None:
    """Render a clickable recipe card as a styled Streamlit button."""
    rid   = recipe["recipe_id"]
    fav   = " ❤️" if recipe["is_favorite"] else ""
    emoji = _CAT_EMOJI.get(recipe["category"], "🍽️")
    tag_text = "  ".join(f"`{t}`" for t in tags[:3])
    label = (
        f"{emoji} **{recipe['title']}**{fav}  \n"
        f"*{recipe['category']}*  \n"
        f"{tag_text}"
    )
    if st.button(label, key=f"open_{rid}", use_container_width=True):
        nav("detail", rid)


def _card_grid(recipes: list) -> None:
    """Render all recipe cards in a responsive CSS grid (3 cols → 1 on mobile)."""
    # Split into 3 columns; CSS grid handles reflow on mobile
    cols = st.columns(3)
    for i, r in enumerate(recipes):
        tags = get_tags_for_recipe(r["recipe_id"])
        with cols[i % 3]:
            _render_card(r, tags)


# ── Page: Browse ──────────────────────────────────────────────────────────────

def render_browse() -> None:
    recipes    = get_all_recipes()
    all_cats   = sorted({r["category"] for r in recipes if r["category"]})
    total      = len(recipes)
    fav_count  = sum(1 for r in recipes if r["is_favorite"])

    # ── Hero header ───────────────────────────────────────────────────────
    st.markdown(
        f'''<div class="rv-hero">
            <h1>🍰 Recipe Vault</h1>
            <p>{total} recipes · {fav_count} favourites</p>
        </div>''',
        unsafe_allow_html=True,
    )

    # ── Search bar ────────────────────────────────────────────────────────
    query = st.text_input(
        "search", placeholder="🔍  Search recipes, ingredients, tags…",
        label_visibility="collapsed",
    )

    # ── Filter row ────────────────────────────────────────────────────────
    col_sort, col_fav = st.columns([3, 1])
    with col_sort:
        sort_by = st.selectbox(
            "sort", ["A → Z", "Newest first"],
            label_visibility="collapsed",
        )
    with col_fav:
        only_favs = st.checkbox("❤️  Favourites only")

    # ── Category pill filter bar ──────────────────────────────────────────
    if "browse_cat" not in st.session_state:
        st.session_state.browse_cat = "All"

    pill_html = '<div style="display:flex;flex-wrap:wrap;gap:8px;margin:1rem 0 0.5rem 0;">' 
    for cat in ["All"] + all_cats:
        active = "background:#e07b54;color:#fff;border-color:#e07b54;" if st.session_state.browse_cat == cat else ""
        pill_html += (
            f'<span style="display:inline-block;padding:5px 15px;border-radius:999px;' +
            f'border:1.5px solid rgba(128,128,128,0.25);font-size:0.82rem;font-weight:500;' +
            f'cursor:default;{active}">{cat}</span>'
        )
    pill_html += '</div>'
    st.markdown(pill_html, unsafe_allow_html=True)

    # Category filter via selectbox (hidden label, synced with pills display)
    sel_cat = st.selectbox(
        "Category filter", ["All"] + all_cats,
        index=(["All"] + all_cats).index(st.session_state.browse_cat)
            if st.session_state.browse_cat in ["All"] + all_cats else 0,
        label_visibility="collapsed",
        key="browse_cat_select",
    )
    if sel_cat != st.session_state.browse_cat:
        st.session_state.browse_cat = sel_cat
        st.rerun()

    # ── Apply filters ─────────────────────────────────────────────────────
    if query.strip():
        from app.recipes import search_recipes
        filtered = search_recipes(
            query=query,
            category=sel_cat if sel_cat != "All" else "",
        )
    else:
        filtered = [r for r in recipes if sel_cat == "All" or r["category"] == sel_cat]

    if only_favs:
        filtered = [r for r in filtered if r["is_favorite"]]

    if sort_by == "A → Z":
        filtered = sorted(filtered, key=lambda r: (r["title"] or "").lower())
    else:
        filtered = sorted(filtered, key=lambda r: r["date_added"] or "", reverse=True)

    # ── Results count ─────────────────────────────────────────────────────
    count = len(filtered)
    st.markdown(
        f'<p style="color:#888;font-size:0.85rem;margin-bottom:0.25rem">' +
        f'{count} recipe{"s" if count != 1 else ""}</p>',
        unsafe_allow_html=True,
    )

    if not filtered:
        st.info("No recipes found — try a different search or filter.")
        return

    # ── Card grid ─────────────────────────────────────────────────────────
    _card_grid(filtered)


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
            _card_grid(results)
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
    _card_grid(list(recipes))


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

    # ── Title + meta ──────────────────────────────────────────────────────
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

    # ── Compact action bar ────────────────────────────────────────────────
    fav_icon  = "❤️" if recipe["is_favorite"] else "🤍"
    fav_label = "Unfavorite" if recipe["is_favorite"] else "Favorite"
    md = recipe_to_markdown(recipe, tags)

    a1, a2, a3, a4, spacer = st.columns([1, 1, 1.2, 1, 4])
    with a1:
        if st.button(f"{fav_icon} {fav_label}", key="btn_fav"):
            toggle_favorite(recipe_id)
            st.rerun()
    with a2:
        if st.button("✏️ Edit", key="btn_edit"):
            st.session_state.edit_mode = True
            st.rerun()
    with a3:
        st.download_button(
            "⬇️ Export",
            data=md,
            file_name=f"{recipe['title'].lower().replace(' ', '_')}.md",
            mime="text/markdown",
            key="btn_export",
        )
    with a4:
        if not st.session_state.confirm_delete:
            if st.button("🗑️ Delete", key="btn_del"):
                st.session_state.confirm_delete = True
                st.rerun()
        else:
            if st.button("⚠️ Confirm", key="btn_del_confirm"):
                delete_recipe(recipe_id)
                nav("browse")
            if st.button("Cancel", key="btn_del_cancel"):
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
