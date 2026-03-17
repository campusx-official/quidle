# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Inkwell** is a Flask-based blog application. Currently, it's in its initial skeleton phase with hard-coded posts in `app.py`. The database module (`database/db.py`) is stubbed out and will be implemented to persist posts and users to SQLite.

## Development Roadmap
The project is built in 11 steps. Current status:
- [x] Skeleton — home page and post page
- [ ] Step 1: Database setup (raw SQLite, no SQLAlchemy)
- [ ] Step 2: Login system (admin only)
- [ ] Step 3: Admin panel
- [ ] Step 4: Blog home page (from DB)
- [ ] Step 5: View blog page (from DB)
- [ ] Step 6: User registration
- [ ] Step 7: User login
- [ ] Step 8: Search
- [ ] Step 9: Like button
- [ ] Step 10: Save for later
- [ ] Step 11: Share functionality

## Development Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run the development server (runs at http://localhost:5000)
python app.py

# Deactivate virtual environment
deactivate
```

## Architecture

### Application Structure

- **`app.py`**: Main Flask application with routes:
  - `/` → home page listing all posts
  - `/post/<slug>` → individual post page
  - `/about` → about page

- **`database/`**: Database layer (stubbed, to be implemented)
  - `db.py` should contain `get_db()`, `init_db()`, and `seed_db()` functions

- **`templates/`**: Jinja2 templates
  - `base.html` → layout template with navbar and footer
  - `home.html` → posts list view (extends base.html)
  - `post.html` → individual post view
  - `about.html` → about page

- **`static/`**: Static assets
  - `css/style.css` → stylesheet
  - `js/main.js` → client-side JavaScript

### Data Model

Posts currently have this structure:
```python
{
    "title": str,
    "slug": str,           # URL-safe identifier
    "author": str,
    "date": str,           # YYYY-MM-DD format
    "excerpt": str,
    "content": str         # HTML content
}
```

Posts are stored as a list in `app.py` but will be migrated to SQLite via the database module.

## Key Implementation Notes

- Flask debug mode is enabled in development (`debug=True`)
- Posts are looked up by slug using `next()` with a default of None (404 if not found)
- Template inheritance uses Jinja2 blocks for consistent page structure
- The project will eventually need user authentication and admin functionality for post creation

## Git Conventions
- Branch naming: feature/<step-name>
- Commit format: Conventional Commits (feat:, fix:, chore:, docs:)
- Never commit directly to main
- One branch per feature step

## Database Rules
- Use raw SQLite via the sqlite3 module only
- No SQLAlchemy, no Flask-SQLAlchemy, no ORMs
- All queries go through get_db() in database/db.py
- Always use parameterised queries — never string formatting in SQL
- foreign_keys PRAGMA must be enabled on every connection