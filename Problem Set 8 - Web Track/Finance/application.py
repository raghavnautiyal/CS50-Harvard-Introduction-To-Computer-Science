import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
   # Query infos from database
    rows = db.execute("SELECT * FROM transactions WHERE id = :user",
                          user=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :user",
                          user=session["user_id"])[0]['cash']

    # pass a list of lists to the template page, template is going to iterate it to extract the data into a table
    total = cash
    stocks = []
    for index, row in enumerate(rows):
        stock_info = lookup(row['symbol'])

        # create a list with all the info about the stock and append it to a list of every stock owned by the user
        stocks.append(list((stock_info['symbol'], stock_info['name'], row['shares'], stock_info['price'], round(stock_info['price'] * row['shares'], 2))))
        total += stocks[index][4]

    return render_template("index.html", stocks=stocks, cash=round(cash, 2), total=round(total, 2))



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        ans = lookup(request.form.get("symbol"))
        if not ans:
            return apology("Symbol doesn't exist")

        elif not request.form.get("shares"):
            return apology("Buy at least one share")

        else:
            name = ans["name"]
            symbol = ans["symbol"]
            price = ans["price"]
            shares = int(request.form.get("shares"))
            total = int(ans["price"]) * int(request.form.get("shares"))
            query = db.execute("SELECT cash FROM users WHERE id = :idi", idi=session.get("user_id"))
            print(query)
            cash = query[0]["cash"]
            print(cash)
            if total > int(cash):
                return apology("Can't afford")
            else:
                name = ans["name"]
                symbol = ans["symbol"]
                price = ans["price"]
                total = int(ans["price"]) * int(request.form.get("shares"))
                stock = db.execute("SELECT shares FROM transactions WHERE id = :user AND symbol = :symbol", user=session["user_id"], symbol=symbol)
                new_total = int(cash) - total
                if not stock:
                    row = db.execute("INSERT INTO transactions (id, username, symbol, name, shares, price, total) VALUES (:idi, (SELECT username FROM users WHERE id = :idi), :symbol, :name, :shares, :price,:total)", idi=session.get("user_id"), symbol=symbol, name=name, shares=int(request.form.get("shares")),price=price,total=total)
                else:
                    shares += stock[0]["shares"]
                    row = db.execute("UPDATE transactions SET shares = :newVal WHERE id = :idi", newVal=shares, idi=session.get("user_id"))

                new = db.execute("UPDATE users SET cash = :newVal WHERE id = :idi", newVal=new_total, idi=session.get("user_id"))
                db.execute("INSERT INTO history(id, symbol, shares, price) VALUES (:user, :symbol, :amount, :value)",user=session["user_id"], symbol=symbol, amount=shares, value=price)
                flash("Bought!")
                return redirect('/')

    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
     # query database with the transactions history
    rows = db.execute("SELECT * FROM history WHERE id = :user",
                            user=session["user_id"])

    # pass a list of lists to the template page, template is going to iterate it to extract the data into a table
    transactions = []
    for row in rows:
        stock_info = lookup(row['symbol'])

        # create a list with all the info about the transaction and append it to a list of every stock transaction
        transactions.append(list((stock_info['symbol'], stock_info['name'], row['shares'], row['price'], row['date'])))

    # redirect user to index page
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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    if request.method == "POST":
        ans = lookup(request.form.get("quote"))
        if not ans:
            name = ''
            symbol = ''
            price = ''
            return apology("Symbol doesn't exist")

        else:
            name = ans["name"]
            symbol = ans["symbol"]
            price = ans["price"]
            return render_template("quoted.html", name=name, price=price, symbol=symbol)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        elif request.form.get("confirmation") !=  request.form.get("password"):
            return apology("passwords must match", 403)

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username doesn't exist
        if len(rows) == 1:
            return apology("Username already exists", 403)

        # add user into database
        user = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=request.form.get("username"), password=generate_password_hash(request.form.get("password")))

        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # collect relevant informations
        amount=int(request.form.get("amount"))
        symbol=request.form.get("symbol")
        price=lookup(symbol)["price"]
        value=round(price*float(amount))

        # Update stocks table
        amount_before = db.execute("SELECT shares FROM transactions WHERE id = :user AND symbol = :symbol",
                          symbol=symbol, user=session["user_id"])[0]["shares"]
        print(amount_before)
        print(amount)

        amount_after = amount_before - amount

        # delete stock from table if we sold every unit we had
        if amount_after <= 0:
            db.execute("DELETE FROM transactions WHERE id = :user AND symbol = :symbol",
                          symbol=symbol, user=session["user_id"])

        # stop the transaction if the user does not have enough stocks
        elif amount_after < 0:
            return apology("That's more than the stocks you own")

        # otherwise update with new value
        else:
            db.execute("UPDATE transactions SET shares = :amount WHERE id = :user AND symbol = :symbol",
                          symbol=symbol, user=session["user_id"], amount=amount_after)

        # calculate and update user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = :user",
                          user=session["user_id"])[0]['cash']
        cash_after = cash + price * float(amount)

        db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                          cash=cash_after, user=session["user_id"])

        # Update history table
        db.execute("INSERT INTO history(id, symbol, shares, price) VALUES (:user, :symbol, :amount, :value)",
                user=session["user_id"], symbol=symbol, amount=-amount, value=value)

        # Redirect user to home page with success message
        flash("Sold!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # query database with the transactions history
        rows = db.execute("SELECT symbol, shares FROM transactions WHERE id = :user",
                            user=session["user_id"])

        # create a dictionary with the availability of the stocks
        stocks = {}
        for row in rows:
            stocks[row['symbol']] = row['shares']

        return render_template("sell.html", stocks=stocks)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)