from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from src.models.inventory_model import InventoryModel
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
    @blp.response(201, LinkUserAndProductSchema)
    def put(self, qa_history_data):
        product_id = qa_history_data["product_id"]
        count = qa_history_data["count"]

        result: InventoryModel = inventory_service.get_inventory_item_by_product_id(
            product_id
        )

        if result.available_count > count:
            inventory_data = {
                "available_count": result.available_count - count,
                "pending_count": result.pending_count + count,
            }

            result = inventory_service.update_inventory_item_by_product_id(
                inventory_data, product_id
            )

            result = user_product_service.update_products_to_user(
                qa_history_data, "add"
            )
            return result
        return {"message": "Not enough available items to add"}


@blp.route("/remove_from_cart")
class AddProductsToUser(MethodView):
    @jwt_required()
    @blp.arguments(UpdateUserAndProductSchema)
    @blp.response(201, LinkUserAndProductSchema)
    def put(self, qa_history_data):
        product_id = qa_history_data["product_id"]
        count = qa_history_data["count"]

        result: InventoryModel = inventory_service.get_inventory_item_by_product_id(
            product_id
        )

        inventory_data = {
            "available_count": result.available_count + count,
            "pending_count": result.pending_count - count,
        }

        result = inventory_service.update_inventory_item_by_product_id(
            inventory_data, product_id
        )

        result = user_product_service.update_products_to_user(qa_history_data, "remove")

        return result
