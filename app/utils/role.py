'''
decorator used to protect routes by enforcing access based controls
'''
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models import Users
from app import db
from flask import jsonify


def role_required(role):
    '''
    a decorator factory
    takes the role as an argument
    returns a decorator that can be applied to routes
    '''
    def decorator(func):
    '''
    takes the decorated function as an argument
    returns a wrapper that adds role checking logic to the decorated route's function
    '''
        @wraps(func)
        def wrapper(*args, **kwargs):
        '''
        runs before the decorated function is accessed
        '''
            user_id = int(get_jwt_identity())

            if not user_id:
                return jsonify({'error': 'Missing or invalid token!'}), 401

            current_user = db.session.get(Users, user_id)

            if not current_user:
                return jsonify({'error': 'User not found!'}), 404

            if current_user.role != role:
                return jsonify({'error': 'Unauthorized access!'}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
