from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.product import Product
from models.image import ProductImage
from models.category import Category
from models import db
from admin.routes_auth import admin_login_required
import os
from supabase_client import supabase
import uuid

products_bp = Blueprint("products", __name__)

@products_bp.route("/")
@admin_login_required
def product_list():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "")
    category_id = request.args.get("category_id", "")
    query = Product.query.order_by(Product.id.asc())
    if q:
        query = query.filter(
            (Product.name.ilike(f"%{q}%")) | (Product.sku.ilike(f"%{q}%"))
        )
    if status:
        query = query.filter_by(status=status)
    if category_id.isdigit():
        query = query.filter_by(category_id=int(category_id))
    products = query.all()
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        "admin/product_list.html",
        products=products,
        categories=categories,
        q=q,
        status=status,
        category_id=category_id,
    )

@products_bp.route("/<int:product_id>")
@admin_login_required
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)

    return render_template("admin/product_detail.html", product=product, images=images)

@products_bp.get("/edit/<int:product_id>")
@admin_login_required
def product_edit(product_id):
    product = Product.query.get_or_404(product_id)
    
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        "admin/product_edit.html",
        product=product,
        categories=categories
    )

@products_bp.post("/edit/<int:product_id>")
@admin_login_required
def product_edit_action(product_id):

    print("DEBUG: product_edit_action POST received")
   
    product = Product.query.get_or_404(product_id)

    product.name = request.form.get("name")
    product.price = request.form.get("price")
    product.stock = request.form.get("stock")
    product.sku = request.form.get("sku")
    product.brand = request.form.get("brand")
    product.description = request.form.get("description")
    product.category_id = request.form.get("category_id")
    product.status = request.form.get("status")

    # JSON のパース
    spec_json_raw = request.form.get("spec_json")
    try:
        product.spec_json = json.loads(spec_json_raw) if spec_json_raw else None
    except:
        flash("仕様（JSON）が不正です", "danger")

    db.session.commit()

    # 新規画像アップロード
    images = request.files.getlist("images")
    for img in images:
        if img.filename:
            # Supabase にアップロード（後で実装）
            image_url = upload_to_supabase(img)

            new_img = ProductImage(
                product_id=product.id,
                image_url=image_url
            )
            db.session.add(new_img)

    # 既存画像の sort_order 更新（ここを修正）
    for img in product.images:
        key = f"sort_order_{img.id}"
        new_order = request.form.get(key)

        if new_order is not None:
            img.sort_order = int(new_order)
        db.session.commit()

    return redirect(url_for("products.product_edit", product_id=product.id))


@products_bp.get("/image/delete/<int:image_id>")
@admin_login_required
def product_image_delete(image_id):
    img = ProductImage.query.get_or_404(image_id)
    product_id = img.product_id

    db.session.delete(img)
    db.session.commit()

    return redirect(url_for("products.product_edit", product_id=product_id))

def upload_to_supabase(file):
    bucket = os.getenv("SUPABASE_BUCKET")

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_bytes = file.read()

    supabase.storage.from_(bucket).upload(
        filename,
        file_bytes,
        file_options={"content-type": file.mimetype}
    )

    return supabase.storage.from_(bucket).get_public_url(filename)

