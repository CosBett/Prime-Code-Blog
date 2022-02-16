from curses import flash
from flask import render_template,request, redirect,url_for
from flask_login import login_user,logout_user,login_required
from app.auth import auth
from app. models import User
from .forms import SigninForm,SignupForm

@auth.route('/signin', methods =['POST', 'GET'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user != None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Wrong Username or Password')

    return render_template('signin.html',form = form)

@auth.route('/signup')
def signup():
  
    return render_template('signup.html')    