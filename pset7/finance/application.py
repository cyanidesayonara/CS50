from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import time

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    """ Show current portfolio """
    
    cash = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"]) #SQL code returns a list of dicts from db where id is user id
    money = cash[0]["cash"]                                                          # we then take the list item and get the value of "cash"
    
    stocks = db.execute("SELECT * FROM stocks WHERE id = :id", id=session["user_id"])
    history = db.execute("SELECT * FROM history WHERE id = :id", id=session["user_id"])

    total = money                                                                         # user's total assets
    
    signal = 0
    
    if len(stocks) == 0:                # hacky way of signaling whether user owns any stocks (to hide/display buy form)
        signal = 1
        
    else:
        for stock in stocks:                                                                # iterate through list of stocks
            stock.update(lookup(stock["symbol"]))                       # lookup data for each stock's symbol, update add it to stock
            total += (stock["price"] * stock["shares"])                                 # total assets incremented with every stock
            stock["orig"] = 0                                                           # original price set to 0
            for x in range(len(history)):
                if stock["symbol"] == history[x]["symbol"]:                                 # for every transaction where symbol,
                    sum = (history[x]["value"] * int(history[x]["shares"]))             # loop gets original value, 
                    if int(history[x]["shares"]) < 0:                                           # negative if share's are negative
                        sum = -(sum)                                                                # it all gets added to original price
                    stock["orig"] += sum
            dif = stock["orig"] - stock["price"] * stock["shares"]                              # difference of original and current value
            stock["change"] = (dif / stock["orig"]) * 100                               # percentage of same
            stock["value"] = usd(stock["price"] * stock["shares"])                                       
            stock["price"] = usd(stock["price"])                                    # money values formatted to usd
            stock["orig"] = usd(stock["orig"])
        
    return render_template("index.html", cash=usd(money), total=usd(total), stocks=stocks, username=cash[0]["username"], signal=signal)    # stocks data and username returned to index page

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    if request.method == "POST":                                                    # if request method was post,
                                                                                        # request meaning when you pressed the button
        if not request.form.get("symbol"):
            return apology("must provide stock")                                # if field was empty, you have to apologize?
           
        elif not request.form.get("shares"):
            return apology("must provide shares")
            
        quote = lookup(request.form.get("symbol"))                      # lookup stats for requested symbol

        if quote == None:                                                   # if none exist
            return apology("stock doesn't exists")
         
        try:
            shares = int(request.form.get("shares"))                     # form gives a string, convert to int
        except ValueError:                                          # this handy way to validate numeric input from stackoverflow
            return apology("invalid shares")
        
        if  not shares > 0:
            return apology("number must be positive")
        
        value = quote["price"] * shares                            # calculate value of purchase
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])   # get cash from db

        if (cash[0]["cash"]) < value:                                   # if less cash than value
            return apology("not enough money")
            
        db.execute("UPDATE users SET cash = cash - :value WHERE id = :id", value=value, id=session["user_id"])  # update cash

        stocks = db.execute("SELECT * FROM stocks WHERE id = :id and symbol = :symbol", id=session["user_id"], symbol=request.form.get("symbol"))
                                                                               # if stock is not already owned, stock returns no results, in which case insert stock into stocks
        if len(stocks) == 0:                        # else update stocks, also of course insert into history
                                                                                                              
            db.execute("INSERT INTO stocks (id, symbol, shares, name) VALUES(:id, :symbol, :shares, :name)", id=session["user_id"], symbol=request.form.get("symbol"), shares=shares, name=quote["name"])
        else:
            db.execute("UPDATE stocks SET shares = shares + :x WHERE symbol = :symbol", x=request.form.get("shares"), symbol=request.form.get("symbol"))
                                                                                                                                                            # history gets original price and time and stuff
            
        db.execute("INSERT INTO history (id, time, value, shares, symbol) VALUES(:id, :time, :value, :shares, :symbol)", id=session["user_id"], time=time.asctime(time.localtime(time.time()))[4:], value=quote["price"], shares=shares, symbol=request.form.get("symbol"))
            
        return redirect(url_for("index"))       # go back to index
        
    else:
        return render_template("buy.html")          # if didn't come here by post, try again

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    
    history = db.execute("SELECT * FROM history WHERE id = :id", id=session["user_id"])         # get history from db
    
    for stock in history:                                                   
        stock["price"] = stock["value"] * stock["shares"]               # for each stock, get original purchase value
        if int(stock["shares"]) < 0:
            stock["price"] = -(stock["price"])                      # if negative shares (sell), make value negative
        stock["price"] = usd(stock["price"])                                # dispite multiplication making it positive
    
    return render_template("history.html", history=history)         # return history data to page

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
            
        username, password = request.form.get("username"), request.form.get("password")
            
        if len(username) > 20 or len(password) > 20:
            return apology("invalid")
            
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"), ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            username = username.replace(old, new)

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(password, rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    if request.method == "POST":                            # gotta be post
        
        if not request.form.get("symbol"):                   
            return apology("field can't be empty")
            
        if not request.form.get("symbol").isalpha:
            return apology("invalid input")
            
        quote = lookup(request.form.get("symbol"))           # just lookup value for stock sent through form
        
        if quote == None:                                       # if none exist
            return apology("stock doesn't exists")
        
        else:                                                   # else return quote
            return render_template("quoted.html", name=quote["name"], price=usd(quote["price"]), symbol=quote["symbol"])   
        
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    session.clear()
    
    if request.method == "POST":
        
        if not request.form.get("username"):
            return apology("must provide username")

        elif not request.form.get("password"):
            return apology("must provide password")
            
        elif not request.form.get("confirmation"):
            return apology("confirm password")
            
        username, password, confirmation = request.form.get("username"), request.form.get("password"), request.form.get("confirmation")
            
        if len(username) > 20 or len(password) > 20 or len(confirmation) > 20:      # length limited to a totally arbitrary 20
            return apology("invalid")
        
        elif not password == confirmation:      # if passwords don't match
            return apology("passwords don't match")
            
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"), ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            username = username.replace(old, new)                                           # escape bad characters
    
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        if len(rows) >= 1:                          # if username exists
            return apology("username taken")
            
        hash = pwd_context.hash(password)       # create hash for password
                                                                                    # insert user into users, returns id
        id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=username, hash=hash)
            
        session["user_id"] = id     # remember which user has logged in

        return redirect(url_for("index"))           # redirect user to home page
    
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    if request.method == "POST":
        
        if not request.form.get("symbol"):
            return apology("symbol missing")
        
        if not request.form.get("shares"):                              # get input
            return apology("amount missing")
            
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a number")
            
        if not request.form.get("symbol").isalpha:
            return apology("invalid")
        
        symbol = request.form.get("symbol")

        stocks = db.execute("SELECT * FROM stocks WHERE id = :id and symbol = :symbol", id=session["user_id"], symbol=symbol)
        
        if len(stocks) == 0:                        # see if stock exists in db
            return apology("symbol not owned")
 
        owned = stocks[0]["shares"]
                                                                            # if stocks owned is fewer that request
        if owned < shares:
            return apology("not enough shares")
            
        quote = lookup(symbol)                                       # get quote
            
        if quote == None:                                             # if quote is none, return
            return apology("stock doesn't exists")

        else:                                                                 # else update cash, insert transaction to history
            value = shares * quote["price"]            # get value of transaction
            db.execute("UPDATE users SET cash = cash + :value WHERE id = :id", value=value, id=session["user_id"])
            db.execute("INSERT INTO history (id, time, value, shares, symbol) VALUES(:id, :time, :value, :shares, :symbol)", id=session["user_id"], time=time.asctime(time.localtime(time.time()))[4:], value=-(value), shares=-(shares), symbol=symbol)
            
        if shares == share:                                      # if all stocks sold, delete from stocks
            db.execute("DELETE FROM stocks WHERE id = :id and symbol = :symbol", id=session["user_id"], symbol=request.form.get("symbol"))
            
        else:                                                               # else, just decrement shares
            db.execute("UPDATE stocks SET shares = shares - :sell WHERE id = :id and symbol = :symbol", sell=int(request.form.get("shares")), id=session["user_id"], symbol=request.form.get("symbol"))
        
        return redirect(url_for("index"))
        
    else:
        return render_template("sell.html")

