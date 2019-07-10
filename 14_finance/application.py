import os
from datetime import datetime

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
    return table()

@app.route("/index", methods=["GET"])
@login_required
def table():
    user_id = session["user_id"]
    stocks_owned_row = db.execute("SELECT ticker, quantity FROM stocks_owned WHERE user_id = :user_id", user_id=user_id)
    total_value = 0
    rows = []
    for row in stocks_owned_row:
        tmp_row = [row["ticker"], row["quantity"]]
        response = lookup(row["ticker"])
        tmp_row.append(usd(response["price"]))
        value = response["price"] * row["quantity"]
        tmp_row.append(usd(value))
        rows.append(tmp_row)
        # add total value
        total_value += value
    # get cash value of user
    user_info = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
    cash = user_info[0]["cash"]
    total_value += cash
    return render_template("index.html", rows = rows, cash=usd(cash), total_value=usd(total_value))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        # Ensure submitted form has no nil entries
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("Please make sure the form has been filled up", 400)
        # Ensure number of shares are not negative
        try:
            if int(request.form.get("shares")) < 0:
                return apology("Please make sure number of shares purchased are a positive integer", 400)
        except:
            return apology("Please make sure number of shares purchased are a positive integer", 400)
        
        # Lookup price of stock
        response = lookup(request.form.get("symbol"))
        
        if response is not None:
            # Parse response
            price = response["price"]
        else:
            return apology("Stock not found", 400)
        
        # Establish variables
        user_id = session["user_id"]
        quantity = int(request.form.get("shares"))
        total_cost = quantity * price
        time = datetime.now()
        share = str(request.form.get("symbol")).upper()
        
        # Render apology if user cannot afford shares
        old_balance_row = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=user_id)
        old_balance = old_balance_row[0]["cash"]
        if total_cost > old_balance:
            return apology("You cannot afford the purchase", 400)
        
        # Add transaction to transactions table
        db.execute("INSERT INTO transactions(user_id, time_of_purchase, share, quantity, cost, transaction_type) VALUES(:user_id, :time, :share, :quantity, :cost, 'B')", user_id=user_id, time=time, share=share, quantity=quantity, cost=total_cost)
        
        # Add to stocks_owned table
        stocks_owned_count = db.execute("SELECT COUNT(*) AS count FROM stocks_owned WHERE user_id = :user_id AND ticker = :share", user_id=user_id, share=share)
        stocks_owned_row = db.execute("SELECT quantity FROM stocks_owned WHERE user_id = :user_id AND ticker = :share", user_id=user_id, share=share)
        if stocks_owned_count[0]["count"] == 0:
            db.execute("INSERT INTO stocks_owned(user_id, ticker, quantity) VALUES(:user_id, :share, :quantity)", user_id=user_id, share=share, quantity=quantity)
        else:
            old_quantity = stocks_owned_row[0]["quantity"]
            new_quantity = old_quantity + quantity
            db.execute("UPDATE stocks_owned SET quantity = :new_quantity WHERE user_id = :user_id AND ticker = :share", new_quantity=new_quantity, user_id=user_id, share=share)
        
        # Deduct cash from user
        new_balance = old_balance - total_cost
        db.execute("UPDATE users SET cash = :new_balance WHERE id = :user_id", new_balance=new_balance, user_id=user_id)
        
        # Success
        return render_template("success_buy.html", ticker=share, quantity=quantity, cost=usd(total_cost), balance=usd(new_balance))
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get('username', 0, type=str)
    if len(username) > 1:
        checkAvailability = db.execute("SELECT COUNT(*) AS count FROM users WHERE username = :username", username=username)
        if checkAvailability[0]["count"] == 0:
            return jsonify(availability="true")
    return jsonify(availability="false")


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    transactions_list = []
    transaction_info = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id=user_id)
    for row in transaction_info:
        tmp_row = []
        if row["transaction_type"] == "B":
            tmp_row.append("Buy")
        else:
            tmp_row.append("Sell")
        tmp_row.append(row["time_of_purchase"])
        tmp_row.append(row["share"])
        tmp_row.append(row["quantity"])
        tmp_row.append(usd(row["cost"]))
        transactions_list.append(tmp_row)
    return render_template("history.html", rows=transactions_list)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return table()

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

