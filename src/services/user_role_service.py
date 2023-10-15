from flask_smorest import abort

from src.db import db
from src.models.role_model import RoleModel
from src.models.user_model import UserModel


def link_roles_to_user(user_id, role_id):
    user = UserModel.query.filter_by(id=user_id).first()
    role = RoleModel.query.filter_by(id=role_id).first()

    user.roles.append(role)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        abort(500, message="An error occurred while inserting the role.")

    return role


def delete_roles_to_user(user_id, role_id):
    user = UserModel.query.filter_by(id=user_id).first()
    role = RoleModel.query.filter_by(id=role_id).first()

    user.roles.remove(role)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        abort(500, message="An error occurred while deleting the role.")

    return {"message": "User removed from role", "user": user, "role": role}
