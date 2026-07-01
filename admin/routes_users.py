from flask import Blueprint, render_template

users_bp = Blueprint("users", __name__)

@users_bp.get("/")
def user_list():
    return render_template("admin/users/list.html")

@users_bp.get("/<int:id>")
def user_detail(id):
    return render_template("admin/users/detail.html", id=id)
