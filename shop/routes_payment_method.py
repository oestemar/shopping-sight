from flask import Blueprint, render_template, request, session, redirect, url_for
from models.cart import Cart

shop_payment_method_bp = Blueprint("shop_payment_method", __name__, url_prefix="/payment_method")

@shop_payment_method_bp.get('/')
def payment_method():
    """決済方法選択"""
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/shop/login")

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('payment_method.html', cart_items=cart_items, total_price=total_price, step="payment_method") 