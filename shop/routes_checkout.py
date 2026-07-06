from flask import Blueprint, render_template, request, session, redirect, url_for
from models.cart import Cart

shop_checkout_bp = Blueprint("shop_checkout", __name__, url_prefix="/checkout")

# -------------------------
# ① 精算（カート）表示（DBから取得）
# -------------------------
@shop_checkout_bp.get("/")
def checkout():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/shop/login")

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render_template("/checkout.html", cart_items=cart_items, total_price=total_price, step="checkout")

