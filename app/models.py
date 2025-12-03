from app import db, bcrypt
import uuid
from datetime import datetime
from sqlalchemy import TIMESTAMP, Enum
from sqlalchemy.sql import func


class Users(db.Model):
    '''
    stores user data
    '''
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, nullable=False, unique=True, default=uuid.uuid4)
    email = db.Column(db.String(50), nullable=False, unique=True)
    passwordhash = db.Column(db.String(100), nullable=False)
    role = db.Column(Enum('member', 'admin', 'superadmin', name='role_enum'), nullable=False, default='member')
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    registered_on = db.Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    def __init__(email, password):
        '''
        instantiates a user object
        '''
        self.email = email
        self.passwordhash = self.generate_passwordhash(password)

    def generate_passwordhash(self, password):
        '''
        hashes the password for security reasons
        '''
        return bcrypt.generate_password_hash(password)
