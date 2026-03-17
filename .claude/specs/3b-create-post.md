# Spec: Create Post

## Overview
Add a "Create Post" page in the admin area that allows the admin to write and save a new blog post using a plain HTML `<textarea>`. This is the first step in building the full post authoring flow. The form collects a title, excerpt, content (plain textarea), and a status choice (draft or published). A URL slug is auto-generated from the title on the server side before inserting the record into the database. On success, the admin is redirected back to the dashboard. This step intentionally keeps the editor as a plain textarea; Step 3c will replace it with a rich text editor.

## Depends on
- Step 1: Database Setup — the `posts` table must exist with columns: `title`, `slug`, `content`, `excerpt`, `status`, `author_id`.
- Step 2: Login System — the `admin_required` decorator must be in place.
- Step 3a: Admin Dashboard — the dashboard's "New Post" button/link is the entry point for this route.

## Routes
- `GET /admin/posts/new` — render the create-post form — admin only
- `POST /admin/posts/new` — handle form submission, insert post, redirect — admin only

## Database changes
No database changes. All required columns already exist in the `posts` table.

## Templates
- **Create**: `templates/admin/create_post.html` — extends `base.html`; contains the new-post form with fields: title, excerpt, content (textarea), status (select: draft/published), and a submit button
- **Modify**: `templates/admin/dashboard.html` — wire up the existing "New Post" placeholder link to `url_for('admin_create_post')`

## Files to change
- `app.py` — add `GET/POST /admin/posts/new` route protected by `@admin_required`; on POST: validate inputs, generate slug, insert into `posts`, redirect to `/admin`
- `templates/admin/dashboard.html` — update the "New Post" button/link href to point to `/admin/posts/new`

## Files to create
- `templates/admin/create_post.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never format values into SQL strings
- The route must use the existing `@admin_required` decorator
- Slug generation rules (server-side Python):
  - Lowercase the title
  - Replace any character that is not a-z, 0-9, or a space with a space
  - Strip leading/trailing whitespace
  - Replace one or more spaces/hyphens with a single hyphen
  - Maximum 80 characters
- If a generated slug already exists in the database, append `-2`, `-3`, etc. until a unique slug is found
- `author_id` must be read from `session['user_id']` — never hardcoded
- If title or content is empty, re-render the form with a user-facing validation error message; do not insert a partial record
- After a successful INSERT, redirect to `url_for('admin_dashboard')` using `redirect()`
- Status field must only accept `'draft'` or `'published'`; default to `'draft'` if an unexpected value is submitted

## Definition of done
- [ ] Visiting `/admin/posts/new` while logged in as admin renders the create-post form
- [ ] Visiting `/admin/posts/new` while not logged in redirects to `/login`
- [ ] The form has input fields for: title, excerpt, content (textarea), and status (draft/published)
- [ ] Submitting the form with valid data inserts a new row into the `posts` table and redirects to `/admin`
- [ ] The new post appears in the admin dashboard table immediately after creation
- [ ] A post created with status `published` appears on the home page at `/`
- [ ] A post created with status `draft` does NOT appear on the home page
- [ ] Submitting without a title shows a validation error and does not insert a record
- [ ] Submitting without content shows a validation error and does not insert a record
- [ ] The slug is auto-generated from the title (lowercase, hyphenated, no special characters)
- [ ] Submitting a post whose title produces a duplicate slug results in a unique slug (e.g. `-2` suffix)
- [ ] The "New Post" button on the admin dashboard links to `/admin/posts/new`
