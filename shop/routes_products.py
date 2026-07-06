from flask import Blueprint, render_template
from models.product import Product

shop_products_bp = Blueprint("shop_products", __name__, url_prefix="/products")

@shop_products_bp.get('/<int:category_id>')
def product_list(category_id):

    try:
        products = Product.query.filter_by(category_id=category_id).all()        
        return render_template('products.html', products=products, step=None)
    except Exception as e:
        return render_template('error.html', message=str(e))