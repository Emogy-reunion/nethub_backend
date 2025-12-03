from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Config

db = SQLAlchemy
bcrypt = Bcrypt()

def create_app():
    '''
    creates the flask's application instance
    return: application instance
    '''
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app()
    bcrypt.init_app()

    return app

