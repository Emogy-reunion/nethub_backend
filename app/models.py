from app import db, bcrypt
import uuid
from datetime import datetime
from sqlalchemy import TIMESTAMP, Enum
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

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
    products = db.relationship('Products', back_populates='user', lazy='selectin')

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

    def check_passwordhash(self, password):
        '''
        checks if the input password matches the stored hash
        '''
        return bcrypt.check_password_hash(self.passwordhash, password)


class Products(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(Enum('networking-devices', 'computer-accessories', name='product_category'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Float, default=0)
    description = db.Column(db.Text, nullable=False)
    features = db.Column(JSONB, nullable=False, default=dict)
    stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    user = db.relationship('Users', back_populates='products', lazy='selectin')
    images = db.relationship('ProductImages', back_populates='product', lazy='selectin', cascade='all, delete')

    @property
    def final_price(self):
        if not self.discount or self.discount <= 0:
            return self.price

        return self.price - (self.price * Decimal(self.discount) / Decimal(100))


    def get_preview(self):
        return {
                'product_id': self.id,
                'name': self.name,
                'price': self.price,
                'stock': self.stock,
                'discount': self.discount,
                'final_price': self.final_price,
                'image': self.images[0].filename if self.images else None
                }

    def get_full(self):
        return {
                'product_id': self.id,
                'name': self.name,
                'price': self.price,
                'final_price': self.final_price,
                'discount': self.discount,
                'description': self.description,
                'features': self.features,
                'stock': self.stock,
                'images': [image.filename for image in self.images] if self.images else None
                }

class ProductImages(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='cascade'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    product = db.relationship('Products', back_populates='images', lazy='selectin')
