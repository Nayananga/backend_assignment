from marshmallow import Schema, fields


class PlainProductSchema(Schema):
    id = fields.Int(dump_only=True)
    product_name = fields.Str(required=True)
    description = fields.Str(required=True)
