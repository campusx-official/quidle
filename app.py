from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        "title": "Getting Started with Python",
        "slug": "getting-started-with-python",
        "author": "Alice",
        "date": "2024-01-15",
        "excerpt": "Python is one of the most beginner-friendly languages out there. Let's explore why.",
        "content": "<p>Python is one of the most beginner-friendly languages out there. It has a clean syntax, a massive community, and libraries for virtually everything.</p><p>In this post we'll look at how to get started from scratch.</p>"
    },
    {
        "title": "Understanding Flask Routing",
        "slug": "understanding-flask-routing",
        "author": "Bob",
        "date": "2024-01-22",
        "excerpt": "Routing is the backbone of any Flask application. Here is how it works.",
        "content": "<p>Flask routing maps URLs to Python functions. Every time a user visits a URL, Flask figures out which function to call and returns its response.</p><p>Let's break down how this works under the hood.</p>"
    },
    {
        "title": "Why SQLite is Perfect for Small Projects",
        "slug": "why-sqlite-is-perfect-for-small-projects",
        "author": "Alice",
        "date": "2024-02-03",
        "excerpt": "No server, no setup, no hassle. SQLite just works.",
        "content": "<p>SQLite is a file-based database that requires zero configuration. There is no server to run, no credentials to manage, and no installation beyond a Python package.</p><p>For small to medium projects, it is often the best choice.</p>"
    }
]

@app.route("/")
def home():
    return render_template("home.html", posts=posts)

@app.route("/post/<slug>")
def post(slug):
    selected = next((p for p in posts if p["slug"] == slug), None)
    if not selected:
        return "Post not found", 404
    return render_template("post.html", post=selected)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)