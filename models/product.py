from models import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    sku = db.Column(db.String(100), unique=True)
    brand = db.Column(db.String(100))
    status = db.Column(db.Integer, nullable=False, default=1)
    spec_json = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    images = db.relationship("ProductImage", backref="product", lazy=True)
    category = db.relationship("Category", backref="products")
