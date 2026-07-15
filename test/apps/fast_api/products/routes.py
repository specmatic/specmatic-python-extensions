from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from ..schemas import Product, ProductType
from ..services import ProductService

products = APIRouter()


@products.get("/findAvailableProducts")
async def find_available_products(
    type: ProductType | None = None, pageSize: int = Header(default=None)
):
    if not pageSize:
        raise HTTPException(400, "pageSize is required")

    # NOTE: API_SPEC v4 requires expects TIMEOUT when type="other" or pageSize=20
    if type == ProductType.OTHER or pageSize == 20:
        raise HTTPException(503, "Timeout")

    products = await ProductService.find_products(type)
    return JSONResponse(content=products)


@products.post("/products", status_code=201)
async def add_product(request: Request, data: Product) -> dict[str, int]:
    if request.headers.get("content-type", "").split(";")[0].strip() != "application/json":
        raise HTTPException(status_code=415, detail="Unsupported Media Type")
    product = await ProductService.create_product(data)
    return {"id": product["id"]}
