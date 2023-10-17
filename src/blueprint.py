from flask_smorest import Api

from src.controllers.inventory_controller import blp as InventoryBluePrint
from src.controllers.order_controller import blp as OrderBlueprint
from src.controllers.permission_controller import blp as PermissionBlueprint
from src.controllers.product_controller import blp as ProductBluePrint
from src.controllers.role_controller import blp as RoleBlueprint
from src.controllers.role_permission_controller import blp as RolePermissionBlueprint
from src.controllers.user_controller import blp as UserBlueprint
from src.controllers.user_product_controller import blp as UserProductBlueprint
from src.controllers.user_role_controller import blp as UserRoleBlueprint


# Register Blueprint
def register_routing(app, prefix):
    api = Api(app)
    api.register_blueprint(UserBlueprint, url_prefix=prefix+"/v1")
    api.register_blueprint(RoleBlueprint, url_prefix=prefix+"/v1")
    api.register_blueprint(PermissionBlueprint, url_prefix=prefix+"/v1")
    api.register_blueprint(UserRoleBlueprint, url_prefix=prefix+"/v1")
    api.register_blueprint(RolePermissionBlueprint, url_prefix=prefix+"/v1")
    api.register_blueprint(ProductBluePrint, url_prefix=prefix+"/v1")
    api.register_blueprint(InventoryBluePrint, url_prefix=prefix+"/v1")
    api.register_blueprint(UserProductBlueprint, url_prefix=prefix+"/v1")
    api.register_blueprint(OrderBlueprint, url_prefix=prefix+"/v1")
