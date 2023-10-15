from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_principal import Permission, RoleNeed
from flask_smorest import Blueprint

from src.schemas.product_schema import PlainProductSchema
from src.services import product_service

# Define permissions
read_permission = Permission(RoleNeed("read"))
write_permission = Permission(RoleNeed("write"))

blp = Blueprint("Product", __name__, description="Product API")


@blp.route("/product")
class ProductList(MethodView):
    @jwt_required()
    @read_permission.require(http_exception=403)
    @blp.response(200, PlainProductSchema(many=True))
    def get(self):
        result = product_service.get_all_products()
        return result

    @jwt_required()
    @write_permission.require(http_exception=403)
    @blp.arguments(PlainProductSchema)
    def post(self, qa_history_data):
        result = product_service.post_product(qa_history_data)
        return result


@blp.route("/product/<int:product_id>")
class Product(MethodView):
    @jwt_required()
    @read_permission.require(http_exception=403)
    @blp.response(200, PlainProductSchema)
    def get(self, product_id):
        result = product_service.get_product(product_id)
        return result

    @jwt_required()
    @write_permission.require(http_exception=403)
    @blp.arguments(PlainProductSchema)
    def put(self, product_data, product_id):
        result = product_service.update_product(product_data, product_id)
        return result
