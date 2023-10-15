import unittest
from datetime import datetime

import click
import coverage
from passlib.hash import pbkdf2_sha256

from src import db
from src.models.inventory_model import InventoryModel
from src.models.order_model import OrderModel
from src.models.permission_model import PermissionModel
from src.models.product_model import ProductModel
from src.models.role_model import RoleModel
from src.models.role_permission_model import RolePermissionModel
from src.models.user_model import UserModel
from src.models.user_product_model import UserProductModel
from src.models.user_role_model import UserRoleModel


@click.option(
    "--pattern", default="tests_*.py", help="Test search pattern", required=False
)
def cov(pattern):
    """
    Run the unit tests with coverage
    """
    cov = coverage.coverage(branch=True, include="app/*")
    cov.start()
    tests = unittest.TestLoader().discover("tests", pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        cov.stop()
        cov.save()
        print("Coverage Summary:")
        cov.report()
        cov.erase()
        return 0
    return 1


@click.option(
    "--pattern", default="tests_*.py", help="Test search pattern", required=False
)
def cov_html(pattern):
    """
    Run the unit tests with coverage and generate an HTML report.
    """
    cov = coverage.coverage(branch=True, include="app/*")
    cov.start()

    tests = unittest.TestLoader().discover("tests", pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        cov.stop()
        cov.save()

        print("Coverage Summary:")
        cov.report()
        cov.html_report(directory="report/htmlcov")
        cov.erase()
        return 0

    return 1


@click.option("--pattern", default="tests_*.py", help="Test pattern", required=False)
def tests(pattern):
    """
    Run the tests without code coverage
    """
    tests = unittest.TestLoader().discover("tests", pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


def create_db():
    """
    Create Database.
    """
    db.create_all()
    db.session.commit()


def reset_db():
    """
    Reset Database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


def drop_db():
    """
    Drop Database.
    """
    db.drop_all()
    db.session.commit()


def init_db_user():
    # Insert Permission
    read_permission = PermissionModel(name="read", description="Read data")
    write_permission = PermissionModel(name="write", description="Write data")
    delete_permission = PermissionModel(name="delete", description="Delete data")
    db.session.add_all([read_permission, write_permission, delete_permission])
    db.session.commit()

    # Insert Role
    admin_role = RoleModel(name="Admin", description="Full Permission")
    user_role = RoleModel(name="User", description="Can read, write data")
    guest_role = RoleModel(name="Guest", description="Just read data")
    db.session.add_all([admin_role, user_role, guest_role])
    db.session.commit()

    # Insert Role_Permission
    role_permission_admin1 = RolePermissionModel(role_id=1, permission_id=1)
    role_permission_admin2 = RolePermissionModel(role_id=1, permission_id=2)
    role_permission_admin3 = RolePermissionModel(role_id=1, permission_id=3)
    role_permission_user1 = RolePermissionModel(role_id=2, permission_id=1)
    role_permission_user2 = RolePermissionModel(role_id=2, permission_id=2)
    role_permission_guest = RolePermissionModel(role_id=3, permission_id=1)
    db.session.add_all(
        [
            role_permission_admin1,
            role_permission_admin2,
            role_permission_admin3,
            role_permission_user1,
            role_permission_user2,
            role_permission_guest,
        ]
    )
    db.session.commit()

    # Insert User
    password = pbkdf2_sha256.hash("123456")
    admin_user = UserModel(username="admin", password=password)
    normal_user = UserModel(username="user", password=password)
    guest_user = UserModel(username="guest", password=password)
    db.session.add_all([admin_user, normal_user, guest_user])
    db.session.commit()

    # Insert UserRole
    user_role1 = UserRoleModel(user_id=1, role_id=1)
    user_role2 = UserRoleModel(user_id=2, role_id=2)
    user_role3 = UserRoleModel(user_id=3, role_id=3)
    db.session.add_all([user_role1, user_role2, user_role3])
    db.session.commit()

    # Insert Order
    order1 = OrderModel(user_id=1, delivery_datetime=datetime.now())
    order2 = OrderModel(user_id=2, delivery_datetime=datetime.now())
    order3 = OrderModel(user_id=3, delivery_datetime=datetime.now())
    db.session.add_all([order1, order2, order3])
    db.session.commit()

    # Insert Product
    product1 = ProductModel(
        product_name="Side Mirror",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing",
    )
    product2 = ProductModel(
        product_name="Fog Light",
        description="Ut enim ad minim veniam, quis nostrud exercitation",
    )
    product3 = ProductModel(
        product_name="Headlight",
        description="Duis aute irure dolor in reprehenderit in voluptate",
    )
    db.session.add_all([product1, product2, product3])
    db.session.commit()

    # Insert UserProduct
    user_product1 = UserProductModel(user_id=1, product_id=3)
    user_product2 = UserProductModel(user_id=2, product_id=2)
    user_product3 = UserProductModel(user_id=3, product_id=1)
    db.session.add_all([user_product1, user_product2, user_product3])
    db.session.commit()

    # Insert Inventory
    inventory1 = InventoryModel(product_id=1)
    inventory2 = InventoryModel(product_id=2)
    inventory3 = InventoryModel(product_id=3)
    db.session.add_all([inventory1, inventory2, inventory3])
    db.session.commit()


def create_user_admin(username="admin"):
    """
    Create User Admin.
    """
    admin = UserModel.query.filter_by(username=username).first()

    if admin is None:
        print("user-admin is not created before!")
        init_db_user()
    else:
        print("user-admin is created!")


def init_app(app):
    if app.config["APP_ENV"] == "production":
        commands = [create_db, reset_db, drop_db, create_user_admin]
    else:
        commands = [
            create_db,
            reset_db,
            drop_db,
            create_user_admin,
            tests,
            cov_html,
            cov,
        ]

    for command in commands:
        app.cli.add_command(app.cli.command()(command))
