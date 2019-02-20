import os
import datetime

import matplotlib.pyplot as plt
import pandas as pd

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")



@app.route("/history")
@login_required
def history():
    """Display all records for users"""

    rows = db.execute("SELECT counter, expenses, amount, note, date FROM record WHERE id = :id", id=session["user_id"])

    rows1 = db.execute("SELECT spend FROM users where id = :id", id=session["user_id"])

    return render_template("history.html", rows=rows, rows1=rows1)



@app.route("/")
@login_required
def index():
    """Display the pie chart and total expenditures for each type of expenses"""

    home = db.execute("SELECT home FROM totalcompute WHERE id = :id", id = session["user_id"])
    personalcare = db.execute("SELECT personalcare FROM totalcompute WHERE id = :id", id=session["user_id"])
    food = db.execute("SELECT food FROM totalcompute WHERE id = :id", id = session["user_id"])
    child = db.execute("SELECT child FROM totalcompute WHERE id = :id", id = session["user_id"])
    debt = db.execute("SELECT debt FROM totalcompute WHERE id = :id", id = session["user_id"])
    healthcare = db.execute("SELECT healthcare FROM totalcompute WHERE id = :id", id = session["user_id"])
    transportation = db.execute("SELECT transportation FROM totalcompute WHERE id = :id", id = session["user_id"])
    petcare = db.execute("SELECT petcare FROM totalcompute WHERE id = :id", id = session["user_id"])
    entertainment = db.execute("SELECT entertainment FROM totalcompute WHERE id = :id", id = session["user_id"])
    others = db.execute("SELECT others FROM totalcompute WHERE id = :id", id = session["user_id"])

    # Check if the expenditure of each type exists and convert the dict to float
    if home:
        homec = float(home[0]["home"])
    else:
        homec = 0

    if food:
        foodc = float(food[0]["food"])
    else:
        foodc = 0

    if personalcare:
        personalcarec = float(personalcare[0]["personalcare"])
    else:
        personalcarec = 0

    if child:
        childc = float(child[0]["child"])
    else:
        childc = 0

    if debt:
        debtc = float(debt[0]["debt"])
    else:
        debtc = 0

    if healthcare:
        healthcarec = float(healthcare[0]["healthcare"])
    else:
        healthcarec = 0

    if transportation:
        transportationc = float(transportation[0]["transportation"])
    else:
        transportationc = 0

    if petcare:
        petcarec = float(petcare[0]["petcare"])
    else:
        petcarec = 0

    if entertainment:
        entertainmentc = float(entertainment[0]["entertainment"])
    else:
        entertainmentc = 0

    if others:
        othersc = float(others[0]["others"])
    else:
        othersc = 0
    # Display the total expenditures for each type of expenses
    totals = db.execute("SELECT home, personalcare, food, child, debt, healthcare, transportation, petcare, entertainment, others FROM totalcompute WHERE id = :id",
            id=session["user_id"])

    # Plot the pie chart
    category = ["home", "personalcare", "food", "child", "debt", "healthcare", "transportation", "petcare", "entertainment", "others"]
    expenses = pd.Series([homec, personalcarec, foodc, childc, debtc, healthcarec, transportationc, petcarec, entertainmentc, othersc], index=['','','','','','','','','',''], name='Expenses')
    plt.ylabel('')
    expenses.plot.pie(figsize=(8, 8))
    plt.legend(category, loc=3, fontsize=10)
    plt.title("Overall Expenditure", size=20)

    plt.savefig("static/images/pie.jpg")

    return render_template("plotly.html", totals=totals)



