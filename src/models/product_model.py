from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String

from src.db import db


class ProductModel(db.Model):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    product_name = Column(String(80), unique=True, nullable=False)
    description = Column(String, nullable=False)
    block = Column(Boolean, default=False, nullable=False)
    time_created = Column(String, default=datetime.now())
    users = db.relationship(
        "UserModel", back_populates="products", secondary="user_product"
    )
