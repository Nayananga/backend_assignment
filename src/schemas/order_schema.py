from marshmallow import Schema, fields


class PlainOrderSchema(Schema):
    user_id = fields.Int(required=True)
    delivery_datetime = fields.DateTime(required=True)
