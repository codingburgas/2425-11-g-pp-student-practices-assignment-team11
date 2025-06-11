from flask import Blueprint

companies_bp = Blueprint('companies', __name__)

from . import routes