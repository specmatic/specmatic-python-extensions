from fastapi import APIRouter, HTTPException, Request

from ..schemas import Order
from ..services import OrdersService

orders = APIRouter()


@orders.post("/orders", status_code=201)
async def create_order(request: Request, order: Order) -> dict[str, int]:
    if request.headers.get("content-type", "").split(";")[0].strip() != "application/json":
        raise HTTPException(status_code=415, detail="Unsupported Media Type")
    new_order = await OrdersService.create_order(order)
    return {"id": new_order["id"]}
