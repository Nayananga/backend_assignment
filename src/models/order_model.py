from datetime import datetime

from src.db import db


class OrderModel(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    delivery_datetime = db.Column(db.DateTime(), nullable=False)
    time_created = db.Column(db.String(), default=datetime.now())
