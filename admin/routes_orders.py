from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.order import Order
from models.order_item import OrderItem
from models.product import Product
from models.user import User
from models import db
from admin.routes_auth import admin_login_required
from models.inventory_history import InventoryHistory
from admin.routes_auth import get_current_admin

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/")
@admin_login_required
def order_list():
    q = request.args.get("q", "")
    payment_method = request.args.get("payment_method", "")
    status = request.args.get("status", "")
    created_at = request.args.get("created_at", "")

    query = (
        db.session.query(Order, User)
        .join(User, Order.user_id == User.id)
        .order_by(Order.created_at.desc())
    )

    if q:
        query = query.filter(
            (User.name.ilike(f"%{q}%")) | (User.email.ilike(f"%{q}%"))
        )

    if payment_method := request.args.get("payment_method"):
        query = query.filter(Order.payment_method == payment_method)

    if status:
        query = query.filter(Order.status == status)

    if created_at:
        query = query.filter(db.func.date(Order.created_at) == created_at)

    orders = query.all()

    return render_template("admin/order_list.html", orders=orders, payment_method=payment_method, status=status, created_at=created_at)


@orders_bp.get("/<int:order_id>")
@admin_login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    user = order.user
    items = (
        db.session.query(OrderItem, Product)
        .join(Product, OrderItem.product_id == Product.id)
        .filter(OrderItem.order_id == order_id)
        .all()
    )

    return render_template(
        "admin/order_detail.html",
        order=order,
        user=user,
        items=items
    )

@orders_bp.post("/update_status/<int:order_id>")
@admin_login_required
def order_update_status(order_id):
    order = Order.query.get_or_404(order_id)
    status = request.form.get("status", order.status)
    order.status = status

    if status in ["canceled", "refunded"]:
        for item in order.order_items:
            product = Product.query.get(item.product_id)
            product.stock += item.quantity
            history = InventoryHistory(
                product_id=product.id,
                admin_id=get_current_admin().id,
                change=item.quantity,
                note="注文キャンセルによる在庫戻し"
            )
            db.session.add(history)

    db.session.commit()
    for item in order.order_items:
        product = Product.query.get(item.product_id)

    db.session.commit()

    flash("注文ステータスを更新しました。", "success")
    return redirect(url_for("orders.order_detail", order_id=order.id))
