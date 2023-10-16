from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from src.models.inventory_model import InventoryModel
from src.models.user_product_model import UserProductModel
from src.schemas.user_product_schema import (
    LinkUserAndProductSchema,
    UpdateUserAndProductSchema,
)
from src.services import inventory_service, user_product_service

blp = Blueprint("Shopping Cart", __name__, description="User And Product API")


@blp.route("/user/<int:user_id>/product/<int:product_id>")
class LinkProductsToUser(MethodView):
    @jwt_required()
    @blp.response(201, LinkUserAndProductSchema)
    def post(self, user_id, product_id):
        result = user_product_service.link_products_to_user(user_id, product_id)
        return result

    @blp.response(200, LinkUserAndProductSchema)
    def delete(self, user_id, product_id):
        result = user_product_service.delete_products_to_user(user_id, product_id)
        return result


@blp.route("/add_to_cart")
class AddProductsToUser(MethodView):
    @jwt_required()
    @blp.arguments(UpdateUserAndProductSchema)
    def put(self, qa_history_data):
        product_id = qa_history_data["product_id"]
        count = qa_history_data["count"]

        inventory_item: InventoryModel = (
            inventory_service.get_inventory_item_by_product_id(product_id)
        )

        if inventory_item.available_count > count:
            user_product_service.update_products_to_user(qa_history_data, "add")

            inventory_data = {
                "available_count": inventory_item.available_count - count,
                "pending_count": inventory_item.pending_count + count,
            }

            inventory_item = inventory_service.update_inventory_item_by_product_id(
                inventory_data, product_id
            )

            return inventory_item
        return {"message": "Not enough available items to add"}


@blp.route("/remove_from_cart")
class RemoveProductsFromUser(MethodView):
    @jwt_required()
    @blp.arguments(UpdateUserAndProductSchema)
    def put(self, qa_history_data):
        product_id = qa_history_data["product_id"]
        count = qa_history_data["count"]

        user_product_service.update_products_to_user(qa_history_data, "remove")

        inventory_item: InventoryModel = (
            inventory_service.get_inventory_item_by_product_id(product_id)
        )

        inventory_data = {
            "available_count": inventory_item.available_count + count,
            "pending_count": inventory_item.pending_count - count,
        }

        inventory_item = inventory_service.update_inventory_item_by_product_id(
            inventory_data, product_id
        )

        return inventory_item


@blp.route("/view_cart/user/<int:user_id>")
class ViewCart(MethodView):
    @jwt_required()
    def get(self, user_id):
        result: [
            UserProductModel
        ] = user_product_service.get_ordered_products_by_user_id(user_id)
        return result