@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    """Add cash to user."""
    
    if request.method == "POST":
        
        if not request.form.get("cash"):                # if empty field
            return apology("field empty")

        try:
            cash = float(request.form.get("cash"))          # if input is float
        except ValueError:                                  # else error
            return apology("cash must be a number")  
            
        cash = int(request.form.get("cash"))
            
        if not cash > 0:                                                     # if input not positive
            return apology("number must be positive")       
                                                                                # update cash with added cash
        db.execute("UPDATE users SET cash = cash + :money WHERE id = :id", money=cash, id=session["user_id"])
        
        return redirect(url_for("index"))
        
    else:
        return render_template("index.html")
        
@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Change password"""
    
    if request.method == "POST":
        
        if not request.form.get("new_password"):
            return apology("field empty")                                       # no empty fields
            
        elif not request.form.get("confirmation"):
            return apology("field empty")
            
        elif not request.form.get("new_password") == request.form.get("confirmation"):
            return apology("passwords don't match")                                     # password must match
            
        password = request.form.get("new_password")
        
        if len(password) > 20:
            return apology("password too long")
            
        hash = pwd_context.hash(password)                                   # get hash for new pw
        
        db.execute("UPDATE users SET hash = :hash WHERE id = :id", hash=hash, id=session["user_id"]) # update hash field in db
        
        return redirect(url_for("index"))
            
    else:
        return render_template("password.html")
