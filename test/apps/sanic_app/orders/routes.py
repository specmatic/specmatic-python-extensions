from typing import TYPE_CHECKING

from sanic import Blueprint, json
from sanic.exceptions import SanicException

from ..orders.models import Order
from ..services import OrdersService

if TYPE_CHECKING:
    from sanic import Request

orders = Blueprint("orders")


@orders.route("/orders", methods=["POST"])
async def create_order(request: "Request"):
    if request.headers.get("content-type", "").split(";", 1)[0].strip() != "application/json":
        raise SanicException("Unsupported Media Type", status_code=415)
    data: Order = Order.load(request.json)
    order = OrdersService.create_order(data)
    return json({"id": order["id"]}, status=201)
