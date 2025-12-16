from flask import Blueprint, request, jsonify
from app.models import Products, ProductImages
from sqlalchemy.orm import selectinload


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

        paginated_results = Products.query(
            .options(selectinload(Products.images))
            .filter_by(category=category)
            .paginate(page=page, per_page=per_page, error_out=False)
            )

        if not paginated_results.items:
            products = []
        else:
            products = [product.get_preview() for product in paginated_results.items]

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






