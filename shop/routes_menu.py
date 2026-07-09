from flask import Blueprint, render_template
from models.category import Category

shop_menu_bp = Blueprint("shop_menu", __name__)

# ==================== メニュー関連ルート ====================
@shop_menu_bp.get("/")
def menu():
    categories = Category.query.all()
    return render_template("menu.html", categories=categories)

