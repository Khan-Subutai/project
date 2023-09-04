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

### Create route for index.html what a user would see when first visitng the website ###
@app.route("/", methods=['GET', 'POST'])
def index():
    """ Render the landing page of the web app """
    if request.method == "GET":
        return render_template("index.html", user_name=session["user_name"])
### End route for rendering the homepage of the web app ###


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


