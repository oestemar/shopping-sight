from flask import Blueprint, render_template

shop_complete_bp = Blueprint("shop_complete", __name__, url_prefix="/complete")

@shop_complete_bp.get("/success")
def complete_success():
    return render_template("success.html")

@shop_complete_bp.get("/cancel")
def complete_cancel():
    return render_template("cancel.html")
