from sqlalchemy import Column, ForeignKey, Integer

from src.db import db


class UserProductModel(db.Model):
    __tablename__ = "user_product"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    count = Column(Integer, default=0, nullable=False)
