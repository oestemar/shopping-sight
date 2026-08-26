from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.product import Product
from models.image import ProductImage
from models.category import Category
from models import db
from admin.routes_auth import admin_login_required, get_current_admin
from admin.routes_auth import role_required
import os
from supabase_client import supabase
import uuid
import json
import csv
import io
import zipfile
from flask import current_app

products_bp = Blueprint("products", __name__)

@products_bp.route("/")
@admin_login_required
@role_required(1, 2, 3)
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
@role_required(1, 2, 3)
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    images = ProductImage.query.filter_by(product_id=product_id).order_by(ProductImage.sort_order.asc()).all()
    return render_template("admin/product_detail.html", product=product, images=images)

@products_bp.get("/edit/<int:product_id>")
@admin_login_required
@role_required(1, 2, 3)
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
@role_required(2, 3)
def product_edit_action(product_id):

    print("DEBUG: product_edit_action POST received")
   
    product = Product.query.get_or_404(product_id)

    # バリデーション
    name = request.form.get("name", "").strip()
    price_raw = request.form.get("price", "").strip()
    sku = request.form.get("sku", "").strip()
    brand = request.form.get("brand", "").strip()
    description = request.form.get("description", "").strip()
    category_id = request.form.get("category_id")
    status = request.form.get("status")

    # name
    if not name or name == "":
        flash("商品名は必須です", "danger")
        return redirect(url_for("products.product_edit", product_id=product.id))

    # price
    if not price_raw.isdigit():
        flash("価格は数値で入力してください", "danger")
        return redirect(url_for("products.product_edit", product_id=product.id))

    price = int(price_raw)

    # sku
    if not sku:
        flash("SKUは必須です", "danger")
        return redirect(url_for("products.product_edit", product_id=product.id))

    # status
    if status not in ["1", "2", "3"]:
        flash("ステータスが不正です", "danger")
        return redirect(url_for("products.product_edit", product_id=product.id))

    # --- 値をセット ---
    product.name = name
    product.price = price
    product.sku = sku
    product.brand = brand
    product.description = description
    product.category_id = category_id
    product.status = int(status)

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
            ext = img.filename.rsplit('.', 1)[-1].lower()
            new_filename = f"{uuid.uuid4()}.{ext}"
            image_url = upload_to_supabase_any(img.read(), new_filename, img.mimetype)

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

    return redirect(url_for("products.product_detail", product_id=product.id))

@products_bp.get("/add")
@admin_login_required
@role_required(1, 2, 3)
def product_add():
    categories = Category.query.all()
    return render_template(
        "admin/product_add.html", categories=categories
    )

@products_bp.post("/add")
@admin_login_required
@role_required(2, 3)
def product_add_action():

    name=request.form.get("name","").strip()
    price_raw=request.form.get("price","").strip()
    stock=request.form.get("stock","").strip()
    sku=request.form.get("sku","").strip()
    brand=request.form.get("brand","").strip()
    description=request.form.get("description","").strip()
    category_id=request.form.get("category_id")
    status=request.form.get("status")

    # name
    if not name:
        flash("商品名は必須です", "danger")
        return redirect(url_for("products.product_edit", product_id=product.id))

    # price
    if not price_raw.isdigit():
        flash("価格は数値で入力してください", "danger")
        return redirect(url_for("products.product_edit", product_id=product.id))

    price = int(price_raw)

    # sku
    if not sku:
        flash("SKUは必須です", "danger")
        return redirect(url_for("products.product_edit", product_id=product.id))

    # status
    if status not in ["1", "2", "3"]:
        flash("ステータスが不正です", "danger")
        return redirect(url_for("products.product_edit", product_id=product.id))

    # --- 値をセット ---
    product = Product()
    product.name = name
    product.price = price
    product.stock = stock
    product.sku = sku
    product.brand = brand
    product.description = description
    product.category_id = category_id
    product.status = int(status)

    # JSON のパース
    spec_json_raw = request.form.get("spec_json")
    try:
        product.spec_json = json.loads(spec_json_raw) if spec_json_raw else None
    except:
        flash("仕様（JSON）が不正です", "danger")

    db.session.add(product)
    db.session.commit()

    # 新規画像アップロード
    images = request.files.getlist("images")
    for img in images:
        if img.filename:
            # Supabase にアップロード（後で実装）
            ext = img.filename.rsplit('.', 1)[-1].lower()
            new_filename = f"{uuid.uuid4()}.{ext}"
            image_url = upload_to_supabase_any(img.read(), new_filename, img.mimetype)

            new_img = ProductImage(
                product_id=product.id,
                image_url=image_url,
                sort_order=0
            )
            db.session.add(new_img)

    db.session.commit()

    return redirect(url_for("products.product_list"))


