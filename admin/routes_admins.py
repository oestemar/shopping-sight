from flask import Blueprint, render_template, request, redirect, url_for
from models.admin import Admin
from admin.routes_auth import role_required
from models import db
from werkzeug.security import check_password_hash, generate_password_hash
from admin.routes_auth import admin_login_required

admins_bp = Blueprint("admins", __name__)

@admins_bp.route("/")
@role_required(1, 2, 3)
@admin_login_required
def admin_list():
    admins = Admin.query.order_by(Admin.id).all()
    for admin in admins:
        print(admin.id)
    return render_template("admin/admin_list.html", admins=admins)

@admins_bp.get("/password/<int:admin_id>")
@role_required(3)
@admin_login_required
def password_change(admin_id):
    return render_template("admin/admin_password.html", admin_id=admin_id)

@admins_bp.post("/password")
@role_required(3)
@admin_login_required
def password_change_action():
    """パスワード変更"""
    try:
        admin_id = request.form.get("admin_id")
        current_password = request.form.get('current')
        new_password = request.form.get('new')
        confirm_password = request.form.get('confirm')

        # 新パスワードチェック
        if new_password != confirm_password:
            return render_template(
                'admin/admin_password.html',
                admin_id=admin_id,
                error='新しいパスワードが一致しません'
            )

        # 管理者取得                  
        admin = Admin.query.get(admin_id)
        if not admin:
            return render_template(
                'admin/admin_password.html',
                message='現在のパスワードが正しくありません'
            )
        
        # 現在のパスワードチェック
        if not check_password_hash(admin.password_hash, current_password):
            return render_template(
                "admin/admin_password.html",
                admin_id=admin_id,
                error="現在のパスワードが正しくありません"
        ) 

        admin.password_hash=generate_password_hash(new_password)
        db.session.commit()        
        return redirect(url_for("admins.admin_list"))        
    except Exception as e:
        return render_template('admin/admin_error.html', message=str(e))

@admins_bp.get("/add")
@role_required(3)
@admin_login_required
def admin_add():
    return render_template("admin/admin_add.html")

@admins_bp.post("/add")
@role_required(3)
@admin_login_required
def admin_add_action():
    """管理者追加"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if not email or not password:
            return render_template(
                "admin/admin_add.html",
                error="メールアドレスとパスワードは必須です"
            )

        # パスワードハッシュ化
        password_hash = generate_password_hash(password)

        new_admin = Admin(
            email=email,
            password_hash=password_hash,
            role=role
        )

        db.session.add(new_admin)
        db.session.commit()

        return redirect(url_for("admins.admin_list"))

    except Exception as e:
        return render_template("admin/admin_error.html", message=str(e))

@admins_bp.get("/delete/<int:admin_id>")
@role_required(3)
@admin_login_required
def admin_delete(admin_id):
    admin = Admin.query.get(admin_id)
    return render_template("admin/admin_delete.html",admin=admin ,admin_id=admin_id)

@admins_bp.post("/delete/<int:admin_id>")
@role_required(3)
@admin_login_required
def admin_delete_action(admin_id):
    """管理者削除"""
    try:
        admin = Admin.query.get(admin_id)
        if not admin:
            return render_template(
                "admin/admin_error.html",
                message="指定された管理者が存在しません"
            )

        db.session.delete(admin)
        db.session.commit()

        return redirect(url_for("admins.admin_list"))

    except Exception as e:
        return render_template("admin/admin_error.html", message=str(e))

