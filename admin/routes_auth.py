from flask import Blueprint, render_template, request, redirect, session

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/login")
def login_page():
    return render_template("admin/login.html")

@auth_bp.post("/login")
def login_action():
    # 認証処理
    pass

@auth_bp.get("/logout")
def logout():
    session.clear()
    return redirect("/admin/login")

@auth_bp.get("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")
