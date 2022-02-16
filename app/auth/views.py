from flask import render_template, redirect,url_for
from app.auth import auth

@auth.route('/signin')
def signin():
  
    return render_template('signin.html')
@auth.route('/signup')
def signup():
  
    return render_template('signup.html')    