from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from models import db

from shop.routes_menu import shop_menu_bp
from shop.routes_products import shop_products_bp
from shop.routes_product_detail import shop_product_detail_bp
from shop.routes_cart import shop_cart_bp
from shop.routes_checkout import shop_checkout_bp
from shop.routes_payment_method import shop_payment_method_bp
from shop.routes_payment import shop_payment_bp
from shop.routes_complete import shop_complete_bp

from admin.routes_auth import auth_bp
from admin.routes_products import products_bp
from admin.routes_categories import categories_bp
from admin.routes_orders import orders_bp
from admin.routes_users import users_bp
from admin.routes_admins import admins_bp
from admin.routes_images import images_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    # Blueprint 登録
    app.register_blueprint(shop_menu_bp, url_prefix="/shop/menu")
    app.register_blueprint(shop_products_bp, url_prefix="/shop/products")
    app.register_blueprint(shop_cart_bp, url_prefix="/shop/cart")
    app.register_blueprint(shop_checkout_bp, url_prefix="/shop/checkout")
    app.register_blueprint(shop_payment_method_bp, url_prefix="/shop/payment_method")
    app.register_blueprint(shop_payment_bp, url_prefix="/shop/payment")
    app.register_blueprint(shop_complete_bp, url_prefix="/shop/complete")

    app.register_blueprint(auth_bp, url_prefix="/admin")
    app.register_blueprint(products_bp, url_prefix="/admin/products")
    app.register_blueprint(categories_bp, url_prefix="/admin/categories")
    app.register_blueprint(orders_bp, url_prefix="/admin/orders")
    app.register_blueprint(users_bp, url_prefix="/admin/users")
    app.register_blueprint(admins_bp, url_prefix="/admin/admins")
    app.register_blueprint(images_bp, url_prefix="/admin/images")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
