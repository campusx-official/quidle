from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from database.db import init_db, seed_db, get_db

app = Flask(__name__)
app.secret_key = "dev-secret-key"

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

with app.app_context():
    init_db()
    seed_db()

@app.route("/")
def home():
    db = get_db()
    posts = db.execute(
        "SELECT * FROM posts WHERE status = ? ORDER BY created_at DESC",
        ("published",),
    ).fetchall()
    return render_template("home.html", posts=posts)

@app.route("/post/<slug>")
def post(slug):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE slug = ?", (slug,)).fetchone()
    if not post:
        return "Post not found", 404
    return render_template("post.html", post=post)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if user and check_password_hash(user["password_hash"], password) and user["is_admin"]:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["is_admin"] = user["is_admin"]
            return redirect(url_for("admin_dashboard"))
        return render_template("login.html", error="Invalid credentials or not an admin.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/admin")
@admin_required
def admin_dashboard():
    db = get_db()
    posts = db.execute(
        """SELECT posts.*, users.username as author
           FROM posts
           JOIN users ON posts.author_id = users.id
           ORDER BY posts.created_at DESC""",
    ).fetchall()
    total = len(posts)
    published = sum(1 for p in posts if p["status"] == "published")
    drafts = total - published
    return render_template(
        "admin/dashboard.html",
        posts=posts,
        total=total,
        published=published,
        drafts=drafts,
    )

if __name__ == "__main__":
    app.run(debug=True)