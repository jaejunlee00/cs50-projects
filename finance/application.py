import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

import datetime
import re


now = datetime.datetime.now()
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio1 of stocks"""
    # display symbol, name, share, price, and total at the main page. display cash left at the main page.
    rows = db.execute("SELECT symbol, name, share, price, total FROM portfolio1 WHERE id=:id", id=session["user_id"])
    """
    user_cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])

    user_cash = usd(user_cash[0]["cash"])

    db.execute("UPDATE users SET cash = :cash WHERE id = :id", id = session["user_id"], cash=user_cash)
    """
    rows1 = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

    return render_template("index.html", rows=rows, rows1=rows1)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # return apology page if anything isn't provided correctly
        if not request.form.get("symbol"):
            return apology("provide symbol")
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("provide valid symbol")

        if not request.form.get("shares"):
            return apology("provide share")

        share = int(request.form.get("shares"))
        if share < 1:
            return apology("provide positive share")

        afford = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        totprice = quote['price']*share
        # purchase the stock only if the user's cash is enough to purchase the stock
        if float(afford[0]["cash"]) >= totprice:
            # subtract the total price of purchased stock from the user's cash
            db.execute("UPDATE users SET cash = cash - :totprice WHERE id = :id", id=session["user_id"], totprice=totprice)
            # display this transaction in the history tab
            db.execute("INSERT INTO history (symbol, share, price, date, id) \
            VALUES(:symbol, :share, :price, :date, :id)", symbol=quote["symbol"], share=share, price=usd(quote["price"]), id=session["user_id"], date=now.strftime("%Y-%m-%d %H:%M:%S"))
            # check if the user already has this stock
            cur_share = db.execute("SELECT share FROM portfolio1 WHERE id = :id AND symbol = :symbol",
                                   id=session["user_id"], symbol=quote["symbol"])
            # if the user already has the stock, increase the number of share and the total price instead of inserting a whole new line
            if cur_share:
                totshare = cur_share[0]["share"] + share
                newtotprice = totshare*quote["price"]
                db.execute("UPDATE portfolio1 SET share = :share, total = :total WHERE symbol = :symbol AND id = :id",
                           id=session["user_id"], total=usd(newtotprice), share=totshare, symbol=quote["symbol"])
            else:
                db.execute("INSERT INTO portfolio1 (symbol, name, share, price, total, id) VALUES(:symbol, :name, :share, :price, :total, :id)",
                           symbol=quote["symbol"], name=quote["name"], share=share, price=usd(quote["price"]), total=usd(totprice), id=session["user_id"])

        else:
            return apology("you do not have enough money")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    # validate the username using javascript
    username = request.args.get("username")
    check_name = db.execute("SELECT username FROM users")
    if len(username) < 1 or username in check_name:
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/history")
@login_required
def history():
    # display symbol, share, price, and date for transcations
    history = db.execute("SELECT symbol, share, price, date FROM history WHERE id=:id", id=session["user_id"])

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

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
    # check if the valid symbol is entered
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("provide symbol")

        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("invalid stock symbol")
        # template that displays the information about the stock
        return render_template("quote1.html", quote=quote)
    else:
        # template to search the stock
        return render_template("quote.html")


@app.route("/")
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # check if the user puts the username and also if the username is not already taken
        username = request.form.get("username")
        names = db.execute("SELECT username FROM users WHERE username = :username", username=username)
        if names:
            return apology("username already taken")
        if not request.form.get("username"):
            return apology("provide username")
        # check if the user enters the password and confirmation password, and also if those two match
        password = request.form.get("password")
        if not request.form.get("password"):
            return apology("Provide password")

        confirmation = request.form.get("confirmation")
        if not request.form.get("confirmation"):
            return apology("Provide confirmation password")

        if password not in confirmation:
            return apology("passwords are not matched")
        # store hash instead of the actual user password for privacy
        hash = generate_password_hash(password)
        # insert the username and hash into the database
        rows = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=username, hash=hash)
        # remember which user is which
        session["user_id"] = rows

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # store all stock symbols that the user bought in rows2 variable to iterate in html
    rows2 = db.execute("SELECT symbol FROM portfolio1 WHERE id = :id", id=session["user_id"])
    if request.method == "POST":
        # check if the user enters valid symbol
        if not request.form.get("symbol"):
            return apology("provide symbol")
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("provide valid symbol")
        # check if the user enters valid number of shares
        if not request.form.get("shares"):
            return apology("provide share")

        share = int(request.form.get("shares"))
        # if the share is not a positive number, return apology
        if share < 1:
            return apology("share must be a positive number")
        afford = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        totprice = quote['price']*share
        # check if the user owns the stock that he/she wants to sell
        check_have = db.execute("SELECT share FROM portfolio1 WHERE id = :id AND symbol = :symbol",
                                id=session["user_id"], symbol=quote["symbol"])

        if check_have:
            # if the user owns the stock that he/she wants to sell, record this transaction to history table
            db.execute("INSERT INTO history (symbol, share, price, date, id) VALUES(:symbol, :share, :price, :date, :id)",
                       symbol=quote["symbol"], share=share, price=usd(quote["price"]), id=session["user_id"], date=now.strftime("%Y-%m-%d %H:%M:%S"))
            # update the number of shares for the stock he/she just sold
            totshare = check_have[0]["share"] - share
            # if the share is zero, remove the entire row from the portfolio table
            if totshare == 0:
                db.execute("DELETE FROM portfolio1 WHERE id =:id AND symbol = :symbol",
                           id=session["user_id"], symbol=quote["symbol"])
            # update the total price and total share that the user has for the stock
            else:
                newtotprice = totshare*quote["price"]
                db.execute("UPDATE portfolio1 SET share = :share, total = :total WHERE symbol = :symbol AND id = :id",
                           id=session["user_id"], total=usd(newtotprice), share=totshare, symbol=quote["symbol"])

        else:

            return apology("You don't have this stock")
        # update the cash that the user has
        db.execute("UPDATE users SET cash = cash + :totprice WHERE id = :id", id=session["user_id"], totprice=totprice)

        return redirect("/")
    else:
        return render_template("sell.html", rows2=rows2)


@app.route("/password", methods=["GET", "POST"])
def passowrd():
    """change password"""
    if request.method == "POST":
        # check if the user enters his/her current password
        password = request.form.get("password")
        if not request.form.get("password"):
            return apology("Provide password")
        # ask for the new password
        password_new = request.form.get("newpassword")
        if not request.form.get("newpassword"):
            return apology("provide new password")
        # ask for the confirmation of the new password
        confirmation = request.form.get("confirmation")
        if not request.form.get("confirmation"):
            return apology("Provide confirmation password")
        # check if those two match
        if password_new not in confirmation:
            return apology("new passwords are not matched")
        # hash the password
        hash = generate_password_hash(password_new)
        # update the password on the users table
        password_final = db.execute("UPDATE users SET hash = :hash WHERE id = :id", id=session["user_id"], hash=hash)

        return redirect("/")

    else:
        return render_template("password.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
