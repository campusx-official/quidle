# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Inkwell** is a Flask-based blog application. The skeleton (home and post pages) is complete, and the database layer with SQLite has been implemented. Posts, users, likes, and saved posts are persisted in the database.

## Development Roadmap
The project is built in steps. Current status:
- [x] Skeleton — home page and post page
- [x] Step 1: Database setup (raw SQLite, no SQLAlchemy)
- [x] Step 2: Login system (admin only)
- [x] Step 3a: Admin dashboard
- [ ] Step 3b: Create post (plain textarea)
- [ ] Step 3c: Rich text editor (Quill or TinyMCE)
- [ ] Step 3d: Image uploads
- [ ] Step 3e: Edit and delete post
- [ ] Step 3f: Publish/unpublish toggle
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

- **`database/`**: Database layer with SQLite
  - `db.py` contains `get_db()`, `init_db()`, and `seed_db()` functions

- **`templates/`**: Jinja2 templates
  - `base.html` → layout template with navbar and footer
  - `home.html` → posts list view (extends base.html)
  - `post.html` → individual post view
  - `about.html` → about page

- **`static/`**: Static assets
  - `css/style.css` → stylesheet
  - `js/main.js` → client-side JavaScript

### Data Model

The database contains 4 tables:

**posts** table:
```
id, title, slug (unique), content, excerpt, status (draft/published),
author_id (FK → users.id), created_at, updated_at
```

**users** table:
```
id, username (unique), email (unique), password_hash, is_admin, created_at
```

**likes** and **saved_posts** tables:
```
Linking tables with unique constraints on (post_id, user_id)
```

## Key Implementation Notes

- Flask debug mode is enabled in development (`debug=True`)
- Posts are queried from the database by slug using parameterized queries
- All database operations use `get_db()` from `database/db.py`
- Template inheritance uses Jinja2 blocks for consistent page structure
- Admin user is automatically seeded on first run (username: `admin`, password: `admin123`)
- SQLite database is created in `inkwell.db` at project root on startup

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