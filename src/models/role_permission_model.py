from sqlalchemy import Column, ForeignKey, Integer

from src.db import db


class RolePermissionModel(db.Model):
    __tablename__ = "role_permission"

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"))
    permission_id = Column(Integer, ForeignKey("permission.id"))
