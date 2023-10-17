from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from src.schemas.user_schema import RoleSchema, UserAndRoleSchema
from src.services import user_role_service

blp = Blueprint("User And Role", __name__, description="User And Role API")


@blp.route("/users/<int:user_id>/roles/<int:role_id>")
class LinkRolesToUser(MethodView):
    @jwt_required()
    @blp.response(201, RoleSchema)
    def post(self, user_id, role_id):
        result = user_role_service.link_roles_to_user(user_id, role_id)
        return result

    @jwt_required()
    @blp.response(200, UserAndRoleSchema)
    def delete(self, user_id, role_id):
        result = user_role_service.delete_roles_to_user(user_id, role_id)
        return result
