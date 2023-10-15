from sqlalchemy import Column, ForeignKey, Integer

from src.db import db


class UserRoleModel(db.Model):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    role_id = Column(Integer, ForeignKey("role.id"))
