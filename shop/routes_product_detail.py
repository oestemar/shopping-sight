import json
from flask import Blueprint, render_template
from models.product import Product

shop_product_detail_bp = Blueprint("shop_product_detail", __name__)

@shop_product_detail_bp.get("/detail/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    images = sorted(product.images, key=lambda img: img.sort_order)

    # ★ 画像の中身を確認するログ
    print("DEBUG: product.id =", product.id)
    print("DEBUG: images count =", len(images))
    for i, img in enumerate(images):
        print(f"DEBUG: image[{i}] id={img.id}, url={img.image_url}, sort_order={img.sort_order}")

    spec = None
    if product.spec_json:
        spec = product.spec_json or {}

    return render_template(
        "product_detail.html", 
        product=product,
        spec=spec,
        step=None,
        images=images
    )
