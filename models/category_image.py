from models import db

class CategoryImage(db.Model):
    __tablename__ = "category_images"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

    category = db.relationship("Category", backref="images")
