from flask import Blueprint, request, jsonify
from app.forms import RegistrationForm
from app.models import Users
from app import db
import uuid
from werkzeug.datastructures import MultiDict
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jwt_required, get_jwt_identity


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    '''
    allows users to create accounts
    '''
    try:
        json_data = request.get_json() or {}
        form = RegistrationForm(formdata=MultiDict(json_data))

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
            return jsonify({'success': 'Your account was created successfully. Enjoy your experience.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500


@auth.route('/login', methods=['POST'])
def login():
    '''
    authenticates the users
    '''
    try:
        json_data = request.get_json() or {}
        form = LoginForm(formdata=MultiDict(json_data))

        if not form.validate():
            return jsonify({"errors": form.errors}), 400

        email = form.email.data.strip().lower()
        password = form.password.data.strip()

        user = Users.query.filter_by(email=email).first()

        if user and user.check_passwordhash(password):
            '''
            checks if the user exists
            compares the user password and stored hash
            create the user access and refresh token
            adds the tokens to the cookies
            '''
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            response = jsonify({'success': 'Logged in successfully. Welcome!'})
            set_access_cookies(response, access_token)
            set_refresh_token(response, refresh_token)
            return response, 200
        else:
            return jsonify({'error': 'Incorrect credentials. Please try again!'}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500


@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        #extract the user id from the refresh token
        user_id = get_jwt_identity()

        #create a new access token with the user id
        access_token = create_access_token(identity=user_id)
        response = ({'success': 'Access token refreshed successfully'})
        set_access_cookies(response, access_token)
        return response, 201
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500


@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    '''
    removes the access and refresh token from the cookies
    logging the user out
    '''
    try:
        response = jsonify({'success': 'Logged out successfully'})
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500



@auth.route('/is_logged_in', methods=['GET'])
@jwt_required()
def is_logged_in():
    '''
    checks is a user is logged in
    '''
    try:
        user_id = uuid.UUID(get_jwt_identity())

        user = db.session.get(Users, user_id)

        if not user:
            return jsonify({'error': 'User not found!'}), 404

        response = {
                'role': user.role,
                'success': 'User is authenticated'
                }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": 'An unexpected error occured. Please try again!'}), 500

    @auth.route('/user_data', methods=['GET'])
    @jwt_required()
    def user_data():
        try:
            user_id = uuid.UUID(get_jwt_identity())

            user = db.session.get(Users, user_id)
            
            if not user:
                return jsonify({'error': 'User not found!'}), 404

            data = {
                    'email': user.email
                    }
            return jsonify(data), 200
        except Exception as E:
            return jsonify({"error": 'An unexpected error occured. Please try again!'}), 500
