# Spec: Rich Text Editor

## Overview
Replace the plain `<textarea>` in the Create Post form with a rich text editor
powered by **Quill.js** (loaded from CDN). This gives the admin a WYSIWYG
writing experience — bold, italic, headings, lists, links, blockquotes — and
stores the resulting HTML in the existing `content` column. No server-side
logic changes are required because the `posts.content` column already stores
HTML; only the client-side authoring experience is upgraded.

## Depends on
- Step 3b: Create Post — the `/admin/posts/new` route and
  `templates/admin/create_post.html` must already exist.

## Routes
No new routes. The existing `GET/POST /admin/posts/new` route is unchanged.

## Database changes
No database changes. The `content` column is already `TEXT` and already stores
HTML (the seed data uses `<p>` tags).

## Templates
- **Modify**: `templates/admin/create_post.html`
  - Add Quill CSS `<link>` in a `{% block head %}` (or inline `<style>`) and
    Quill JS `<script>` tag pointing to the CDN.
  - Replace the `<textarea id="content" name="content">` with:
    1. A `<div id="quill-editor">` that Quill mounts onto.
    2. A `<input type="hidden" id="content" name="content">` that holds the
       HTML submitted to the server.
  - Add a `<script>` block that:
    - Initialises Quill on `#quill-editor` with the `snow` theme and a
      standard toolbar (bold, italic, underline, headings H1/H2, ordered list,
      bullet list, blockquote, link, clean).
    - If the form is being re-rendered after a server-side validation error
      (i.e. `form.get('content')` is non-empty), pre-populates the editor with
      that HTML via `quill.root.innerHTML = …`.
    - On `form.submit`, copies `quill.root.innerHTML` into the hidden input
      before the form is sent.

## Files to change
- `templates/admin/create_post.html` — all changes described above.

## Files to create
No new files.

## New dependencies
No new pip packages. Quill.js is loaded from the official CDN:
- CSS: `https://cdn.jsdelivr.net/npm/quill@2/dist/quill.snow.css`
- JS:  `https://cdn.jsdelivr.net/npm/quill@2/dist/quill.js`

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only — `app.py` is not modified.
- Use **Quill 2.x** loaded from CDN — do not download or bundle the library.
- Use the `snow` theme (white toolbar, standard look).
- The hidden `<input name="content">` is the field the server reads; its `id`
  may be anything that does not conflict with existing element IDs.
- The JavaScript that populates the hidden input **must** run inside a
  `submit` event listener on the `<form>` element, not as inline `onsubmit`.
- Do not remove the existing title, excerpt, or status fields.
- Do not alter `app.py` — the POST handler already accepts raw HTML in the
  `content` field and stores it unchanged.
- The Quill editor `<div>` should visually replace the old textarea in the
  same position in the layout, preserving the existing CSS class structure
  where possible.

## Definition of done
- [ ] Visiting `/admin/posts/new` renders a Quill rich-text editor instead of
      a plain textarea.
- [ ] The Quill toolbar includes at minimum: bold, italic, heading (H1, H2),
      ordered list, bullet list, blockquote, link, and clear-formatting.
- [ ] Typing and formatting text in the editor and clicking "Save Post"
      successfully saves the post; the `content` column in the database
      contains valid HTML (e.g. `<p>`, `<strong>`, `<h1>` tags).
- [ ] A post saved as `published` displays its formatted HTML correctly on the
      public `/post/<slug>` page (bold renders as bold, headings as headings,
      etc.).
- [ ] If the form is re-rendered due to a missing title, any content already
      entered in the editor is preserved (not lost).
- [ ] Submitting with an empty editor (no content entered) still triggers the
      existing server-side "Content is required" validation error.
- [ ] The title, excerpt, and status fields continue to work as before.
- [ ] No JavaScript console errors on page load or form submit.
