from marshmallow import Schema, fields


class PlainInventorySchema(Schema):
    product_id = fields.Int(dump_only=True)
    available_count = fields.Int()
    pending_count = fields.Int()
    sold_count = fields.Int()