@app.route("/calendar", methods=["GET", "POST"])
@login_required
def calendar():
    """Record the type of expenses and the amount with optional notes"""
    if request.method == "POST":

        note = request.form.get("note")
        # return apology page if the amount isn't provided correctly
        amount = float(request.form.get("amount"))
        if amount < 0 or not amount:
            return apology("provide a valid amount")

        expenses = request.form.get("expenses")

        home = db.execute("SELECT home FROM totalcompute WHERE id = :id", id = session["user_id"])
        personalcare = db.execute("SELECT personalcare FROM totalcompute WHERE id = :id", id=session["user_id"])
        food = db.execute("SELECT food FROM totalcompute WHERE id = :id", id = session["user_id"])
        child = db.execute("SELECT child FROM totalcompute WHERE id = :id", id = session["user_id"])
        debt = db.execute("SELECT debt FROM totalcompute WHERE id = :id", id = session["user_id"])
        healthcare = db.execute("SELECT healthcare FROM totalcompute WHERE id = :id", id = session["user_id"])
        transportation = db.execute("SELECT transportation FROM totalcompute WHERE id = :id", id = session["user_id"])
        petcare = db.execute("SELECT petcare FROM totalcompute WHERE id = :id", id = session["user_id"])
        entertainment = db.execute("SELECT entertainment FROM totalcompute WHERE id = :id", id = session["user_id"])
        others = db.execute("SELECT others FROM totalcompute WHERE id = :id", id = session["user_id"])

        # Recognize the type of expenses and update the amount of the chosen expense type
        if expenses == "home":
            if home:
                home = home[0]["home"]+amount
                db.execute("UPDATE totalcompute SET home = :home WHERE id = :id", id=session["user_id"], home=home)
            else:
                db.execute("INSERT INTO totalcompute (id, home) VALUES(:id, :home)", id=session["user_id"], home=amount)

        elif expenses == "personalcare":
            if personalcare:
                personalcare = personalcare[0]["personalcare"]+amount
                db.execute("UPDATE totalcompute SET personalcare = :personalcare WHERE id = :id", id=session["user_id"], personalcare=personalcare)
            else:
                db.execute("INSERT INTO totalcompute (id, personalcare) VALUES(:id, :personalcare)", id=session["user_id"], personalcare=amount)

        elif expenses == "food":
            if food:
                food = food[0]["food"]+amount
                db.execute("UPDATE totalcompute SET food = :food WHERE id = :id", id=session["user_id"], food=food)
            else:
                db.execute("INSERT INTO totalcompute (id, food) VALUES(:id, :food)", id=session["user_id"], food=amount)

        elif expenses == "child":
            if child:
                child = child[0]["child"]+amount
                db.execute("UPDATE totalcompute SET child = :child WHERE id = :id", id=session["user_id"], child=child)
            else:
                db.execute("INSERT INTO totalcompute (id, child) VALUES(:id, :child)", id=session["user_id"], child=amount)

        elif expenses == "debt":
            if debt:
                debt = debt[0]["debt"]+amount
                db.execute("UPDATE totalcompute SET debt = :debt WHERE id = :id", id=session["user_id"], debt=debt)
            else:
                db.execute("INSERT INTO totalcompute (id, debt) VALUES(:id, :debt)", id=session["user_id"], debt=amount)

        elif expenses == "healthcare":
            if healthcare:
                healthcare = healthcare[0]["healthcare"]+amount
                db.execute("UPDATE totalcompute SET healthcare = :healthcare WHERE id = :id", id=session["user_id"], healthcare=healthcare)
            else:
                db.execute("INSERT INTO totalcompute (id, healthcare) VALUES(:id, :healthcare)", id=session["user_id"], healthcare=amount)

        elif expenses == "transportation":
            if transportation:
                transportation = transportation[0]["transportation"]+amount
                db.execute("UPDATE totalcompute SET transportation = :transportation WHERE id = :id", id=session["user_id"], transportation=transportation)
            else:
                db.execute("INSERT INTO totalcompute (id, transportation) VALUES(:id, :transportation)", id=session["user_id"], transportation=amount)

        elif expenses == "petcare":
            if petcare:
                petcare = petcare[0]["petcare"]+amount
                db.execute("UPDATE totalcompute SET petcare = :petcare WHERE id = :id", id=session["user_id"], petcare=petcare)
            else:
                db.execute("INSERT INTO totalcompute (id, petcare) VALUES(:id, :petcare)", id=session["user_id"], petcare=amount)

        elif expenses == "entertainment":
            if entertainment:
                entertainment = entertainment[0]["entertainment"]+amount
                db.execute("UPDATE totalcompute SET entertainment = :entertainment WHERE id = :id", id=session["user_id"], entertainment=entertainment)
            else:
                db.execute("INSERT INTO totalcompute (id, entertainment) VALUES(:id, :entertainment)", id=session["user_id"], entertainment=amount)

        elif expenses == "others":
            if others:
                others = others[0]["others"]+amount
                db.execute("UPDATE totalcompute SET others = :others WHERE id = :id", id=session["user_id"], others=others)
            else:
                db.execute("INSERT INTO totalcompute (id, others) VALUES(:id, :others)", id=session["user_id"], others=amount)

        # update the record
        db.execute("INSERT INTO record (expenses, id, amount, note, date) VALUES(:expenses, :id, :amount, :note, :date)", expenses=expenses, id=session["user_id"], amount=amount, note=note, date=now.strftime("%m/%d/%Y %H:%M:%S"))
        # update the cumulative expenditure of the user
        spend = db.execute("SELECT spend FROM users WHERE id = :id", id=session["user_id"])
        new_spend = spend[0]["spend"] + amount
        db.execute("UPDATE users SET spend = :spend WHERE id = :id", id=session["user_id"], spend=new_spend)


        return redirect("/")
    else:
        return render_template("calendar.html")



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


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Let users delete any record they need to"""

    if request.method == "POST":
        expenses = request.form.get("expenses")
        # safety check for input expense type
        if not expenses:
            return apology("Provide an expense type")
        # counter serves as an index
        counter = request.form.get("counter")
        # safety check for counter
        if not counter:
            return apology("Provide a valid index")
        # check if the record the users intend to delete exists
        todelete = db.execute("SELECT expenses FROM record WHERE id = :id AND counter = :counter", id=session["user_id"], counter=counter)
        # if so, delete the record. else, return apology
        if todelete:
            db.execute("DELETE FROM record WHERE id = :id AND counter = :counter", id=session["user_id"], counter=counter)

        else:
            return apology("You don't have this record")

        return redirect("/")
    else:
        return render_template("delete.html")



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

