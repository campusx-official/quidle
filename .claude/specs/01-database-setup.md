# Spec: Database Setup

## Overview
Replace the hardcoded posts list in app.py with a proper SQLite 
database. This is the foundation for all 11 steps in the roadmap.

## Decisions
- All 4 tables created upfront — users, posts, likes, saved_posts
- Seed data includes admin user + 5 dummy posts
- init_db() and seed_db() run automatically on app startup
  but only if the database does not already exist

## Tables

### users
| Column        | Type         | Constraints                  |
|---------------|--------------|------------------------------|
| id            | INTEGER      | Primary key, autoincrement   |
| username      | TEXT         | Unique, not null             |
| email         | TEXT         | Unique, not null             |
| password_hash | TEXT         | Not null                     |
| is_admin      | INTEGER      | Default 0 (0=false, 1=true)  |
| created_at    | TEXT         | Default datetime('now')      |

### posts
| Column     | Type    | Constraints                          |
|------------|---------|--------------------------------------|
| id         | INTEGER | Primary key, autoincrement           |
| title      | TEXT    | Not null                             |
| slug       | TEXT    | Unique, not null                     |
| content    | TEXT    | Not null                             |
| excerpt    | TEXT    | Nullable                             |
| status     | TEXT    | Default 'draft' (draft/published)    |
| author_id  | INTEGER | Foreign key → users.id               |
| created_at | TEXT    | Default datetime('now')              |
| updated_at | TEXT    | Default datetime('now')              |

### likes
| Column  | Type    | Constraints                        |
|---------|---------|------------------------------------|
| id      | INTEGER | Primary key, autoincrement         |
| post_id | INTEGER | Foreign key → posts.id             |
| user_id | INTEGER | Foreign key → users.id             |

Unique constraint on (post_id, user_id) — a user can only 
like a post once.

### saved_posts
| Column   | Type    | Constraints                        |
|----------|---------|------------------------------------|
| id       | INTEGER | Primary key, autoincrement         |
| post_id  | INTEGER | Foreign key → posts.id             |
| user_id  | INTEGER | Foreign key → users.id             |
| saved_at | TEXT    | Default datetime('now')            |

Unique constraint on (post_id, user_id) — a user can only 
save a post once.

## Functions to implement in database/db.py

### get_db()
- Returns a SQLite connection
- Sets row_factory = sqlite3.Row so rows behave like dicts
- Enables foreign key support with PRAGMA foreign_keys = ON

### init_db()
- Creates all 4 tables using CREATE TABLE IF NOT EXISTS
- Safe to call multiple times — never drops existing tables

### seed_db()
- Checks if users table already has rows — if yes, returns early
- Inserts admin user:
  - username: admin
  - email: admin@inkwell.com
  - password: admin123 (hashed with werkzeug)
  - is_admin: 1
- Inserts 5 dummy posts (reuse content from current hardcoded 
  list in app.py)
- All posts authored by admin, status = published

## Changes to app.py

### Add at the top
```python
from database.db import init_db, seed_db
```

### Add startup logic before routes
```python
with app.app_context():
    init_db()
    seed_db()
```

### Replace hardcoded posts
- Remove the posts list
- Remove get_post_by_slug() helper function
- Update the home route to query all published posts from DB
- Update the post route to query by slug from DB
- Return 404 if slug not found

## Files to change
- database/db.py — write all three functions
- app.py — add imports, startup logic, replace hardcoded data

## Files to create
None

## Dependencies
No new dependencies — sqlite3 is part of Python's standard 
library and werkzeug is already installed

## Definition of done
- [ ] All 4 tables exist in inkwell.db after running the app
- [ ] Admin user exists with a hashed password
- [ ] 5 dummy posts exist with status = published
- [ ] Home page loads posts from DB not from hardcoded list
- [ ] Post page loads individual post from DB by slug
- [ ] 404 returned for unknown slugs
- [ ] App runs cleanly with no errors on startup
- [ ] foreign_keys PRAGMA is enabled on every connection
- [ ] No raw string formatting in any SQL query