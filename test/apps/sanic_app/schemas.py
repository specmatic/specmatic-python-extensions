import enum

from marshmallow import Schema, fields, validate


class OrderStatus(str, enum.Enum):
    FULFILLED = "fulfilled"
    PENDING = "pending"
    CANCELLED = "cancelled"


class ProductType(str, enum.Enum):
    GADGET = "gadget"
    FOOD = "food"
    BOOK = "book"
    OTHER = "other"


class AvailableProductSchema(Schema):
    type = fields.Enum(
        ProductType, required=False, by_value=True, load_default=None, allow_none=True
    )
    page_size = fields.Integer(
        required=True
    )


class ProductSchema(Schema):
    id = fields.Integer(required=False, strict=True)
    name = fields.String(required=True)
    type = fields.Enum(ProductType, required=True, by_value=True)
    inventory = fields.Integer(
        required=True,
        strict=True,
        validate=validate.Range(min_inclusive=True, max_inclusive=True, min=1, max=101),
    )
    description = fields.String(required=False, dump_default="")


class OrderSchema(Schema):
    productid = fields.Integer(required=True, strict=True)
    count = fields.Integer(required=True, strict=True)
    status = fields.Enum(OrderStatus, by_value=True, load_default=OrderStatus.PENDING)
