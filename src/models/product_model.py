from datetime import datetime

from src.db import db


class ProductModel(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(), nullable=False)
    block = db.Column(db.Boolean, default=False, nullable=False)
    time_created = db.Column(db.String(), default=datetime.now())
    users = db.relationship(
        "UserModel", back_populates="products", secondary="user_product"
    )
