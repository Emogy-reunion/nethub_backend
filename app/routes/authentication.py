from flask import Blueprint, request, jsonify
from app.forms import RegistrationForm
from app.models import Users
from app import db


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    '''
    allows users to create accounts
    '''
    try:
        data = request.get_json()
        form = RegistrationForm(**data)

        if not form.validate():
            return jsonify({'errors': form.errors}), 400

        email = form.email.data.lower().strip()
        password = form.password.data.strip()

        user = Users.query.filter_by(email=email).first()

        if user:
            return jsonify({'error': 'We couldn’t create your account — this email is already in use.'}), 400
        else:
            new_user = Users(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'success': 'Your account was created successfully. Enjoy your experience.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500
