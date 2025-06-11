from flask import Blueprint

companies_bp = Blueprint('companies', __name__, template_folder="companies" ,url_prefix='/companies')

from . import routes