import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Gets necessary information about user's stocks
    user_stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM purchases WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", session["user_id"])

    # Updates all of necessary information
    for stock in user_stocks:
        stock_info = lookup(stock["symbol"])
        stock["name"] = stock_info["name"]
        stock["price"] = stock_info["price"]
        stock["total_value"] = stock_info["price"] * stock["total_shares"]

    # Gets user's balance information
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # Calculates grand total
    grand_total = user_cash + sum(stock["total_value"] for stock in user_stocks)

    return render_template("index.html", stocks=user_stocks, cash=user_cash, grand_total=grand_total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Ensures user provide valid symbol and number of shares
        if not request.form.get("symbol"):
            return apology("Provide stock symbol!", 400)
        elif not request.form.get("shares"):
            return apology("Provide number of shares!", 400)

        quote_info = lookup(request.form.get("symbol"))
        if quote_info is None:
            return apology("Invalid stock symbol!", 403)

        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("Provide positive number of shares!", 400)

        # Check if user can afford the stock
        cost = quote_info["price"] * shares
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        if cost > user_cash:
            return apology("You can't afford this stock purchase!", 403)

        # Update user's stock information after purchase
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, datetime('now'))",
                   session["user_id"], quote_info["symbol"], shares, quote_info["price"])
        # Update user's cash balance
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])

        return redirect("/")

    # User reached to the site via GET
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT symbol, shares, price, timestamp FROM purchases WHERE user_id = ? ORDER BY timestamp DESC", session["user_id"])
    return render_template("history.html", transactions=transactions)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Making sure symbol was submitted
        if not request.form.get("symbol"):
            return apology("Provide stock symbol", 403)

        # Looking up the quote information and returning it
        quote_info = lookup(request.form.get("symbol"))
        return render_template("quoted.html", quote_info=quote_info)
    # User reached to the site via GET
    else:
        return render_template("quote.html")


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

        # Hashing the password and inserting user's info to the database
        password_hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), password_hash)

        return redirect ("/")

    # User reached to the site via GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Checks user's input
        if not request.form.get("symbol"):
            return apology("Select stock symbol!", 403)
        elif not request.form.get("shares"):
            return apology("Provide number of shares!", 400)

        # Checks for validity of symbol
        quote_info = lookup(request.form.get("symbol"))
        if quote_info is None:
            return apology("Invalid stock symbol!", 400)

        # Checks for validity of amount of shares
        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("Number of shares have to be positive!", 403)

        # Checks if user owns enough shares to sell
        user_shares = db.execute("SELECT SUM(shares) as total_shares FROM purchases WHERE user_id = ? AND symbol = ? GROUP BY symbol",
                                 session["user_id"], quote_info["symbol"])
        if not user_shares or shares > user_shares[0]["total_shares"]:
            return apology("You don't own that amount of shares of this stock!", 403)

        # Update with information about sale
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], quote_info["symbol"], - shares, quote_info["price"])

        # Update user's cash balance
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", quote_info["price"] * shares, session["user_id"])

        return redirect("/")

    # User reached to the site via GET
    else:
        user_stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM purchases WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", session["user_id"])

        return render_template("sell.html", stocks=user_stocks)

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Allow users to add additional cash to their account"""
    if request.method == "POST":
        # Ensures correct usage
        if not request.form.get("amount"):
            return apology("Please, provide an amount!", 403)

        try:
            amount = float(request.form.get("amount"))
            if amount <= 0:
                raise ValueError
        except ValueError:
            return apology("Prvoide positive number!", 403)

        # Updates user's balance
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, session["user_id"])

        return redirect("/")

    # User reached to the site via GET
    else:
        return render_template("add_cash.html")

