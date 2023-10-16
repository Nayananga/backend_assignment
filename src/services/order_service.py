from flask_smorest import abort

from src.db import db
from src.models.order_model import OrderModel


def post_order(order_data):
    user_id = order_data["user_id"]
    delivery_datetime = order_data["delivery_datetime"]

    try:
        new_row = OrderModel(user_id=user_id, delivery_datetime=delivery_datetime)

        db.session.add(new_row)
        db.session.commit()
    except:
        db.session.rollback()
        abort(400, message="Can not add order!")

    return {"message": "Add successfully!", "order_id": new_row.id}
