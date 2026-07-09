from flask import Blueprint, render_template

admins_bp = Blueprint("admins", __name__)

@admins_bp.get("/password")
def password_change():
    return render_template("admin/admins/password.html")

@admins_bp.post("/password")
def password_change_action():
    pass

@admins_bp.get("/add")
def admin_add():
    return render_template("admin/admins/add.html")

@admins_bp.post("/add")
def admin_add_action():
    pass

@admins_bp.get("/delete/<int:admin_id>")
def admin_delete(admin_id):
    return render_template("admin/admins/delete.html", admin_id=admin_id)

@admins_bp.post("/delete/<int:admin_id>")
def admin_delete_action(admin_id):
    pass