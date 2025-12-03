from flask import Flask

def create_app():
    '''
    creates the flask's application instance
    return: application instance
    '''
    app = Flask(__name__)

    return app

