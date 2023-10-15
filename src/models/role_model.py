from sqlalchemy import Column, Integer, String

from src.db import db


class RoleModel(db.Model):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    permissions = db.relationship(
        "PermissionModel", back_populates="roles", secondary="role_permission"
    )
    users = db.relationship("UserModel", back_populates="roles", secondary="user_role")
