import logging

from flask.views import MethodView
from flask_principal import Permission, RoleNeed
from flask_smorest import Blueprint

from src.schemas.order_schema import PlainOrderSchema
from src.schemas.user_schema import *
from src.services import inventory_service, order_service, user_product_service

# Create logger for this module
logger = logging.getLogger(__name__)

# Define permissions
read_permission = Permission(RoleNeed("read"))
write_permission = Permission(RoleNeed("write"))
delete_permission = Permission(RoleNeed("delete"))

blp = Blueprint("Order", __name__, description="Order API")


@blp.route("/orders")
class Order(MethodView):
    @blp.arguments(PlainOrderSchema)
    def post(self, order_data):
        user_id = order_data["user_id"]
        logger.info(f"Order data for {user_id} is processing...")

        cart_items = user_product_service.get_ordered_products_by_user_id(user_id)

        for item in cart_items:
            product_id = item["product_id"]
            user_id = item["user_id"]
            count = item["count"]

            user_product_service.delete_products_to_user(user_id, product_id)
            result = inventory_service.get_inventory_item_by_product_id(product_id)

            inventory_data = {
                "pending_count": result.pending_count - count,
                "sold_count": result.sold_count + count,
            }

            inventory_service.update_inventory_item_by_product_id(
                inventory_data, product_id
            )

        result = order_service.post_order(order_data)

        return result
