from  app import db
from app.models import Users
from flask import current_app


def create_initial_admin():
    try:
        email = current_app.config['ADMIN_EMAIL']
        password = current_app.config['ADMIN_PASSWORD']

        user = Users.query.filter_by(email=email).first()

        if user:
            print('Email is already in use!')
            return

        new_admin = Users(email=email, password=password)
        new_admin.role = 'admin'
        db.session.add(new_admin)
        db.session.commit()
        print('Admin created successfully!')
        return
    except Exception as e:
        db.session.rollback
        print(f"Error creating admin: {e}")

