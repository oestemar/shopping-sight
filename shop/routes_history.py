from flask import Blueprint, render_template, request
from models import db
from models.order import Order
from models.user import User
from shop.auth_utils import user_login_required
from shop.auth_utils import get_current_user

history_bp = Blueprint("history", __name__)

@history_bp.route("/")
@user_login_required
def order_history():
    user = get_current_user()

    # --- ベースクエリ（このユーザーの注文のみ） ---
    orders = (
        Order.query
        .filter_by(user_id=user.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    return render_template(
        "history.html",
        user=user,
        orders=orders
    )
