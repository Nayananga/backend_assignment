from flask_smorest import abort
from sqlalchemy import asc

from src.db import db
from src.models.permission_model import PermissionModel
from src.models.product_model import ProductModel


def get_all_products():
    results = ProductModel.query.order_by(asc(ProductModel.id)).all()
    return results


def post_product(product_data):
    product_name = product_data["product_name"]
    description = product_data["description"]

    try:
        new_row = ProductModel(product_name=product_name, description=description)

        db.session.add(new_row)
        db.session.commit()
    except:
        db.session.rollback()
        abort(400, message="Can not add product!")

    return {"message": "Add successfully!", "product_id": new_row.id}


def get_product(product_id):
    results = ProductModel.query.filter_by(id=product_id).first()
    return results


def update_product(product_data, product_id):
    product: ProductModel = ProductModel.query.filter_by(id=product_id).first()

    if not product:
        abort(400, message="product doesn't exist, cannot update!")

    try:
        if product_data["product_name"]:
            product.product_name = product_data["product_name"]

        if product_data["description"]:
            product.description = product_data["description"]

        db.session.commit()
    except:
        db.session.rollback()
        abort(400, message="Can not update product!")

    return {"message": "Update successfully!"}
