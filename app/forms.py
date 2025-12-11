from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, DecimalField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, Length, Regexp, NumberRange, AnyOf, 
from app.utils.custom_form_validators import length_check, validate_features_field


class RegistrationForm(FlaskForm):
    '''
    validates the registration form data
    '''
    email = StringField('Email:', validators=[
        DataRequired,
        Email(),
        Length(min=4, max=45, message='Email must be between 4 and 45 characters!')
        ])

    password = PasswordField('Password: ', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long!"),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter!"),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter!"),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character!")
        ])

    confirmpassword = PasswordField('Confirm Password:', validators=[
        DataRequired(),
        EqualTo()
        ])

class LoginForm(FlaskForm):
    email = StringField('Email:' validators=[
        Email(),
        Length(min=4, max=45, message='Email must be between 4 and 45 characters!')
        ])
    password = PasswordField('Password:', validators=[
        DataRequired(),
        Length(min=2, max=50, message='Password ust be between two and 50 characters!')
        ])


class ProductUploadForm(FlaskForm):
    '''
    validates the product upload form fields
    '''
    name = StringField('Name', validators=[
        DataRequired(),
        length_check(4, 50, 'Name')
        ])
    category = StringField('Category', validators=[
        DataRequired(),
        AnyOf(['networking-devices', 'computer-accessories'], message='Please select a valid category.')
        ])
    price = DecimalField('Price',
                         places=2,
                         rounding=None,
                         validators=[
                             DataRequired(),
                             NumberRange(min=1, max=1000000, message="Price must be at least 1")
                        ])
    description = TextAreaField('Description', validators=[
        DataRequired(),
        length_check(80, 250, 'Description')
        ])
    features = TextAreaField('Features', validators=[
        DataRequired(),
        validate_features_field
        ])
    stock = IntegerField('Stock', validators=[
        DataRequired(),
        NumberRange(min=1, max=1000000, message="Stock must be at least 1")
        ])
