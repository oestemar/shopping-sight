import stripe
from flask import Blueprint, render_template, request, session, redirect, url_for
from models.cart import Cart
import os

shop_payment_bp = Blueprint("shop_payment", __name__, url_prefix="/payment")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


# 決済方法を受け取る
@shop_payment_bp.post("")
def payment_router():
    method = request.form.get("method")

    if method == "stripe":
        return redirect(url_for("shop_payment.stripe_checkout"))

    elif method == "paspo":
        return redirect(url_for("shop_payment.paspo_checkout"))

    elif method == "qr":
        return redirect(url_for("shop_payment.qr_checkout"))

    else:
        return "Invalid payment method", 400


@shop_payment_bp.get("/stripe")
def stripe_checkout():
    user_id = session.get("user_id")
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    line_items = []
    for item in cart_items:
        line_items.append({
            "price_data": {
                "currency": "jpy",
                "product_data": {"name": item.product.name},
                "unit_amount": item.product.price * 100,
            },
            "quantity": item.quantity,
        })

    session_obj = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=url_for("shop_payment.payment_success", _external=True),
        cancel_url=url_for("shop_payment.payment_cancel", _external=True),
    )

    return redirect(session_obj.url)


@shop_payment_bp.get("/paspo")
def paspo_checkout():
    return render_template("payment_paspo.html", step="paspo")


@shop_payment_bp.get("/qr")
def qr_checkout():
    return render_template("payment_qr.html", step="qr")


@shop_payment_bp.get("/success")
def payment_success():
    return render_template("success.html")


@shop_payment_bp.get("/cancel")
def payment_cancel():
    return render_template("cancel.html")
