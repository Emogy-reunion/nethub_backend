from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy
bcrypt = Bcrypt()

def create_app():
    '''
    creates the flask's application instance
    return: application instance
    '''
    app = Flask(__name__)

    db.init_app()
    bcrypt.init_app()

    return app

