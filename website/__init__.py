from flask import Flask  # python framework we use in this project
from flask_sqlalchemy import SQLAlchemy  # toolkit and ORM for python-facilitates
                                         # the communication between program and databases
from os import path  
from flask_login import LoginManager  # help to manage all logins

db = SQLAlchemy()  # database object which use throughout project to do tasks related to database
DB_NAME = "database.db"  # define database name


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '34242343244898'  # encrypt cookies and session data 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # tell flask where database is located
    db.init_app(app)  # initialize database fo flask app

    from .views import views  # register our blueprints in other files
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')  # register imported blueprints
    app.register_blueprint(auth, url_prefix='/')

    from .models import User  # import models

    with app.app_context():  # create database
        db.create_all()

    login_manager = LoginManager()  
    login_manager.login_view = 'auth.login'  # if not logged in redirect to this page
    login_manager.init_app(app)  # specifying the app we using 

    @login_manager.user_loader  # use this function to load the user
    def load_user(id):
        return User.query.get(int(id))

    return app

