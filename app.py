from flask import Flask, redirect, session, request
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import traceback
from flask import send_from_directory

from models import db

from shop.routes_register import shop_register_bp
from shop.routes_login import shop_login_bp
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
#from admin.routes_images import images_bp
from admin.routes_inventory import inventory_bp
from supabase import create_client

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    # モデルを読み込む
    from models.user import User
    from models.admin import Admin
    from models.category import Category
    from models.category_image import CategoryImage
    from models.product import Product
    from models.image import ProductImage
    from models.order import Order
    from models.order_item import OrderItem
    from models.cart import Cart
    from models.inventory_history import InventoryHistory

    with app.app_context():
        db.create_all()

    # Blueprint 登録
    app.register_blueprint(shop_register_bp)
    app.register_blueprint(shop_login_bp)
    app.register_blueprint(shop_menu_bp, url_prefix="/shop/menu")
    app.register_blueprint(shop_products_bp, url_prefix="/shop/products")
    app.register_blueprint(shop_product_detail_bp, url_prefix="/shop/product_detail")
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
#    app.register_blueprint(images_bp, url_prefix="/admin/images")
    app.register_blueprint(inventory_bp, url_prefix="/admin/inventory")

    # 一時的に入れているデバッグコード下記２つ
    @app.before_request
    def _log_request():
        print("DEBUG: incoming request", request.method, request.path)
    # 同上
    @app.errorhandler(Exception)
    def _log_exception(e):
        print("DEBUG: exception caught:", type(e), e)
        traceback.print_exc()
        raise e

    @app.context_processor
    def inject_cart_count():
        user_id = session.get("user_id")
        if not user_id:
            print("cart_count: 0(no user)")
            return dict(cart_count=0)

        count = db.session.query(db.func.sum(Cart.quantity))\
                        .filter_by(user_id=user_id).scalar() or 0

        print(f"cart_count: {count}")
        return dict(cart_count=count)

    @app.context_processor
    def inject_user():
        user_id = session.get("user_id")
        if not user_id:
            return dict(login_user=None)

        user = User.query.get(user_id)
        return dict(login_user=user)

    @app.get("/")  
    def index():
        return redirect("/shop/menu")

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )

    app.supabase = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
