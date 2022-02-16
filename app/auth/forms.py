from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, IntegerField,SubmitField,ValidationError
from wtforms.validators import InputRequired,Length,Email

class SigninForm(FlaskForm):
  username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=25)])

  remember = BooleanField('remember me')
  submit =  SubmitField('Login')

class SignupForm(FlaskForm):
  first_name = StringField('First name', validators=[InputRequired(), Length(min=4, max=15)])
  last_name = StringField('Last name', validators=[InputRequired(), Length(min=4, max=15)])
  email = StringField('email', validators=[InputRequired(),Email(message='Invalid email'), Length(min=10, max =80)])
  username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
  password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=25)])
  password_confirm =PasswordField('password', validators=[InputRequired(), Length(min=8, max=25)])
  submit = SubmitField('SignUp')
  