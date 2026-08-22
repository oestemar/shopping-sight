from flask import Blueprint, render_template, request, redirect, session
from models.user import User

shop_login_bp = Blueprint("shop_login", __name__, url_prefix="/shop")

@shop_login_bp.get("/login")
def login_form():
    return render_template("login.html")

@shop_login_bp.post("/login")
def login():
    email = request.form.get("email")
    password = request.form.get("password_hash")

    user = User.query.filter_by(email=email, password_hash=password).first()

    if not user:
        return render_template("login.html", error="メールアドレスまたはパスワードが違います")

    session["user_id"] = user.id
    return redirect("/shop/menu")

@shop_login_bp.get("/logout")
def logout():
    session.clear()
    return render_template("logout.html")
