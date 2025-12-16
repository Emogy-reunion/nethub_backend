from flask import Blueprint, jsonify, request, current_app
from app import db
from app.models import Products, ProductImages
from app.forms import ProductUploadForm
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role import role_required
from app.utils.check_filename import check_file_extension
from werkzeug.utils import secure_filename
import os


post = Blueprint('post', __name__)

@post.route('/upload_product', methods=['POST'])
@jwt_required()
@role_required('admin')
def upload_product():
    try:
        current_user_id = get_jwt_identity()
        saved_files = []
        data = request.form
        form = ProductUploadForm(data)

        if not form.validate():
            return jsonify({"errors": form.errors}), 400

        name = form.name.data.strip().lower()
        category = form.category.data.strip().lower()
        price = form.price.data
        description = form.description.data.strip()
        features = form.features.data
        stock = form.stock.data
        discount = form.discount.data
        images = request.files.getlist('images')

        if not images or len(images) < 4:
            return jsonify({'error': 'Please upload at least 4 images to showcase the product clearly'}), 400

        if images and len(images) > 6:
            return jsonify({'error': 'You can upload a maximum of 6 images. Choose the most relevant ones.'}), 400

        new_product = Products(
                user_id=current_user_id,
                name=name,
                category=category,
                price=price,
                description=description,
                features=features,
                stock=stock
                discount=discount,
                )

        db.session.add(new_product)
        db.session.flush()

        for image in images:
            if image and check_file_extension(image.filename):
                filename = secure_filename(image.filename)
                file_path = (os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                image.save(filepath)
                saved_files.append(filepath)

                new_image = ProductImages(
                        product_id=new_product.id,
                        filename=filename
                        )
                db.session.add(new_image)
            else:
                #remove already saved files
                for file in saved_files:
                    if os.path.exists(file):
                        os.remove(file)

                db.session.rollback()
                return jsonify({"error": 'One or more images are missing or have an invalid file extension.'}), 400
        db.session.commit()
        return jsonify({"success": 'Product uploaded successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred. Please try again.'}), 500


