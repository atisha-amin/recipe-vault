# 🍰 Recipe Vault

A personal recipe library built with Python and Streamlit. Import recipes from a Word document, browse and search them on a clean web interface, and manage everything — add, edit, delete, favorite — without touching any code.

Deployable for free on [Streamlit Community Cloud](https://streamlit.io/cloud) and shareable via a single public URL.

---

## Features

- **29 recipes** seeded from a personal Word document on first launch
- **Full-text search** across titles, ingredients, instructions, and notes (SQLite FTS5)
- **Filter** by category and tag
- **Add, edit, delete** recipes entirely through the UI — no code changes ever needed
- **Favorite** recipes and browse your favorites
- **Recently viewed** history
- **Dashboard** with category chart and tag stats
- **Export** any recipe to Markdown
- **Import** new recipes from a `.docx` file via the sidebar uploader
- **Mobile-friendly** layout
- **Persistent storage** via [Turso](https://turso.tech) (SQLite-compatible hosted database)

---

## Architecture

```
recipe_vault/
├── app.py                    # Streamlit entrypoint & page router
├── requirements.txt
├── .gitignore
│
├── .streamlit/
│   ├── config.toml           # Streamlit server config
│   └── secrets.toml.example  # Turso credential template (never committed)
│
├── app/
│   ├── database.py           # DB connection (local SQLite or Turso)
│   ├── recipes.py            # All CRUD + search operations
│   ├── parser.py             # .docx → structured recipe dicts
│   ├── export.py             # Recipe → Markdown
│   └── seed.py               # 29 real recipes as fallback seed data
│
├── data/                     # Local SQLite file lives here (git-ignored)
│
├── docs/                     # Architecture notes & screenshots
│
└── tests/
    └── test_recipes.py       # pytest suite (CRUD, search, tags)
```

### Database schema

```sql
recipes      (recipe_id, title, category, ingredients, instructions,
              notes, source, date_added, last_updated, is_favorite, last_viewed)

tags         (tag_id, name UNIQUE COLLATE NOCASE)

recipe_tags  (recipe_id FK, tag_id FK)   -- many-to-many junction

recipes_fts  -- FTS5 virtual table, auto-synced via INSERT/UPDATE/DELETE triggers
```

---

## Local setup

**Requirements:** Python 3.11+

```bash
# 1. Clone the repo
git clone https://github.com/your-username/recipe-vault.git
cd recipe-vault

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`. On first launch it seeds the database with all 29 recipes automatically.

---

## Deployment to Streamlit Community Cloud

### Why Turso?

Streamlit Community Cloud runs your app in an ephemeral container — any files written at runtime (including a local SQLite database) are lost on redeploy. [Turso](https://turso.tech) is a hosted LibSQL database (SQLite wire-compatible) with a free tier. Your recipes persist across every redeploy.

### Step 1 — Create a Turso database

```bash
# Install the Turso CLI
curl -sSfL https://get.tur.so/install.sh | bash

# Log in and create a database
turso auth login
turso db create recipe-vault

# Get your credentials
turso db show recipe-vault          # copy the URL (libsql://...)
turso db tokens create recipe-vault # copy the auth token
```

### Step 2 — Deploy to Streamlit Cloud

1. Push this repository to GitHub (public or private)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo and set **Main file path** to `app.py`
4. Open **Advanced settings → Secrets** and add:

```toml
TURSO_DATABASE_URL = "libsql://your-database-name.turso.io"
TURSO_AUTH_TOKEN   = "your-auth-token-here"
```

5. Click **Deploy**

On first launch, Streamlit Cloud installs dependencies, connects to Turso, creates the schema, and seeds your 29 recipes. The public URL is immediately shareable — no accounts needed for visitors.

### Local development with Turso credentials

Copy the example secrets file and fill it in:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your real credentials
```

The app uses Turso when both `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN` are set, and falls back to a local SQLite file otherwise.

---

## Running tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Adding recipes

**Via the UI** (recommended): click **➕ Add Recipe** in the sidebar. Fill in the form and save. Changes persist immediately.

**Via Word document import**: click **Import Recipes** in the sidebar and upload a `.docx` file. Recipes are parsed automatically and duplicates are skipped.

---

## Future roadmap

- **AI tagging** — auto-suggest tags using the Claude API
- **Semantic search** — find recipes by vibe, not just keywords
- **Nutritional analysis** — estimate macros per recipe
- **Meal planner** — weekly plan with a shopping list export
- **Recipe scaling** — adjust servings and quantities automatically
- **Image support** — attach photos to recipes

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | [Streamlit](https://streamlit.io) |
| Language | Python 3.11+ |
| Database | SQLite (local) / [Turso](https://turso.tech) (production) |
| Search | SQLite FTS5 |
| Doc parsing | [python-docx](https://python-docx.readthedocs.io) |
| Data | [pandas](https://pandas.pydata.org) |
| Hosting | [Streamlit Community Cloud](https://streamlit.io/cloud) |
