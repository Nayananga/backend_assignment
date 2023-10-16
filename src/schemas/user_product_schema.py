from marshmallow import Schema, fields


class PlainUserAndProductSchema(Schema):
    user_id = fields.Int()
    product_id = fields.Int()


class LinkUserAndProductSchema(PlainUserAndProductSchema):
    message = fields.Str()


class UpdateUserAndProductSchema(PlainUserAndProductSchema):
    count = fields.Int()
