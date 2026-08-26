from flask import Blueprint, render_template, request, redirect, url_for
from admin.routes_auth import role_required
from admin.routes_auth import admin_login_required
from models.category import Category
from models import db

categories_bp = Blueprint("categories", __name__)

@categories_bp.get("/")
@admin_login_required
@role_required(1, 2, 3)
def category_list():
    categories = Category.query.order_by(Category.id).all()
    return render_template("admin/category_list.html", categories=categories)

@categories_bp.get("/edit/<int:category_id>")
@admin_login_required
@role_required(1, 2, 3)
def category_edit(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template("admin/category_edit.html", category=category)

@categories_bp.post("/edit/<int:category_id>")
@admin_login_required
@role_required(2, 3)
def category_edit_action(category_id):
    category = Category.query.get_or_404(category_id)

    category.name = request.form.get("name")
    category.status = request.form.get("status")
    category.sort_order = request.form.get("sort_order")

    db.session.commit()

    return redirect(url_for("categories.category_list", category_id=category.id))

@categories_bp.get("/add")
@admin_login_required
@role_required(1, 2, 3)
def category_add():
    return render_template("admin/category_add.html")

@categories_bp.post("/add")
@admin_login_required
@role_required(2, 3)
def category_add_action():
    """カテゴリー追加"""
    try:
        name = request.form.get("name")
        status = request.form.get("status")
        sort_order = request.form.get("sort_order")

        if not name or not sort_order:
            return render_template(
                "admin/category_add.html",
                error="カテゴリー名と並び順番号は必須です"
            )

        new_category = Category(
            name=name,
            status=status,
            sort_order=sort_order
        )

        db.session.add(new_category)
        db.session.commit()

        return redirect(url_for("categories.category_list"))

    except Exception as e:
        return render_template("admin/admin_error.html", message=str(e))