@products_bp.get("/image/delete/<int:image_id>")
@admin_login_required
@role_required(2, 3)
def product_image_delete(image_id):
    img = ProductImage.query.get_or_404(image_id)
    product_id = img.product_id

    db.session.delete(img)
    db.session.commit()

    return redirect(url_for("products.product_edit", product_id=product_id))

@products_bp.get("/import")
@admin_login_required
@role_required(1, 2, 3)
def product_import():
    return render_template("admin/product_import.html")


@products_bp.post("/import")
@admin_login_required
@role_required(2, 3)
def product_import_action():
    csv_file = request.files.get("csv_file")
    image_zip = request.files.get("image_zip")
    print("ZIP FILE EXISTS:", image_zip is not None)

    if not csv_file:
        flash("CSVファイルが選択されていません", "danger")
        return redirect(url_for("products.product_import"))

    # ZIP画像を辞書に展開
    image_dict = {}
    if image_zip:
        with zipfile.ZipFile(image_zip) as z:
            print("ZIP CONTENTS:", z.namelist())
            for filename in z.namelist():
                image_dict[filename] = z.read(filename)
                print("ZIP IMAGE READ:", filename, len(image_dict[filename]), "bytes")

    # CSV読み込み
    stream = io.StringIO(csv_file.stream.read().decode("utf-8"))
    reader = csv.DictReader(stream)

    for row in reader:
        existing = Product.query.filter_by(sku=row['sku']).first()
        print(existing.__dict__ if existing else "No existing product for SKU:", row['sku'])
        for img in existing.images if existing else []:
            db.session.delete(img)
            db.session.commit()
        if existing:
            # UPDATE
            product = existing
            product.name = row['name']
            product.price = row['price']
            product.description = row['description']
            product.category_id = row['category_id']
            product.stock = row['stock']
            product.brand = row['brand']
            product.status = row['status']
        else:
            # 商品作成
            product = Product(
                name=row["name"],
                price=row["price"],
                stock=row["stock"],
                sku=row["sku"],
                brand=row["brand"],
                description=row["description"],
                category_id=row["category_id"],
                status=row["status"]
            )

        # JSON仕様
        if row.get("spec_json"):
            try:
                product.spec_json = json.loads(row["spec_json"])
            except:
                flash(f"JSONが不正です: {row['name']}", "danger")

        db.session.add(product)
        try:
            db.session.commit()
        except Exception as e:
            print("IMPORT ERROR:", e)
            raise

        ProductImage.query.filter_by(product_id=product.id).delete()
        db.session.commit()

        # 画像登録
        for key in ["image1", "image2", "image3"]:
            print("キー：", key, "値：", row.get(key))
            filename = row.get(key)
            if filename and filename in image_dict:
                print("アップロードされる画像：", filename)
                # Supabaseへアップロード
                image_bytes = image_dict[filename]
                print("SUPABASE UPLOAD:", filename, len(image_bytes), "bytes")
                ext = filename.rsplit('.', 1)[-1].lower()
                new_filename = f"{uuid.uuid4()}.{ext}"
                image_url = upload_to_supabase_any(image_bytes, new_filename, "image/png")

                new_img = ProductImage(
                    product_id=product.id,
                    image_url=image_url,
                    sort_order=0
                )
                print("DB INSERT:", product.id, image_url)                
                db.session.add(new_img)

        db.session.commit()

    flash("CSVインポートが完了しました", "success")
    return redirect(url_for("products.product_list"))

def upload_to_supabase_any(bytes_data, filename, mime="image/png"):
    bucket_name = os.getenv("SUPABASE_BUCKET")
    supabase = current_app.supabase
    bucket = supabase.storage.from_(bucket_name)

    # 上書き許可してアップロード
    res_upload = bucket.upload(
        filename,
        bytes_data,
        file_options={"content-type": mime},
    )
    print("UPLOAD RESULT:", res_upload)

    return bucket.get_public_url(filename)

