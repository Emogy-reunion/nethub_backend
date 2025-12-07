from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Length, Regexp


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
