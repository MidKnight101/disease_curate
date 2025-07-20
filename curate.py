from flask import Flask, render_template, url_for, request, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import re
import psycopg2
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import mapped_column
from datetime import datetime


curate = Flask(__name__)

curate.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mainuser:Afferloo@localhost/user_info'
curate.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(curate) #creates db for this app

class User(db.Model): #user object that takes in empty db and creates a table within it called 'users'
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True) #unique ID for each user
    
    uname = db.Column(db.String(15), unique=True, nullable=False) #string username
    pword = db.Column(db.String(30), nullable=False) #string password
    
    favorites = db.relationship('user_faves', backref = 'user', cascade = "all,delete", lazy = True)

    def __init__ (self, uname, pword): #takes passed in values and creates an instance of user object with them
        self.uname = uname
        self.pword = pword

class user_faves(db.Model):
    __tablename__ = "favs"
    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, db.ForeignKey(User.id))

    title = db.Column(db.String(100), nullable = False)
    media_url = db.Column(db.String(100), nullable = False)
    type_of_media = db.Column(db.String(100),  nullable = False)
    time_added_to_db = db.Column(db.DateTime,default = datetime.utcnow, nullable = False)

    def __init__(self, userId, title, type_of_media):
        self.userId = userId
        self.title = title
        self.type_of_media = type_of_media
    

        
        
@curate.route('/')
def index():
    return render_template('greetscreen.html')

@curate.route('/about')
def about():
    return render_template('about.html')

@curate.route('/contact')
def contact():
    return render_template('contact.html')


@curate.route('/curate')
def curate_page():
    return render_template('mainpage.html')

@curate.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        username = request.form['uname']
        password = request.form['pword']

        user = User.query.filter_by(uname = username, pword = password).first()
        if user:
            return 'Signed up!'
        

    return render_template('login.html')

@curate.route('/signup', methods = ['GET', 'POST'])
def reroute_to_signup():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pword']
        
        user = User.query.filter_by(uname = username, pword = password).first()
        if user:
            return 'Signed up successfully!'
        else:
            return 'Invalid credentials.'
    return render_template('signup.html')
        


@curate.route('/submit', methods = ['GET', 'POST']) #interacts with the form in the greetscreen html file; once the input tag 'submit' is clicked, we post the data from the user into the database
def submit():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pword']
        
        user = User(uname = username, pword = password)
        db.session.add(user)
        db.session.commit()
    return redirect('/')    

if __name__ == "__main__":
    curate.run(debug=True)