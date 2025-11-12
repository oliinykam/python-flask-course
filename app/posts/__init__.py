from flask import Blueprint

post_bp = Blueprint("posts", 
                    __name__, 
                    url_prefix="/post",
                    template_folder="templates/posts",
                    static_folder='static'
                    )

from . import views