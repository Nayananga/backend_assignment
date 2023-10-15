from marshmallow import Schema, fields


class LinkUserAndProductSchema(Schema):
    message = fields.Str()
    user_id = fields.Int()
    product_id = fields.Int()


class UpdateUserAndProductSchema(Schema):
    user_id = fields.Int()
    product_id = fields.Int()
    count = fields.Int()
