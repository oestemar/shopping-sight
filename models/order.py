from models import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    delivery_method = db.Column(db.String(20), nullable=False)
    stripe_payment_intent_id = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="paid")
    created_at = db.Column(db.DateTime, default=datetime.now)

    items = db.relationship("OrderItem", backref="order", lazy=True)
