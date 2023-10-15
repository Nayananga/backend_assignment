from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String

from src.db import db


class UserModel(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String, nullable=False)
    block = Column(Boolean, default=False, nullable=False)
    time_created = Column(String, default=datetime.now())
    roles = db.relationship("RoleModel", back_populates="users", secondary="user_role")
    products = db.relationship(
        "ProductModel", back_populates="users", secondary="user_product"
    )
