from flask_smorest import abort
from sqlalchemy import asc

from src.db import db
from src.models.permission_model import PermissionModel


def get_all_permission():
    results = PermissionModel.query.order_by(asc(PermissionModel.id)).all()
    return results


def post_permission(permission_data):
    name = permission_data["name"]
    description = permission_data["description"]

    try:
        new_row = PermissionModel(name=name, description=description)

        db.session.add(new_row)
        db.session.commit()
    except:
        db.session.rollback()
        abort(400, message="Can not add permission!")

    return {"message": "Add successfully!"}


def get_permission(permission_id):
    results = PermissionModel.query.filter_by(id=permission_id).first()
    return results


def update_permission(permission_data, permission_id):
    permission = PermissionModel.query.filter_by(id=permission_id).first()

    if not permission:
        abort(400, message="permission doesn't exist, cannot update!")

    try:
        if permission_data["name"]:
            permission.name = permission_data["name"]

        if permission_data["description"]:
            permission.description = permission_data["description"]

        db.session.commit()
    except:
        db.session.rollback()
        abort(400, message="Can not update permission!")

    return {"message": "Update successfully!"}
