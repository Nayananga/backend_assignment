from flask_smorest import abort

from src.db import db
from src.models.product_model import ProductModel
from src.models.user_model import UserModel
from src.models.user_product_model import UserProductModel


def link_products_to_user(user_id, product_id):
    user: UserModel = UserModel.query.filter_by(id=user_id).first()
    product: ProductModel = ProductModel.query.filter_by(id=product_id).first()

    user.products.append(product)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        abort(500, message="An error occurred while inserting the product.")

    return {
        "message": "Product added to the user",
        "user_id": user.id,
        "product_id": product.id,
    }


def delete_products_to_user(user_id, product_id):
    user: UserModel = UserModel.query.filter_by(id=user_id).first()
    product: ProductModel = ProductModel.query.filter_by(id=product_id).first()

    user.products.remove(product)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        abort(500, message="An error occurred while deleting the product.")

    return {
        "message": "Product removed from user",
        "user_id": user.id,
        "product_id": product.id,
    }


def update_products_to_user(cart_data, operation):
    user_product: UserProductModel = (
        UserProductModel.query.filter_by(user_id=cart_data["user_id"])
        .filter_by(product_id=cart_data["product_id"])
        .first()
    )

    if not user_product:
        abort(400, message="cart item doesn't exist, cannot update!")

    try:
        if str(operation).lower() == "add":
            user_product.count += cart_data["count"]
        else:
            user_product.count -= cart_data["count"]

        db.session.commit()
    except:
        db.session.rollback()
        abort(400, message="Can not update cart item!")

    return {"message": "Update successfully!"}
