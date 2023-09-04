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


### Create route for index.html what a user would see when first visitng the website ###
@app.route("/", methods=['GET', 'POST'])
def index():
    """ Render the landing page of the web app """
    if request.method == "GET":
        return render_template("index.html")
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


