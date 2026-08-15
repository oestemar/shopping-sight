from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.product import Product
from models.inventory_history import InventoryHistory
from .routes_auth import admin_login_required, get_current_admin
from models import db
from admin.routes_auth import admin_login_required

inventory_bp = Blueprint("inventory", __name__, template_folder="templates")


@inventory_bp.route("/")
@admin_login_required
def inventory_list():
    products = Product.query.order_by(Product.name).all()
    return render_template("admin/inventory/list.html", products=products)


@inventory_bp.route("/update/<int:product_id>", methods=["POST"])
@admin_login_required
def inventory_update(product_id):
    product = Product.query.get_or_404(product_id)
    change = int(request.form.get("change", 0))
    note = request.form.get("note", "").strip()
    product.stock = max(0, product.stock + change)
    db.session.add(product)

    admin = get_current_admin()
    if not admin:
        flash("管理者情報が取得できません。再ログインしてください。", "danger")
        return redirect(url_for("auth.login"))

    history = InventoryHistory(
        product_id=product.id,
        admin_id=get_current_admin().id,
        change=change,
        note=note,
        created_at=datetime.utcnow(),
    )
    db.session.add(history)
    db.session.commit()
    flash("在庫を更新しました。", "success")
    return redirect(url_for("inventory.inventory_list"))


@inventory_bp.route("/history")
@admin_login_required
def inventory_history():
    histories = InventoryHistory.query.order_by(InventoryHistory.created_at.desc()).limit(200).all()
    return render_template("admin/inventory/history.html", histories=histories)
