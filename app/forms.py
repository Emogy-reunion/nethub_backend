from flask_wtf import  FlaskForm
from wtforms import FloatField, StringField, PasswordField, DecimalField, TextAreaField, IntegerField, MultipleFileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, InputRequired, EqualTo, Email, Length, Regexp, NumberRange, AnyOf
from app.utils.custom_form_validators import length_check, validate_features_field


GROUPS = [
            "networking-equipment",
            "structured-cabling",
            "audio-visual",
            "fibre-optic",
            "accessories-tools"
        ]

class RegistrationForm(FlaskForm):
    '''
    validates the registration form data
    '''
    email = StringField('Email:', validators=[
        DataRequired(),
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
        EqualTo('password', message='Passwords do no match!')
        ])

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[
        Email(),
        Length(min=4, max=45, message='Email must be between 4 and 45 characters!')
        ])
    password = PasswordField('Password:', validators=[
        DataRequired(),
        length_check(8, 50, 'Password')
        ])


class ProductUploadForm(FlaskForm):
    '''
    validates the product upload form fields
    '''
    class Meta:
        csrf = False

    name = StringField('Name', validators=[
        DataRequired(),
        length_check(4, 50, 'Name')
        ])
    group = StringField(
            'Group',
            validators=[
                DataRequired(),
                AnyOf(GROUPS, message="Please select a valid group.")
                ]
            )
    category = category = StringField('Category', validators=[Length(min=4, max=45, message="Category can't be longer that 50 characters!")])
    price = DecimalField('Price',
                         places=2,
                         rounding=None,
                         validators=[
                             InputRequired(),
                             NumberRange(min=1, max=1000000, message="Price must be at least 1")
                        ])
    description = TextAreaField('Description', validators=[
        DataRequired(),
        length_check(80, 800, 'Description')
        ])
    features = TextAreaField('Features', validators=[
        DataRequired(),
        validate_features_field
        ])
    stock = IntegerField('Stock', validators=[
        InputRequired(),
        NumberRange(min=1, max=1000000, message="Stock must be at least 1")
        ])
    discount = FloatField('Discount', validators=[
        InputRequired(),
        NumberRange(min=0, max=100, message="Discount can't be less that 0")
        ])
    images = MultipleFileField('Images', validators=[
        FileAllowed(['png', 'jpg', 'jpeg', 'webp'], message='Only images are allowed!')
        ])
