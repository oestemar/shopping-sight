from flask import Blueprint, render_template, request
from models.user import User
from admin.routes_auth import role_required
from admin.routes_auth import admin_login_required
from models import db
from models.order import Order
from models.product import Product

users_bp = Blueprint("users", __name__)

@users_bp.route("/")
@admin_login_required
@role_required(1, 2, 3)
def user_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users_list.html", users=users)


@users_bp.route("/users/<int:user_id>")
@admin_login_required
@role_required(1, 2, 3)
def user_detail(user_id):
    user = User.query.get_or_404(user_id)

    # --- 検索パラメータ ---
    q = request.args.get("q", "").strip()
    payment_method = request.args.get("payment_method", "")
    status = request.args.get("status", "")
    created_at = request.args.get("created_at", "")

    # --- ベースクエリ（このユーザーの注文のみ） ---
    query = (
        db.session.query(Order, User)
        .join(User, Order.user_id == User.id)
        .filter(Order.user_id == user_id)
    )

    # --- キーワード検索（商品名 / SKU） ---
    if q:
        query = query.join(Order).join(Product).filter(
            db.or_(
                Product.name.like(f"%{q}%"),
                Product.sku.like(f"%{q}%")
            )
        )

    # --- 支払方法 ---
    if payment_method:
        query = query.filter(Order.payment_method == payment_method)

    # --- ステータス ---
    if status:
        query = query.filter(Order.status == status)

    # --- 注文日 ---
    if created_at:
        query = query.filter(db.func.date(Order.created_at) == created_at)

    # --- 並び順 ---
    orders = query.order_by(Order.created_at.desc()).all()

    return render_template(
        "admin/user_detail.html",
        user=user,
        orders=orders,
        q=q,
        payment_method=payment_method,
        status=status,
        created_at=created_at
    )
