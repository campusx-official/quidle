# Spec: Admin Dashboard

## Overview
Add an admin dashboard landing page at `/admin` that is only accessible to logged-in admin users. This step establishes the admin area as a protected hub from which all future admin actions (create, edit, delete, publish) will be linked. At this stage the dashboard displays a summary of blog stats (total posts, published vs draft counts) and a table listing all posts with their title, status, and creation date. Action buttons for edit, delete, and publish/unpublish are included in the table as placeholders — they will be wired up in Steps 3b–3f.

## Depends on
- Step 1: Database Setup — the `posts` and `users` tables must exist.
- Step 2: Login System — the `admin_required` decorator and session-based authentication must be in place so the `/admin` route can be protected.

## Routes
- `GET /admin` — display the admin dashboard with stats and post list — admin only

## Database changes
No database changes. All required data is already in the `posts` table.

## Templates
- **Create**: `templates/admin/dashboard.html` — extends `base.html`; shows stat cards (total posts, published, drafts) and a table of all posts (columns: title, status, created_at, actions)
- **Modify**: `templates/base.html` — add an "Admin" link in the navbar that is only visible when `session['is_admin']` is truthy

## Files to change
- `app.py` — add `GET /admin` route protected by `@admin_required`; query all posts with author username via a JOIN; pass posts and stats to the template
- `templates/base.html` — add conditional "Admin" navbar link

## Files to create
- `templates/admin/dashboard.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never format values into SQL strings
- The `/admin` route must use the existing `@admin_required` decorator from `app.py`
- Derive stats (total, published count, draft count) from the query results in Python — do not run separate COUNT queries
- Action buttons (Edit, Delete, Publish/Unpublish) should render as styled `<a>` or `<button>` elements but may link to `#` for now; they will be wired up in later steps
- After successful login, redirect admin users to `/admin` instead of `/` (update the login POST handler in `app.py`)

## Definition of done
- [ ] Visiting `/admin` while logged in as admin renders the dashboard page
- [ ] Visiting `/admin` while not logged in redirects to `/login`
- [ ] The dashboard shows three stat cards: total posts, published count, draft count
- [ ] The dashboard shows a table listing all posts with title, status, and creation date
- [ ] The table has Edit, Delete, and Publish/Unpublish action columns (links may point to `#`)
- [ ] The navbar shows an "Admin" link when the user is logged in as admin
- [ ] The "Admin" link is not visible to logged-out visitors
- [ ] Logging in as admin redirects to `/admin` instead of the home page
