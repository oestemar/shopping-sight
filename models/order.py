from models import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    payment_id = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="processing")
    created_at = db.Column(db.DateTime, default=datetime.now)

    order_items = db.relationship("OrderItem", backref="order", lazy=True)
