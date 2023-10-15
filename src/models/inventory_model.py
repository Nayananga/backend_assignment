from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String

from src.db import db


class InventoryModel(db.Model):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    available_count = Column(Integer, default=0, nullable=False)
    pending_count = Column(Integer, default=0, nullable=False)
    sold_count = Column(Integer, default=0, nullable=False)
    time_created = Column(String, default=datetime.now())
