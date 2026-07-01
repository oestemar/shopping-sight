from flask import Blueprint, render_template, request, session, redirect, url_for
from models.product import Product
from models.cart import Cart
from extensions import db

shop_cart_bp = Blueprint("shop_cart", __name__, url_prefix="/cart")

# -------------------------
# ① カート表示（DBから取得）
# -------------------------
@shop_cart_bp.get("/")
def view_cart():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/shop/login")

    cart_items = Cart.query.filter_by(user_id=user_id).all()

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render_template("shop/cart.html", cart_items=cart_items, total_price=total_price)


# -------------------------
# ② カートに追加（INSERT or UPDATE）
# -------------------------
@shop_cart_bp.post("/add")
def add_to_cart():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/shop/login")

    product_id = int(request.form.get("product_id"))
    quantity = int(request.form.get("quantity", 1))

    # 既にカートにあるか確認
    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

    if cart_item:
        # 数量を加算
        cart_item.quantity += quantity
    else:
        # 新規追加
        new_item = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(new_item)

    db.session.commit()

    return redirect(url_for("shop_cart.view_cart"))


# -------------------------
# ③ カートから削除（DELETE）
# -------------------------
@shop_cart_bp.post("/remove")
def remove_from_cart():
    user_id = session.get("user_id")
    product_id = int(request.form.get("product_id"))

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()

    return redirect(url_for("shop_cart.view_cart"))
