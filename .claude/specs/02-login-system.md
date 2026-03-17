# Spec: Login System

## Overview
Add an admin-only login system to Inkwell using Flask sessions. This step introduces authentication so that future admin-only routes (Step 3: Admin Panel) can be protected. Only users with `is_admin = 1` in the database can log in. Regular users cannot authenticate at this stage — that comes in Step 7. The feature adds `/login` and `/logout` routes, a login form template, and session-based state tracked across requests.

## Depends on
- Step 1: Database Setup — the `users` table with `password_hash` and `is_admin` columns must exist, and the admin seed user must be present.

## Routes
- `GET /login` — display the login form — public
- `POST /login` — process login credentials, start session on success, show error on failure — public
- `GET /logout` — clear the session and redirect to home — logged-in

## Database changes
No database changes. The `users` table already has `password_hash` and `is_admin` columns from Step 1.

## Templates
- **Create**: `templates/login.html` — login form with username and password fields, displays flash/error messages
- **Modify**: `templates/base.html` — add a "Login" link to the navbar when the user is not logged in; replace it with a "Logout" link when `session['user_id']` is set

## Files to change
- `app.py` — set `app.secret_key`, import `check_password_hash`, add `/login` GET/POST and `/logout` routes
- `templates/base.html` — conditionally show Login / Logout in the navbar

## Files to create
- `templates/login.html`

## New dependencies
No new dependencies. `werkzeug.security` is already installed and `flask.session` is built into Flask.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never format values into SQL strings
- Passwords must be verified with `werkzeug.security.check_password_hash`
- Use Flask's built-in `session` dict to store login state (`session['user_id']`, `session['username']`, `session['is_admin']`)
- `app.secret_key` must be set before any session usage — use a hard-coded dev string for now (e.g. `"dev-secret-key"`)
- Only users where `is_admin = 1` may log in at this step; reject others with an error message
- On failed login show an inline error message — do not use Flask `flash()` to keep it simple
- On successful login redirect to `/` (home)
- On logout, call `session.clear()` then redirect to `/`

## Definition of done
- [ ] Visiting `/login` renders a page with a username and password form
- [ ] Submitting incorrect credentials shows an error message on the login page
- [ ] Submitting `admin` / `admin123` logs in and redirects to the home page
- [ ] After login the navbar shows a "Logout" link instead of a "Login" link
- [ ] Visiting `/logout` while logged in clears the session and redirects to home
- [ ] After logout the navbar shows "Login" again
- [ ] A non-admin user record (if inserted manually with `is_admin = 0`) is rejected at login with an error message
- [ ] Refreshing any page after login keeps the user logged in (session persists)
- [ ] `app.secret_key` is set and the app starts with no errors
