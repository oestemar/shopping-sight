from flask import Blueprint, render_template

images_bp = Blueprint("images", __name__)

@images_bp.get("/<int:product_id>")
def image_list(product_id):
    return render_template("admin/products/images/list.html", product_id=product_id)

@images_bp.post("/<int:product_id>/add")
def image_add(product_id):
    pass

@images_bp.post("/<int:product_id>/delete/<int:image_id>")
def image_delete(product_id, image_id):
    pass
