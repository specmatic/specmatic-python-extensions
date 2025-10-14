import os
from typing import ClassVar

import requests
from fastapi import HTTPException

from .schemas import Order, Product, ProductType

ENVS = {
    "ORDER_API_HOST": os.getenv("ORDER_API_HOST"),
    "ORDER_API_PORT": os.getenv("ORDER_API_PORT"),
    "API_URL": "http://" + os.getenv("ORDER_API_HOST") + ":"  + os.getenv("ORDER_API_PORT"),
    "AUTH_TOKEN": os.getenv("AUTH_TOKEN") or "API-TOKEN-SPEC",
    "REQ_TIMEOUT": os.getenv("REQ_TIMEOUT") or 3000,
}


class ProductService:
    _API_LIST: ClassVar[dict[str, str]] = {
        "SEARCH": "/products",
        "CREATE": "/products",
    }

    @staticmethod
    async def find_products(p_type: ProductType | None) -> list[Product]:
        resp = requests.get(
            f"{ENVS['API_URL']}{ProductService._API_LIST['SEARCH']}",
            params={"type": p_type.value if p_type else None},
            timeout=ENVS["REQ_TIMEOUT"],
        )

        if resp.status_code != 200:
            raise HTTPException(
                resp.status_code, "An error occurred while retrieving the products."
            )

        return resp.json()

    @staticmethod
    async def create_product(product: Product) -> dict[str, int]:
        resp = requests.post(
            f"{ENVS['API_URL']}{ProductService._API_LIST['CREATE']}",
            json=product.dict(exclude={"description", "id"}),
            headers={"Authenticate": ENVS["AUTH_TOKEN"]},
            timeout=ENVS["REQ_TIMEOUT"],
        )

        if resp.status_code != 200:
            raise HTTPException(
                resp.status_code, "An error occurred while creating the product."
            )

        return resp.json()


class OrdersService:
    _API_LIST: ClassVar[dict[str, str]] = {
        "CREATE": "/orders",
    }

    @staticmethod
    async def create_order(order: Order) -> dict[str, int]:
        resp = requests.post(
            f"{ENVS['API_URL']}{OrdersService._API_LIST['CREATE']}",
            json=order.dict(),
            headers={"Authenticate": ENVS["AUTH_TOKEN"]},
            timeout=ENVS["REQ_TIMEOUT"],
        )

        if resp.status_code != 200:
            raise HTTPException(
                resp.status_code, "An error occurred while creating the order."
            )

        return resp.json()
