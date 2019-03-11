from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"
mail = Mail()

db = SQLAlchemy() #instantiating SQLAlchemy, database

def create_app(config_type):
    app = Flask(__name__)

    configuration = os.path.join(os.getcwd(),"config",config_type+".py") #cwd= current working directory, telling join the path of "config"
    app.config.from_pyfile(configuration) #config of the app is from python file

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app) #initiating after instantiation
    mail.init_app(app)

    from app.auth import auth
    from app.posts import posts

    app.register_blueprint(auth)
    app.register_blueprint(posts)

    return app
