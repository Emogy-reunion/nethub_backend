import os
from flask import current_app

def create_upload_folder():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    upload_path = os.path.join(current_app.root_path, upload_folder)

    os.makedirs(upload_path, exist_ok=True)
