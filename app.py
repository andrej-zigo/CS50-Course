import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///report.db")

# Responses aren't cached
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def home():
    return render_template("index.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Makes sure everything is submited as it should be
        if not request.form.get("username"):
            return apology("Provide username!", 400)
        elif not request.form.get("password"):
            return apology("Provide password!", 400)
        elif not request.form.get("confirmation"):
            return apology("Confirm password!", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords must match!", 400)

        existing_user = db.execute(
            "SELECT username FROM users WHERE username = ?",
            request.form.get("username"),
        )
        if existing_user:
            return apology("Username already exists", 400)
        # Hashing the password and inserting user's info to the database
        password_hash = generate_password_hash(request.form.get("password"))
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username"),
            password_hash,
        )

        return redirect("/")

    # User reached to the site via GET
    else:
        return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Report
@app.route("/send", methods=["GET", "POST"])
@login_required
def send():
    if request.method == "POST":
        db.execute("INSERT INTO reports (user_id, message) VALUES (?, ?)", session["user_id"], request.form.get("message"))
        return redirect("/view")
    else:
        return render_template("index.html")

# View reports
@app.route("/view", methods=["GET", "POST"])
@login_required
def view():
    user_reports = db.execute("SELECT message FROM reports WHERE user_id = ?", session["user_id"])

    report_messages = []
    for report in user_reports:
        report_messages.append(report["message"])

    return render_template("reports.html", reports=report_messages)

