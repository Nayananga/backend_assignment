from sqlalchemy import Column, Integer, String

from src.db import db


class PermissionModel(db.Model):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    roles = db.relationship(
        "RoleModel", back_populates="permissions", secondary="role_permission"
    )
