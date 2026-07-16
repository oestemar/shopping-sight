from flask import Blueprint, render_template, request, redirect, session
from models.user import User
from models import db

shop_register_bp = Blueprint("shop_register", __name__, url_prefix="/shop")

@shop_register_bp.get("/register")
def register_form():
    return render_template("register.html")

@shop_register_bp.post("/register")
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    password_hash = request.form.get("password_hash")
    address = request.form.get("address")
    phone = request.form.get("phone")

    # メール重複チェック
    if User.query.filter_by(email=email).first():
        return render_template("register.html", error="このメールアドレスは既に登録されています")

    new_user = User(name=name, email=email, password_hash=password_hash, address=address, phone=phone)
    db.session.add(new_user)
    db.session.commit()

    # 自動ログイン
    session["user_id"] = new_user.id

    return redirect("/shop/menu")
