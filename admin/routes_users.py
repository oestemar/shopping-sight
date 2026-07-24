from flask import Blueprint, render_template
from models.user import User
from .routes_auth import admin_login_required

users_bp = Blueprint("users", __name__)

@users_bp.route("/")
@admin_login_required
def user_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users_list.html", users=users)


@users_bp.route("/<int:user_id>")
@admin_login_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("admin/user_detail.html", user=user)
