from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from src.db import db


class OrderModel(db.Model):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey("user.id"))
    delivery_datetime = Column(DateTime, nullable=False)
    time_created = Column(String, default=datetime.now())
