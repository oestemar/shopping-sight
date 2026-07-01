from flask import Blueprint, render_template

orders_bp = Blueprint("orders", __name__)

@orders_bp.get("/")
def order_list():
    return render_template("admin/orders/list.html")

@orders_bp.get("/<int:id>")
def order_detail(id):
    return render_template("admin/orders/detail.html", id=id)

@orders_bp.post("/update_status/<int:id>")
def order_update_status(id):
    pass
