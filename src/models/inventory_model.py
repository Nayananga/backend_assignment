from datetime import datetime

from src.db import db


class InventoryModel(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    available_count = db.Column(db.Integer, default=0, nullable=False)
    pending_count = db.Column(db.Integer, default=0, nullable=False)
    sold_count = db.Column(db.Integer, default=0, nullable=False)
    time_created = db.Column(db.String(), default=datetime.now())
