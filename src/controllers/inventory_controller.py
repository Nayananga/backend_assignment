from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_principal import Permission, RoleNeed
from flask_smorest import Blueprint

from src.schemas.inventory_schema import PlainInventorySchema
from src.services import inventory_service

# Define permissions
read_permission = Permission(RoleNeed("read"))
write_permission = Permission(RoleNeed("write"))

blp = Blueprint("Inventory", __name__, description="Inventory API")


@blp.route("/inventory")
class InventoryList(MethodView):
    @jwt_required()
    @read_permission.require(http_exception=403)
    @blp.response(200, PlainInventorySchema(many=True))
    def get(self):
        result = inventory_service.get_all_inventory_items()
        return result


@blp.route("/inventory/<int:product_id>")
class InventoryItem(MethodView):
    @jwt_required()
    @read_permission.require(http_exception=403)
    @blp.response(200, PlainInventorySchema)
    def get(self, product_id):
        result = inventory_service.get_inventory_item_by_product_id(product_id)
        return result

    @jwt_required()
    @write_permission.require(http_exception=403)
    @blp.arguments(PlainInventorySchema)
    def put(self, inventory_data, product_id):
        result = inventory_service.update_inventory_item_by_product_id(
            inventory_data, product_id
        )
        return result
