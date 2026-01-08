'''
Stores the applications configuration settings
'''
import os
<<<<<<< HEAD
from dotenv import load_dotenv
from datetime  import timedelta
=======
from python_dotenv import load_dotenv
>>>>>>> feature/products

load_dotenv()

class Config():
    SECRET_KEY=os.getenv('SECRET_KEY')
    SQALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_SAMESITE = 'None'
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
    JWT_REFRESH_COOKIE_NAME = "refresh_token_cookie"
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
