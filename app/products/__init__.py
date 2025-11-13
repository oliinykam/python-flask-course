from flask import Blueprint

products_bp = Blueprint("products", 
                    __name__, 
                    url_prefix="/products",
                    static_folder="static",
                    static_url_path="/products/static",
                    template_folder="templates/products"
                    )

from . import views