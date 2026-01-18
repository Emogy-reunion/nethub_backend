from flask import Blueprint, request, jsonify, current_app, send_from_directory
from app.models import Products, ProductImages
from sqlalchemy.orm import selectinload
from sqlalchemy import desc
from app import db
from app.forms import ProductUploadForm
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role import role_required
from werkzeug.utils import secure_filename
import os
import uuid

products_bp = Blueprint('products_bp', __name__)


@products_bp.route('/upload_product', methods=['POST'])
@jwt_required()
@role_required('admin')
def upload_product():
        try:
            current_user_id = uuid.UUID(get_jwt_identity())
            saved_files = [] 
            data = request.form
            form = ProductUploadForm(data)

            if not form.validate():
                return jsonify({"errors": form.errors}), 400

            name = form.name.data.strip().lower()
            category = form.category.data.strip().lower()
            price = form.price.data
            discount = form.discount.data
            description = form.description.data.strip()
            features = form.features.data
            stock = form.stock.data
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
                    discount=discount,
                    description=description,
                    features=features,
                    stock=stock
                    )

            db.session.add(new_product)
            db.session.flush()

            for image in images:
                if image:
                    filename = secure_filename(image.filename)
                    file_path = (os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                    image.save(file_path)
                    saved_files.append(file_path)

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
                     return jsonify({"error": 'One or more images are missing'}), 400
            db.session.commit()
            return jsonify({"success": 'Product uploaded successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An unexpected error occurred. Please try again.'}), 500



@products_bp.route('/get_product_previews', methods=['GET'])
def get_product_previews():
    '''
    Retrieves products from the database
    returns: paginated results
    '''
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 12))
        category = request.args.get('category')
        

        query = Products.query.options(selectinload(Products.images))

        if category:
            query = query.filter(Products.category == category)

        paginated_results = (query
                    .order_by(desc(Products.created_at))         # order descending
                    .paginate(page=page, per_page=per_page, error_out=False)
                    )


        products = [product.get_preview() for product in paginated_results.items] if paginated_results.items else []

        pagination = {
                'next': paginated_results.next_num if paginated_results.has_next else None,
                'prev': paginated_results.prev_num if paginated_results.has_prev else None,
                'page': paginated_results.page,
                'pages': paginated_results.pages,
                'total': paginated_results.total
                }

        return jsonify({
            'pagination': pagination,
            'products': products
            }), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again'}), 500



@products_bp.route('/get_product_details/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    '''
    retrieves details about a specific product
    '''
    try:
        product = Products.query.options(selectinload(Products.images)).filter_by(id=product_id).first()

        product_details = product.get_full() if product else None

        return jsonify({'product_details': product_details}), 200

    except Exception as e:
        return jsonify({"error": 'An unexpected error occurred. Please try again!'}), 500


@products_bp.route('/delete_product/<int:product_id>', methods=['DELETE'])
@jwt_required()
@role_required("admin")
def delete_product(product_id):
    '''
    allows admins to delete products using product id
    '''
    try:
        product = (
                Products.query
                .options(selectinload(Products.images))
                .filter_by(id=product_id)
                .first()
                )
                

        if not product:
            return jsonify({'error': 'Product not found!'}), 404

        for image in product.images:
            if image.filename:
                absolute_path = os.path.join(
                        current_app.root_path,
                        image.filename
                        )

                if os.path.exists(absolute_path):
                    os.remove(absolute_path)

        db.session.delete(product)
        db.session.commit()

        return jsonify({'success': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred. Please try again'}), 500

@products_bp.route('/send_image/<filename>', methods=['GET'])
def send_image(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
