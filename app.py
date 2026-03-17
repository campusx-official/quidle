from flask import Flask, render_template
from database.db import init_db, seed_db, get_db

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)