from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models.admin import Admin
from models.product import Product
from models.order import Order
from models.user import User
from flask import abort

auth_bp = Blueprint("auth", __name__)

def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            admin_id = session.get("admin_id")
            if not admin_id:
                abort(403)

            admin = Admin.query.get(admin_id)
            if admin.role not in roles:
                abort(403)

            return view(*args, **kwargs)
        return wrapped
    return decorator


def admin_login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_id"):
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET": 
        if session.get("admin_id"):
            return redirect(url_for("auth.dashboard"))
        return render_template("admin/login.html", login_page=True)
    else:
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        admin = Admin.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password_hash, password):
            session["admin_id"] = admin.id
            session["admin_role"] = admin.role
            return redirect(url_for("auth.dashboard"))
        flash("メールアドレスまたはパスワードが違います。", "error")
        return render_template("admin/login.html", login_page=True)

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@auth_bp.route("/")
@auth_bp.route("/dashboard")
@admin_login_required
@role_required(1, 2, 3)
def dashboard():
    product_count = Product.query.count()
    order_count = Order.query.count()
    user_count = User.query.count()
    return render_template(
        "admin/dashboard.html",
        product_count=product_count,
        order_count=order_count,
        user_count=user_count,
    )

def get_current_admin():
    admin_id = session.get("admin_id")
    if admin_id:
        return Admin.query.get(admin_id)
    return None

