import stripe
from flask import Blueprint, render_template, request, session, redirect, url_for
from models.cart import Cart
from models.order import Order
from models.order_item import OrderItem
from models import db
from models.product import Product
from models.inventory_history import InventoryHistory

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

    # 注文を作成
    order = Order(
        user_id=user_id,
        total_amount=sum(item.product.price * item.quantity for item in cart_items),
        payment_method="stripe",
        status="processing"
    )
    db.session.add(order)
    db.session.commit()

    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price_at_order=item.product.price
        )
        db.session.add(order_item)
    db.session.commit()

    line_items = []
    for item in cart_items:
        line_items.append({
            "price_data": {
                "currency": "jpy",
                "product_data": {"name": item.product.name},
                "unit_amount": item.product.price
            },
            "quantity": item.quantity,
        })

    session_obj = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=url_for("shop_payment.payment_success", order_id=order.id, _external=True),
        cancel_url=url_for("shop_payment.payment_cancel", order_id=order.id, _external=True),
    )

    return redirect(session_obj.url)

@shop_payment_bp.get("/paspo")
def paspo_checkout():
    user_id = session.get("user_id")
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    order = Order(
        user_id=user_id,
        total_amount=sum(item.product.price * item.quantity for item in cart_items),
        payment_method="paspo",
        status="processing"
    )
    db.session.add(order)
    db.session.commit()

    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price_at_order=item.product.price
        )
        db.session.add(order_item)
    db.session.commit()
    return render_template("payment_paspo.html", order_id=order.id, step="payment")

@shop_payment_bp.get("/qr")
def qr_checkout():
    user_id = session.get("user_id")
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    order = Order(
        user_id=user_id,
        total_amount=sum(item.product.price * item.quantity for item in cart_items),
        payment_method="qr",
        status="processing"
    )
    db.session.add(order)
    db.session.commit()
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price_at_order=item.product.price
        )
        db.session.add(order_item)
    db.session.commit()    
    return render_template("payment_qr.html", order_id=order.id, step="payment")

# Stripe用の関数
@shop_payment_bp.get("/complete")
def payment_success():
    order_id = request.args.get("order_id")
#    print(f"Payment success for order_id: {order_id}")  # デバッグ用に出力
    order = Order.query.get(order_id)
    order.status = "paid"

    for item in order.order_items:
        product = Product.query.get(item.product_id)
        product.stock -= item.quantity

        # 履歴を残す
        history = InventoryHistory(
            product_id=product.id,
            admin_id=0,  # または None
            change=-item.quantity,
            note="注文確定による在庫減少"
        )

        db.session.add(history)

    db.session.commit()
    return redirect(url_for("shop_complete.complete_success"))

# Stripe用の関数
@shop_payment_bp.get("/cancel")
def payment_cancel():
    order_id = request.args.get("order_id")
    order = Order.query.get(order_id)
    order.status = "canceled"
    db.session.commit() 
    return redirect(url_for("shop_complete.complete_cancel"))

@shop_payment_bp.post("/complete_paspo")
def payment_complete_paspo():
    order_id = request.form.get("order_id")
    return redirect(url_for("shop_complete.complete_success", order_id=order_id))
