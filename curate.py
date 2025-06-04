from flask import Flask, render_template, url_for, request, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import re


curate = Flask(__name__)

curate.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mainuser:Afferloo@localhost/user_info'
curate.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(curate) #creates db for this app

class User(db.Model): #user object that takes in empty db and creates a table within it called 'users'
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True) #unique ID for each user
    
    uname = db.Column(db.String(15), unique=True, nullable=False) #string username
    pword = db.Column(db.String(30),unique=True, nullable=False) #string password
    
    
    def __init__ (self, uname, pword): #takes passed in values and creates an instance of user object with them
        self.uname = uname
        self.pword = pword
        
        
@curate.route('/')
def index():
    return render_template('greetscreen.html')

@curate.route('/test.html')
def main():
    return render_template('test.html')

@curate.route('/signup', methods = ['GET', 'POST'])
def reroute_to_signup():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pword']
        
        user = User.query.filter_by(uname = username, pword = password).first()
        if user:
            return 'Logged in successfully!'
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