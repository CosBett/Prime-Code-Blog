from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, IntegerField,SubmitField,ValidationError
from wtforms.validators import InputRequired,Length,Email
from email_validator import validate_email
from ..models import User
class SigninForm(FlaskForm):
  username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=25)])

  remember = BooleanField('remember me')
  submit =  SubmitField('Login')

class SignupForm(FlaskForm):
  first_name = StringField('First name', validators=[InputRequired(), Length(min=4, max=15)])
  last_name = StringField('Last name', validators=[InputRequired(), Length(min=4, max=15)])
  email = StringField('email', validators=[InputRequired(),validate_email, Length(min=10, max =80)])
  username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
  password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=25)])
  password_confirm =PasswordField('password', validators=[InputRequired(), Length(min=8, max=25)])
  submit = SubmitField('SignUp')
  
  def validate_email(self,data_field):
      if User.query.filter_by(email = data_field.data).first():
            raise ValidationError("The Email has already been taken!")

  def validate_username(self, data_field):
      if User.query.filter_by(username = data_field.data).first():
            raise ValidationError("The username has already been taken")