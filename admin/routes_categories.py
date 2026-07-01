from flask import Blueprint, render_template

categories_bp = Blueprint("categories", __name__)

@categories_bp.get("/")
def category_list():
    return render_template("admin/categories/list.html")

@categories_bp.get("/add")
def category_add():
    return render_template("admin/categories/add.html")

@categories_bp.post("/add")
def category_add_action():
    pass

@categories_bp.get("/edit/<int:id>")
def category_edit(id):
    return render_template("admin/categories/edit.html", id=id)

@categories_bp.post("/edit/<int:id>")
def category_edit_action(id):
    pass
