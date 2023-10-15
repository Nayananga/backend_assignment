from flask_smorest import abort

from src.db import db
from src.models.permission_model import PermissionModel
from src.models.role_model import RoleModel
from src.models.role_permission_model import RolePermissionModel


def get_role_permission():
    results = RolePermissionModel.query.all()
    return results


def update_roles_to_permission(permission_data):
    for permission_id in permission_data["data_update"]:
        permission = PermissionModel.query.filter_by(id=int(permission_id)).first()

        permission.roles = []

        for role_id in permission_data["data_update"][permission_id]:
            role = RoleModel.query.filter_by(id=role_id).first()
            permission.roles.append(role)
        try:
            db.session.add(permission)
            db.session.commit()
        except:
            abort(500, message="An error occurred while inserting the roles.")
    return {"message": "Update successfully!"}
