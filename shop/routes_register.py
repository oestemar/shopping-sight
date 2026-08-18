from flask import Blueprint, render_template, request, redirect, session
from models.user import User
from models import db
from flask import flash

shop_register_bp = Blueprint("shop_register", __name__, url_prefix="/shop")

@shop_register_bp.get("/register")
def register_form():
    return render_template("register.html")

@shop_register_bp.post("/register")
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password_hash = request.form.get("password_hash", "").strip()
    address = request.form.get("address", "").strip()
    phone = request.form.get("phone", "").strip()

    # -------------------------
    # ① 必須チェック
    # -------------------------
    if not name or not email or not password_hash or not address or not phone:
        flash("すべての項目を入力してください", "error")
        return redirect("/register")

    # -------------------------
    # ② メール書式チェック（@ があるか）
    # -------------------------
    if "@" not in email:
        flash("メールアドレスの形式が正しくありません", "error")
        return redirect("/register")

    # メール重複チェック
    if User.query.filter_by(email=email).first():
        flash("このメールアドレスは既に登録されています", "error")
        return redirect("/register")

    # -------------------------
    # ③ 住所を全角に変換
    # -------------------------
    address = address.translate(str.maketrans(
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
    ))

    # -------------------------
    # ④ 電話番号のハイフン除去
    # -------------------------
    phone = phone.replace("-", "")
    new_user = User(name=name, email=email, password_hash=password_hash, address=address, phone=phone)

    db.session.add(new_user)
    db.session.commit()

    # 自動ログイン
    session["user_id"] = new_user.id

    return redirect("/shop/menu")