@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    user_id = session["user_id"]
    # User reached route via POST
    if request.method == "POST":
        # Ensure value is entered for amount
        if not request.form.get("amount"):
            return apology("please enter an amount", 400)
        # Ensure amount value is a positive float
        amount = request.form.get("amount")
        try:
            amount = float(amount)
            round(amount, 2)
            if amount < 0:
                return apology("please add a positive number", 400)
        except:
            return apology("please add a positive number", 400)
            
        # Lookup existing cash
        user_info = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=user_id)
        cash = user_info[0]["cash"]
        
        # Add cash balance to user acount
        cash = cash + amount
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=cash, user_id=user_id)

        return render_template("cash_success.html", amount=usd(amount), cash=usd(cash))
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        return render_template("cash.html", cash=usd(cash[0]["cash"]))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    # User reached route via POST
    if request.method == "POST":
        # Ensure value is entered for ticker symbol
        if not request.form.get("symbol"):
            return apology("please enter a ticker symbol", 400)
            
        # Lookup price of stock
        response = lookup(request.form.get("symbol"))
        
        if response is not None:
            # Parse response
            company = response["name"]
            price = response["price"]
            # render quoted.html
            return render_template("quoted.html", company=company, price=usd(price))
        else:
            return apology("Stock not found", 400)
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST
    if request.method == "POST":
        # Ensure username was created
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was created
        elif not request.form.get("password"):
            return apology("must provide password", 400)
            
        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must enter confirmation", 400)
        
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # Ensure passwords match
        if password != confirmation:
            return apology("passwords do not match", 400)
            
        # Reject duplication username
        checkAvailability = db.execute("SELECT COUNT(*) AS count FROM users WHERE username = :username", username=username)
        if checkAvailability[0]["count"] > 0:
            return apology("username already exists", 400)
            
        # Insert new user into db
        hashed_pw = generate_password_hash(password)
        db.execute("INSERT INTO users(username, hash) VALUES(:user, :hash)", user=username, hash=hashed_pw)
        
        # Redirect user to login page
        return redirect("/login")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Please select a stock", 400)
        if not request.form.get("shares"):
            return apology("Please enter the number of shares you wish to sell", 400)
        try:
            num_shares = int(request.form.get("shares"))
            if num_shares < 1:
                return apology("Please provide a positive integer", 400)
        except:
            return apology("Please provide a positive integer", 400)
            
        ticker = request.form.get("symbol")
        
        # Check that user has sufficient shares to sell
        existing_row = db.execute("SELECT quantity FROM stocks_owned WHERE user_id = :user_id AND ticker = :ticker", user_id=user_id, ticker=ticker)
        existing_shares = existing_row[0]["quantity"]
        if existing_shares < num_shares:
            return apology(f"You have insufficient shares of {ticker}", 400)
            
        # Update stocks_owned database
        new_quantity = existing_shares - num_shares
        db.execute("UPDATE stocks_owned SET quantity = :new_quantity WHERE user_id = :user_id AND ticker = :ticker", new_quantity=new_quantity, user_id=user_id, ticker=ticker)
        # Delete row if quantity becomes 0
        db.execute("DELETE FROM stocks_owned WHERE quantity = 0")
        
        # Update transactions database
        time = datetime.now()
        response = lookup(ticker)
        total_cost = response["price"] * num_shares
        db.execute("INSERT INTO transactions(user_id, time_of_purchase, share, quantity, cost, transaction_type) VALUES(:user_id, :time, :share, :quantity, :cost, 'S')", user_id=user_id, time=time, share=ticker, quantity=num_shares, cost=total_cost)
        
        # Update user's cash
        old_cash_row = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        old_cash = old_cash_row[0]["cash"]
        new_cash = old_cash + total_cost
        db.execute("UPDATE users SET cash = :new_cash WHERE id = :user_id", new_cash=new_cash, user_id=user_id)
        
        # Success
        return render_template("success_sell.html", quantity=num_shares, ticker=ticker, cost=usd(total_cost), unit_cost=usd(total_cost/num_shares), new_cash=usd(new_cash))
    else:
        # Obtain list of stocks that the user posesses
        stock_row = db.execute("SELECT ticker FROM stocks_owned WHERE user_id = :user_id", user_id=user_id)
        stocks = []
        for row in stock_row:
            stocks.append(row["ticker"])
        return render_template("sell.html", shares=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
