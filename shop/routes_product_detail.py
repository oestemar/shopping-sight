from flask import Blueprint, render_template
from models.product import Product

shop_product_detail_bp = Blueprint("shop_products_detail", __name__, url_prefix="/product_detail")

@shop_product_detail_bp.get("/detail/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    
    spec = None
    if product.spec_json:
        spec = json.loads(product.spec_json)
    
    return render_template(
        "shop/product_detail.html", 
        product=product,
        spec=spec
    )
