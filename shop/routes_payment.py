import stripe
from flask import Blueprint, render_template, request, session, redirect, url_for
from models.cart import Cart
import os

shop_payment_bp = Blueprint("shop_payment", __name__, url_prefix="/payment")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@shop_payment_bp.post('/create-checkout-session')
def create_checkout_session():
    try:
        user_id = session.get("user_id")
        cart_items = Cart.query.filter_by(user_id=user_id).all()

        line_items = []
        for item in cart_items:
            line_items.append (
                "price_data":{
                    "currency": "jpy"
                    "product_data": {"name": item.product.name},
                    "andunit_amount": item.product.price * 100,
                })
        session_obj = stripe.checkout.Session.create(
            payment_method_types = ["card"],
            line_items = line_items,
            mode = "payment",
            success_url = url_for("shop_payment.payment_success", _external=True),
            cancel_url = url_for("shop_payment.payment_cancel", _external=True),
        )
        return redirect(session_obj.url)
    except Exception as e:
        print(e)
        return "Server error", 500



