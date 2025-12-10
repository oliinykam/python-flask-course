from flask import Blueprint

vacancies_bp = Blueprint(
    'vacancies', 
    __name__, 
    url_prefix='/vacancies',
    template_folder='templates',
    static_folder='static'
)

from . import views, models