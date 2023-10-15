from flask_smorest import abort
from sqlalchemy import asc

from src.db import db
from src.models.inventory_model import InventoryModel
from src.models.permission_model import PermissionModel
from src.models.product_model import ProductModel


def get_all_inventory_items():
    results = InventoryModel.query.order_by(asc(InventoryModel.id)).all()
    return results


def post_inventory_item(inventory_data):
    product_id = inventory_data["product_id"]

    try:
        new_row = InventoryModel(
            product_id=product_id,
        )

        db.session.add(new_row)
        db.session.commit()
    except:
        db.session.rollback()
        abort(400, message="Can not add inventory!")

    return {"message": "Add successfully!"}


def get_inventory_item_by_product_id(product_id):
    results = InventoryModel.query.filter_by(product_id=product_id).first()
    return results


def update_inventory_item_by_product_id(inventory_data, product_id):
    inventory_item: InventoryModel = InventoryModel.query.filter_by(
        product_id=product_id
    ).first()

    if not inventory_item:
        abort(400, message="Inventory item doesn't exist, cannot update!")

    try:
        inventory_item.product_id = product_id

        if inventory_data["available_count"]:
            inventory_item.available_count = inventory_data["available_count"]

        if inventory_data["pending_count"]:
            inventory_item.pending_count = inventory_data["pending_count"]

        if inventory_data["sold_count"]:
            inventory_item.sold_count = inventory_data["sold_count"]

        db.session.commit()
    except:
        db.session.rollback()
        abort(400, message="Can not update inventory item!")

    return {"message": "Update successfully!"}
