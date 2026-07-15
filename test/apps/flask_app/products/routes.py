from flask import Blueprint, abort, jsonify, request

from ..products.models import Product
from ..services import ProductService, ProductType

products = Blueprint("products", __name__)


@products.route("/findAvailableProducts", methods=["GET"])
def find_available_products():
    page_size, p_type = Product.validate_args(request.headers.get("pageSize"), request.args.get("type"))

    # NOTE: API_SPEC v4 requires expects TIMEOUT when type="other" or pageSize=20
    if p_type == ProductType.OTHER or page_size == 20:
        return abort(503, "Timeout")

    products = ProductService.find_products(p_type)
    return jsonify(products)


@products.route("/products", methods=["POST"])
def add_product():
    if request.content_type != "application/json":
        abort(415, "Unsupported Media Type")
    data: Product = Product.load(request.json)
    product = ProductService.create_product(data)
    return jsonify(id=product["id"]), 201
