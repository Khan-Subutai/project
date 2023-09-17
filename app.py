# Import needed libraries:
import os
import uuid
import datetime
import csv
import urllib
import sqlite3
from functools import wraps
from flask import Flask, request, jsonify, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import pytz

# configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
# FROM CS50 WEEK 9 + add ons
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

""" Code to be repeadeted throughout to use sqlite3 without the cs50 training wheels for SQLite3 implementation"""
# Connect to the SQLite db:
#   conn = sqlite3.connect('final.db')
# Create cursor
#   c = conn.cursor()
# Actually impement SQLite3 database to be useful:
#   c.execute("SQL commands to retrieve information from db)
#   variable = c.fetchall() -- Note fetchall is getting you what was found in the SQL query
# Commit transaction and close connection after each use of the database
#   conn.commit()
#   conn.close()
""" End code repeated throughout to get off the cs50 sqlite3 training wheels """

### Create ability to render apology web page letting the user know their input failed server side validation
def apology(message):
    return render_template("apology.html", message=message)
### End Aoplogy Function

### Create route for index.html what a user would see when first visitng the website ###
@app.route("/", methods=['GET', 'POST'])
def index():
    # Render the landing page of the web app
    if request.method == "GET":
        return render_template("index.html")
### End route for rendering the homepage of the web app ###


### Create route for essay2.html for when a user either clicks on the second carousel image or uses a nav-bar link ###
@app.route("/essay2", methods=['GET', 'POST'])
def essay2():
    # Render the landing page of the web app
    if request.method == "GET":
        return render_template("essay2.html")
### End route for rendering the essay2 of the web app ###


#### Create Subscribe Function ###
@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():

    # Clear any user_id from previous session
    session.clear()

    # Render the subscribe web page if the user clicks on subscribe
    if request.method == "GET":
        return render_template('subscribe.html')
    
    # The following code will be server side validation and finally storing the user's
    # username, password and email in a SQLITE3 database
    else:
    ## User input validation:
        # Ensure a user_name was entered
        user_name = request.form.get("user_name")
        if not user_name:
            return apology("Must Enter user_name")
        # Ensure a password was entered
        password = request.form.get("password")
        if not password:
            return apology("Must Enter Password")
        # Ensure the confirmation password = password
        confirm_p = request.form.get("confirm_p")
        if not confirm_p:
            return apology("Must Enter confirm password")
        # Ensure a user_name was entered
        email = request.form.get("email")
        if not email:
            return apology("Must Enter Email")
        # Check passwords against each other then hash to send hashed to db
        if password != confirm_p:
            return apology("Passowrd and password confirmation do not match")
        hashed_password = generate_password_hash(password)
    
    ## Pass user information into SQLite3 db
    conn = sqlite3.connect('project.db')
    c = conn.cursor()
    c.execute("INSERT INTO subscribers (user_name, hashed_password, email) VALUES (?, ?, ?)",
              (user_name, hashed_password, email))
    conn.commit()
    conn.close()

    # Create session for the user who just made subscriber so that they do not have to go to the login page
    # Query Database to get user information that they just submited, ... could this be done another way???
    # Also realize that for now basically the only functionality that this brings is to add the user's username to the navbar
    conn = sqlite3.connect('project.db')
    c = conn.cursor()
    c.execute("SELECT * FROM subscribers WHERE user_name = ?", (user_name,))
    user = c.fetchone() # fetchone used to store row from the table where user_name matches username
    conn.close() #... conn.commit() not needed as simply retrieving from the database

    session["user_id"] = user[0]
    session["user_name"] = user[1]
    session["user_email"] = user[3]

    # Now redirect to the home page
    return redirect("/")
### End subsrcibe function

### Create Login function, user logins will be required to view the subscriber materials
@app.route("/login", methods=["GET", "POST"])
def login():
    # clear any previous session
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    # If user uses login page to login method will be post i.e. else in this scenario
    else:
        user_name = request.form.get("user_name")
        if not user_name:
            return apology("Must enter User Name")
        password = request.form.get("password")
        if not password:
            return apology("Must enter Password")
    conn = sqlite3.connect('project.db')
    c = conn.cursor()
    c.execute("SELECT * FROM subscribers WHERE user_name = ?", (user_name,))
    user = c.fetchone() 
    conn.close() 
    if user == None:
        return apology("Invalid user name if you are not a subscriber jsut click subscribe to register")
    if not check_password_hash(user[2], password):
        return apology("Incorrect password please try again")
    session["user_id"] = user[0]
    session["user_name"] = user[1]
    session["user_email"] = user[3]
    return redirect("/")
### End login function

### Create login required function
# NOTE THIS FUNCTION IS TAKEN IN ITS ENTIRITY FROM CS50 WEEK 9 ALL CREDIT TO THE CS50 TEAM!!!!!
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return apology("Must subscribe to view this content")
        return f(*args, **kwargs)
    return decorated_function
### End login required function 

### Log Out Function:
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
### End Logout Function

### LAST FUNCTION!!!! Create function to only show Essay 3 if the user has "subscribed" and is logged in 
### Goal is to still allow Essay3 the AI arms race to be in the navbar as a link but if someone is not signed in to give an apology
### message and direct them to the subscribe page, once subscribed and logged in the user can now view Essay3 ###
### Create route for essay3.html for when user either click on the third carousel image or uses a nav-bar link ###

### Below is OG route for essay3.html, not requiring the user to be logged in
#@app.route("/essay3", methods = ['GET', 'POST'])
#def essay3():
#    if request.method == "GET":
#        return render_template("essay3.html")
### End route for rendering the essay of the web app ### 

### Login Required Essay3: 
@app.route("/essay3", methods=["GET", "POST"])
@login_required
def essay3():
    if request.method == "GET" or request.method == "POST":
        return render_template("essay3.html")
### End Essay3 "subscriber Access"