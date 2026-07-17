from flask import Blueprint, render_template, session
from models.cart import Cart
from models import db

shop_complete_bp = Blueprint("shop_complete", __name__, url_prefix="/complete")

@shop_complete_bp.get("/success")
def complete_success():
    user_id = session.get("user_id")

    # カートを空にする
    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()    
    return render_template("success.html", step="success")

@shop_complete_bp.get("/cancel")
def complete_cancel():
    return render_template("cancel.html", step="cancel")
