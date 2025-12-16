from flask import Blueprint, request
from app.models import Products, ProductImages


products_bp = Blueprint('products_bp', __name__)

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

        paginated_results = Products.query.options(selectinload(Products.images)).filter(category='networking-devices)'.paginate(page=page, per_page=per_page)

        if paginated_results.items is None:
            return jsonify({'error': 'No available products at the moment. Please try again!'}), 404



