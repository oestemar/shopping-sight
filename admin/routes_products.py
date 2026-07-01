from flask import Blueprint, render_template, request

products_bp = Blueprint("products", __name__)

@products_bp.get("/")
def product_list():
    return render_template("admin/products/list.html")

@products_bp.get("/<int:id>")
def product_detail(id):
    return render_template("admin/products/detail.html", id=id)

@products_bp.get("/edit/<int:id>")
def product_edit(id):
    return render_template("admin/products/edit.html", id=id)

@products_bp.post("/edit/<int:id>")
def product_edit_action(id):
    pass

@products_bp.get("/register")
def product_register():
    return render_template("admin/products/register.html")

@products_bp.post("/register")
def product_register_action():
    pass

@products_bp.post("/import_csv")
def product_import_csv():
    pass
