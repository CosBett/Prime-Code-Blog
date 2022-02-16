from flask import Flask
from config import Config
from flask_mail import Mail
from flask_login import LoginManager, login_user, login_required, logout_user,current_user
from flask_sqlalchemy import SQLAlchemy
# from flask_bootstraps import Bootstrap

# bootstrap = Bootstrap()

app = Flask(__name__)

#create auth instance
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'signin'

db = SQLAlchemy()
mail = Mail()

def create_app():
  app.config.from_object (Config)
  # Registering blueprint
  
  from .main import main as main_blueprint
  from .auth import auth as auth_blueprint
  
  app.register_blueprint(main_blueprint)
  app.register_blueprint(auth_blueprint)

  mail.init_app(app)
  # Initialise bootstrap instance
  # bootstrap.init_app(app)
  
  return app