'''
Stores the applications configuration settings
'''
import os
from python_dotenv import load_dotenv

load_dotenv()

class Config():
    SECRET_KEY=os.getenv('SECRET_KEY')
    SQALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
